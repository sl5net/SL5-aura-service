> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

# ⬟ SL5 ऑरा – आपकी आवाज़। आपके नियम।

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 100% ऑफ़लाइन, गोपनीयता-प्रथम वॉइस असिस्टेंट फ्रेमवर्क.  
> सटीक रूप से परिभाषित करें कि आपकी आवाज़ क्या करती है — एक शब्द से
> पूरा Python स्क्रिप्ट तक। कोई क्लाउड नहीं। कोई डेटा आपके मशीन को नहीं छोड़ता।  
> टर्मिनल, ब्राउज़र में, या बैकग्राउंड सेवा के रूप में चलता है — Linux, macOS, और Windows पर।

| 👵 शुरुआती | 🎓 सीखने वाला | 🧑‍💻 डेवलपर |
|---|---|---|
| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-hilang.md#the-oma-modus-beginner-shortcut) : बस एक शब्द लिखें, बाकी काम ऑरा करती है | कोअन के साथ सीखें — एक समय में एक अवधारणा | पूर्ण पायथन स्क्रिप्टिंग, प्लगइन्स, एपीआई कॉल्स |
| 🗄️ स्टेट प्रबंधन | Trino + Airflow ऑर्केस्ट्रेशन, fzf, CopyQ, वॉइस/टर्मिनल कमांड, ब्राउज़र यूआई |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **प्रति परीक्षण ~2.87 J** (39 tests without LanguageTool across >800 maps @ 0.07s warm / 0.36s cold 🌿 measured with XMDLINK1X) · बिना क्लाउड कंप्यूट

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **पूर्ण परीक्षण सेट:** 94 परीक्षण LanguageTool के साथ >800 मैप्स पर @ 0.07s वार्म / 0.46s कोल्ड · कोई क्लाउड कंप्यूट नहीं

<details>
<summary>त्वरित प्रारंभ</summary>

## त्वरित शुरूआत

### विकल्प A: 1-क्लिक और वेब इंस्टॉलर (Recommended)

Linux, macOS और Windows के लिए वन-लाइनर कमांड या स्टैंडअलोन इंस्टॉलर:
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-hilang.md)**

---

## Option B: मैनुअल इंस्टालेशन (Developers / Git)

