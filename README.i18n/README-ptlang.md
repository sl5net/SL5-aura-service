> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

# ⬟ SL5 Aura – Sua Voz. Suas Regras.

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 100% offline, estrutura de assistente de voz com prioridade à privacidade.  
> Defina exatamente o que sua voz faz — a partir de uma única palavra
> para scripts Python completos. Sem nuvem. Nenhum dado sai da sua máquina.  
> Funciona no terminal, no navegador ou como um serviço em segundo plano — no Linux, macOS e Windows.

| 👵 Iniciante | 🎓 Aprendiz | 🧑‍💻 Desenvolvedor |
|---|---|---|
| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-ptlang.md#the-oma-modus-beginner-shortcut) : basta escrever uma palavra, Aura faz o resto | Aprenda com Koans — um conceito de cada vez | Script completo em Python, plugins, chamadas de API |
| 🗄️ Gerenciamento de Estado | Orquestração Trino + Airflow, fzf, CopyQ, comandos de voz/terminal, interfaces de navegador |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **~2,87 J** por teste (39 tests without LanguageTool across >800 maps @ 0.07s warm / 0.36s cold 🌿 measured with XMDLINK1X) · sem computação em nuvem

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **Conjunto completo de testes:** 94 testes com LanguageTool em mais de 800 mapas @ 0,07s aquecido / 0,46s frio · sem computação em nuvem

<details>
<summary>Início Rápido</summary>

## Início Rápido

### Opção A: Instalador Web e 1-Click (Recommended)

Comando de uma linha ou instalador independente para Linux, macOS e Windows:
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-ptlang.md)**

---

## # Opção B: Instalação Manual (Desenvolvedores / Git)

