> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../uebergabeprotokoll_z_fallback_llm_20260929_1430.md).*

# Handover protocol: z_fallback_llm, CLI input does not produce a joke

As of: 2026-09-29

## 1- Task (understanding, not yet confirmed by you with "yes")

Actual state: The CLI input is exactly "computer exactly tell two jokes". No joke appears.

Target state: The LLM response appears directly in the console, not in a log file.

Not part of the task: rebuild logging, shorten or extend log lines, change cache behavior. The cache bypass ("joke" in the input) is deliberately chosen in this way.

The follower must first match this understanding with you and wait for your “yes”.

## 2 Environment

Manjaro Linux, ZSH, Branch feature/fallback-llm-lazy-install.

Ollama is available at http://localhost:11434 (Binary /usr/bin/ollama). Available models: llama3.2:latest, qwen3:8b.

The Ollama test per curl with model llama3.2, stream:false, num predict:100 and the stop words provides a valid answer ("Why did the computer go to the doctor?") Because he had a virus! Ollama, model name, stop words and token limit are therefore not the cause. The test prompt was shorter than the real prompt from ask ollama.py (without system role, gradient and aura suffix).

Configuration:

```
config/settings_local.py
```

Key: PLUGINS ENABLED = {"z fallback llm": 1}. Access via DynamicSettings().PLUGINS ENABLED.get("z fallback llm", False).

Existing package installer:

```
scripts/py/func/ensure_package.py
```

## 3- Chain sequence (verified from code sections)

Rules:

```
config/maps/plugins/z_fallback_llm/de-DE/FUZZY_MAP_pre.py
```

Rule 1 has priority 10 and requires `{aura1}` plus mode word (normal, slow, flow, slow, accurate, thorough). Rule 2 has priority 100 and requires one of the triggers aura, aurora, laura, dora, era, hurra, prora or computer, then a space and any text. Both call ask ollama.py. Both exclude windows such as Firefox, Chrome, Brave and Element.

Design:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

`execute()` takes the last Regex group as input and makes it small. For "joke" in the input, `bypass_cache = True` is set, the cache check is skipped. This is followed by the Ollama request with the model llama3.2. The timeout is 90 seconds. Early returns without Ollama request are available with empty input ("nothing heard."), with "forget everything", with `check_static_guardrails()` and with the instant words "immediately", "fast", "instant".

CLI return:

```
scripts/py/service_api.py
```

The function reads the latest output file and returns a dict with `status`, `result_text` and `input_text`. The log line "API-CLI-Call: Finished" reduces input and result to 20 characters. This is pure log shortening and not data shortening.

## 4- Observed log of the CLI input

In the log are only `reload_performed` and "API-CLI-Call: Finished". Input="...computer accurate," Result="computer accurate." Every line of `execute()` is missing (no "Input:", no "Cache BYPASS", no "Uncensored AI answer").

This does not prove that `execute()` did not run because:

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

opens the FileHandler with `mode='w'`. The ask ollama.log file is overwritten by `utils` on each import. `log_debug` also writes on stdout, i.e. in the console of the main program.

## 5 Open Questions (not used)

1- Does `execute()` run at all when entering the CLI?
2- Which Rule Matches, Rule 1, Rule 2 or None?
3- Does the CLI client output the value `result_text` in the console?
4- Does the output file contain only the input or also a response? The first 20 characters of input and result are identical, more is not visible.
5- What is the exact CLI call you use to drop the text? It has not yet been mentioned.

## 6- Rejected Hypotheses

1- The input does not arrive shortened; that was only the 20-character truncation in the log.
2- Ollama, stop words, and num_predict are not the cause.
3- The cache is bypassed at "witz" and therefore not the cause.

## 7- Found errors outside the task (do not change anything without a task)

1 file:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

After `if not raw_text:`, `response = answer_for_all_fallback` is set. The next line overwrites it with `clean_text_for_typing(raw_text)`. With an empty Ollama answer, the answer remains empty. Similarly, `response.replace('sl5_config.py', ...)` and `response.replace(' sl5_record_trigger.py ', ...)` have no effect because the result is not assigned.

2 File:

```
config/maps/plugins/internals/de-DE/aura_constants.py
```

According to `Overlay`, an `|` is missing, the variant `OverlayOrange` is created. In addition, `_variants` does not contain the word "computer". Rule 1 can therefore not match "computer exactly ...", Rule 2 can.

3 File:

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

`mode='w'` overwrites the log on every import.

## 8- Next Steps (only after your "yes")

Step A: Ask for the CLI call from you, without prompt characters.

Step B: Find the processing of `result_text`:

```
tools/search.sh "result_text" .
```

Step C: Check the console output after the input. For this, request the complete text from the console of the main program from you.

Step D: Only suggest changes afterwards, only in the before/after format.

## 9- Working rules that the successor must comply with

1- Communication in German. Code, comments, logs and identifiers in English only, even in blocks of code.
2- No statement about system status without proof from your output. Don't guess, don't reconstruct.
3- New task: first describe understanding, waiting for your "yes".
4- No "I have no access to your repository" set.
5- Repository search only via tools/search.sh with the -i, -E and -w options.
6- For errors, get the full traceback first.
7- Commands and file paths are each on their own line, without punctuation at the end.
8- Numbering in the format 1-, 2-, 3-.
9- Code changes only as changed lines in before/after format, without surrounding function code.
10- No python code with leading indentation in blocks of code, instead small functions without indentation.
11- No absolute, user-specific paths and no line numbers without file path.
12- No filling sets, no emotional tone, about 1400 characters per response as target.
13- Treat actions you have already performed as done.
14- When copying outputs do not copy the prompt sign, otherwise exit code 127 is created.
15- Commit to find date and time: ./tools/find-nearest-commit.sh "2026-07-28 17:00"
