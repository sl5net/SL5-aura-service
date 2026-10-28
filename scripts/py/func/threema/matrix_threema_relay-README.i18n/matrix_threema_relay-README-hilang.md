> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../matrix_threema_relay-README.md).*

# तत्व ↔ Threema बीटा GUI रिले

एक छोटा डिमोन जो संदेशों को **Element Desktop** (मैट्रिक्स) और के बीच दर्पण करता है
**Threema बीटा** (Threema डेस्कटॉप क्लाइंट) लिनक्स/X11 पर दोनों को चलाकर
एक उपयोगकर्ता की तरह विंडोज़ का उपयोग करें: कीबोर्ड शॉर्टकट, क्लिपबोर्ड और कुछ माउस क्लिक।

कोई API नहीं, कोई टोकन नहीं, कोई अतिरिक्त Python लाइब्रेरी नहीं। केवल स्टैण्डर्ड X11 कमांड-लाइन टूल्स।

## यह क्या करता है

| दिशा | क्या होता है |
|---|---|
| **एलीमेंट → थ्रीमा** | अंतिम संदेश *जो आपने* एलीमेंट में लिखा था, पढ़ा जाता है और यदि यह नया है, तो थ्रीमा बीटा में चिपकाया जाता है और भेजा जाता है। |
| **Threema → Element** | खुले Threema चैट का आखिरी *आने वाला* संदेश उसके संदर्भ मेनू के माध्यम से कॉपी किया जाता है और, यदि यह नया है, तो Element में चिपकाया जाता है और भेजा जाता है। |

सामान्य उपयोग: एक एलिमेंट रूम में बोलकर या टाइप करके डालना (उदाहरण के लिए ऑरा के साथ)
स्पीच-टू-टेक्स्ट) और टेक्स्ट थ्रीमा चैट में पहुँच जाए, और देखें कि
थ्रीमा के उत्तर उसी एलीमेंट कमरे में दिखाई देते हैं।

दोनों विंडो खुली होनी चाहिए, लॉग इन होनी चाहिए, और वह चैट/रूम दिखा रही हो जिसे आप रिले करना चाहते हैं।

## लूप सुरक्षा

एक नौसैनिक दो-तरफा दर्पण हर संदेश को वापस और आगे हमेशा के लिए उछाल देगा। रिले
इसे अल्पकालिक इतिहास (`relay_history.py`) से रोकता है:

1. प्रत्येक पाठ को रिले फ़ॉरवर्ड्स याद किया जाता है ** पहले** यह 180 सेकंड के लिए भेजा जाता है।
2. यदि कोई पाठ इस इतिहास में है, तो यह हमारा है
   गूंज: यह देखा गया है लेकिन ** नहीं ** फिर से आगे बढ़ना।
3. एक ऐसा पाठ जो नया है *और* अज्ञात एक वास्तविक संदेश है और इसे अग्रेषित किया जाता है।

पाठों की तुलना व्हाइटस्पेस पतन के साथ की जाती है, इसलिए लाइन ब्रेक अंतर से
कॉपी / पेस्ट गार्ड को हरा नहीं है। क्योंकि प्रविष्टियां मर जाती हैं, आप भेज सकते हैं
एक ही पाठ (उदाहरण के लिए "ok") फिर से खिड़की के पारित होने के बाद।

स्टार्ट-अप पर प्रत्येक पक्ष के वर्तमान अंतिम संदेश को **बेसलाइन* के रूप में पढ़ा जाता है और यह है
* आगे नहीं* केवल वही संदेश जो प्रारंभ होने के बाद आते हैं।

## आवश्यकताएँ

- Linux के साथ **X11** (`echo $XDG_SESSION_TYPE` को `x11` प्रिंट करना चाहिए)। वेइलैंड समर्थित नहीं है।
- `xdotool`, `xclip`, `wmctrl`, और `xset` (वैकल्पिक, स्क्रीनसेवर को अक्षम करने के लिए उपयोग किया जाता है)
- एलेमेंट डेस्कटॉप (WM क्लास `element.Element`)
- Threema बीटा (WM क्लास `threema beta.Threema Beta`, जैसे कि फ्लैटपैक
  `ch.threema.threema-desktop`)
- परियोजना के वर्चुअलएन्व के साथ पायथन 3
- एक बार के कैलिब्रेशन स्क्रिप्ट के लिए `zsh`

## सेटअप: एक बार अंशांकन

