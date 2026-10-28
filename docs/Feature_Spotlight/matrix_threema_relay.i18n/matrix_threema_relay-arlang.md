> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../matrix_threema_relay.md).*

ﺔﻴﻠﺳﺮﻟﺍ ﺎﺘﻴﺑ ﺎﻤﻳﺮﺛ ﺔﻬﺟﺍﻭ ↔ ﺮﺼﻨﻋ #

       ﻭ Element Desktop** (Matrix)** ﻦﻴﺑ ﻞﺋﺎﺳﺮﻟﺍ ﺦﺴﻨﻳ ﺮﻴﻐﺻ ﻡﺩﺎﺧ
ﺎﻤﻬﻴﻠﻛ ﻞﻴﻐﺸﺗ ﻖﻳﺮﻃ ﻦﻋ X11/ﺲﻜﻨﻴﻟ ﻰﻠﻋ (ﺐﺘﻜﻤﻟﺍ ﺢﻄﺴﻟ ﺎﻤﻳﺮﺛ ﻞﻴﻤﻋ) **ﺎﺘ
.ﺓﺭﺄﻔﻟﺍ ﺕﺍﺮﻘﻧ ﺾﻌﺑﻭ ﺔﻈﻓﺎﺤﻟﺍ ،ﺢﻴﺗﺎﻔﻤﻟﺍ ﺔﺣﻮﻟ ﺕﺍﺭﺎﺼﺘﺧﺍ :ﻡﺪﺨﺘﺴﻤﻟﺍ ﻞﻌﻔ

.X11 ـﻟ ﺔﻴﺳﺎﻴﻘﻟﺍ ﺮﻣﺍﻭﻷ﻿ﺍ ﺮﻄﺳ ﺕﺍﻭﺩﺃ ﻂﻘﻓ .ﺔﻴﻓﺎﺿﺇ ﻥﻮﺜﻳﺎﺑ ﺕﺎﺒﺘﻜﻣ ﻻ﻿ ،ﺯ

ﻞﻌﻔﻳ ﺍﺫﺎﻣ ##

| ﺙﺪﺤﻳ ﺍﺫﺎﻣ | ﻩﺎﺠﺗﻻ﻿ﺍ |
|---|---|
| **Element → Threema** | ﻲﻓ *ﺎﻬﺘﺒﺘﻛ ﻲﺘﻟﺍ* ﺓﺮﻴﺧﻷ﻿ﺍ ﺔﻟﺎﺳﺮﻟﺍ Elemen
| .ﺎﻬﻟﺎﺳﺭﺇﻭ ﺖﻨﻤﻴﻟﺇ ﻲﻓ ﺎﻬﻘﺼﻟ ﻢﺘﻳ ،ﺓﺪﻳﺪﺟ ﺖﻧﺎﻛ ﺍﺫﺇﻭ ،ﺎﻬﺑ ﺔﺻﺎﺨﻟﺍ ﻕﺎﻴ

