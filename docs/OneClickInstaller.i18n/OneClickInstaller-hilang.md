> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../OneClickInstaller.md).*

# 1-Click Installer (Zero-Setup)

**Aura** प्राप्त करें और एक क्लिक के साथ अपनी मशीन पर चल रहा है। कोई प्रोग्रामिंग ज्ञान, टर्मिनल कमांड या मैनुअल पायथन सेटअप की आवश्यकता नहीं है।

---

## शून्य Prerequisites

आप **नहीं* की जरूरत है:
- पायथन पूर्व स्थापित
- गिट या कोड भंडार
- कमांड लाइन या टर्मिनल अनुभव

---

## त्वरित शुरूआत

## Method 1: Web One-Liner (Fastest & Linux / MacOS के लिए अनुशंसित)
मैन्युअल फ़ाइल हैंडलिंग के ~ 30 सेकंड बचाता है और तुरंत अपने टर्मिनल में शुरू होता है:

** लिनक्स और मैक ओएस: **
### Web One-Liner CodeBerg
```bash
curl -sSL https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | bash
```
या
### Web One-Liner GitHub
```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

** विंडोज (पावरशेल):**
### Web One-Liner CodeBerg

```bash
irm https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | iex
```
या
###                                                                     
```bash
irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

विधि 2: स्टैंडअलोन बाइनरी (विंडोज और डेस्कटॉप क्लिक)

## 2.1 Installer डाउनलोड
[नवीनतम गिटहब रिलीज] से अपने ऑपरेटिंग सिस्टम से मिलान करने वाली एकल इंस्टॉलर फ़ाइल डाउनलोड करें:

- ** Windows:* [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- ** लिनक्स:* [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- ** MacOS:* [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


## 2.2. Installer

Aura-installer-windows.exe.zip to aura-installer-windows.exe

डाउनलोड की गई फ़ाइल को डबल-क्लिक करें। एक सेटअप विंडो दिखाई देगी और स्वचालित रूप से पर्यावरण तैयार करेगी।

## 2.3.
एक बार समाप्त हो जाने के बाद, Aura एक डेस्कटॉप शॉर्टकट बनाता है और तुरंत सुनने लगता है।

---

क्या है?

जब आप इंस्टॉलर चलाते हैं, तो Aura स्वचालित रूप से:
- स्थानीय, निजी भाषण मान्यता इंजन को कॉन्फ़िगर करता है।
- डिफ़ॉल्ट आवाज मॉडल डाउनलोड करें।
- सभी आवश्यक सिस्टम शॉर्टकट और डेस्कटॉप लॉन्चर सेट करें।

---

## स्थापना विवरण & आवश्यकताएँ

- ** स्थापना अवधि:* लगभग 2-3 मिनट
- ** डिस्क स्पेस आवश्यक: ** न्यूनतम ~ 1.5 जीबी (चुने हुए भाषा मॉडल के आधार पर 2.5 जीबी तक)।
- **Installation निर्देशिका:*
  - ** लिनक्स और मैक ओएस: ** `~/opt/sl5-aura-service`
  - ** विंडोज:* `%LOCALAPPDATA%\sl5-aura-service`

---

## अगला कदम

- ** दादी मां:* अपने नियम फ़ाइल में एक एकल शब्द टाइप करें और Aura ऑटो-create नियमों को देखें।
- ** कोन्स के साथ जानें:* [Getting Started](../GettingStarted.i18n/GettingStarted-hilang.md) में चरण-दर-चरण अवधारणाओं का अन्वेषण करें।