थ्रीमा बीटा अपने स्वयं के संदर्भ मेनू को आकर्षित करता है जिसे कीबोर्ड के साथ संचालित नहीं किया जा सकता है,
इसलिए रिले "कॉपी संदेश" पर माउस के साथ स्थिति के सापेक्ष क्लिक करता है
थ्रीमा विंडो। उन्हें एक बार मापें:

```zsh
scripts/py/func/threema/threema-relay.zsh calibrate
```

स्क्रिप्ट तीन माउस पदों के लिए पूछता है, प्रत्येक एक उलटी गिनती के साथ (जो स्पर्श नहीं है)
कीबोर्ड, विंडो को स्थानांतरित या आकार नहीं करते हैं:

1. ** राइट-क्लिक** आखिरी * आने वाला* संदेश (बाएं तरफ एक बुलबुला) और छोड़ दें
   मेनू खुला।
2. माउस ले जाएँ, बिना क्लिक किये, ** "कॉपी संदेश"* पर।
3. माउस को ** संदेश इनपुट फ़ील्ड* पर ले जाएँ।

परिणाम `~/.config/threema-relay.conf` में संग्रहीत है:

To make a key.
|---|---|
`FX` | क्षैतिज क्लिक स्थिति विंडो चौड़ाई के एक अंश के रूप में
`BOTTOM` | क्लिक स्थिति, विंडो के नीचे के किनारे के ऊपर पिक्सेल
`DX`, `DY` | क्लिक बिंदु से "कॉपी संदेश" तक ऑफसेट
`INPUT_FX`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_FX`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_FX`, `INPUT_FX`, `INPUT_BOTTOM`, `INPUT_FX`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`, `INPUT_BOTTOM`,
`DELAY_MENU`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_MENU`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_MENU`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`, `DELAY_COPY`,

चैट में आखिरी संदेश के रूप में आने वाले ताज़ा संदेश के साथ कैलिब्रेशन जांचें:

```zsh
scripts/py/func/threema/threema-relay.zsh test
```

यह कॉपी किए गए टेक्स्ट को फ़ॉरवर्ड किए बिना प्रिंट करता है। कैलिब्रेशन विंडो पर निर्भर करता है।
ज्यामिति: अगर आप Threema विंडो का आकार बहुत बदलते हैं, तो फिर से कैलिब्रेट करें।

## उपयोग

भंडार की जड़ से:

```zsh
PYTHONPATH=. .venv/bin/python3 scripts/py/func/threema/matrix_threema_relay.py
```

विकल्प:

| विकल्प | प्रभाव |
|---|---|
| `--poll SECONDS` | मतदान अंतराल (डिफ़ॉल्ट `2.0`) |
| `--no-threema-to-element` | केवल रिले तत्व → थ्रीमा |
| `--no-element-enter` | Element के इनपुट फील्ड में Threema संदेश पेस्ट करें लेकिन उन्हें **भेजें नहीं** (सुरक्षित परीक्षण मोड) |

`Ctrl+C` के साथ रुकें।

पहली सिफारिश की गई रन: `--no-element-enter` का उपयोग करें, थ्रीमा में अपने आप को एक संदेश भेजें
और जाँच करें कि यह एलिमेंट के इनपुट फील्ड में दिखाई दे रहा है। फिर विकल्प के बिना चलाएँ।

उदाहरण लॉग:

```
[INFO] Initial Element baseline: 'Test'
[INFO] Initial Threema baseline: 'kaa'
[INFO] New Element message -> Threema: 'Hallo Welt'
[INFO] New Threema message -> Element: 'müsli'
[INFO] Element shows our own relayed text - not sending back.
```

क्या यह काम करता है

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

- * तत्व के संगीतकार में अप* अपने अंतिम संदेश को संपादित करता है; *Ctrl+A / Ctrl+C* प्रतियां
  यह और * बच* संपादित मोड छोड़ देता है। यही कारण है कि केवल ** अपने ही* * आखिरी तत्व
  संदेश को थ्रीमा से रिले किया जाता है।
- थ्रीमा के लिए ** सेंटिनल स्ट्रिंग ** पहले क्लिपबोर्ड में डाल दिया जाता है। अगर यह अभी भी है
  बाद में, कुछ भी कॉपी नहीं किया गया (उदाहरण के लिए क्योंकि आपका अपना संदेश है)
  आखिरी एक और क्लिक हिट नो बबल) और प्रयास को नजरअंदाज कर दिया गया है।