1. Baixar ou clonar este repositório
2. Execute o script de configuração para o seu sistema operacional (ver pasta `setup/`):
- Linux (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
- Linux (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
- Linux (openSUSE): `bash setup/suse_setup.sh`
- Linux (NixOS): `nix-shell setup/shell.nix` e `bash setup/nixos_setup.sh`
== Ver também ==== Ligações externas ==   
- macOS: `bash setup/macos_setup.sh`
- Windows: `setup/windows11_setup_with_ahk_copyq.bat`
3. Iniciar Aura: `./scripts/restart_venv_and_run-server.sh`
4. Pressione a tecla de atalho e fale — **[full guide →](../docs/GettingStarted.i18n/GettingStarted-ptlang.md)**

---

Desinstalação
Para remover os serviços de fundo SL5 Aura, entradas de inicialização automática e ambientes virtuais:
- **Linux / macOS:** `bash setup/uninstall.sh`
- **Windows (PowerShell):** `powershell -File setup/uninstall.ps1`
*(Suas regras personalizadas no `config/maps/` são mantidas seguras por padrão a menos que você especifique `--purge`).*

---


Requisitos do sistema e compatibilidade **

* **Windows:** □ Totalmente suportado (usa AutoHotkey/PowerShell).
* ** macOS:** .. Totalmente suportado (usa AppleScript).
* **Linux (X11/Xorg):** Totalmente apoiado.
* **Linux (Wayland): ** Totalmente suportado (testado no KDE Plasma 6 / Wayland).
* **Linux (CachyOS / lançamento de rolamento baseado em arco):** Totalmente apoiado.
Requer mimaloc (`sudo pacman -S mimalloc`) devido à compatibilidade glibc 2.43.
* **Linux (NixOS): ** Experimental — configuração da comunidade, ainda não testada.
Se você tentar, por favor abra um problema ou RP com suas descobertas!   
* **Linux (Manjaro):** Novo : Uma tecla de atalho ampla do sistema abre uma interface fzf-like, orientada pelo teclado para que você possa executar comandos Aura de qualquer lugar no desktop (completamente dissociado da janela ativa). Este lançador orientado por teclas de atalho é atualmente implementado e testado no Linux (Manjaro); outras distribuições podem funcionar, mas requerem a configuração. Ver em [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-ptlang.md)   


    
SL5 Aura é um assistente de voz completo, **offline** construído em **Vosk** (para Speech-to-Text) e **LanguageTool** (para Grammar/Style), apresentando um opcional **Local LLM (Ollama) Fallback** para respostas criativas e correspondência fuzzy avançada. Transforma sua voz em ações e texto precisos, projetados para personalização final através de um sistema de regras plugáveis e um motor de script dinâmico.
    
Traduções: Este documento também existe no [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Nota: Muitos textos são traduções geradas por máquina da documentação original em inglês e destinam-se apenas a orientação geral. Em caso de discrepâncias ou ambiguidades, a versão inglesa sempre prevalece. Congratulamo-nos com a ajuda da comunidade para melhorar esta tradução!

</details>

<details>
<summary>Demo</summary>

### 📺 Demonstração do Terminal 

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **Dica:** Para uma melhor experiência no terminal, veja [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-ptlang.md).

### 🎥 Tutorial em Vídeo
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Link alternativo: [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw))*

</details>

<details>
<summary>Principais Recursos</summary>

# # Principais recursos

* **Offline & Private:** 100% local. Nenhum dado sai da sua máquina.
* ** Motor de Programação Dinâmica:** Vai além da substituição de texto. As regras podem executar scripts Python personalizados (`on_match_exec`) para executar ações avançadas como chamar APIs (por exemplo, pesquisar Wikipedia), interagir com arquivos (por exemplo, gerenciar uma lista de tarefas), ou gerar conteúdo dinâmico (por exemplo, uma saudação de e-mail consciente de contexto).
* ** Regras do Contexto-Aware:** Restrinja regras para aplicações específicas. Usando `only_in_windows`, você pode garantir que uma regra só aciona se um título específico da janela (por exemplo, "Terminal", "Código VS" ou "Browser") estiver ativo. Isso funciona multi-plataforma (Linux, Windows, macOS).
* ** Motor de Transformação de Alto Controle:** Implementa um pipeline de processamento de configuração altamente personalizável. Prioridade de regra, detecção de comandos e transformações de texto são determinadas puramente pela ordem sequencial das regras nos mapas fuzzy, exigindo ** configuração, não codificação**.
* ** Uso conservador da RAM:** Gerencia inteligentemente a memória, pré-carregando modelos apenas se houver RAM livre suficiente, garantindo que outros aplicativos (como seus jogos de PC) sempre tenham prioridade.
* **Cross-Platform:** Funciona em Linux, macOS e Windows.
* **Fully Automated:** Gerencia seu próprio servidor LanguageTool (mas você também pode usar um externo).
* **Blazing Fast:** Caching inteligente garante notificações instantâneas "Ouvir..." e processamento rápido.
* ** Gestão do Estado Dinâmico via Trino:** Motor de configuração de interface
separa as configurações para `speech`, `terminal` e `web` — mude uma sem
que afecta os outros. Inclui um painel em tempo real **Admin Dashboard** (port 8084).
</details>

<details>
<summary> □ Integração pronta para uso</summary>
  
    
## 🔌 Integrações Prontas para Uso

SL5-Aura vem com um vasto ecossistema de mais de **100+ plugins pré-configurados**. Aqui estão alguns destaques:

## # OculiX / SikuliX IDE Controle de Voz
SL5-Aura fornece suporte de voz de primeira classe para o **OculiX** e **SikuliX IDE**. Esta integração permite-lhe "falar" o seu código de automação.

* ** Voz-a-Snippet:** Diga "clique", "esperar" ou "encontrar tudo", e o serviço digita instantaneamente o código Python correto (por exemplo, `click("image.png")`) no IDE.
* ** Window-Aware: ** O plug-in é sensível ao contexto; ele só ativa quando a janela OculiX/SikuliX está focada.
* **Smart English Support:** Otimizado para `en-US` com um foco especial em sotaques não nativos (por exemplo, fonética alemã-inglês), garantindo alta precisão de reconhecimento para a comunidade global.
* **Extensível:** Utiliza o formato fácil de editar `FUZZY_MAP_pre.py`.

> ** Status: ** Reconhecida como um plug-in comunitário pela equipe OculiX (ver [Issue #204](https://github.com/oculix-org/Oculix/issues/204)).

### Controle de Voz do LibreOffice IDE

### 0 A.D. Controle por Voz

---

</details>


<details>
Xhtmltag2XDocumentaçãoXhtmltag3X

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)

## Documentação

Para uma referência técnica completa, incluindo todos os módulos e scripts, por favor visite nossa página oficial de documentação. Ela é gerada automaticamente e está sempre atualizada.

👉 [**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)

## # Spotlights de recurso
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-ptlang.md) — Pesquisa de regras de painel duplo `fzf`, pré-visualizações de contexto ao vivo, execução instantânea de comandos via `Enter`/`Ctrl+R` e integração de editor via `Ctrl+E`. Suportado por uma tecla de atalho global (`Super+S`) e vários ambientes de pesquisa dedicados pré-configurados através de comandos de voz.

## # Construir status

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

Leia isto em outras línguas:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-ptlang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-ptlang.md) | [🇪🇸 Español](../README.i18n/README-eslang-ptlang.md) | [🇫🇷 Français](../README.i18n/README-frlang-ptlang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-ptlang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-ptlang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-ptlang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-ptlang.md) | [🇵🇹 Português](../README.i18n/README-ptlang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-ptlang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-ptlang.md)

---

<details>
<summary>Instalação</summary>

Instalação

Instalação rápida sem moderação (Manjaro/Arch Video)
Assista ao processo completo de configuração de 6 minutos:
* **Download:** ~3 minutos
* ** Setup & First Start:** ~ 3 minutos (incluindo Assistente de Boas-vindas)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


A configuração é um processo em duas etapas:
1. Baixe a versão mais recente ou mestre ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) ou clone este repositório para o seu computador.
2. Execute o script de configuração única para o seu sistema operacional.

