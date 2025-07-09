```
2025-07-03 22:29:51,888 - INFO     - --- Vosk dictation_service starting ---
...
2025-07-03 22:29:51,890 - INFO     - Waiting for LanguageTool Server to be responsive...
2025-07-03 22:29:52,896 - CRITICAL - LanguageTool process terminated unexpectedly.
...
2025-07-03 22:29:52,897 - ERROR    - LanguageTool STDERR:
Exception in thread "main" java.lang.ExceptionInInitializerError
	at org.languagetool.language.identifier.LanguageIdentifierService.getDefaultLanguageIdentifier(LanguageIdentifierService.java:54)
	at org.languagetool.server.TextChecker.<init>(TextChecker.java:187)
	at org.languagetool.server.V2TextChecker.<init>(V2TextChecker.java:48)
	at org.languagetool.server.LanguageToolHttpHandler.<init>(LanguageToolHttpHandler.java:84)
	at org.languagetool.server.HTTPServer.<init>(HTTPServer.java:110)
	at org.languagetool.server.HTTPServer.main(HTTPServer.java:180)
Caused by: java.lang.RuntimeException: java.io.IOException: Common words file not found for Arabic: ar/common_words.txt
	at org.languagetool.language.identifier.LanguageIdentifier.<clinit>(LanguageIdentifier.java:59)
...

Solution:

delete Folder

1. LanguageTool-6.6
2. start setup again