1. इस भंडार को डाउनलोड या क्लोन करें
2. अपने OS (see `setup/` folder) के लिए सेटअप स्क्रिप्ट चलाएं:
लिनक्स (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
लिनक्स (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
लिनक्स (openSUSE): `bash setup/suse_setup.sh`
(NixOS): `nix-shell setup/shell.nix` तो `bash setup/nixos_setup.sh`
==> Experimental — लेखकों द्वारा untested, फीडबैक स्वागत!   
- MacOS: `bash setup/macos_setup.sh`
- विंडोज: `setup/windows11_setup_with_ahk_copyq.bat`
3. स्टार्ट Aura: `./scripts/restart_venv_and_run-server.sh`
4. अपनी हॉटकी दबाएं और बोलें - ** [full guide →](../docs/GettingStarted.i18n/GettingStarted-hilang.md)*

---

## अनइंस्टॉलेशन
SL5 Aura पृष्ठभूमि सेवाओं, ऑटोस्टार्ट प्रविष्टियों और आभासी वातावरण को हटाने के लिए:
** लिनक्स / मैक ओएस: ** `bash setup/uninstall.sh`
** Windows (PowerShell):* `powershell -File setup/uninstall.ps1`
*(Your custom rules in `config/maps/` are kept safe by default unless you specify `--purge`).*

---


**

** विंडोज:*
** MacOS: ** पूरी तरह से समर्थित (uses AppleScript)
** लिनक्स (X11/Xorg): ** पूरी तरह से समर्थित।
** लिनक्स (Wayland): ** पूरी तरह से समर्थित (tested on KDE Plasma 6 / Wayland)
** लिनक्स (CachyOS / Arch-based rolling release): ** पूरी तरह से समर्थित।
Glibc 2.43 संगतता के कारण mimalloc (`sudo pacman -S mimalloc`) की आवश्यकता है।
**Linux (NixOS):***: Experimental — सामुदायिक योगदान सेटअप, अभी तक परीक्षण नहीं.
यदि आप इसे आज़माते हैं, तो कृपया अपने निष्कर्षों के साथ एक मुद्दा या PR खोलें!   
** लिनक्स (Manjaro): ** नया: एक सिस्टम-वाइड हॉटकी एक fzf-like, कीबोर्ड संचालित इंटरफ़ेस खोलता है ताकि आप डेस्कटॉप (completely decoupled from the active window) पर कहीं से Aura कमांड चला सकें। इस हॉटकी-चालित लॉन्चर को वर्तमान में लिनक्स (Manjaro) पर कार्यान्वित और परीक्षण किया गया है; अन्य वितरण सेटअप की आवश्यकता पर काम कर सकते हैं। [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-hilang.md)    में देखें  


    
SL5 Aura एक पूर्ण, **ऑफलाइन वॉयस असिस्टेंट **वोस्क ** (for Speech-to-Text) और **LanguageTool** (for Grammar/Style) पर बनाया गया है, जिसमें एक वैकल्पिक **Local LLM (Ollama) Fallback** * रचनात्मक प्रतिक्रियाओं और उन्नत फजी मिलान के लिए शामिल है। यह आपकी आवाज को सटीक कार्यों और पाठ में बदल देता है, जो प्लग करने योग्य नियम प्रणाली और एक गतिशील स्क्रिप्टिंग इंजन के माध्यम से परम अनुकूलन के लिए डिज़ाइन किया गया है।
    
अनुवाद: यह दस्तावेज़ [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n) में भी मौजूद है।


नोट: कई ग्रंथ मूल अंग्रेजी दस्तावेज़ीकरण के मशीनीकृत अनुवाद हैं और केवल सामान्य मार्गदर्शन के लिए इरादा हैं। विवेक या अस्पष्टता के मामले में, अंग्रेजी संस्करण हमेशा प्रबल होता है। हम इस अनुवाद को बेहतर बनाने के लिए समुदाय से मदद का स्वागत करते हैं!

</details>

<details>
<summary>Demo</summary>

### 📺 टर्मिनल डेमो

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **संकेत:** बेहतर टर्मिनल अनुभव के लिए, [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-hilang.md) देखें।

### 🎥 वीडियो ट्यूटोरियल
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Alternative link: XMDLINK1X)*

</details>

<details>
<summary>मुख्य विशेषताएँ</summary>

## कुंजी सुविधाएँ

* ** ऑफ़लाइन और निजी:* 100% स्थानीय। कोई डेटा कभी भी आपकी मशीन को छोड़ देता है।
** डायनेमिक स्क्रिप्टिंग इंजन:* पाठ प्रतिस्थापन से परे जाओ। नियम कस्टम पायथन स्क्रिप्ट (`on_match_exec`) को निष्पादित कर सकते हैं जैसे एपीआई (e.g., search Wikipedia) को कॉल करना, फ़ाइलों (e.g., manage a to-do list) के साथ बातचीत करना, या गतिशील सामग्री (e.g., a context-aware email greeting) उत्पन्न करना।
**Context-Aware Rules:* विशिष्ट अनुप्रयोगों के लिए प्रतिबंधित नियम। `only_in_windows` का उपयोग करके, आप एक नियम को केवल तभी ट्रिगर कर सकते हैं जब एक विशिष्ट विंडो शीर्षक (e.g., "Terminal", "VS Code" or "Browser") सक्रिय हो। यह क्रॉस-प्लेटफॉर्म (Linux, Windows, macOS) काम करता है।
** उच्च-नियंत्रण परिवर्तन इंजन:* एक विन्यास संचालित, अत्यधिक अनुकूलन प्रसंस्करण पाइपलाइन को लागू करता है। नियम प्राथमिकता, आदेश का पता लगाने और पाठ परिवर्तन पूरी तरह से फजी मैप्स में नियमों के अनुक्रमिक आदेश द्वारा निर्धारित किए जाते हैं, जिसके लिए ** विन्यास की आवश्यकता होती है, कोडिंग नहीं**।
** कंज़र्वेटिव रैम उपयोग:* बुद्धिमानी से स्मृति, प्रीलोडिंग मॉडल का प्रबंधन करता है, अगर पर्याप्त मुफ्त रैम उपलब्ध है, तो अन्य अनुप्रयोगों को सुनिश्चित करना (like your PC games) हमेशा प्राथमिकता है।
** क्रॉस-प्लेटफ़ॉर्म:* लिनक्स, मैकओएस और विंडोज पर काम करता है।
* ** पूरी तरह से स्वचालित: * अपनी भाषा टूल सर्वर (but you can also use an external one) प्रबंधित करें।
* ** ब्लेज़िंग फास्ट:* इंटेलिजेंट कैशिंग तत्काल "लिस्टनिंग" अधिसूचनाओं और तेज प्रसंस्करण सुनिश्चित करता है।
** त्रिनो के माध्यम से डायनेमिक स्टेट मैनेजमेंट:* इंटरफ़ेस-aware विन्यास इंजन
XINlineCODE2X, `terminal` और `web` के लिए सेटिंग्स को अलग करता है - बिना किसी बदलाव के
दूसरों को प्रभावित करना। एक वास्तविक समय ** एडमिन डैशबोर्ड ** (port 8084) शामिल हैं।
</details>

<details>
<summary>.
    
## 🔌 तैयार-से-उपयोग इंटीग्रेशन

SL5-Aura एक विशाल इकोसिस्टम के साथ आता है जिसमें **100+ प्री-कॉन्फ़िगर किए गए प्लगइन्स** शामिल हैं। यहाँ कुछ मुख्य बातें हैं:

## OculiX / SikuliX IDE वॉयस कंट्रोल
SL5-Aura ** Oculix** और **SikuliX IDE* के लिए प्रथम श्रेणी की आवाज समर्थन प्रदान करता है। यह एकीकरण आपको अपने स्वचालन कोड को "स्पाक" करने की अनुमति देता है।

**वोइस-टू-स्निपेट:* "क्लिक करें", "वैइट", या "सभी को खत्म करें", और सेवा तुरंत आईडीई में सही पायथन कोड (e.g., `click("image.png")`) टाइप करती है।
** विंडो-Aware:* प्लगइन संदर्भ-संवेदनशील है; यह केवल तभी सक्रिय होता है जब OculiX/SikuliX विंडो केंद्रित होती है।
** स्मार्ट अंग्रेजी समर्थन:* `en-US` के लिए ऑप्टिमाइज़ किया गया, जिसमें गैर-मूल उच्चारण (e.g., German-English phonetics) पर विशेष ध्यान दिया गया है, जो वैश्विक समुदाय के लिए उच्च मान्यता सटीकता सुनिश्चित करता है।
** आसानी से संपादित `FUZZY_MAP_pre.py` प्रारूप का उपयोग करता है।

> ** OculiX टीम (see XMDLINK0X) द्वारा सामुदायिक प्लगइन के रूप में मान्यता प्राप्त है।

### LibreOffice आईडीई वॉइस कंट्रोल

### 0 ई.स. वॉइस कंट्रोल

---

</details>


<details>
<summary>प्रलेखन</summary>

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)