Os scripts de configuração lidam com tudo: dependências do sistema, ambiente Python e baixando os modelos e ferramentas necessários (~4GB) diretamente de nossos lançamentos GitHub para a velocidade máxima.


### # Para Linux, macOS e Windows (com exclusão opcional da linguagem)

Para economizar espaço em disco e largura de banda, você pode excluir modelos de linguagem específicos (`de`, `en`) ou todos os modelos opcionais (`all`) durante a configuração. ** Componentes de core (LanguageTool, liver.176) estão sempre incluídos.

Abra um terminal no diretório raiz do projeto e execute o script para o seu sistema:

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

Para as janelas
Execute o script de configuração com privilégios de administrador.

**Instale uma ferramenta para ler e executar, por exemplo, [CopyQ](https://github.com/hluk/CopyQ) ou [AutoHotkey v2](https://www.autohotkey.com/)**. Isto é necessário para o observador de digitação de texto.

A instalação é totalmente automatizada e leva cerca de **8-10 minutos** ao usar 2 modelos em um sistema fresco.

1. Navegue para a pasta `setup`.
2. Clique duas vezes em **`windows11_setup_with_ahk_copyq.bat`**.
* * O script irá pedir automaticamente privilégios de administrador.*
* Ele instala o sistema principal, modelos de linguagem, ** AutoHotkey v2**, e ** CopyQ**.*
3. Assim que a instalação estiver completa, **Aura Dictation** será lançada automaticamente.

> **Nota:** Você não precisa instalar Python ou Git de antemão; o script lida com tudo.

---

Instalação avançada / personalizada
Se preferir não instalar as ferramentas do cliente (AHK/CopyQ) ou deseja poupar espaço em disco excluindo linguagens específicas, pode executar o script principal através da linha de comando:

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
<summary>UsageXHTMLTTAG3X

Utilização

# # # 1. Inicie os Serviços

#### No Linux & macOS
Um único guião trata de tudo. Ele inicia o serviço de ditado principal e o monitor de arquivos automaticamente no fundo.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

No Windows
Iniciar o serviço é um processo manual **dois passos**:

1. **Inicie o Serviço Principal:** Execute `start_aura.bat`. ou comece a partir `.venv` o serviço com `python3`

# # # 2. Configure sua tecla de atalho

Para ativar o ditado, você precisa de uma tecla de atalho global que crie um arquivo específico. Recomendamos altamente a ferramenta multiplataforma [CopyQ](https://github.com/hluk/CopyQ).

Nossa recomendação: CopyQ

Criar um novo comando no CopyQ com um atalho global.

**Comando para Linux/macOS:**
```bash
touch /tmp/sl5_record.trigger
```

**Comando para Windows quando usar [CopyQ](https://github.com/hluk/CopyQ):**
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


**Comando para Windows quando usar [AutoHotkey](https://AutoHotkey.com):**
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


Começa a ditar!
Clique em qualquer campo de texto, pressione sua tecla de atalho, e uma notificação "Ouça..." aparecerá. Fala com clareza, depois pára. O texto corrigido será digitado para você.

</details>

---


<details>
Configuração Avançada (Opcional) XHTMLTLTAG3X

# # Configuração Avançada (Opcional)

Você pode personalizar o comportamento da aplicação criando um arquivo de configurações locais.

1. Navegue para o diretório `config/`.
2. Criar uma cópia do `config/settings_local.py_Example.txt` e renomeá-lo para `config/settings_local.py`.
3. Editar `config/settings_local.py` (ele substitui qualquer configuração do arquivo principal `config/settings.py`).

Este arquivo `config/settings_local.py` é ignorado pelo Git por padrão, então suas alterações pessoais não serão sobrescritas por atualizações.

Estrutura e lógica do plug-in

A modularidade do sistema permite uma extensão robusta através do directório/ plugins.

O motor de processamento adere estritamente a uma ** Cadeia Prioritária Hierárquica**:

1. ** Ordem de carregamento do módulo (alta prioridade): ** Regras carregadas dos pacotes de idiomas principais (de-DE, en-US) têm precedência sobre regras carregadas a partir do diretório plugins/ (que carregam por último alfabeticamente).
    
2. **In-File Order (Micro Priority):** Dentro de qualquer arquivo de mapa (FUZZY MAP pre.py), as regras são processadas estritamente por **line number** (top-to-bottom).
    

Esta arquitetura garante que as regras do sistema principal são protegidas, enquanto as regras específicas do projeto ou do contexto (como aquelas para controles CodeIgniter ou jogo) podem ser facilmente adicionadas como extensões de baixa prioridade através de plug-ins.

</details>

<details>
<summary>Key Scripts para usuários do Windows</summary>






## Scripts Principais para Usuários do Windows

Aqui está uma lista dos scripts mais importantes para configurar, atualizar e executar o aplicativo em um sistema Windows.

Configuração e Atualização

*   `chmod +x update.sh; ./update.sh`
* `setup/setup.bat`: O script principal para a configuração inicial** do ambiente.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

* `update.bat` : Execute isso da pasta do projeto para ** obter o código e dependências mais recentes**.

A executar a aplicação
* `start_aura.bat`: Um script primário para **Iniciar o serviço de ditados**.

## # Programas principais e auxiliares
* `aura_engine.py`: O serviço Python (geralmente iniciado por um dos scripts acima).
* `get_suggestions.py`: Um script auxiliar para funcionalidades específicas.

</details>



# # # □ Principais recursos e compatibilidade do sistema operacional

<details>
<summary>Legend para Compatibilidade com o SO</summary>

Legenda para compatibilidade do OS:  
* (por exemplo, Arch, Ubuntu)  
* (**macOS**  )  
*   
* "Android"** (para recursos específicos para dispositivos móveis)  

---

</details>



### **Motor de discurso-texto (Aura)
Nosso motor primário para reconhecimento de fala offline e processamento de áudio.

    
<details>
<summary>Aura- CoreXHTMLTTAG2X
**Aura- Core/ **  
├─ `aura_engine.py` (principal serviço Python orquestrando Aura)  
├┬ **Live Hot-Reload** (Config & Maps)  
│├ **Secure Private Map Loading (Integrity-First)**  
││ * ** Fluxo de trabalho:** Carrega arquivos ZIP protegidos por senha.   
│├ ** Processamento e Correção de Texto/** Agrupado por Língua (por exemplo `de-DE`, `en-US`, ... )   
│├ 1. `normalize_punctuation.py` (Standardiza a pontuação pós-transcrição)  
│├ 2. **Pre- Correcção inteligente** (`FuzzyMap Pre` - [The Primary Command Layer](../docs/CreatingNewPluginModules.i18n/CreatingNewPluginModules-ptlang.md))  
││ * ** Execução de script dinâmico:** As regras podem ativar scripts Python personalizados (`on_match_exec`) para executar ações avançadas, como chamadas API, arquivo I/O ou gerar respostas dinâmicas.   
││ * ** Execução em cascata:** As regras são processadas sequencialmente e seus efeitos são ** cumulativos **. Regras posteriores se aplicam ao texto modificado por regras anteriores.  
││ * **Critério de Paragem de Prioridade mais Alta:**Se uma regra atingir um **Full Match** (^...$), todo o oleoduto de processamento para esse token para imediatamente. Este mecanismo é fundamental para implementar comandos de voz confiáveis.   
│├ 3. `correct_text_by_languagetool.py` (Integra Linguagem para correção gramatical/estilo)  
│├ **4. Motor Hierárquico RegEx-Regra com Ollama AI Fallback**  
││ * ** Controle determinístico:** Usa o RegEx-Rule-Engine para comando preciso, de alta prioridade e controle de texto.   
│├ **Plugin Vector-Search** (Carregamento preguiçoso): Activa a Busca Semântica conectando incorporações vetoriais locais com a camada de retrocesso Ollama/LLM  
││ * ** Ollama AI (LLM Local) Serve como uma verificação opcional de baixa prioridade para ** respostas criativas, Q&A, e Fuzzy Matching avançado** quando nenhuma regra determinística é cumprida.  
││ * ** Status:** Integração LLM local.
│└ 5. **Intelligent Post-Correction** (`FuzzyMap`)**– Refinamento pós-LT**  
││ * Aplicado após LanguageTool para corrigir saídas específicas de LT. Segue a mesma lógica estrita de prioridade em cascata que a camada Pré-Correção.  
││ * ** Execução de script dinâmico:** Regras podem ativar scripts Python personalizados ([on_match_exec](../docs/advanced-scripting.i18n/advanced-scripting-ptlang.md)) para executar ações avançadas, como chamadas API, arquivo I/O, ou gerar respostas dinâmicas.   
││ * **Fuzzy Fallback:** O **Fuzzy Semelhance Check** (controlado por um limiar, por exemplo, 85%) atua como a camada de correção de erro de menor prioridade. Ele só é executado se toda a regra determinística/cascading anterior não conseguir encontrar uma correspondência (current rule matched é Falso), otimizando o desempenho evitando verificações lentas sempre que possível.   
├┬ **Modelo de Gestão/**   
│├─ `prioritize_model.py` (Otimiza o carregamento/desloading do modelo com base no uso)  
│└─ `setup_initial_model.py` (Configura a configuração do modelo pela primeira vez)  
├─ ** Tempo limite de adaptação do DAV**  
├─ ** Tecla de atalho adaptativa (Iniciar/Parar)**  
├─ **Comutação de linguagem instantânea** (Experimental via pré-carregamento do modelo)  
├─ **Airflow Orchestration** (Automação de fluxo de trabalho baseada em DAG) 🐧 🍏 🪟
│   Requer Docker · UI: `http://localhost:8081`  
├─ **Trino State Engine** (Configuração interface-aware por fala/terminal/web) 🐧 🍏 🪟
└─  Requer Docker · Admin UI: `http://localhost:8084`  

**SystemUtilities/ **   
├┬ **LanguageTool Server Management/**   
│├─ `start_languagetool_server.py` (Inicializa o servidor local da Linguagem)  
│└─ `stop_languagetool_server.py` (Desliga o servidor LanguageTool) 🐧 🍏 
├─ `monitor_mic.sh` (p. ex. para uso com Headset sem teclado de uso e Monitor)  

### **Modelo e Gestão de Pacotes**  
Ferramentas para manuseio robusto de modelos de linguagem de grande porte.  

**ModeloManagement/**  
├─ **Robust Model Downloader** (GitHub Release blocks)  
├─ `split_and_hash.py` (Utilidade para os proprietários de repo para dividir arquivos grandes e gerar somas de verificação)  
└─ `download_all_packages.py` (Ferramenta para usuários finais para baixar, verificar e remontar arquivos multi-partes)  

</details>


<details>
Ajudadores de Desenvolvimento e Implantação XHTMLTTAG2X

### **Auxiliadores de desenvolvimento e implantação**  
Scripts para configuração de ambiente, testes e execução de serviço.   

*Dica: glogg permite que você use expressões regulares para pesquisar eventos interessantes em seus arquivos de log.*   
Por favor, verifique a caixa de seleção ao instalar para associar com arquivos de log.   
https://glogg.bonnefon.org/   
    
*Dica: Depois de definir seus padrões de regex, execute `python3 tools/map_tagger.py` para gerar automaticamente exemplos pesquisáveis para as ferramentas CLI. Veja [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-ptlang.md) para mais detalhes.*

Então talvez um duplo clique
`log/aura_engine.log`
    
**DevHelpers/**  
├┬ ** Gestão Virtual do Ambiente/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macos)  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows)  
├┬ ** Integração de Ditação por Sistema / **  
│├ Integração Vosk-System-Listener  
│├ `scripts/monitor_mic.sh` (monitoramento de microfone específico para Linux)  
│└ `scripts/type_watcher.ahk` (AutoHotkey escuta para o texto reconhecido e digita-lo para fora do sistema-wide)  
└─ **CI/CD Automation/**  
    └─ Fluxos de trabalho do GitHub expandidos (instalação, testes, implantação de documentos)                  , * (corre em ações do GitHub)*   

</details>

<details>
<summary>Características experimentais</summary>
    
### **Avançar / Características Experimentais**  
Características atualmente em desenvolvimento ou em status de esboço.  

** Características experimentais / **   
├─ **ENTER AFTER DICTATION REGEX** Regra de ativação de exemplo "(ExemploAplication ThatNotExist, your personal AI)"  
├┬Plugins  
│Recarregamento de preguiçosos ao vivo** (*)  
(*Alterações para ativação/desativação do Plugin, e suas configurações, são aplicadas na próxima execução de processamento sem reiniciar o serviço.*)  
│ ├ **Git commands** (Controle de voz para enviar comandos git)  
│ ├ **wannweil** (Mapa para Localização Alemanha-Wannweil)  
│ ├ **Poker Plugin (Draft)** (Controlo de voz para aplicações de poker)  
│ └ **0 A.D. Plugin (Draft)** (Controlo de voz para o jogo de 0 A.D.)  
├─ **Saída sonora quando iniciar ou terminar uma sessão** (Descrição pendente)  
├─ **SpaceBREAKX  
└─ **SL5 Aura Android Prototype** (Ainda não totalmente offline)  

---

*(Nota: distribuições específicas do Linux como o Arch (ARL) ou Ubuntu (UBT) são cobertas pelo símbolo geral do Linux. Distinções detalhadas podem ser cobertas em guias de instalação.
</details>

<details>
<summary>Clique para ver o comando usado para gerar esta lista de script</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>A visão gráfica da arquitetura</summary>

### Uma visão gráfica da arquitetura:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>Modelos Usados</summary>

# # Modelos usados:

Recomendação: utilizar modelos de espelho https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (provavelmente mais rápido)

Estes modelos zipados devem ser salvos na pasta `models/`

`mv vosk-model-*.zip models/`


□ Modelo : Tamanho : Taxa de erro do Word / Velocidade Notas
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
* [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) * 1.8G * 5.69 (librispeech test-clean) XHTMLTAG 0X6.05 (télio) <br/>29.78 (callcenter) * Accurate generic US English model * Apache 2.0 *
<br/>24.00 (podcast)<br/>12.82 (cv-test)<br/>12.42 (mls)<br/>33.26 (mtedx)

Esta tabela fornece uma visão geral de diferentes modelos Vosk, incluindo seu tamanho, taxa de erro de palavra ou velocidade, notas e informações de licença.


- **Modelos Vosk:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **Língua:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**Licença da ferramenta de linguagem:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

# # Apoie o projeto
Se você achar esta ferramenta útil, por favor considere comprar-nos um café! O seu apoio ajuda a alimentar melhorias futuras.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

