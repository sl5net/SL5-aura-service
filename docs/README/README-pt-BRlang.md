# Voz offline em todo o sistema para comandos ou texto, sistema conectável

**⚠️ Requisitos do sistema e compatibilidade**

* **Windows:** ✅ Totalmente compatível (usa AutoHotkey/PowerShell).
* **macOS:** ✅ Totalmente compatível (usa AppleScript).
* **Linux (X11/Xorg):** ✅ Totalmente suportado. Recomendado para melhor experiência.
* **Linux (Wayland):** ⚠️ **Limitado/Experimental.**
* *As teclas de atalho globais e a digitação automática geralmente não funcionam no Wayland devido a restrições de segurança.*
* *Por favor, mude para uma **Sessão X11** no login (por exemplo, "Plasma (X11)" ou "Ubuntu no Xorg") para usar todos os recursos.*


Bem-vindo ao Serviço SL5 Aura! Este documento fornece uma visão geral rápida dos nossos principais recursos e da compatibilidade do sistema operacional.

Aura não é apenas uma transcritora; é um poderoso mecanismo de processamento off-line que transforma sua voz em ações e textos precisos.

É um **assistente de voz off-line** completo baseado em **Vosk** (para conversão de fala em texto) e **LanguageTool** (para gramática/estilo), agora com um **Local LLM (Ollama) Fallback** opcional para respostas criativas e correspondência difusa avançada. Ele foi projetado para personalização definitiva por meio de um sistema de regras conectável e um mecanismo de script dinâmico.

  
Traduções: Este documento também existe em [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/docs).

Nota: Muitos textos são traduções geradas automaticamente da documentação original em inglês e destinam-se apenas a orientação geral. Em caso de discrepâncias ou ambiguidades, prevalece sempre a versão em inglês. Agradecemos a ajuda da comunidade para melhorar esta tradução!

___

