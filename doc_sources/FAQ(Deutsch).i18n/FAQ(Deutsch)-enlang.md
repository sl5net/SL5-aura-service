> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../FAQ(Deutsch).md).*

### FAQ (German) 3.8.'2025 Sun

**1.Q: What is SL5 aura? ***
A: It is a system-wide offline speech recognition program. You can use it to dictate to any application on your computer (Windows, macOS, Linux) without needing an Internet connection.

Q: Is offline speech recognition Alexa/Siri and the like?
A: Good question. No, it's the exact opposite. Alexa/Siri are cloud-based. The voice data is sent to their server for processing. offline: everything happens safely on the user’s device. This is the decisive advantage for data protection.

Q: Why should I use this? What is special? * *
A: **Privacy.** Your voice data is processed 100% on your local computer and never sent to the cloud. This makes it absolutely private and GDPR compliant.

Q: Is it free? ***
A: Yes, the Community Edition is completely free and open source. The code and the installer can be found on our GitHub: [https://github.com/sl5net/Vosk-System-Listener](https://github.com/sl5net/Vosk-System-Listener)

Q: What do I need to use it? ***
A: A computer and a microphone. For the best accuracy, we strongly recommend a good headset mic instead of the built-in laptop mic.

**5.Q: The accuracy is not perfect. How can I improve them? * *
A: Try to speak clearly, at even volume and speed. Reducing background noise and a better microphone make the biggest difference.

--------------------- Here we could mention that we have various FuzzyMaps with which you can greatly improve the accuracy or even design your own languages






#### **Part 1: General questions * *

**F: What is SL5 Auro? ***
A: SL5 Auro is a system-wide offline speech recognition program. It allows you to dictate text to any application on your computer (e.g., email program, word processor, code editor) without needing an Internet connection.

**F: What does "offline" mean and why is it important? * *
A: "Offline" means that all language processing takes place directly on your computer. Your voice data is **never** sent to a cloud server (such as Google, Amazon or OpenAI). This provides maximum privacy and security, ideal for sensitive information (e.g. for lawyers, doctors, journalists) and is fully compliant with data protection regulations such as GDPR.

**F: Is it really free? Where's the catch? * *
A: The Community Edition is 100% free and open source. There is no catch. We believe in the power of open source tools. If you find the software useful and would like to support its further development, you can do so via our [Ko-fi Seite](https://ko-fi.com/sl5).

**F: Who is this software intended for? * *
A: For anyone who writes a lot and wants to increase their efficiency: authors, students, programmers, lawyers and medical professionals, people with physical limitations or anyone who simply prefers to speak than type.

#### **Part 2: Installation & Furnishing * *

**F: Which operating systems are supported? * *
A: The software has been successfully tested on Windows 11, Manjaro Linux and Ubuntu and macOS.

**F: How do I install it on Windows? ***
A: We offer a simple one-click installer. It is a batch script that requires administrator rights to set up the environment and download the necessary models. Once executed, it does everything for you.

**F: The download for the models is very large. Why?**
A: The voice recognition models allow the software to work offline. They contain all the data that AI needs to understand your language. Larger, more precise models can be several gigabytes in size. Our new downloader divides these into smaller, verifiable parts to ensure a reliable download.

**F: I am on Linux. How do I proceed? * *
A: On Linux, you typically clone GitHub’s repository and run a setup script as though. This script creates a virtual Python environment, installs dependencies, and launches the dictation service.

**F: When I double-click a `.py` file on Windows, it opens in the text editor. How do I execute them?* *
A: This is a common Windows problem where `.py` files are not associated with the Python interpreter. You should not run the individual Python scripts directly. Always use the main boot script provided (e.g. a `.bat` file) as this ensures that the correct environment is activated first.

#### **Part 3: Use and Functions * *

**F: How do I use it to dictate? * *
A: First, start the dictation service by executing the appropriate script. He then walks in the background. After that, use a trigger (such as a hotkey or special script) to start and stop recording. The recognized text is then automatically written into the currently active window.

**F: How can I improve accuracy? * *
A: 1. **Use a good microphone:** A headset microphone is far better than the built-in microphone of a laptop. **Minimize background noise:** A quiet environment is crucial. **Speak clearly:** Speak at a steady pace and with constant volume. Avoid mugging or rushing.
Software customization (the strength of the software): For even higher accuracy, SL5 Auro offers a very powerful feature: FuzzyMaps. Think of it as your personal, intelligent dictionary. You can create simple text files with rules to fix typical, recurring detection errors.

Example: If the software stubbornly understands "get hap" instead of "GitHub", you can create a rule in a FuzzyMap that automatically corrects this.

Advantage: In this way you can teach the software your special jargon, product name, abbreviations or even your own "languages". By adjusting these maps, you can significantly increase the accuracy for your personal use case.

Q: Can I change languages? ***
A: Yes. The system supports hot reloading of configuration files during operation. You can change the language model in configuration, and the service switches to the new language immediately and without restarting.

**F: What is "LanguageTool"? * *
A: LanguageTool is an open source exam for grammar and style that we have integrated. After your language is converted to text, LanguageTool automatically corrects common transcription errors (such as "be" vs. "since") and punctuation, which greatly improves the final output.

#### **Part 4: Troubleshooting & Support * *

**F: I started the service, but nothing happens if I want to dictate. ***
A: Please check the following:
1. Is the service still running in your terminal/console? Look for error messages.
2. Is your microphone correctly selected as the default input device in your operating system?
3. Is the microphone muted or the volume set too low?

**F: I found an error or an idea for a new function. What should I do?**
A: That's great! The best place to report errors or suggest functions is to create an “issue” in our [GitHub Repository](https://github.com/sl5net/Vosk-System-Listener).





Absolutely right, this is a crucial point and one of our strengths. I revised the answer to highlight the FuzzyMaps.

***

### Revised FAQ Answer

#### **English:**

**5.Q: The accuracy is not perfect. How can I improve them? * *
A: Accuracy depends on both your equipment and software customization.

*   **Your equipment (The Basics):** Try to speak clearly, at even volume and speed. Reducing background noise and using a good headset mic instead of the built-in laptop mic makes the biggest difference.

*   **Software customization (the strength of the software):** For even greater accuracy, SL5 Auro offers a very powerful feature: **FuzzyMaps**. Think of it as your personal, intelligent dictionary. You can create simple text files with rules to fix typical, recurring detection errors.

    *   **Example:** If the software stubbornly understands "get hap" instead of "GitHub", you can create a rule in a FuzzyMap that automatically corrects this.
    *   **Advantage:** This way you can teach the software your special jargon, product name, abbreviations or even your own "languages". By adjusting these maps, you can significantly increase the accuracy for your personal use case.

    
# Live hot reload for configurations

SL5 Aura offers a powerful live hot reload capability for configuration changes, such as activating or deactivating Git commands. This means that you can make adjustments without having to restart the SL5 Aura service – a huge benefit for productivity!

How it works:
To ensure optimal performance, configuration changes are only checked and applied when a new processing run is started. This means:

1 Save change: You change a setting (e.g. activate Git commands).
2 Activation: The change becomes active the next time SL5 Aura processes an action (for example, you enter a command). The cache is then updated.

Important note: Your changes are "marked" immediately after saving, but only become active with the next interaction. No restart of the service is required.
