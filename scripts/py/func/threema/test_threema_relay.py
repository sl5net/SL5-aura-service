"""Tests for the bidirectional Element <-> Threema relay (no X11 needed)."""
import unittest
from unittest import mock

from scripts.py.func.threema import matrix_threema_relay as relay
from scripts.py.func.threema.read_last_threema_message import (
    ThreemaCopyConfig,
    compute_click_points,
    config_from_values,
    parse_conf_text,
)
from scripts.py.func.threema.relay_history import RelayHistory, normalize_text


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


class HistoryTests(unittest.TestCase):
    def test_normalize_collapses_whitespace(self):
        self.assertEqual(normalize_text("  a \n b\t c "), "a b c")
        self.assertEqual(normalize_text(None), "")

    def test_knows_after_remember_even_with_other_whitespace(self):
        h = RelayHistory()
        h.remember("Hallo  Welt\n")
        self.assertTrue(h.knows("Hallo Welt"))
        self.assertFalse(h.knows("Anderes"))

    def test_entries_expire_so_repeated_text_is_forwarded_later(self):
        clock = FakeClock()
        h = RelayHistory(ttl_seconds=10, clock=clock)
        h.remember("ok")
        clock.now = 5
        self.assertTrue(h.knows("ok"))
        clock.now = 11
        self.assertFalse(h.knows("ok"))


class ClassifyTests(unittest.TestCase):
    def test_verdicts(self):
        h = RelayHistory()
        self.assertEqual(relay.classify_candidate("a", "a", h), "unchanged")
        self.assertEqual(relay.classify_candidate("a", None, h), "unchanged")
        self.assertEqual(relay.classify_candidate("a", "b", h), "forward")
        h.remember("b")
        self.assertEqual(relay.classify_candidate("a", "b", h), "echo")


class ConfigTests(unittest.TestCase):
    def test_german_decimal_comma_and_comments(self):
        values = parse_conf_text("# c\nFX=0,9353\nBOTTOM=96\nDX=-128\nDY=-225  # menu goes up\n")
        cfg = config_from_values(values)
        self.assertAlmostEqual(cfg.fx, 0.9353)
        self.assertEqual((cfg.bottom, cfg.dx, cfg.dy), (96, -128, -225))

    def test_composer_position_is_read(self):
        cfg = config_from_values({"INPUT_FX": "0,5537", "INPUT_BOTTOM": "33"})
        self.assertAlmostEqual(cfg.input_fx, 0.5537)
        self.assertEqual(cfg.input_bottom, 33)

    def test_invalid_value_falls_back_to_default(self):
        cfg = config_from_values({"FX": "abc"})
        self.assertEqual(cfg.fx, ThreemaCopyConfig().fx)

    def test_click_points(self):
        cfg = ThreemaCopyConfig(fx=0.5, bottom=100, dx=-10, dy=-20)
        click, copy = compute_click_points(100, 50, 800, 600, cfg)
        self.assertEqual(click, (500, 550))
        self.assertEqual(copy, (490, 530))


class RelayLoopTests(unittest.TestCase):
    """Run the real loop with fake GUI functions; stop via KeyboardInterrupt."""

    def run_loop(self, element_reads, threema_reads):
        sent_to_threema, sent_to_element = [], []
        elem_iter, thr_iter = iter(element_reads), iter(threema_reads)

        def fake_element():
            return next(elem_iter)

        def fake_threema(_cfg=None):
            return next(thr_iter)

        def fake_sleep(_s):
            pass

        def to_threema(text, press_enter=True):
            sent_to_threema.append(text)
            return True

        def to_element(text, press_enter=True):
            sent_to_element.append(text)
            return True

        with mock.patch.object(relay, "read_last_element_message", fake_element), \
             mock.patch.object(relay, "read_last_threema_message", fake_threema), \
             mock.patch.object(relay, "send_to_threema_window", to_threema), \
             mock.patch.object(relay, "send_to_element_window", to_element), \
             mock.patch.object(relay, "configure_x11_screensaver", lambda: None), \
             mock.patch.object(relay, "load_config", lambda: ThreemaCopyConfig()), \
             mock.patch.object(relay.time, "sleep", fake_sleep):
            try:
                relay.run_relay(poll_interval_seconds=0)
            except StopIteration:
                pass  # iterators exhausted -> test over
        return sent_to_threema, sent_to_element

    def test_new_element_message_goes_to_threema_only_once(self):
        to_t, to_e = self.run_loop(
            element_reads=["old", "hello", "hello", "hello"],
            threema_reads=[None, None, None, None],
        )
        self.assertEqual(to_t, ["hello"])
        self.assertEqual(to_e, [])

    def test_new_threema_message_goes_to_element_and_is_not_echoed_back(self):
        # Threema delivers "antwort"; afterwards Element's last own message is
        # that pasted text -> must NOT be forwarded to Threema again.
        to_t, to_e = self.run_loop(
            element_reads=["old", "old", "antwort", "antwort"],
            threema_reads=[None, "antwort", "antwort", "antwort"],
        )
        self.assertEqual(to_e, ["antwort"])
        self.assertEqual(to_t, [])

    def test_own_element_text_seen_in_threema_is_not_sent_back(self):
        to_t, to_e = self.run_loop(
            element_reads=["old", "frage", "frage", "frage"],
            threema_reads=[None, None, "frage", "frage"],
        )
        self.assertEqual(to_t, ["frage"])
        self.assertEqual(to_e, [])


if __name__ == "__main__":
    unittest.main()