## फ़ाइलें

To use a file.
|---|---|
`matrix_threema_relay.py` (`classify_candidate`)
`read_last_element_message.py` (`read_last_element_message.py`)
`send_to_threema_window.py` (`send_to_threema_window.py`)
`read_last_threema_message.py` | Reads Threema's last incoming संदेश, loads calibration, |
`send_to_element_window.py` (`send_to_element_window.py`)
`relay_history.py`
`threema-relay.zsh` (XINlineCODE8X)
`test_threema_relay.py` | यूनिट परीक्षण (कोई X11 आवश्यक नहीं)

टेस्ट चलाएँ साथ में:

```zsh
PYTHONPATH=. .venv/bin/python3 -m unittest scripts.py.func.threema.test_threema_relay
```

## सीमाएं

- ** रिले आपके माउस और कीबोर्ड फोकस का उपयोग करता है। ************ प्रत्येक मतदान के दौरान तीनमा और
  तत्व विंडोज ध्यान केंद्रित कर रहे हैं और माउस को संक्षेप में कूदते हैं (यह बहाल किया गया है)। नहीं
  जबकि एक पोल रन टाइप करें, या अब `--poll` का उपयोग करें।
- प्रत्येक मतदान पर क्लिपबोर्ड को ओवरराइट करता है।
- **{{{}{{}{}{}{}{}{}}{}{}}{}}{}}{}}{}}{}}{}}}{}}{}}{}}}}{}}}}{}}}{}}}}}{}}{}}}}{}}}}}{}}{}}}}{}}}{}}}{}}}{}{}}{}}}{}}{}}{}}{}}{}}}}{}}{}}}{}}}}}}{}}}}}}}}{}}}}}}}{}}}}}}{}}}}}}}{}{}{}}}}}}}}}}}}}}}}}{}}{}{}{}{}}}}{}{}{}{}{}{}}}}{}{}{}}{}{}{}{}}{}{}}{}}}}}}}}
  चैट, एक जवाब है कि सिर्फ इससे पहले कि यह नहीं देखा गया है।
- **केवल अंतिम संदेश* प्रति मतदान पढ़ी जाती है। यदि कई संदेश एक के भीतर आते हैं
  अंतराल, केवल नवीनतम रिले किया जाता है।
- ** छवियाँ, फाइलें, प्रतिक्रियाएं और संपादन नहीं किए जाते हैं।
- ** एक चैट जोड़ी प्रत्येक विंडो में जो भी चैट/रूम खुलता है उसका उपयोग किया जाता है।
- ** एलिमेंट के इनपुट फ़ील्ड में एक ड्राफ्ट* को अगले पेस्ट के साथ जोड़ा जाएगा
  संदेश
- ** वेलैंड सिंथेटिक इनपुट और विंडो फोकस परिवर्तन को अवरुद्ध करता है।
- रिले X11 स्क्रीनसेवर और DPMS को स्टार्ट (XINlineCODE1X) पर निष्क्रिय करता है;
  जब तक आप उन्हें फिर से सक्षम नहीं करते हैं या फिर लॉग इन नहीं करते हैं।

## समस्या निवारण

The symptom of the symptom is likely कारण / फिक्स
|---|---|
`Threema window ... not found` | `xdotool search --class "Threema Beta"` और `xprop WM_CLASS` की जाँच करें (विंडो पर क्लिक करें)।
`Nothing copied` / no threema → Element | Re-run `calibrate`; पिछले एक के रूप में आने वाले संदेश के साथ `test` चलाएं। `DELAY_MENU` / `DELAY_COPY` को एक धीमी मशीन पर विन्यास में बढ़ाएं।
पाठ | थ्रीमा में आता है लेकिन इसे नहीं भेजा जाता है, इनपुट फ़ील्ड केंद्रित नहीं है; चेक `INPUT_FX`/`INPUT_BOTTOM` अंशांकन से।
The threema text in the एलिमेंट, लेकिन नहीं भेजा जाता रिले `--no-element-enter` के साथ शुरू किया गया था।
Decimal number of `0,9353` in the config | एक जर्मन स्थानीय के तहत एक पुराने स्क्रिप्ट संस्करण द्वारा लिखित। पायथन कोड उन्हें स्वीकार करता है; वर्तमान स्क्रिप्ट के साथ फिर से कैलिब्रेट डॉट्स लिखते हैं। (c)
