### FAQ (English) 3.8.'2025 Sun

**1. Q: What is SL5 Aura?**
A: It's a system-wide, offline speech-to-text program. It allows you to dictate into any application on your computer (Windows, macOS, Linux) without needing an internet connection.

**2. Q: Why should I use this? What makes it special?**
A: **Privacy.** Your voice data is processed 100% on your local machine and never sent to the cloud. This makes it fully private and GDPR compliant.

**3. Q: Is it free?**
A: Yes, the Community Edition is completely free and open-source. You can find the code and installer on our GitHub: [https://github.com/sl5net/Vosk-System-Listener](https://github.com/sl5net/Vosk-System-Listener)

**4. Q: What do I need to use it?**
A: A computer and a microphone. For best accuracy, we strongly recommend a dedicated headset microphone over a built-in laptop mic.

**5. Q: The accuracy isn't perfect. How can I improve it?**
A: Try to speak clearly at a consistent volume and pace. Reducing background noise and using a better microphone makes the biggest difference.
Software Customization (Advanced Power): For next-level accuracy, SL5 Aura uses a powerful feature called FuzzyMaps. Think of these as your personal, intelligent dictionary. You can create simple text files with rules to fix common, recurring recognition errors.

Example: If the software often hears "get hap" instead of "GitHub", you can add a rule that automatically corrects this every time.

Benefit: This allows you to "teach" the software your specific technical jargon, product names, abbreviations, or even create rule-sets for unique vocabularies. By customizing these maps, you can significantly improve accuracy for your specific use case.

***

#### **Part 1: General Questions**

**Q: What is SL5 Auro?**
A: SL5 Auro is a system-wide, offline speech-to-text program. It allows you to dictate text into any application on your computer (e.g., your email client, a word processor, a code editor) without needing an internet connection.

**Q: What does "offline" mean and why is it important?**
A: "Offline" means all voice processing happens directly on your computer. Your voice data is **never** sent to a cloud server (like Google, Amazon, or OpenAI). This provides maximum privacy and security, making it ideal for confidential information (e.g., for lawyers, doctors, journalists) and fully compliant with data protection regulations like GDPR.

**Q: Is it really free? What's the catch?**
A: The "Community Edition" is 100% free and open-source. There is no catch. We believe in the power of open-source tools. If you find the software valuable and wish to support its continued development, you can do so via our [Ko-fi page](https://ko-fi.com/sl5).

**Q: Who is this software for?**
A: It's for anyone who writes a lot and wants to increase their efficiency: writers, students, programmers, legal and medical professionals, people with physical limitations, or anyone who simply prefers speaking to typing.

#### **Part 2: Installation & Setup**

**Q: What operating systems are supported?**
A: The software is tested and confirmed to work on Windows 11, Manjaro Linux, and Ubuntu and macOS.

**Q: How do I install it on Windows?**
A: We provide a simple one-click installer. It's a .Bat script that requires administrative rights to set up the environment and download the necessary models. Once run, it will handle everything for you.

**Q: The download for the models is very large. Why?**
A: The speech recognition models are what allow the software to work offline. They contain all the necessary data for the AI to understand your language. Larger, more precise models can be several gigabytes in size. Our new downloader splits these into smaller, verifiable chunks to ensure a reliable download.

**Q: I'm on Linux. What's the process?**
A: On Linux, you will typically clone the repository from GitHub and run a setup script. This script creates a Python virtual environment, installs dependencies, and starts the dictation service.

**Q: When I double-click a `.py` file on Windows, it opens in a text editor. How do I run it?**
A: This is a common Windows issue where `.py` files are not associated with the Python interpreter. You should not run the individual Python scripts directly. Always use the main startup script provided (e.g., a `.bat` file), as this ensures the correct environment is activated first.

#### **Part 3: Usage & Features**

**Q: How do I actually use it to dictate?**
A: First, you start the "dictation service" by running the appropriate script. It will run in the background. Then, you use a trigger (like a hotkey or a dedicated script) to start and stop recording. The recognized text will then be automatically typed into whichever window is currently active.

**Q: How do I improve the accuracy?**
A: 1. **Use a good microphone:** A headset microphone is far better than a laptop's built-in mic. 2. **Minimize background noise:** A quiet environment is key. 3. **Speak clearly:** Speak at a consistent pace and volume. Don't mumble or rush.
Software Customization (Advanced Power): For next-level accuracy, SL5 Auro uses a powerful feature called FuzzyMaps. Think of these as your personal, intelligent dictionary. You can create simple text files with rules to fix common, recurring recognition errors.

Example: If the software often hears "get hap" instead of "GitHub", you can add a rule that automatically corrects this every time.

Benefit: This allows you to "teach" the software your specific technical jargon, product names, abbreviations, or even create rule-sets for unique vocabularies. By customizing these maps, you can significantly improve accuracy for your specific use case.

**Q: Can I switch languages?**
A: Yes. The system supports live "hot-reloading" of configuration files. You can change the language model in the config, and the service will switch to it instantly without needing a restart.

**Q: What is "LanguageTool"?**
A: LanguageTool is an open-source grammar and style checker that we've integrated. After your speech is turned into text, LanguageTool automatically corrects common transcription errors (e.g., "right" vs. "write") and fixes punctuation, improving the final output significantly.

#### **Part 4: Troubleshooting & Support**

**Q: I started the service, but nothing happens when I try to dictate.**
A: Check the following:
1.  Is the service still running in your terminal/console? Look for any error messages.
2.  Is your microphone correctly selected as the default input device in your operating system?
3.  Is the microphone muted or the volume set too low?

**Q: I found a bug or have an idea for a new feature. What should I do?**
A: That's great! The best place to report bugs or suggest features is by opening an "Issue" on our [GitHub repository](https://github.com/sl5net/Vosk-System-Listener).



**5. Q: The accuracy isn't perfect. How can I improve it?**
A: Accuracy depends on both your setup and software customization.

*   **Your Setup (The Basics):** Try to speak clearly at a consistent volume and pace. Reducing background noise and using a good headset microphone instead of a laptop's built-in mic makes a huge difference.

*   **Software Customization (Advanced Power):** For next-level accuracy, SL5 Auro uses a powerful feature called **FuzzyMaps**. Think of these as your personal, intelligent dictionary. You can create simple text files with rules to fix common, recurring recognition errors.

    *   **Example:** If the software often hears "get hap" instead of "GitHub", you can add a rule that automatically corrects this every time.
    *   **Benefit:** This allows you to "teach" the software your specific technical jargon, product names, abbreviations, or even create rule-sets for unique vocabularies. By customizing these maps, you can significantly improve accuracy for your specific use case.




### Architectural Deep Dive: Achieving Continuous "Walkie-Talkie" Style Recording

Our dictation service implements a robust, state-driven architecture to provide a seamless, continuous recording experience, akin to using a walkie-talkie. The system is always ready to capture audio, but only processes it when explicitly triggered, ensuring high responsiveness and low resource usage.

This is achieved by decoupling the audio listening loop from the processing thread and managing the system state with two key components: an `active_session` event flag and our `audio_manager` for OS-level microphone control.

**The State Machine Logic:**

The system operates in a perpetual loop, managed by a single hotkey that toggles between two primary states:

1.  **LISTENING State (Default/Ready):**
    *   **Condition:** The `active_session` flag is `False`.
    *   **Mic Status:** The microphone is **unmuted** via `unmute_microphone()`. The Vosk listener is active and waiting for audio input.
    *   **Action:** When the user presses the hotkey, the state transitions. The `active_session` flag is set to `True`, signaling the start of a "real" dictation.

2.  **PROCESSING State (User has finished speaking):**
    *   **Condition:** The user presses the hotkey while the `active_session` flag is `True`.
    *   **Mic Status:** The **first action** is to immediately **mute** the microphone via `mute_microphone()`. This instantly stops the audio stream to the Vosk engine.
    *   **Action:**
        *   The `active_session` flag is set to `False`.
        *   The final recognized audio chunk is retrieved from Vosk.
        *   The processing thread is launched with this final text.
        *   Crucially, within a `finally` block, the processing thread executes `unmute_microphone()` upon completion.

**The "Magic" of the Unmute Signal:**

The key to the endless loop is the final `unmute_microphone()` call. As soon as the processing of dictation `A` is finished and the microphone is unmuted, the system automatically and instantly reverts to the **LISTENING** state. The Vosk listener, which was patiently waiting, immediately starts receiving audio again, ready to capture dictation `B`.

This creates a highly responsive cycle:
`Press -> Speak -> Press -> (Mute & Process) -> (Unmute & Listen)`

This architecture ensures that the microphone is only ever muted for the brief duration of text processing, making the system feel instantaneous to the user while maintaining robust control and preventing runaway recordings.