## दस्तावेज़ीकरण

एक पूर्ण तकनीकी संदर्भ के लिए, जिसमें सभी मॉड्यूल और स्क्रिप्ट शामिल हैं, कृपया हमारे आधिकारिक प्रलेखन पृष्ठ पर जाएं। यह स्वचालित रूप से उत्पन्न होता है और हमेशा अद्यतन होता है।

👉 [**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)

### फीचर स्पॉटलाइट
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-hilang.md) - दोहरी पेन `fzf` नियम खोज, लाइव संदर्भ पूर्वावलोकन, XINlineCODE1X / `Ctrl+R` के माध्यम से तत्काल आदेश निष्पादन और `Ctrl+E` के माध्यम से संपादक एकीकरण। एक वैश्विक हॉटकी (`Super+S`) द्वारा समर्थित और कई समर्पित खोज-पर्यावरणों ने आवाज कमांड के माध्यम से पूर्व विन्यास किया।

################################################################################################################################################################################################################################################################

[![Linux Manjaro](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)

[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/mac_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/win11_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![OculiX Compatible](https://img.shields.io/badge/OculiX-Compatible-blueviolet?style=for-the-badge&logo=python)](https://github.com/oculix-org/Oculix)
<div align="left">
<a href="https://github.com/sl5net/SL5-aura-service/stargazers">
<img src="https://img.shields.io/github/stars/sl5net/SL5-aura-service?style=social" alt="Stargazers">
</a>
<img src="https://img.shields.io/github/license/sl5net/SL5-aura-service" alt="License">
<a href="https://sl5net.github.io/SL5-aura-service/">
<img src="https://img.shields.io/badge/documentation-live-brightgreen" alt="Documentation">
</a>
</div>

</details>

**इसे अन्य भाषाओं में पढ़ें:*

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-hilang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-hilang.md) | [🇪🇸 Español](../README.i18n/README-eslang-hilang.md) | [🇫🇷 Français](../README.i18n/README-frlang-hilang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-hilang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-hilang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-hilang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-hilang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-hilang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-hilang.md)

---

<details>
<summary>Installation</summary>

## स्थापना

बिना मॉडरेशन (Manjaro/Arch Video)
पूर्ण 6 मिनट की सेटअप प्रक्रिया देखें:
डाउनलोड:* ~3 मिनट
** सेटअप और फर्स्ट स्टार्ट:* ~ 3 मिनट (including Welcome Wizard)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


सेटअप एक दो-चरण प्रक्रिया है:
1. नवीनतम रिलीज या मास्टर ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) डाउनलोड करें या अपने कंप्यूटर के लिए इस भंडार को क्लोन करें।
2. अपने ऑपरेटिंग सिस्टम के लिए एक बार सेटअप स्क्रिप्ट चलाएं।

सेटअप स्क्रिप्ट सब कुछ संभालती हैं: सिस्टम निर्भरताएं, पायथन पर्यावरण, और आवश्यक मॉडल और उपकरण (~4GB) को सीधे अधिकतम गति के लिए हमारे गिटहब रिलीज से डाउनलोड करती हैं।


####                                                                                                                             

डिस्क स्पेस और बैंडविड्थ को बचाने के लिए, आप सेटअप के दौरान विशिष्ट भाषा मॉडल (`de`, `en`) या सभी वैकल्पिक मॉडल (`all`) को बाहर कर सकते हैं। ** कोर घटक (LanguageTool, lid.176) हमेशा शामिल हैं।*

परियोजना की मूल निर्देशिका में एक टर्मिनल खोलें और अपने सिस्टम के लिए स्क्रिप्ट चलाएं:

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

# For Arch-based systems (Manjaro, CachyOS, EndeavourOS, etc.):
`bash setup/manjaro_arch_setup.sh`

```sudo pacman -S mimalloc```


# Examples:
# Install everything (Default):
# bash setup/manjaro_arch_setup.sh

# Exclude German models:
# bash setup/manjaro_arch_setup.sh exclude=de

# Exclude all VOSK language models:
# bash setup/manjaro_arch_setup.sh exclude=all

# For Windows in an Admin-Powershell session

setup/windows11_setup.ps1 -Exclude [OPTION]

# Examples:
# Install everything (Default):
# setup/windows11_setup.ps1

# Exclude English models:
# setup/windows11_setup.ps1 -Exclude "en"

# Exclude German and English models:
# setup/windows11_setup.ps1 -Exclude "de,en"

# Or (recommend) - Run the BAT file: 
windows11_setup.bat -Exclude "en"
```

###
व्यवस्थापक विशेषाधिकारों के साथ सेटअप स्क्रिप्ट चलाएं।

** पढ़ने और चलाने के लिए एक उपकरण स्थापित करें, उदाहरण के लिए, [CopyQ](https://github.com/hluk/CopyQ) या [AutoHotkey v2](https://www.autohotkey.com/)*। यह पाठ टाइपिंग घड़ी के लिए आवश्यक है।

स्थापना पूरी तरह से स्वचालित है और एक ताजा प्रणाली पर 2 मॉडल का उपयोग करते समय लगभग 8-10 मिनट** लेता है।

1. `setup` फ़ोल्डर में नेविगेट करें।
2. ** `windows11_setup_with_ahk_copyq.bat`* पर डबल क्लिक करें।
* * स्क्रिप्ट स्वचालित रूप से प्रशासक विशेषाधिकारों के लिए संकेत देगा।*
* यह कोर सिस्टम, भाषा मॉडल, **AutoHotkey v2**, और **CopyQ** स्थापित करता है।*
3. एक बार इंस्टॉलेशन पूरा होने के बाद, **Aura Dictation** स्वचालित रूप से लॉन्च होगा।

> ** आपको पहले पायथन या गिट स्थापित करने की आवश्यकता नहीं है; स्क्रिप्ट सब कुछ संभालती है।

---

### उन्नत / कस्टम स्थापना
यदि आप क्लाइंट टूल (AHK/CopyQ) को इंस्टॉल नहीं करना चाहते हैं या विशिष्ट भाषाओं को छोड़कर डिस्क स्पेस को सहेजना चाहते हैं, तो आप कमांड लाइन के माध्यम से मुख्य स्क्रिप्ट चला सकते हैं:

```powershell
# Core Setup only (No AHK, No CopyQ)
setup/windows11_setup_with_ahk_copyq.bat

# Exclude specific language models (saves space):
# Exclude English:
setup/windows11_setup_with_ahk_copyq.bat -Exclude "en"

# Exclude German and English:
setup/windows11_setup_with_ahk_copyq.bat -Exclude "de,en"
```

---
</details>


<details>
<summary>Usage</summary>

# उपयोग

## 1। सेवा शुरू करें

###                                                                   
एक एकल स्क्रिप्ट सब कुछ संभालती है। यह मुख्य तानाशाही सेवा शुरू करता है और फ़ाइल दर्शक स्वचालित रूप से पृष्ठभूमि में।
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

###
सेवा शुरू करना एक ** दो-चरण मैनुअल प्रक्रिया है*:

1. ** मेन सर्विस शुरू करें:* रन `start_aura.bat`. या `.venv` से शुरू होकर `python3` के साथ सेवा शुरू करें

##2. अपने हॉटकी को कॉन्फ़िगर करें

डिक्टेशन को ट्रिगर करने के लिए, आपको एक वैश्विक हॉटकी की आवश्यकता है जो एक विशिष्ट फ़ाइल बनाता है। हम अत्यधिक क्रॉस-प्लेटफॉर्म टूल [CopyQ](https://github.com/hluk/CopyQ) की सिफारिश करते हैं।

### हमारी सिफारिश: CopyQ

एक वैश्विक शॉर्टकट के साथ कॉपीक्यू में एक नया कमांड बनाएं।

** Linux/macOS के लिए
```bash
touch /tmp/sl5_record.trigger
```

** [CopyQ](https://github.com/hluk/CopyQ) का उपयोग करते समय Windows के लिए कमीशन:*
```js
copyq:
var filePath = 'c:/tmp/sl5_record.trigger';

var f = File(filePath);

if (f.openAppend()) {
    f.close();
} else {
    popup(
        'error',
        'cant read or open:\n' + filePath
        + '\n' + f.errorString()
    );
}
```


** [AutoHotkey](https://AutoHotkey.com) का उपयोग करते समय Windows के लिए कमीशन:*
```sh
; trigger-hotkeys.ahk
; AutoHotkey v2 Skript
#SingleInstance Force ; Stellt sicher, dass nur eine Instanz des Skripts läuft

;===================================================================
; Hotkey zum Auslösen des Aura Triggers
; Drücke Strg + Alt + T, um die Trigger-Datei zu schreiben.
;===================================================================
f9::
f10::
f11::
{
    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("Aura Trigger ausgelöst!")
    SetTimer(() => ToolTip(), -1500)
}
```


##1.
किसी भी टेक्स्ट फ़ील्ड में क्लिक करें, अपनी हॉटकी दबाएं, और एक "लिस्टिंग" अधिसूचना दिखाई देगी। स्पष्ट रूप से बोलो, फिर रोकें। सही पाठ आपके लिए टाइप किया जाएगा।

</details>

---


<details>
<summary>Advanced विन्यास (Optional)</summary>

## उन्नत विन्यास (Optional)

आप एक स्थानीय सेटिंग फ़ाइल बनाकर एप्लिकेशन के व्यवहार को अनुकूलित कर सकते हैं।

1. `config/` निर्देशिका में नेविगेट करें।
2. `config/settings_local.py_Example.txt` की एक प्रति बनाएं और इसे `config/settings_local.py` में बदलें।
3. `config/settings_local.py` (it overrides any setting from the main `config/settings.py` file) संपादित करें।

इस XINlineCODE5X फ़ाइल को डिफ़ॉल्ट रूप से गिट द्वारा नजरअंदाज कर दिया गया है, इसलिए आपके व्यक्तिगत परिवर्तन अद्यतनों से अधिक नहीं होंगे।

## प्लग-इन संरचना और तर्क

सिस्टम की मॉड्यूलरिटी प्लगइन्स / डायरेक्टरी के माध्यम से मजबूत विस्तार की अनुमति देती है।

प्रसंस्करण इंजन सख्ती से एक ** ऐतिहासिक प्राथमिकता श्रृंखला का पालन करता है*:

** मॉड्यूल लोडिंग ऑर्डर (High Priority):* कोर भाषा पैक (de-DE, en-US) से लोड किए गए नियम प्लगइन्स / निर्देशिका (which load last alphabetically) से लोड किए गए नियमों पर प्राथमिकता लेते हैं।
    
2. **इन-फ़ाइल ऑर्डर (Micro Priority):* किसी भी दिए गए मानचित्र फ़ाइल (FUZZY_MAP_pre.py) के भीतर नियमों को सख्ती से ** लाइन नंबर* (top-to-bottom) द्वारा संसाधित किया जाता है।
    

यह वास्तुकला यह सुनिश्चित करती है कि कोर सिस्टम नियम संरक्षित हैं, जबकि परियोजना-विशिष्ट या संदर्भ-जारी नियम (like those for CodeIgniter or game controls) को आसानी से प्लग-इन के माध्यम से कम प्राथमिकता एक्सटेंशन के रूप में जोड़ा जा सकता है।

</details>

<details>
<summary>Key Scripts for Windows user</summary>






## विंडोज उपयोगकर्ताओं के लिए प्रमुख स्क्रिप्ट

यहाँ विंडोज़ सिस्टम पर एप्लिकेशन सेट अप, अपडेट और चलाने के लिए सबसे महत्वपूर्ण स्क्रिप्ट्स की सूची है।

### सेटअप और अपडेट

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat`: वातावरण की **प्रारंभिक एक-बार की सेटअप** के लिए मुख्य स्क्रिप्ट।
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : परियोजना फ़ोल्डर से इसे चलाएं **ताज़ा कोड और डिपेंडेंसीज़ प्राप्त करने के लिए**।

### एप्लिकेशन चलाना
*   `start_aura.bat`: **वाच्य सेवा शुरू करने** के लिए एक प्राथमिक स्क्रिप्ट।

### मुख्य और सहायक स्क्रिप्ट्स
*   `aura_engine.py`: कोर पायथन सेवा (usually started by one of the scripts above).
*   `get_suggestions.py`: विशिष्ट कार्यों के लिए एक सहायक स्क्रिप्ट।

</details>



## 🚀 प्रमुख विशेषताएँ और OS संगतता

<details>
OS संगतता के लिए लीजेंड

OS संगतता के लिए किंवदंती:  
*   🐧 **लिनक्स** (e.g., Arch, Ubuntu)  
    *   🍏 **macOS**  
*   🪟 **विंडोज़**  
*   📱 **एंड्रॉइड** (for mobile-specific features)  

---

</details>



## ** कोर स्पीच-टू-टेक्सट (Aura) इंजन **
ऑफ़लाइन भाषण मान्यता और ऑडियो प्रसंस्करण के लिए हमारा प्राथमिक इंजन।

    
<details>
<summary>Aura-Core</summary>
  
**Aura-Core/***  
├─ `aura_engine.py` (Main Python service orchestrating Aura) 🐧 🍏 🪟  
├┬ ** लाइव हॉट-रीलोड** (Config & Maps)  
│├ ** सुरक्षित निजी मानचित्र लोड हो रहा है (Integrity-First)***  
││ ** वर्कफ़्लो:* पासवर्ड संरक्षित ZIP अभिलेखागार लोड करता है।   
│├ **टेक्स्ट प्रोसेसिंग और सुधार Language ( e.g. `de-DE`, `en-US`, ... )   
│├ 1. `normalize_punctuation.py` (Standardizes punctuation post-transcription) 🐧 🍏 🪟  
│├ **इंटेलिजेंट प्री-कोरेक्शन*** (`FuzzyMap Pre` - XMDLINK0X)  
││ **************************************************************************************************************************************************************************************************************************************************************** नियम कस्टम पायथन स्क्रिप्ट (`on_match_exec`) को एपीआई कॉल, फ़ाइल I/O जैसे उन्नत कार्यों को करने या गतिशील प्रतिक्रियाओं को उत्पन्न करने के लिए ट्रिगर कर सकते हैं।   
││ **Cascading निष्पादन:* नियम क्रमिक रूप से संसाधित होते हैं और उनके प्रभाव ** संचयी* हैं। बाद में नियम पहले के नियमों द्वारा संशोधित पाठ पर लागू होते हैं।   
││ **सबसे ज्यादा प्राथमिकता बंद मानदंड:* यदि कोई नियम ** पूर्ण मैच** (^...$) को प्राप्त करता है, तो उस टोकन के लिए पूरी प्रोसेसिंग पाइपलाइन तुरंत बंद हो जाती है। यह तंत्र विश्वसनीय वॉयस कमांड को लागू करने के लिए महत्वपूर्ण है।   
│├ 3. `correct_text_by_languagetool.py` (Integrates LanguageTool for grammar/style correction) 🐧 🍏 🪟  
│├ **4. Hierarchical RegEx-Rule-Engine with Ollama AI Fallback***  
││ **परिचय नियंत्रण:* सटीक, उच्च प्राथमिकता आदेश और पाठ नियंत्रण के लिए RegEx-Rule-इंजन का उपयोग करता है।   
│├ ** वेक्टर-खोज प्लगइन** (Lazy loading): Ollama/LLM गिरने वाली परत के साथ स्थानीय वेक्टर एम्बेडिंग को जोड़कर Semantic खोज को सक्षम करता है।  
││ ** Ollama AI (Local LLM) Fallback:* ** रचनात्मक उत्तर, क्यू एंड ए और उन्नत फ़ज़ी मैचिंग* के लिए वैकल्पिक, कम प्राथमिकता जांच के रूप में सेवा करता है जब कोई निश्चित नियम पूरा नहीं होता है।   
││ **Status:* स्थानीय LLM एकीकरण।  
│└ **इंटेलिजेंट पोस्ट-Correction** (`FuzzyMap`)**- पोस्ट-LT रिफाइनमेंट****  
││ * LT-विशिष्ट आउटपुट को सही करने के लिए LanguageTool के बाद लागू। एक ही सख्त cascading प्राथमिकता तर्क के रूप में पूर्व सुधार परत.  
││ **************************************************************************************************************************************************************************************************************************************************************** नियम कस्टम पायथन स्क्रिप्ट (XMDLINK1X) को एपीआई कॉल, फ़ाइल I/O जैसे उन्नत कार्यों को करने या गतिशील प्रतिक्रियाओं को उत्पन्न करने के लिए ट्रिगर कर सकते हैं।   
││ **Fuzzy Fallback:* ** Fuzzy समानता चेक** (controlled by a threshold, e.g., 85%) सबसे कम प्राथमिकता त्रुटि सुधार परत के रूप में कार्य करता है। यह केवल तभी निष्पादित किया जाता है जब पूरे पूर्ववर्ती नियतात्मक/cascading नियम रन एक मैच (current_rule_matched is False) खोजने में विफल रहा, जब भी संभव हो तो धीमी गति से फजी चेक से बचने के द्वारा प्रदर्शन का अनुकूलन किया गया।   
├┬ ** मॉडल प्रबंधन/*   
│├─ `prioritize_model.py` (Optimizes model loading/unloading based on usage) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (Configures the first-time model setup) 🐧 🍏 🪟  
├─ **Adaptive VAD Timeout**  
├─ **Adaptive Hotkey (Start/Stop)***  
├─ **इंस्टेंट भाषा स्विचिंग** (Experimental via model preloading)
├─ **एयरफ्लो ऑर्केस्ट्रेशन** (DAG-based workflow automation)  
│   की आवश्यकता है Docker · यूआई: `http://localhost:8081`
├─ **Trino State Engine** (Interface-aware config per speech/terminal/web)  
└─  की आवश्यकता है Docker · व्यवस्थापक यूआई: `http://localhost:8084`
  
** सिस्टम उपयोगिताएँ/*   
├┬ **LanguageTool सर्वर प्रबंधन /*   
│├─ `start_languagetool_server.py` (Initializes the local LanguageTool server) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py` (Shuts down the LanguageTool server) 🐧 🍏  
├─ `monitor_mic.sh` (e.g. for use with Headset without use keyboard and Monitor) 🐧 🍏 🪟  

## **मॉडल और पैकेज प्रबंधन**  
बड़ी भाषा मॉडलों की मजबूत हैंडलिंग के लिए उपकरण।   

**ModelManagement/***  
├─ **Robust Model Downloader** (GitHub Release chunks)  
├─ `split_and_hash.py` (Utility for repo owners to split large files and generate checksums) 🐧 🍏 🪟  
└─ `download_all_packages.py` (Tool for end-users to download, verify, and reassemble multi-part files) 🐧 🍏 🪟  

</details>


<details>
<summary>विकास और तैनाती सहायक </summary>

## **विकास और तैनाती सहायक***  
पर्यावरण सेटअप, परीक्षण और सेवा निष्पादन के लिए स्क्रिप्ट।   

*टिप: गलॉग आपको अपनी लॉग फ़ाइलों में दिलचस्प घटनाओं की खोज के लिए नियमित अभिव्यक्तियों का उपयोग करने में सक्षम बनाता है।   
लॉग-फ़ाइल्स के साथ जुड़ने के लिए इंस्टॉल करते समय कृपया चेकबॉक्स की जांच करें।   
https://glogg.bonnefon.org/   
    
* टिप: अपने रेगेक्स पैटर्न को परिभाषित करने के बाद, CLI उपकरणों के लिए स्वचालित रूप से खोज योग्य उदाहरण उत्पन्न करने के लिए XINlineCODE0X चलाएं। [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-hilang.md) विवरण के लिए देखें।*

फिर शायद डबल क्लिक करें
`log/aura_engine.log`
    
**DevHelpers /*  
├┬ ** पर्यावरण प्रबंधन  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ ** सिस्टम-वाइड डिक्टेशन इंटीग्रेशन/*   
│├ Vosk-System-Listener इंटीग्रेशन 🔥  
│├ `scripts/monitor_mic.sh` (Linux-specific microphone monitoring) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey listens for recognized text and types it out system-wide) 🪟  
└─ **CI/CD स्वचालन/*  
    └─ विस्तारित गिटहब वर्कफ़्लोज़ (Installation, testing, docs deployment)  

</details>

<details>
<summary> एक्सपेरिमेंटल फीचर्स</summary>
  
    
## **Upcoming / Experimental Features**  
वर्तमान में विकास या मसौदा स्थिति में सुविधाएँ   

** एक्सपेरिमेंटल फीचर्स /*   
├─ **ENTER AFTER DICTATION REGEX ** उदाहरण सक्रियण नियम "(ExampleAplicationThatNotExist|Pi, your personal AI)"  
├┬प्लगइन्स   
│Englishالعربية中文(简体)हिन्दी; हिंदीاردو  
(*Changes to Plugin activation/deactivation, and their configurations, are applied on the next processing run without service restart.*)  
│ ├ ** (Voice control for send git commands).  
│ ├ **wannweil** (Map for Location Germany-Wannweil)  
│ ├ ** पोकर प्लगइन (Draft)** (Voice control for poker applications)  
│ └ **0 एडी प्लगइन (Draft)**(Voice control for 0 A.D. game)  
├─ ** ध्वनि आउटपुट जब सत्र * (Description pending) शुरू या समाप्त होता है  
├─ ** विजुअल इम्पीयर्ड** (Description pending) के लिए स्पीच आउटपुट  
└─ **SL5 Aura Android प्रोटोटाइप* (Not fully offline yet)  

---

* (Note: Specific Linux distributions like Arch (ARL) या उबंटू (UBT) सामान्य लिनक्स 🔥 प्रतीक से ढके हुए हैं। विस्तृत भेदों को स्थापना मार्गदर्शिका में शामिल किया जा सकता है।
</details>

<details>
<summary>इस स्क्रिप्ट सूची को उत्पन्न करने के लिए इस्तेमाल किए गए आदेश को देखने के लिए क्लिक करें</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>A वास्तुकला का चित्रमय अवलोकन </summary>

### वास्तुकला का एक चित्रमय अवलोकन:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>Used Models</summary>

## प्रयुक्त मॉडल:

सिफारिश: मिरर से मॉडल का उपयोग https://github.com/sl5net/SL5-aura-service/release/tag/v0.2.0.1 (probably faster)

इन ज़िपित मॉडल को `models/` फ़ोल्डर में बचाया जाना चाहिए

`mv vosk-model-*.zip models/`


The number of the number of the number of the number of the number of the number.
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
[vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) ([vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip))
Apache 2.0 (mls)<br/>33.26 (mtedx)

यह तालिका विभिन्न वोस्क मॉडलों का अवलोकन प्रदान करती है, जिसमें उनके आकार, शब्द त्रुटि दर या गति, नोट्स और लाइसेंस की जानकारी शामिल है।


**वोस्क मॉडल:* [Vosk-Model List](https://alphacephei.com/vosk/models)
**LanguageTool:*  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

** LanguageTool की लाइसेंस:* [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

## समर्थन परियोजना
यदि आप इस उपकरण को उपयोगी पाते हैं तो कृपया हमें कॉफी खरीदने पर विचार करें! आपका समर्थन भविष्य में सुधार को बढ़ावा देने में मदद करता है।

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

