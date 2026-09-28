> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

SL5 Aura - आपकी आवाज। आपका नियम

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 100% ऑफ़लाइन, गोपनीयता-पहले वॉयस असिस्टेंट फ्रेमवर्क।  
> वास्तव में क्या आपकी आवाज़ करता है - एक ही शब्द से  
> पूर्ण पायथन स्क्रिप्ट के लिए। कोई बादल नहीं। कोई डेटा आपकी मशीन को छोड़ देता है।  
> टर्मिनल, ब्राउज़र में या एक पृष्ठभूमि सेवा के रूप में - लिनक्स, मैकओएस और विंडोज पर।

The first day of the day.
|---|---|---|
Aura is the rest of a time.
The State Management of Trino + Airflow orchestration, fzf, CopyQ, आवाज/terminal commands, ब्राउज़र UIs

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

A ** 2.87 J** प्रति परीक्षण ( LanguageTool के बिना 3 9 परीक्षण पूरे >800 मानचित्र @ 0.07s गर्म / 0.36s ठंड utter [Eco-CI](https://metrics.green-coding.io/index.html) के साथ मापा) · कोई बादल compute नहीं

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

A ** पूर्ण परीक्षण सूट:* 94 test with languageTool on>800 maps @ 0.07s warm / 0.46s ठंड · कोई बादल compute

<details>
<summary>क्विक स्टार्ट</summary>

## त्वरित शुरूआत

### विकल्प A: 1-क्लिक और वेब इंस्टॉलर (अनुशंसित)

Linux, macOS और Windows के लिए वन-लाइनर कमांड या स्टैंडअलोन इंस्टॉलर:
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-hilang.md)**

---

## Option B: मैनुअल इंस्टालेशन (डेवलपर्स / गिट)

1. इस भंडार को डाउनलोड या क्लोन करें
2. अपने ओएस के लिए सेटअप स्क्रिप्ट चलाएँ (`setup/` फ़ोल्डर देखें):
   - लिनक्स (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
   - लिनक्स (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
   - लिनक्स (openSUSE): `bash setup/suse_setup.sh`
   - लिनक्स (NixOS): `nix-shell setup/shell.nix` तो `bash setup/nixos_setup.sh`
   ==> 👉️ प्रायोगिक - लेखकों द्वारा अप्रमाणित, फीडबैक स्वागत!   
   - MacOS: `bash setup/macos_setup.sh`
   - विंडोज: `setup/windows11_setup_with_ahk_copyq.bat`
3. Aura: `./scripts/restart_venv_and_run-server.sh`
4. अपनी हॉटकी दबाएं और बोलें - ** [full guide →](../docs/GettingStarted.i18n/GettingStarted-hilang.md) * *

---

## अनइंस्टॉलेशन
SL5 Aura पृष्ठभूमि सेवाओं, ऑटोस्टार्ट प्रविष्टियों और आभासी वातावरण को हटाने के लिए:
- ** लिनक्स / मैक ओएस: ** `bash setup/uninstall.sh`
- ** Windows (PowerShell):* `powershell -File setup/uninstall.ps1`
`config/maps/` में आपका कस्टम नियम डिफ़ॉल्ट रूप से सुरक्षित रखा जाता है जब तक कि आप `--purge` निर्दिष्ट नहीं करते हैं। *

---


सिस्टम आवश्यकताएं और संगतता * *

*   ** विंडोज: ** पूरी तरह से समर्थित (AutoHotkey / PowerShell का उपयोग करता है)।
*   ** MacOS: ** पूरी तरह से समर्थित (AppleScript का उपयोग करता है)।
*   ** लिनक्स (X11/Xorg):* पूरी तरह से समर्थित।
*   ** लिनक्स (वेलैंड): ** पूरी तरह से समर्थित (KDE प्लाज्मा 6 / वेलैंड पर परीक्षण किया गया)।
*   ** लिनक्स (CachyOS / आर्क आधारित रोलिंग रिलीज):** पूरी तरह से समर्थित।
    Glibc 2.43 संगतता के कारण mimalloc (XINlineCODE4X) की आवश्यकता है।
*   **Linux (NixOS):**, Experimental — सामुदायिक योगदान सेटअप, अभी तक परीक्षण नहीं किया गया।
    यदि आप इसे आज़माते हैं, तो कृपया अपने निष्कर्षों के साथ एक मुद्दा या PR खोलें!    
*   ** लिनक्स (Manjaro):* नई: एक सिस्टम-वाइड हॉटकी एक fzf-like, कीबोर्ड-संचालित इंटरफ़ेस को खोलती है ताकि आप डेस्कटॉप पर कहीं से भी Aura कमांड चला सकें (पूर्ण रूप से सक्रिय विंडो से अलग)। यह हॉटकी-चालित लॉन्चर वर्तमान में लिनक्स (मंजरो) पर लागू और परीक्षण किया गया है; अन्य वितरण काम कर सकते हैं लेकिन सेटअप की आवश्यकता हो सकती है। [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-hilang.md) में देखें    


    
SL5 Aura एक पूर्ण, ** ऑफलाइन वॉयस असिस्टेंट** है जिसका निर्माण **वोस्क* (भाषा से पाठ के लिए) और **भाषाटूल** (ग्राममार / शैली के लिए) पर किया गया है, जिसमें रचनात्मक प्रतिक्रियाओं और उन्नत फजी मिलान के लिए एक वैकल्पिक ** लोकल एलएलएम (Ollama) Fallback*** शामिल है। यह आपकी आवाज को सटीक कार्यों और पाठ में बदल देता है, जो प्लग करने योग्य नियम प्रणाली और एक गतिशील स्क्रिप्टिंग इंजन के माध्यम से परम अनुकूलन के लिए डिज़ाइन किया गया है।
    
अनुवाद: यह दस्तावेज़ [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n) में भी मौजूद है।


नोट: कई ग्रंथ मूल अंग्रेजी दस्तावेज़ीकरण के मशीनीकृत अनुवाद हैं और केवल सामान्य मार्गदर्शन के लिए इरादा हैं। विवेक या अस्पष्टता के मामले में, अंग्रेजी संस्करण हमेशा प्रबल होता है। हम इस अनुवाद को बेहतर बनाने के लिए समुदाय से मदद का स्वागत करते हैं!

</details>

<details>
<summary>डेमो</summary>

### 📺 टर्मिनल डेमो

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **संकेत:** बेहतर टर्मिनल अनुभव के लिए, [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-hilang.md) देखें।

### 🎥 वीडियो ट्यूटोरियल
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(वैकल्पिक लिंक: [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw))*

</details>

<details>
<summary>मुख्य विशेषताएँ</summary>

##

*   ** ऑफलाइन और प्राइवेट:* 100% स्थानीय। कोई डेटा कभी भी आपकी मशीन को छोड़ देता है।
*   ** डायनेमिक स्क्रिप्टिंग इंजन:* पाठ प्रतिस्थापन से परे जाओ। नियम कस्टम पाइथन स्क्रिप्ट्स (XINlineCODE0X) को निष्पादित कर सकते हैं जैसे एपीआई (जैसे, खोज विकिपीडिया), फाइलों के साथ बातचीत करना (जैसे, to do सूची प्रबंधित करना), या गतिशील सामग्री उत्पन्न करना (जैसे, एक संदर्भ-जारी ईमेल ग्रीटिंग)।
*   **Context-Aware Rules:* विशिष्ट अनुप्रयोगों के लिए प्रतिबंधित नियम। `only_in_windows` का उपयोग करके, आप एक नियम केवल तभी ट्रिगर कर सकते हैं जब एक विशिष्ट विंडो शीर्षक (जैसे, "टर्मिनल", "वीएस कोड" या "ब्रोशर") सक्रिय है। यह क्रॉस-प्लेटफॉर्म (लिनक्स, विंडोज, मैकओएस) का काम करता है।
*  ** उच्च नियंत्रण परिवर्तन इंजन:* एक विन्यास संचालित, अत्यधिक अनुकूलन प्रसंस्करण पाइपलाइन को लागू करता है। नियम प्राथमिकता, आदेश का पता लगाने और पाठ परिवर्तन पूरी तरह से फजी मैप्स में नियमों के अनुक्रमिक आदेश द्वारा निर्धारित किए जाते हैं, जिसके लिए ** विन्यास की आवश्यकता होती है, कोडिंग नहीं**।
*   ** कंज़र्वेटिव रैम उपयोग:* बुद्धिमानी से स्मृति, प्रीलोडिंग मॉडल का प्रबंधन करता है, अगर पर्याप्त मुफ्त रैम उपलब्ध है, तो अन्य अनुप्रयोगों को सुनिश्चित करना (जैसे कि आपका पीसी गेम) हमेशा प्राथमिकता है।
*   ** क्रॉस प्लेटफार्म:* लिनक्स, मैकओएस और विंडोज पर काम करता है।
*   ** पूरी तरह से स्वचालित:* अपने खुद के LanguageTool सर्वर को प्रबंधित करता है (लेकिन आप बाहरी एक का भी उपयोग कर सकते हैं)।
*   ** ब्लेज़िंग फास्ट: ** इंटेलिजेंट कैशिंग तत्काल "लिस्टिंग" अधिसूचनाओं और तेज प्रसंस्करण सुनिश्चित करता है।
*   ** त्रिनो के माध्यम से डायनेमिक स्टेट मैनेजमेंट:* इंटरफ़ेस-aware विन्यास इंजन
    XINlineCODE2X, `terminal` और `web` के लिए सेटिंग्स को अलग करता है - बिना किसी बदलाव के
    दूसरों को प्रभावित करना। एक वास्तविक समय ** एडमिन डैशबोर्ड ** (पोर्ट 8084) शामिल है।
</details>

<details>
<summary>रेडी-टू-यूज़ एकीकरण</summary>
    
## 🔌 तैयार-से-उपयोग इंटीग्रेशन

SL5-Aura एक विशाल इकोसिस्टम के साथ आता है जिसमें **100+ प्री-कॉन्फ़िगर किए गए प्लगइन्स** शामिल हैं। यहाँ कुछ मुख्य बातें हैं:

Oculix / Sikulix IDE वॉयस कंट्रोल
SL5-Aura ** Oculix** और **SikuliX IDE* के लिए प्रथम श्रेणी की आवाज समर्थन प्रदान करता है। यह एकीकरण आपको अपने स्वचालन कोड को "स्पाक" करने की अनुमति देता है।

*   **वोइस-टू-स्निपेट:* "क्लिक करें", "वैइट", या "सभी को खत्म करें", और सेवा तुरंत आईडीई में सही पायथन कोड (जैसे XINlineCODE0X) टाइप करती है।
*   **विंडो-Aware:* प्लगइन संदर्भ-संवेदनशील है; यह केवल तभी सक्रिय होता है जब OculiX/SikuliX विंडो केंद्रित होती है।
*   ** स्मार्ट अंग्रेजी समर्थन: ** `en-US` के लिए ऑप्टिमाइज़ किया गया, जिसमें गैर-मूल उच्चारण (जैसे, जर्मन-अंग्रेजी फोनेटिक्स) पर विशेष ध्यान दिया गया है, जो वैश्विक समुदाय के लिए उच्च मान्यता सटीकता सुनिश्चित करता है।
*   **Extensible:* आसानी से संपादित `FUZZY_MAP_pre.py` प्रारूप का उपयोग करता है।

> ** Oculix टीम ([Issue #204](https://github.com/oculix-org/Oculix/issues/204) देखें).

### LibreOffice IDE वॉइस कंट्रोल

### 0 ई.स. ध्वनि नियंत्रण

---

</details>


<details>
<summary>प्रलेखन</summary>

## प्रलेखन

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)

एक पूर्ण तकनीकी संदर्भ के लिए, जिसमें सभी मॉड्यूल और स्क्रिप्ट शामिल हैं, कृपया हमारे आधिकारिक दस्तावेज़ पृष्ठ पर जाएँ। यह स्वचालित रूप से उत्पन्न होता है और हमेशा अद्यतन रहता है।

👉 [**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)

### फीचर स्पॉटलाइट्स
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-hilang.md) — डुअल-पैन `fzf` नियम खोज, लाइव संदर्भ पूर्वदर्शनी, `Enter`/`Ctrl+R` के माध्यम से तात्कालिक कमांड निष्पादन, और `Ctrl+E` के माध्यम से संपादक एकीकरण। एक वैश्विक हॉटकी (`Super+S`) और कई समर्पित खोज-पर्यावरणों द्वारा समर्थित, जिन्हें वॉइस कमांड्स के माध्यम से पूर्व-निर्धारित किया गया है।

### निर्माण स्थिति

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

👉 **इसे अन्य भाषाओं में पढ़ें:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-hilang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-hilang.md) | [🇪🇸 Español](../README.i18n/README-eslang-hilang.md) | [🇫🇷 Français](../README.i18n/README-frlang-hilang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-hilang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-hilang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-hilang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-hilang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-hilang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-hilang.md)

---

<details>
<summary>स्थापना</summary>

## स्थापना

###                                                                                                                              
पूर्ण 6 मिनट की सेटअप प्रक्रिया देखें:
* डाउनलोड: ~3 मिनट
* ** सेटअप एंड फर्स्ट स्टार्ट:* ~ 3 मिनट ( Welcome Wizard सहित)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


सेटअप एक दो-चरण प्रक्रिया है:
1.  नवीनतम रिलीज या मास्टर डाउनलोड करें ( https://github.com/sl5net/SL5-aura-service/archive/master.zip) या अपने कंप्यूटर के लिए इस भंडार को क्लोन करें।
2.  अपने ऑपरेटिंग सिस्टम के लिए एक बार सेटअप स्क्रिप्ट चलाएं।

सेटअप स्क्रिप्ट सब कुछ संभालती हैं: सिस्टम निर्भरताएं, पायथन पर्यावरण, और अधिकतम गति के लिए हमारे गिटहब रिलीज से सीधे आवश्यक मॉडल और उपकरण (~ 4GB) डाउनलोड करना।


लिनक्स, मैकओएस और विंडोज के लिए (वैकल्पिक भाषा अपवाद के साथ)

डिस्क स्पेस और बैंडविड्थ को बचाने के लिए, आप सेटअप के दौरान विशिष्ट भाषा मॉडल (XINlineCODE0X, `en`) या सभी वैकल्पिक मॉडल (XINlineCODE2X) को बाहर कर सकते हैं। ** कोर घटक (LanguageTool, lid.176) हमेशा शामिल हैं। ************

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
   * * स्क्रिप्ट स्वचालित रूप से प्रशासक विशेषाधिकारों के लिए संकेत देगा। *
   * * यह कोर सिस्टम, भाषा मॉडल, **AutoHotkey v2*, और **CopyQ** स्थापित करता है। *
3. एक बार जब स्थापना पूरी हो जाती है, तो **Aura Dictation** स्वचालित रूप से शुरू हो जाएगा।

> ** आपको पहले पायथन या गिट स्थापित करने की आवश्यकता नहीं है; स्क्रिप्ट सब कुछ संभालती है।

---

### उन्नत / कस्टम स्थापना
यदि आप क्लाइंट टूल (AHK/CopyQ) को स्थापित नहीं करना चाहते हैं या विशिष्ट भाषाओं को छोड़कर डिस्क स्पेस को सहेजना चाहते हैं, तो आप कमांड लाइन के माध्यम से मुख्य स्क्रिप्ट चला सकते हैं:

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
<summary>प्रयोग</summary>

# उपयोग

##

लिनक्स और मैक ओएस पर
एक एकल स्क्रिप्ट सब कुछ संभालती है। यह मुख्य तानाशाही सेवा शुरू करता है और फ़ाइल दर्शक स्वचालित रूप से पृष्ठभूमि में।
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

###
सेवा शुरू करना एक ** दो चरण मैनुअल प्रक्रिया है ***:

1.  ** मुख्य सेवा शुरू करें:* रन `start_aura.bat`. या `.venv` से `python3` के साथ सेवा शुरू करें

अपनी हॉटकी को कॉन्फ़िगर करें

डिक्टेशन को ट्रिगर करने के लिए, आपको एक वैश्विक हॉटकी की आवश्यकता है जो एक विशिष्ट फ़ाइल बनाता है। हम अत्यधिक क्रॉस-प्लेटफॉर्म टूल [CopyQ](https://github.com/hluk/CopyQ) की सिफारिश करते हैं।

#### हमारी सिफारिश: CopyQ

CopyQ में एक नया कमांड एक ग्लोबल शॉर्टकट के साथ बनाएं।

**Linux/macOS के लिए कमांड:**
```bash
touch /tmp/sl5_record.trigger
```

**Windows के लिए कमांड जब [CopyQ](https://github.com/hluk/CopyQ) का उपयोग करें:**
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


**[AutoHotkey](https://AutoHotkey.com) का उपयोग करते समय Windows के लिए कमांड:**
```sh
; trigger-hotkeys.ahk
; AutoHotkey v2 script
#SingleInstance Force ; Ensures only one instance of the script runs

;===================================================================
; Hotkey to trigger Aura
; Press Ctrl + Alt + T to write the trigger file.
;===================================================================
f9::
f10::
f11::
{
    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("Aura Trigger activated!")
    SetTimer(() => ToolTip(), -1500)
}
```


### 3rd start Dictating!
किसी भी टेक्स्ट फ़ील्ड में क्लिक करें, अपनी हॉटकी दबाएं, और एक "लिस्टिंग" अधिसूचना दिखाई देगी। स्पष्ट रूप से बोलो, फिर रोकें। सही पाठ आपके लिए टाइप किया जाएगा।

</details>

---


<details>
<summary>उन्नत विन्यास (वैकल्पिक)</summary>

## उन्नत विन्यास (वैकल्पिक)

आप एक स्थानीय सेटिंग फ़ाइल बनाकर एप्लिकेशन के व्यवहार को अनुकूलित कर सकते हैं।

1.  `config/` निर्देशिका में नेविगेट करें।
2.  `config/settings_local.py_Example.txt` की एक प्रति बनाएं और इसे `config/settings_local.py` में बदलें।
3.  `config/settings_local.py` संपादित करें (यह मुख्य `config/settings.py` फ़ाइल से किसी भी सेटिंग को ओवरराइड करता है)।

इस XINlineCODE5X फ़ाइल को डिफ़ॉल्ट रूप से गिट द्वारा नजरअंदाज कर दिया गया है, इसलिए आपके व्यक्तिगत परिवर्तन अद्यतनों से अधिक नहीं होंगे।

प्लग-इन संरचना और तर्क

सिस्टम की मॉड्यूलरिटी प्लगइन्स / डायरेक्टरी के माध्यम से मजबूत विस्तार की अनुमति देती है।

प्रसंस्करण इंजन सख्ती से एक ** ऐतिहासिक प्राथमिकता श्रृंखला का पालन करता है ***:

1. ** मॉड्यूल लोडिंग ऑर्डर (उच्च प्राथमिकता):** कोर भाषा पैक (de-DE, en-US) से लोड किए गए नियम प्लगइन्स/डायरेक्टरी (जो अंतिम वर्णमाला को लोड करते हैं) से लोड किए गए नियमों पर प्राथमिकता लेते हैं।
    
2. **इन-फ़ाइल ऑर्डर (माइक्रो प्रायोरिटी):* किसी भी दिए गए मानचित्र फ़ाइल (FUZZY MAP pre.py) के भीतर, नियमों को सख्ती से **लाइन नंबर* (शीर्ष से नीचे) द्वारा संसाधित किया जाता है।
    

यह वास्तुकला यह सुनिश्चित करती है कि कोर सिस्टम नियम सुरक्षित हैं, जबकि परियोजना-विशिष्ट या संदर्भ-अवकाश नियम (जैसे कोडइग्नेटर या गेम कंट्रोल के लिए) को आसानी से प्लग-इन के माध्यम से कम प्राथमिकता एक्सटेंशन के रूप में जोड़ा जा सकता है।

</details>

<details>
<summary>विंडोज उपयोगकर्ताओं के लिए कुंजी स्क्रिप्ट</summary>






विंडोज उपयोगकर्ताओं के लिए कुंजी स्क्रिप्ट

यहां विंडोज सिस्टम पर एप्लिकेशन को सेट करने, अद्यतन करने और चलाने के लिए सबसे महत्वपूर्ण स्क्रिप्ट की सूची दी गई है।

### सेटअप और अद्यतन

*   `chmod +x update.sh; ./update.sh`
*   XINlineCODE1X: पर्यावरण के ** प्रारंभिक एक बार सेटअप * के लिए मुख्य स्क्रिप्ट।
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : इसे परियोजना फ़ोल्डर से ** नवीनतम कोड और निर्भरता ** प्राप्त करें।

##########                                      
*   `start_aura.bat`: एक प्राथमिक स्क्रिप्ट ** dictation सेवा ** शुरू करने के लिए।

### कोर & हेल्पर स्क्रिप्ट
*   XINlineCODE0X: कोर पायथन सेवा (आमतौर पर उपरोक्त लिपियों में से एक द्वारा शुरू)।
*   `get_suggestions.py`: विशिष्ट कार्यात्मकताओं के लिए एक सहायक स्क्रिप्ट।

</details>



## 🚀 प्रमुख विशेषताएँ और OS संगतता

<details>
<summary>OS संगतता के लिए लीजेंड</summary>

ओएस संगतता के लिए संकेतक:  
*   🐧 **लिनक्स** (जैसे, आर्च, उबंटू)  
    *   🍏 **मैकओएस**  
*   🪟 **विंडोज़**  
*   📱 **एंड्रॉइड** (मोबाइल-विशेष सुविधाओं के लिए)  

---

</details>



## **Core Speech-to-Text (Aura) Engine* *
    ऑफ़लाइन भाषण मान्यता और ऑडियो प्रसंस्करण के लिए हमारा प्राथमिक इंजन।

    
<details>
<summary>Aura कोर</summary>

** Aura-Core/** 🐧 🍏 🪟  
├─ XINlineCODE0X (मुख्य पायथन सेवा orchestrating Aura) 🐧 🍏 🪟  
├┬ ** लाइव हॉट-रीलोड* (Config & Maps) 🐧 🍏 🪟  
│├ ** सुरक्षित निजी मानचित्र लोडिंग (Integrity-First)** 🔒  🐧 🍏 🪟  
││ * ** वर्कफ़्लो:* पासवर्ड संरक्षित ZIP अभिलेखागार लोड करता है।   
│├ **टेक्स्ट प्रोसेसिंग और सुधार/** भाषा द्वारा समूहित (जैसे `de-DE`, `en-US`, ...)   
│├ 1. XINlineCODE3X (Punctuation post-transcription) 🐧 🍏 🪟  
│├ 2. **इंटेलिजेंट प्री-कोरेक्शन* (`FuzzyMap Pre` - [The Primary Command Layer](../docs/CreatingNewPluginModules.i18n/CreatingNewPluginModules-hilang.md)) 🐧 🍏 🪟  
││ * **Dynamic स्क्रिप्ट निष्पादन: नियम एपीआई कॉल, फ़ाइल I/O जैसे उन्नत कार्यों को करने के लिए कस्टम पायथन स्क्रिप्ट (XINlineCODE5X) को ट्रिगर कर सकते हैं, या गतिशील प्रतिक्रिया उत्पन्न कर सकते हैं।  
││ * **Cascading निष्पादन:* नियम क्रमिक रूप से संसाधित होते हैं और उनके प्रभाव ** संचयी* हैं। बाद में नियम पहले नियमों द्वारा संशोधित पाठ पर लागू होते हैं।  
││ * ** उच्चतम प्राथमिकता स्टॉप मानदंड:* यदि कोई नियम ** पूर्ण मैच* (^...$) प्राप्त करता है, तो उस टोकन के लिए पूरी प्रोसेसिंग पाइपलाइन तुरंत बंद हो जाती है। यह तंत्र विश्वसनीय वॉयस कमांड को लागू करने के लिए महत्वपूर्ण है।  
│├ 3. `correct_text_by_languagetool.py` (grammar / शैली सुधार के लिए एकीकृत भाषा टूल) 🐧 🍏 🪟  
│├ ** 4। Ollama AI Fallback * * के साथ Hierarchical RegEx नियम इंजन 🐧 🍏 🪟  
││ * ** निर्धारित नियंत्रण:* सटीक, उच्च प्राथमिकता आदेश और पाठ नियंत्रण के लिए RegEx नियम इंजन का उपयोग करता है।  
│├ * Vector-Search Plugin** (Lazy Load): Ollama/LLM गिरने वाली परत के साथ स्थानीय वेक्टर एम्बेडिंग को जोड़कर Semantic खोज सक्षम करता है। 🐧  
││ * ** Ollama AI (Local LLM) Fallback:* ** रचनात्मक उत्तर, क्यू एंड ए और उन्नत फ़ज़ी मैचिंग ** के लिए वैकल्पिक, कम प्राथमिकता जांच के रूप में सेवा करता है जब कोई निश्चित नियम पूरा नहीं होता है।  
││ * **Status:* स्थानीय LLM एकीकरण।
│└ 5. **इंटेलिजेंट पोस्ट-Correction** (`FuzzyMap`)**- पोस्ट-LT रिफाइनमेंट* ** 🐧 🍏 🪟  
││ * LT-विशिष्ट आउटपुट को सही करने के लिए भाषा टूल के बाद लागू किया गया। पूर्व सुधार परत के रूप में एक ही सख्त कैस्केड प्राथमिकता तर्क का पालन करता है।  
││ * * डायनेमिक स्क्रिप्ट निष्पादन: नियम एपीआई कॉल, फ़ाइल I/O जैसे उन्नत कार्यों को करने के लिए कस्टम पाइथन स्क्रिप्ट ([on_match_exec](../docs/advanced-scripting.i18n/advanced-scripting-hilang.md)) को ट्रिगर कर सकते हैं, या गतिशील प्रतिक्रिया उत्पन्न कर सकते हैं।  
││ * **Fuzzy Fallback:* ** Fuzzy समानता चेक* (एक सीमा द्वारा नियंत्रित, उदाहरण के लिए, 85%) न्यूनतम प्राथमिकता त्रुटि सुधार परत के रूप में कार्य करता है। यह केवल तभी निष्पादित किया जाता है जब पूरे पूर्ववर्ती नियतात्मक/cascading नियम रन एक मैच खोजने में विफल हो गया (वर्तमान नियम मिलान गलत है), जब भी संभव हो तो धीमी फजी चेक से बचने के द्वारा प्रदर्शन को अनुकूलित करना।  
├┬ ** मॉडल प्रबंधन   
│├─ `prioritize_model.py` (उपयोग के आधार पर मॉडल लोडिंग / अनलोडिंग को अनुकूलित करता है) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (पहली बार मॉडल सेटअप को कॉन्फ़िगर करता है) 🐧 🍏 🪟  
├─ ** एडप्टिव VAD टाइमआउट 🐧 🍏 🪟  
├─ **Adaptive Hotkey (Start/Stop)*** 🐧 🍏 🪟  
├─ ** तत्काल भाषा स्विचिंग ** (मॉडल प्रीलोडिंग के माध्यम से प्रायोगिक) 🐧 🍏         
├─ ** एयरफ्लो ऑर्केस्ट्रेशन ** (डीएजी आधारित वर्कफ़्लो स्वचालन) 🐧 🍏 🪟
│   की आवश्यकता है Docker · UI: `http://localhost:8081` 🐧 🍏 🪟  
├─ **Trino स्टेट इंजन* (interface-aware config per speech/terminal/web) 🐧 🍏 🪟
└─  की आवश्यकता है Docker · व्यवस्थापक यूआई: `http://localhost:8084` 🐧 🍏 🪟  

** सिस्टम उपयोगिताएँ   
├┬ **LanguageTool सर्वर प्रबंधन /*   
│├─ `start_languagetool_server.py` (स्थानीय भाषा उपकरण सर्वर को सम्मिलित करता है) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py` (लैंग्वेज टूल सर्वर को नीचे छोड़ देता है) 🐧 🍏 
├─ `monitor_mic.sh` (जैसे कीबोर्ड और मॉनिटर का उपयोग किए बिना हेडसेट के साथ उपयोग के लिए) 🐧 🍏 🪟  

### **मॉडल और पैकेज प्रबंधन**  
    बड़े भाषा मॉडल को मजबूत तरीके से संभालने के लिए उपकरण।  

**मॉडलप्रबंधन/** 🐧 🍏 🪟  
├─ **मज़बूत मॉडल डाउनलोडर** (GitHub रिलीज़ चंक्स) 🐧 🍏 🪟  
├─ `split_and_hash.py` (भंडार मालिकों के लिए उपयोगिता ताकि बड़े फ़ाइलों को विभाजित किया जा सके और चेकसम बनाया जा सके) 🐧 🍏 🪟  
└─ `download_all_packages.py` (अंत-उपयोगकर्ताओं के लिए एक उपकरण जो बहु-भाग फ़ाइलों को डाउनलोड, सत्यापित और पुनः संयोजित करने के लिए है) 🐧 🍏 🪟  

</details>


<details>
<summary>विकास और परिनियोजन सहायक</summary>

## **विकास और तैनाती सहायक  
    पर्यावरण सेटअप, परीक्षण और सेवा निष्पादन के लिए स्क्रिप्ट।  

*टिप: गलॉग आपको अपनी लॉग फ़ाइलों में रोचक घटनाओं की खोज के लिए नियमित अभिव्यक्तियों का उपयोग करने में सक्षम बनाता है।     
लॉग फ़ाइलों के साथ जुड़ने के लिए इंस्टॉल करते समय कृपया चेकबॉक्स की जांच करें।    
https://glogg.bonnefon.org/     
    
टिप: अपने रेगेक्स पैटर्न को परिभाषित करने के बाद, CLI उपकरण के लिए स्वचालित रूप से खोज योग्य उदाहरण उत्पन्न करने के लिए `python3 tools/map_tagger.py` चलाएं। [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-hilang.md) विवरण के लिए देखें।

फिर शायद डबल क्लिक करें
`log/aura_engine.log`
    
**DevHelpers  
├┬ ** पर्यावरण प्रबंधन  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ ** सिस्टम-वाइड डिक्टेशन इंटीग्रेशन/* *  
│├ वोस्क सिस्टम श्रोता एकीकरण 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (Linux-विशिष्ट माइक्रोफोन निगरानी) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey मान्यता प्राप्त पाठ के लिए सुनता है और इसे सिस्टम-वाइड प्रकार करता है) 🪟  
└─ **CI/CD स्वचालन  
    └─ विस्तारित गिटहब वर्कफ़्लोज़ (इंस्टॉलेशन, टेस्टिंग, डॉक्स परिनियोजन) UM Gb 🇺 * (GitHub कार्रवाई पर रन)*  

</details>

<details>
<summary>प्रायोगिक विशेषताएं</summary>
    
## ** आगामी / प्रायोगिक विशेषताएं *  
    वर्तमान में विकास या मसौदा स्थिति में विशेषताएं।  

** एक्सपेरिमेंटल विशेषताएं  
├─ **ENTER AFTER DICTATION REGEX** उदाहरण सक्रियण नियम "(ExampleAplicationThatNotExist |Pi, आपकी व्यक्तिगत AI)" 🐧  
├┬प्लगइन  
│**Live Lazy-Reload* (*) 🐧 🍏 🪟  
(*Changes to Plugin सक्रियण/deactivation, और उनके विन्यास, सेवा पुनरारंभ के बिना अगले प्रसंस्करण रन पर लागू होते हैं।*)  
│ ├ ** गिट कमांड* (जिसका नियंत्रण भेजने के लिए गिट कमांड) 🐧 🍏 🪟  
│ ├ **wannweil** (स्थान जर्मनी-Wannweil के लिए मानचित्र) 🐧 🍏 🪟  
│ ├ ** पोकर प्लगइन (Draft)** ( पोकर अनुप्रयोगों के लिए आवाज नियंत्रण) 🐧 🍏 🪟  
│ └ **0 A.D. Plugin (Draft)* (0 A.D. खेल के लिए आवाज नियंत्रण) 🐧   
├─ ** एक सत्र शुरू करने या समाप्त होने पर ध्वनि आउटपुट* (विवरण लंबित) 🐧   
├─ ** विजुअल इम्पीयर्ड* (Description लंबित) के लिए स्पीच आउटपुट 🐧 🍏 🪟  
└─ Aura Android Prototype*: 📱  

---

* (नोट: आर्क (ARL) या उबंटू (UBT) जैसे विशिष्ट लिनक्स वितरण सामान्य लिनक्स 🔥 प्रतीक द्वारा कवर किए गए हैं। विस्तृत भेदों को स्थापना मार्गदर्शिका में शामिल किया जा सकता है।
</details>

<details>
<summary>इस स्क्रिप्ट सूची को उत्पन्न करने के लिए इस्तेमाल किए गए आदेश को देखने के लिए क्लिक करें</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>वास्तुकला का एक चित्रमय अवलोकन</summary>

### वास्तुकला का एक ग्राफिकल अवलोकन:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>उपयोग किए गए मॉडल</summary>

## उपयोग किए गए मॉडल:

सिफारिश: मिरर से मॉडल का उपयोग करें https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (संभवतः तेज़)

इन ज़िप किए गए मॉडलों को `models/` फ़ोल्डर में सहेजा जाना चाहिए

`mv vosk-model-*.zip models/`


The number of the number of the number of the number of the number of the number.
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
Apache 2.0 (Apache 2.0)
Apache 2.0 (Apache 2.0) <br/>12.42 (MLs) <br/>33.26 (Mttedx) <br/>24.00 (podcast) <br/>12.82 (Cv-test) <br/>12.42 (MLs) <br/>33.26 (Mttedx)

यह तालिका विभिन्न Vosk मॉडलों का एक सिंहावलोकन प्रदान करती है, जिसमें उनके आकार, शब्द त्रुटि दर या गति, नोट्स, और लाइसेंस जानकारी शामिल है।


- **वॉस्क-मॉडल्स:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **LanguageTool:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**लाइसेंस ऑफ़ लैंग्वेजटूल:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

## परियोजना का समर्थन करें
यदि आपको यह उपकरण उपयोगी लगे, तो कृपया हमारे लिए एक कॉफी खरीदने पर विचार करें! आपका समर्थन भविष्य में सुधारों को ऊर्जा देने में मदद करता है।

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

