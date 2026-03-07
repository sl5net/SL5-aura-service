## Objetivo: O modelo de "Sessão de Ditado"

### Unser Ziel(alemão): Die "Diktier-Sitzung"

Ein einziger Trigger startet eine **"Diktier-Sitzung"**, die aus drei Phasen besteht:

1. **Fase inicial (Warten auf Sprache):**
* Após o acionamento do sistema ser iniciado.
* Se **keine** Spracheingabe for erfolgt, endet die gesamte Sitzung nach `PRE_RECORDING_TIMEOUT` (z.B. 12s).

2. **Fase ativa (Kontinuierliches Diktieren):**
* Sobald die erste Spracheingabe erkannt wird, wechselt die Sitzung in the activen Modus.
* Mesmo que VOSK eine Sprechpause seja aberto e um Textblock exista (por exemplo, um Satz), este Block **sofort** para Verarbeitung (LanguageTool, etc.) será adicionado e o Text será adicionado.
* Die Aufnahme läuft währenddessen **nahtlos weiter**. Die Sitzung wartet auf den nächsten Satz.

3. **Fase final (Ende der Sitzung):**
* Die gesamte Sitzung endet nur, wenn eine dieser beiden Bedingungen erfüllt ist:
* Der Nutzer bleibt für die Dauer des `SPEECH_PAUSE_TIMEOUT` (z.B. 1-2s) ainda completo.
* Der Nutzer interrompe a situação manualmente por gatilho.

**Zusammengefasst:** Eine Sitzung, viele sofortige Textausgaben. A posição está ativa, até que o Nutzer faça uma pausa prolongada ou faça uma pausa manual.


### **Objetivo: O modelo de "Sessão de Ditado"**

Um único gatilho inicia uma **"Sessão de Ditado"**, que consiste em três fases:
1. **Fase de inicialização (aguardando fala):**
* Após o disparo, o sistema começa a escutar.
* Se **nenhuma fala** for detectada, toda a sessão termina após `PRE_RECORDING_TIMEOUT` (por exemplo, 12s).
2. **Fase Ativa (Ditado Contínuo):**
* Assim que a primeira entrada de fala for detectada, a sessão muda para o modo ativo.
* Sempre que o VOSK detecta uma pausa e entrega um pedaço de texto (por exemplo, uma frase), esse pedaço é **imediatamente** passado para o pipeline de processamento (LanguageTool, etc.) e gerado como texto.
* A gravação continua **perfeitamente** em segundo plano, aguardando a próxima declaração.
3. **Fase de Encerramento (Encerramento da Sessão):**
* A sessão inteira termina somente quando uma das duas condições for atendida:
* O usuário permanece completamente em silêncio durante o `SPEECH_PAUSE_TIMEOUT` (por exemplo, 1-2s).
* O usuário interrompe manualmente a sessão por meio do gatilho.
**Resumindo:** Uma sessão, múltiplas saídas de texto imediatas. A sessão permanece ativa até que o usuário faça uma pausa longa ou a termine manualmente.