Aura's ﻊﻣ ﻝﺎﺜﻤﻟﺍ ﻞﻴﺒﺳ ﻰﻠﻋ) ﺮﺻﺎﻨﻌﻟﺍ ﺔﻓﺮﻏ ﻲﻓ ﺔﺑﺎﺘﻜﻟﺍ ﻭﺃ ءﻼ﻿ﻣﻹ﻿ﺍ :ﻲﺟﺫ
    ﺪﻫﺎﺷﻭ ،Threema ﺔﺷﺩﺭﺩ ﻰﻟﺇ ﺺﻨﻟﺍ ﻝﻮﺻﻭ ﺐﻠﻃﺍﻭ (ﺺﻧ ﻰﻟﺇ ﻡﻼ﻿ﻜﻟﺍ ﻞﻳﻮﺤﺗ
                          .ﺮﺻﺎﻨﻌﻟﺍ ﺔﻓﺮﻏ ﺲﻔﻧ ﻲﻓ Threema ﺩﻭﺩﺭ ﺮﻬﻈﺗ

.ﺎﻬﻠﻴﺣﺮﺗ ﺪﻳﺮﺗ ﻲﺘﻟﺍ ﺔﻓﺮﻐﻟﺍ/ﺔﺷﺩﺭﺪﻟﺍ ﺭﺎﻬﻇﺇﻭ ،ﻝﻮﺧﺪﻟﺍ ﻞﻴﺠﺴﺗ ﻢﺘﻳ ﻥﺃﻭ ،

الحماية من الأعشاب

المرآة الساذجة ذات الاتجاهين سترفع كل رسالة إلى الأبد النفقة
يحول دون ذلك مع تاريخ قصير الأجل (`relay_history.py`):

1. ويُذكر كل نص يُرسل إلى المستقبل ** قبل** إرساله، لمدة 180 ثانية.
2. إذا ظهر نص على الجانب الآخر في هذا التاريخ، هو لنا
   &quot; صدى &quot; : يُشار إليه على أنه غير مسموع**، ويُرسل مرة أخرى.
3. A text that is new *and* unknown is a genuine message and is forwarded.

تُقارن النصوص مع انهيار الفضاء الأبيض، لذا فروق الكسر من
لا تهزم الحارس لأن القيد يموت، يمكنك إرسال
نفس النص (مثل "حسنا") مرة أخرى بعد مرور النافذة

في البداية، تُقرأ الرسالة الأخيرة الحالية لكل جانب على أنها خط سباحة** وهي
*لم تُرسل* فقط الرسائل التي تصل بعد البداية يتم نقلها

المتطلبات

- Linux with **X11** (`echo $XDG_SESSION_TYPE` mustprint `x11`). (وايلاند) غير مدعوم
- `xdotool`, `xclip`, `wmctrl`, and `xset` (optional, used to disable the screensaver)
- Element Desktop (WM class `element.Element`)
- 3ma Beta (WM class `threema beta.Threema Beta`, e.g. the Flatpak)
  `ch.threema.threema-desktop`)
- (بيثون 3) مع المشروع الافتراضي
- `zsh` لكتاب معايرة لمرة واحدة

# Setup: one-time calibration

ترسم 3ma Beta قائمة السياق الخاصة بها التي لا يمكن تشغيلها مع لوحة المفاتيح،
لذا يَنْقرُ التَرَقُّبُ "رسالةِ الكوب" مَع الفأرِ في مواقعِ نسبيةِ
نافذة ثلاثية مقاييس لهم مرة واحدة:

```zsh
scripts/py/func/threema/threema-relay.zsh calibrate
```

يطلب النص ثلاث وظائف في الفأر، كل منها مع العد التنازلي (لا تلمس
لوحة المفاتيح، لا تتحرك أو تغلق النافذة

1. ** الرسالة الأخيرة الواردة* (فقاعة على الجانب الأيسر)
   القائمة مفتوحة
2. حرّك الفأر، دون النقر، إلى **"رسالة نسخ"**.
3. حرّك الفأر إلى حقل المُدخّلات**.

وتخزن النتيجة في `~/.config/threema-relay.conf`:

| Key   meaning |
|---|---|
| `FX` | Horizontal react position as a fraction of the window width  the
| `BOTTOM` s Click position, pixels above the window's bottom edge |
| `DX`, `DY`  the Offset from the call to "Copy Message" "
| `INPUT_FX`, `INPUT_BOTTOM` | Position of the message input field |
| `DELAY_MENU`, `DELAY_COPY` s Optional waits in seconds (defaults 0.30 / 0.20) |

تحقق من المعايرة مع رسالة جديدة واردة كآخر رسالة في الدردشة:

```zsh
scripts/py/func/threema/threema-relay.zsh test
```

إنه يطبع النص المنسخ بدون إرساله العيار يعتمد على النافذة
الهندسة: إذا غيّرت حجم نافذة 3ma كثيرا، معايرة مرة أخرى.

# Usage

من جذور المستودع:

```zsh
PYTHONPATH=. .venv/bin/python3 scripts/py/func/threema/matrix_threema_relay.py
```

الخيارات:

| Option   Effect |
|---|---|
| `--poll SECONDS` ) Poll interval (default `2.0`) |
| `--no-threema-to-element` | Relay only Element | threema |
| `--no-element-enter` ) Paste Threema messages into Element's input field but do **not** send them (safe test mode) )

توقّفْ مَع `Ctrl+C`.

الركض الأول الموصى به: استخدام `--no-element-enter`، إرسال رسالة لنفسك في 3ma
وتحقق من أنه يظهر في مدخل (إيمنت) ثم اهرب بدون الخيار

سجل مثال:

