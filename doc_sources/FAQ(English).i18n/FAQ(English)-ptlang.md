### FAQ (Inglês) 3.8.'2025 Dom

**1. P: O que é SL5 Aura?**
R: É um programa de conversão de fala em texto off-line para todo o sistema. Ele permite que você dite em qualquer aplicativo do seu computador (Windows, macOS, Linux) sem precisar de conexão com a internet.

**2. P: Por que devo usar isso? O que o torna especial?**
R: **Privacidade.** Seus dados de voz são processados 100% em sua máquina local e nunca enviados para a nuvem. Isso o torna totalmente privado e compatível com GDPR.

**3. P: É grátis?**
R: Sim, a Community Edition é totalmente gratuita e de código aberto. Você pode encontrar o código e o instalador em nosso GitHub: [https://github.com/sl5net/Vosk-System-Listener](https://github.com/sl5net/Vosk-System-Listener)

**4. P: O que preciso para usá-lo?**
R: Um computador e um microfone. Para melhor precisão, recomendamos fortemente um microfone headset dedicado em vez de um microfone embutido em laptop.

**5. P: A precisão não é perfeita. Como posso melhorá-lo?**
R: Tente falar claramente em volume e ritmo consistentes. Reduzir o ruído de fundo e usar um microfone melhor faz a maior diferença.
Personalização de software (poder avançado): para precisão de próximo nível, SL5 Aura usa um recurso poderoso chamado FuzzyMaps. Pense neles como seu dicionário pessoal e inteligente. Você pode criar arquivos de texto simples com regras para corrigir erros de reconhecimento comuns e recorrentes.

Exemplo: se o software ouvir frequentemente "get hap" em vez de "GitHub", você poderá adicionar uma regra que corrija isso automaticamente sempre.

Benefício: Isso permite que você "ensine" ao software seu jargão técnico específico, nomes de produtos, abreviações ou até mesmo crie conjuntos de regras para vocabulários exclusivos. Ao personalizar esses mapas, você pode melhorar significativamente a precisão para seu caso de uso específico.

***

#### **Parte 1: Perguntas Gerais**

**P: O que é SL5 Auro?**
R: SL5 Auro é um programa de conversão de fala em texto off-line para todo o sistema. Ele permite que você dite texto em qualquer aplicativo do seu computador (por exemplo, seu cliente de e-mail, um processador de texto, um editor de código) sem precisar de uma conexão com a Internet.

**P: O que significa "offline" e por que é importante?**
R: "Off-line" significa que todo o processamento de voz acontece diretamente no seu computador. Seus dados de voz **nunca** são enviados para um servidor em nuvem (como Google, Amazon ou OpenAI). Isto proporciona máxima privacidade e segurança, tornando-o ideal para informações confidenciais (por exemplo, para advogados, médicos, jornalistas) e totalmente compatível com regulamentos de proteção de dados como o GDPR.

**P: É realmente grátis? Qual é o truque?**
R: A "Community Edition" é 100% gratuita e de código aberto. Não há pegadinha. Acreditamos no poder das ferramentas de código aberto. Se você considera o software valioso e deseja apoiar seu desenvolvimento contínuo, você pode fazê-lo através do nosso [Ko-fi page](https://ko-fi.com/sl5).

**P: Para quem é este software?**
R: É para quem escreve muito e deseja aumentar sua eficiência: escritores, estudantes, programadores, profissionais jurídicos e médicos, pessoas com limitações físicas ou qualquer pessoa que simplesmente prefira falar a digitar.

#### **Parte 2: Instalação e configuração**

**P: Quais sistemas operacionais são compatíveis?**
R: O software foi testado e confirmado para funcionar no Windows 11, Manjaro Linux e Ubuntu e macOS.

**P: Como faço para instalá-lo no Windows?**
R: Fornecemos um instalador simples com um clique. É um script .Bat que requer direitos administrativos para configurar o ambiente e baixar os modelos necessários. Depois de executado, ele cuidará de tudo para você.

**P: O download dos modelos é muito grande. Por que?**
R: Os modelos de reconhecimento de fala permitem que o software funcione offline. Eles contêm todos os dados necessários para que a IA entenda o seu idioma. Modelos maiores e mais precisos podem ter vários gigabytes de tamanho. Nosso novo downloader os divide em partes menores e verificáveis para garantir um download confiável.

**P: Estou no Linux. Qual é o processo?**
R: No Linux, você normalmente clonará o repositório do GitHub e executará um script de configuração. Este script cria um ambiente virtual Python, instala dependências e inicia o serviço de ditado.

**P: Quando clico duas vezes em um arquivo `.py` no Windows, ele abre em um editor de texto. Como faço para executá-lo?**
R: Este é um problema comum do Windows em que os arquivos `.py` não estão associados ao interpretador Python. Você não deve executar scripts Python individuais diretamente. Sempre use o script de inicialização principal fornecido (por exemplo, um arquivo `.bat`), pois isso garante que o ambiente correto seja ativado primeiro.

#### **Parte 3: Uso e recursos**

**P: Como posso usá-lo para ditar?**
R: Primeiro, você inicia o "serviço de ditado" executando o script apropriado. Ele será executado em segundo plano. Em seguida, você usa um gatilho (como uma tecla de atalho ou um script dedicado) para iniciar e parar a gravação. O texto reconhecido será então digitado automaticamente em qualquer janela que esteja ativa no momento.

**P: Como posso melhorar a precisão?**
R: 1. **Use um bom microfone:** Um microfone headset é muito melhor do que o microfone embutido em um laptop. 2. **Minimize o ruído de fundo:** Um ambiente silencioso é fundamental. 3. **Fale claramente:** Fale em ritmo e volume consistentes. Não resmungue nem tenha pressa.
Personalização de software (poder avançado): Para precisão de próximo nível, SL5 Auro usa um recurso poderoso chamado FuzzyMaps. Pense neles como seu dicionário pessoal e inteligente. Você pode criar arquivos de texto simples com regras para corrigir erros de reconhecimento comuns e recorrentes.

Exemplo: se o software ouvir frequentemente "get hap" em vez de "GitHub", você poderá adicionar uma regra que corrija isso automaticamente sempre.

Benefício: Isso permite que você "ensine" ao software seu jargão técnico específico, nomes de produtos, abreviações ou até mesmo crie conjuntos de regras para vocabulários exclusivos. Ao personalizar esses mapas, você pode melhorar significativamente a precisão para seu caso de uso específico.

**P: Posso mudar de idioma?**
R: Sim. O sistema suporta "recarregamento a quente" de arquivos de configuração. Você pode alterar o modelo de idioma na configuração e o serviço mudará para ele instantaneamente, sem precisar reiniciar.

**P: O que é "LanguageTool"?**
R: LanguageTool é um verificador gramatical e de estilo de código aberto que integramos. Depois que seu discurso é transformado em texto, o LanguageTool corrige automaticamente erros comuns de transcrição (por exemplo, "certo" vs. "escrever") e corrige a pontuação, melhorando significativamente o resultado final.

#### **Parte 4: Solução de problemas e suporte**

**P: Iniciei o serviço, mas nada acontece quando tento ditar.**
R: Verifique o seguinte:
1. O serviço ainda está em execução no seu terminal/console? Procure por mensagens de erro.
2. O seu microfone está selecionado corretamente como dispositivo de entrada padrão no seu sistema operacional?
3. O microfone está mudo ou o volume está muito baixo?

**P: Encontrei um bug ou tenho uma ideia para um novo recurso. O que devo fazer?**
R: Isso é ótimo! O melhor lugar para relatar bugs ou sugerir recursos é abrindo um "Problema" em nosso [GitHub repository](https://github.com/sl5net/Vosk-System-Listener).



**5. P: A precisão não é perfeita. Como posso melhorá-lo?**
R: A precisão depende da configuração e da personalização do software.

* **Sua configuração (o básico):** Tente falar claramente em volume e ritmo consistentes. Reduzir o ruído de fundo e usar um bom microfone headset em vez do microfone embutido em um laptop faz uma enorme diferença.

* **Personalização de software (potência avançada):** Para maior precisão, o SL5 Auro usa um recurso poderoso chamado **FuzzyMaps**. Pense neles como seu dicionário pessoal e inteligente. Você pode criar arquivos de texto simples com regras para corrigir erros de reconhecimento comuns e recorrentes.

* **Exemplo:** Se o software ouvir frequentemente "get hap" em vez de "GitHub", você poderá adicionar uma regra que corrija isso automaticamente sempre.
* **Benefício:** Isso permite que você "ensine" ao software seu jargão técnico específico, nomes de produtos, abreviações ou até mesmo crie conjuntos de regras para vocabulários exclusivos. Ao personalizar esses mapas, você pode melhorar significativamente a precisão para seu caso de uso específico.




### Aprofundamento arquitetônico: alcançando gravação contínua no estilo "Walkie-Talkie"

Nosso serviço de ditado implementa uma arquitetura robusta e orientada pelo estado para fornecer uma experiência de gravação contínua e contínua, semelhante ao uso de um walkie-talkie. O sistema está sempre pronto para capturar áudio, mas só o processa quando acionado explicitamente, garantindo alta capacidade de resposta e baixo consumo de recursos.

Isso é conseguido desacoplando o loop de escuta de áudio do thread de processamento e gerenciando o estado do sistema com dois componentes principais: um sinalizador de evento `active_session` e nosso `audio_manager` para controle de microfone no nível do sistema operacional.

**A Lógica da Máquina de Estado:**

O sistema opera em loop perpétuo, gerenciado por uma única tecla de atalho que alterna entre dois estados primários:

1. **Estado de ESCUTA (Padrão/Pronto):**
* **Condição:** O sinalizador `active_session` é `False`.
* **Status do microfone:** O microfone está **silenciado** para `ativar o microfone()`. O ouvinte Vosk está ativo e aguardando entrada de áudio.
* **Ação:** Quando o usuário pressiona a tecla de atalho, o estado muda. O sinalizador `active_session` está definido como `True`, sinalizando o início de um ditado "real".

2. **Estado PROCESSING (o usuário terminou de falar):**
* **Condição:** O usuário pressiona a tecla de atalho enquanto o sinalizador `active_session` é `True`.
* **Status do microfone:** A **primeira ação** é **silenciar** imediatamente o microfone via `mute_microphone()`. Isso interrompe instantaneamente o fluxo de áudio para o mecanismo Vosk.
*   **Ação:**
* O sinalizador `active_session` está definido como `False`.
* O pedaço de áudio final reconhecido é recuperado do Vosk.
* O thread de processamento é iniciado com este texto final.
* Crucialmente, dentro de um bloco `finally`, o thread de processamento executa `unmute_microphone()` após a conclusão.

**A "mágica" do sinal de ativação do som:**

A chave para o loop infinito é a chamada final `unmute_microphone()`. Assim que o processamento do ditado `A` for concluído e o microfone for ativado, o sistema reverterá automática e instantaneamente para o estado **LISTENING**. O ouvinte Vosk, que esperava pacientemente, imediatamente começa a receber áudio novamente, pronto para capturar o ditado `B`.

Isso cria um ciclo altamente responsivo:
`Pressione -> Falar -> Pressione -> (Mudo e Processar) -> (Ativar som e Ouvir)`

Essa arquitetura garante que o microfone fique silenciado apenas durante o breve período do processamento de texto, fazendo com que o sistema pareça instantâneo para o usuário, ao mesmo tempo que mantém um controle robusto e evita gravações descontroladas.