[![SL5 Aura (v0.16.1): HowTo crash SL5 Aura? -  seeh Hierarchical and Recursive Rule Engine](https://img.youtube.com/vi/d98ml86u68g/maxresdefault.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)
( https://www.youtube.com/watch?v=BZCHonTqwUw ou https://skipvids.com/?v=BZCHonTqwUw )

## Principais recursos

* **Off-line e privado:** 100% local. Nenhum dado sai da sua máquina.
* **Mecanismo de script dinâmico:** Vá além da substituição de texto. As regras podem executar scripts Python personalizados (`on_match_exec`) para executar ações avançadas, como chamar APIs (por exemplo, pesquisar na Wikipedia), interagir com arquivos (por exemplo, gerenciar uma lista de tarefas) ou gerar conteúdo dinâmico (por exemplo, uma saudação por e-mail com reconhecimento de contexto).
* **Mecanismo de transformação de alto controle:** Implementa um pipeline de processamento altamente personalizável e orientado por configuração. A prioridade das regras, a detecção de comandos e as transformações de texto são determinadas puramente pela ordem sequencial das regras nos Mapas Fuzzy, exigindo **configuração, não codificação**.
* **Uso conservador de RAM:** Gerencia a memória de forma inteligente, pré-carregando modelos apenas se houver RAM livre suficiente disponível, garantindo que outros aplicativos (como jogos de PC) sempre tenham prioridade.
* **Plataforma cruzada:** Funciona em Linux, macOS e Windows.
* **Totalmente Automatizado:** Gerencia seu próprio servidor LanguageTool (mas você também pode usar um externo).
* **Extremamente rápido:** O cache inteligente garante notificações instantâneas de "escuta..." e processamento rápido.

## Documentação

Para uma referência técnica completa, incluindo todos os módulos e scripts, visite nossa página de documentação oficial. Ele é gerado automaticamente e está sempre atualizado.

[**Go to Documentation >>**](https://sl5net.github.io/SL5-aura-service/)


### Status da compilação
[![Linux Manjaro](https://img.shields.io/badge/Manjaro-Tested-27ae60?style=for-the-badge&logo=manjaro)](https://youtu.be/D9ylPBnP2aQ)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)
[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![Documentation](https://img.shields.io/badge/documentation-live-brightgreen)](https://sl5net.github.io/SL5-aura-service/)

**Leia isto em outros idiomas:**

[🇬🇧 English](README.md) | [🇸🇦 العربية](./README-arlang.md) | [🇩🇪 Deutsch](./README-delang.md) | [🇪🇸 Español](./README-eslang.md) | [🇫🇷 Français](./README-frlang.md) | [🇮🇳 हिन्दी](./README-hilang.md) | [🇯🇵 日本語](./README-jalang.md) | [🇰🇷 한국어](./README-kolang.md) | [🇵🇱 Polski](./README-pllang.md) | [🇵🇹 Português](./README-ptlang.md) | [🇧🇷 Português Brasil](./README-pt-BRlang.md) | [🇨🇳 简体中文](./README-zh-CNlang.md)

---







## Instalação

A configuração é um processo de duas etapas:
1. Baixe a última versão ou master (https://github.com/sl5net/Vosk-System-Listener/archive/master.zip) ou clone este repositório em seu computador.
2. Execute o script de configuração único para seu sistema operacional.

Os scripts de configuração cuidam de tudo: dependências do sistema, ambiente Python e download dos modelos e ferramentas necessários (~ 4 GB) diretamente de nossas versões do GitHub para velocidade máxima.


#### Para Linux, macOS e Windows (com exclusão opcional de idioma)

Para economizar espaço em disco e largura de banda, você pode excluir modelos de linguagem específicos (`de`, `en`) ou todos os modelos opcionais (`all`) durante a configuração. **Os componentes principais (LanguageTool, lid.176) estão sempre incluídos.**

Abra um terminal no diretório raiz do projeto e execute o script para o seu sistema:

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

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

# Or (recommend) - Start des BAT: 
windows11_setup.bat -Exclude "en"
```

#### Para Windows
Execute o script de configuração com privilégios de administrador.

**Instale uma ferramenta para leitura e execução, por exemplo. [CopyQ](https://github.com/hluk/CopyQ) ou [AutoHotkey v2](https://www.autohotkey.com/)**. Isso é necessário para o observador de digitação de texto.

A instalação é totalmente automatizada e leva cerca de **8 a 10 minutos** ao usar 2 modelos em um sistema novo.

1. Navegue até a pasta `setup`.
2. Clique duas vezes em **`windows11_setup_with_ahk_copyq.bat`**.
* *O script solicitará automaticamente privilégios de administrador.*
* *Ele instala o sistema principal, modelos de linguagem, **AutoHotkey v2** e **CopyQ**.*
3. Assim que a instalação for concluída, **Aura Dictation** será iniciado automaticamente.

> **Observação:** Você não precisa instalar o Python ou o Git previamente; o script cuida de tudo.

---

#### Instalação avançada/personalizada
Se preferir não instalar as ferramentas cliente (AHK/CopyQ) ou quiser economizar espaço em disco excluindo idiomas específicos, você pode executar o script principal por meio da linha de comando:

```powershell
# Core Setup only (No AHK, No CopyQ)
setup\windows11_setup.bat

# Exclude specific language models (saves space):
# Exclude English:
setup\windows11_setup.bat -Exclude "en"

# Exclude German and English:
setup\windows11_setup.bat -Exclude "de,en"
```


---

## Uso

### 1. Inicie os serviços

#### No Linux e macOS
Um único script cuida de tudo. Ele inicia o serviço principal de ditado e o observador de arquivos automaticamente em segundo plano.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

#### No Windows
Iniciar o serviço é um **processo manual de duas etapas**:

1. **Inicie o serviço principal:** Execute `start_dictation_v2.0.bat`. ou inicie em `.venv` o serviço com `python3`

### 2. Configure sua tecla de atalho

Para acionar o ditado, você precisa de uma tecla de atalho global que crie um arquivo específico. Recomendamos enfaticamente a ferramenta multiplataforma [CopyQ](https://github.com/hluk/CopyQ).

#### Nossa recomendação: CopyQ

Crie um novo comando no CopyQ com um atalho global.

**Comando para Linux/macOS:**
__CODE_BLOCO_3__

**Comando para Windows ao usar [CopyQ](https://github.com/hluk/CopyQ):**
```bash
touch /tmp/sl5_record.trigger
```


**Comando para Windows ao usar [AutoHotkey](https://AutoHotkey.com):**
__CODE_BLOCO_5__


### 3. Comece a ditar!
Clique em qualquer campo de texto, pressione a tecla de atalho e uma notificação "Ouvindo..." aparecerá. Fale claramente e depois faça uma pausa. O texto corrigido será digitado para você.

---


## Configuração avançada (opcional)

Você pode personalizar o comportamento do aplicativo criando um arquivo de configurações locais.

1. Navegue até o diretório `config/`.
2. Crie uma cópia de `config/settings_local.py_Example.txt` e renomeie-a para `config/settings_local.py`.
3. Edite `config/settings_local.py` (substitui qualquer configuração do arquivo principal `config/settings.py`).

Este arquivo `config/settings_local.py` é (talvez) ignorado pelo Git, então suas alterações pessoais (talvez) não serão substituídas por atualizações.

### Estrutura e lógica do plug-in

A modularidade do sistema permite uma extensão robusta através do diretório plugins/.

O mecanismo de processamento segue estritamente uma **Cadeia de Prioridade Hierárquica**:

1. **Ordem de carregamento do módulo (alta prioridade):** As regras carregadas dos pacotes de idiomas principais (de-DE, en-US) têm precedência sobre as regras carregadas do diretório plugins/ (que são carregadas por último em ordem alfabética).
  
2. **Ordem no arquivo (Micro Prioridade):** Dentro de qualquer arquivo de mapa (FUZZY_MAP_pre.py), as regras são processadas estritamente por **número de linha** (de cima para baixo).
  

Essa arquitetura garante que as regras básicas do sistema sejam protegidas, enquanto regras específicas do projeto ou sensíveis ao contexto (como aquelas para CodeIgniter ou controles de jogos) podem ser facilmente adicionadas como extensões de baixa prioridade por meio de plug-ins.
## Scripts principais para usuários do Windows

Aqui está uma lista dos scripts mais importantes para configurar, atualizar e executar o aplicativo em um sistema Windows.

### Configuração e atualização
* `setup/setup.bat`: O script principal para a **configuração inicial única** do ambiente.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Executar powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

* `update.bat` : Execute-os na pasta do projeto **obtenha o código e as dependências mais recentes**.

### Executando o aplicativo
* `start_dictation_v2.0.bat`: Um script primário para **iniciar o serviço de ditado**.

### Scripts principais e auxiliares
* `aura_engine.py`: O serviço principal do Python (geralmente iniciado por um dos scripts acima).
* `get_suggestions.py`: Um script auxiliar para funcionalidades específicas.




## 🚀 Principais recursos e compatibilidade de sistema operacional

Legenda para compatibilidade de sistema operacional:  
* 🐧 **Linux** (por exemplo, Arch, Ubuntu)  
* 🍏 **macOS**  
* 🪟 **Windows**  
* 📱 **Android** (para recursos específicos para dispositivos móveis)  

---

### **Motor principal de conversão de fala em texto (Aura)**
Nosso principal mecanismo para reconhecimento de fala offline e processamento de áudio.

  
**Aura-Core/** 🐧 🍏 🪟  
├─ `aura_engine.py` (principal serviço Python orquestrando Aura) 🐧 🍏 🪟  
├┬ **Live Hot-Reload** (Configuração e Mapas) 🐧 🍏 🪟  
│├ **Carregamento seguro de mapa privado (integridade em primeiro lugar)** 🔒 🐧 🍏 🪟  
││ * **Fluxo de trabalho:** Carrega arquivos ZIP protegidos por senha.   
│├ **Processamento e correção de texto/** Agrupado por idioma (por exemplo, `de-DE`, `en-US`, ...)   
│├ 1. `normalize_punctuation.py` (padroniza a pontuação pós-transcrição) 🐧 🍏 🪟  
│├ 2. **Pré-correção inteligente** (`FuzzyMap Pre` - [The Primary Command Layer](docs/CreatingNewPluginModules-pt-BRlang.md)) 🐧 🍏 🪟  
││ * **Execução dinâmica de script:** As regras podem acionar scripts Python personalizados (on_match_exec) para executar ações avançadas como chamadas de API, E/S de arquivo ou gerar respostas dinâmicas.  
││ * **Execução em Cascata:** As regras são processadas sequencialmente e seus efeitos são **cumulativos**. Regras posteriores se aplicam ao texto modificado por regras anteriores.  
││ * **Critério de parada de prioridade mais alta:** Se uma regra atingir uma **Correspondência completa** (^...$), todo o pipeline de processamento desse token será interrompido imediatamente. Este mecanismo é fundamental para implementar comandos de voz confiáveis.  
│├ 3. `correct_text_by_languagetool.py` (Integra o LanguageTool para correção de gramática/estilo) 🐧 🍏 🪟  
│├ **4. Motor de regras RegEx hierárquico com Ollama AI Fallback** 🐧 🍏 🪟  
││ * **Controle Determinístico:** Usa RegEx-Rule-Engine para comando preciso e de alta prioridade e controle de texto.  
││ * **Ollama AI (Local LLM) Fallback:** Serve como uma verificação opcional de baixa prioridade para **respostas criativas, perguntas e respostas e correspondência difusa avançada** quando nenhuma regra determinística é atendida.  
││ * **Status:** Integração LLM local.
│└ 5. **Pós-Correção Inteligente** (`FuzzyMap`)**– Refinamento Pós-LT** 🐧 🍏 🪟
││ * Aplicado após o LanguageTool para corrigir saídas específicas do LT. Segue a mesma lógica estrita de prioridade em cascata da camada de pré-correção.  
││ * **Execução dinâmica de script:** As regras podem acionar scripts Python personalizados ([on_match_exec](docs/advanced-scripting-pt-BRlang.md)) para executar ações avançadas, como chamadas de API, E/S de arquivo ou gerar respostas dinâmicas.  
││ * **Fuzzy Fallback:** A **Verificação de similaridade difusa** (controlada por um limite, por exemplo, 85%) atua como a camada de correção de erros de prioridade mais baixa. Ele só será executado se toda a execução anterior da regra determinística/em cascata não conseguir encontrar uma correspondência (current_rule_matched é False), otimizando o desempenho evitando verificações difusas lentas sempre que possível.  
├┬ **Gerenciamento de modelo/**   
│├─ `prioritize_model.py` (otimiza o carregamento/descarregamento do modelo com base no uso) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (configura a configuração inicial do modelo) 🐧 🍏 🪟  
├─ **Tempo limite do VAD adaptável** 🐧 🍏 🪟  
├─ **Tecla de atalho adaptativa (Iniciar/Parar)** 🐧 🍏 🪟  
└─ **Troca instantânea de idioma** (Experimental via pré-carregamento de modelo) 🐧 🍏   

**Utilitários do sistema/**   
├┬ **Gerenciamento de servidor LanguageTool/**   
│├─ `start_languagetool_server.py` (inicializa o servidor LanguageTool local) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py` (Desliga o servidor LanguageTool) 🐧 🍏
├─ `monitor_mic.sh` (por exemplo, para uso com fone de ouvido sem usar teclado e monitor) 🐧 🍏 🪟  

### **Gerenciamento de modelos e pacotes**  
Ferramentas para manipulação robusta de modelos de linguagem grandes.  

**Gerenciamento de modelo/** 🐧 🍏 🪟  
├─ **Downloader de modelo robusto** (pedaços de lançamento do GitHub) 🐧 🍏 🪟  
├─ `split_and_hash.py` (Utilitário para proprietários de repositórios dividirem arquivos grandes e gerarem somas de verificação) 🐧 🍏 🪟  
└─ `download_all_packages.py` (ferramenta para usuários finais baixarem, verificarem e remontarem arquivos de várias partes) 🐧 🍏 🪟  


### **Ajudantes de desenvolvimento e implantação**  
Scripts para configuração de ambiente, teste e execução de serviço.  

*Dica: glogg permite que você use expressões regulares para pesquisar eventos interessantes em seus arquivos de log.*   
Marque a caixa de seleção ao instalar para associar aos arquivos de log.    
https://translate.google.com/translate?hl=en&sl=en&tl=pt-BR&u=https://glogg.bonnefon.org/     
  
*Dica: depois de definir seus padrões regex, execute `python3 tools/map_tagger.py` para gerar automaticamente exemplos pesquisáveis para as ferramentas CLI. Consulte [Map Maintenance Tools](docs/Developer_Guide/Map_Maintenance_Tools-pt-BRlang.md) para obter detalhes.*

Então talvez clique duas vezes
`log/aura_engine.log`
  
  
**DevHelpers/**  
├┬ **Gerenciamento de ambiente virtual/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ **Integração de ditado em todo o sistema/**  
│├ Integração Vosk-System-Listener 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (monitoramento de microfone específico do Linux) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey escuta texto reconhecido e digita-o em todo o sistema) 🪟  
└─ **Automação CI/CD/**  
└─ Fluxos de trabalho expandidos do GitHub (instalação, teste, implantação de documentos) 🐧 🍏 🪟 *(Executado em ações do GitHub)*  

### **Recursos futuros/experimentais**  
Recursos atualmente em desenvolvimento ou em status de rascunho.  

**Recursos Experimentais/**  
├─ **ENTER_AFTER_DICTATION_REGEX** Exemplo de regra de ativação "(ExampleAplicationThatNotExist|Pi, sua IA pessoal)" 🐧  
├┬Plugins  
│╰┬ **Live Lazy-Reload** (*) 🐧 🍏 🪟  
(*Alterações na ativação/desativação do plug-in e suas configurações são aplicadas na próxima execução de processamento sem reinicialização do serviço.*)  
│ ├ **comandos git** (Controle de voz para enviar comandos git) 🐧 🍏 🪟  
│ ├ **wannweil** (Mapa para localização Alemanha-Wannweil) 🐧 🍏 🪟  
│ ├ **Poker Plugin (Draft)** (Controle de voz para aplicativos de pôquer) 🐧 🍏 🪟  
│ └ **Plugin 0 A.D. (Draft)** (Controle de voz para jogo 0 A.D.) 🐧   
├─ **Saída de som ao iniciar ou encerrar uma sessão** (Descrição pendente) 🐧   
├─ **Saída de fala para deficientes visuais** (Descrição pendente) 🐧 🍏 🪟  
└─ **Protótipo SL5 Aura Android** (Ainda não totalmente offline) 📱  

---

*(Nota: Distribuições específicas do Linux como Arch (ARL) ou Ubuntu (UBT) são cobertas pelo símbolo geral do Linux 🐧. Distinções detalhadas podem ser abordadas nos guias de instalação.)*









<detalhes>
<summary>Clique para ver o comando usado para gerar esta lista de scripts</summary>

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
</detalhes>


### observe graficamente o que está por trás:

![yappi_call_graph](doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

  
![pydeps -v -o dependencies.svg scripts/py/func/main.py](doc_sources/dependencies.svg)


# Modelos Usados:

Recomendação: use modelos do Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (provavelmente mais rápido)

Estes modelos compactados devem ser salvos na pasta `models/`

`mv vosk-model-*.zip modelos/`


| Modelo | Tamanho | Taxa/velocidade de erros de palavras | Notas | Licença |
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1,8G | 5,69 (librisspeech test-clean)<br/>6,05 (tedlium)<br/>29,78 (callcenter) | Modelo genérico preciso do inglês dos EUA | Apache2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) | 1,9G | 9,83 (teste Tuda-de)<br/>24,00 (podcast)<br/>12,82 (teste cv)<br/>12,42 (mls)<br/>33,26 (mtedx) | Grande modelo alemão para telefonia e servidor | Apache2.0 |

Esta tabela fornece uma visão geral dos diferentes modelos Vosk, incluindo tamanho, taxa ou velocidade de erro de palavras, notas e informações de licença.


- **Modelos Vosk:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **Ferramenta de Idioma:**  
(6.6)[https://languagetool.org/download/](https://languagetool.org/download/)

**Licença do LanguageTool:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---

## Apoie o Projeto
Se você achar esta ferramenta útil, considere comprar um café para nós! Seu apoio ajuda a impulsionar melhorias futuras.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)



IgnorePkg = linux66-nvidia-575xx nvidia-575xx-utils lib32-nvidia-575xx-utils

configurações nvidia-575xx mhwd-nvidia-575xx