```
[INFO] Initial Element baseline: 'Test'
[INFO] Initial Threema baseline: 'kaa'
[INFO] New Element message -> Threema: 'Hallo Welt'
[INFO] New Threema message -> Element: 'müsli'
[INFO] Element shows our own relayed text - not sending back.
```

# How it works

```
every poll interval
├─ Element:  focus window (wmctrl) → Up, Ctrl+A, Ctrl+C, Escape (xdotool) → read clipboard (xclip)
│            new + unknown  → paste into Threema + Return, remember text
│            new + known    → echo, ignore
└─ Threema:  focus window → right-click last incoming bubble → click "Copy Message"
                          → click input field (restores focus) → read clipboard
             new + unknown  → paste into Element (+ Return), remember text
             new + known    → echo, ignore
```

- في مركب (إيلينتر) يحرر رسالتك الأخيرة
  ويترك طريقة التحرير هذا هو السبب فقط ** عنصرك الخاص**
  تُنقل الرسالة إلى "ثلاثيما".
- بالنسبة لـ 3ma a **sentinel string** وَضعَ في مشبكِ أولاً. إذا كان لا يزال
  بعد ذلك، لم يتم نسخ شيء (على سبيل المثال لأن رسالتك هي
  والنقطة الأخيرة والنقر لم يضربا أي فقاعة، وتتجاهل المحاولة.

الملفات

File   Purpose |
|---|---|
| `matrix_threema_relay.py` ) الحلقة الرئيسية، CLI، منطق القرار (`classify_candidate`) |
| `read_last_element_message.py` s Read Element آخر رسالة الخاصة |
| `send_to_threema_window.py`   Pastes text into Threema Beta |
| `read_last_threema_message.py` s Reads Threema آخر رسالة واردة، حمولات معايرة |
| `send_to_element_window.py`   Pastes text into Element |
| `relay_history.py`   Loop protection |
| `threema-relay.zsh` ) Calibration and manual test tool (`calibrate`, `test`) |
| `test_threema_relay.py` ) Unit tests (no X11 required) |

أجري الاختبارات مع:

```zsh
PYTHONPATH=. .venv/bin/python3 -m unittest scripts.py.func.threema.test_threema_relay
```

الحديات

- ** تُستخدم النفقة فأرك ومحور تركيزك. ? ? خلال كل استطلاع
  Element Windows are focused and the mouse jumps briefly ( it is restored). لا
  من النوع الذي يُجرى فيه الاقتراع، أو يُستخدم فيه جهازاً أطول من طراز `--poll`.
- يكتب اللوحة على كل إستطلاع
- رسالة أخيرة في (ثلاثيما)** عندما تكون رسالتك الأخيرة في (الثالثة)
  (تشات)، رد وصل قبل أن يُشاهد
- ** تُقرأ الرسالة الأخيرة فقط** لكل اقتراع. إذا وصلت عدة رسائل
  على فترات، فقط الأحدث يتم نقله
- ** النص فقط**. الصور والملفات و ردود الفعل والمحررات لا يتم نقلها
- ** زوج حديث** أيًّا كان الدردشة/الغرفة مفتوحة في كلّ نافذة، يُستخدم.
- مسودّة في مُدخل (إيمنت)** ستُدمج مع المُسابقة القادمة
  رسالة
- **X11 فقط**. (وايلاند) يحجب المدخلات الاصطناعية وتغيرات تركيز النوافذ
- The relay disables the X11 screensaver and DPMS on start (`xset s off -dpms`);
  يبقون مبتعدين حتى تعيدي تشغيلهم أو تدخلي مجدداً

? Problemubleshooting

| Symptom   Likely cause / fix |
|---|---|
| `Threema window ... not found` ). check `xdotool search --class "Threema Beta"` and `xprop WM_CLASS` (click the window). ).
| `Nothing copied` / no Threema . Element . Re-run `calibrate`; run `test` with an incoming message as the last one. زيادة `DELAY_MENU`/`DELAY_COPY` في الثقة على آلة بطيئة. .
| Text arrives in Threema but is not sent . Input field not focused; check `INPUT_FX`/`INPUT_BOTTOM` from calibration. |
| Threema text appears in Element but is not sent | لقد بدأت عملية النقل مع (سينلينكود 10اكس)
. Decimal numbers like `0,9353` in the config . written by an older script version under a German locale. قانون (بيثون) يقبلهم، يُعاد ترتيبه مع النص الحالي يكتب النقاط. ?
