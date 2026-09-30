> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

# ⬟ SL5 Aura – Sua Voz. Suas Regras.

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> Framework de assistente de voz 100% offline, com foco na privacidade.  
> Defina exatamente o que sua voz faz — a partir de uma única palavra  
> para scripts Python completos. Sem nuvem. Nenhum dado sai da sua máquina.  
> Funciona no terminal, no navegador ou como um serviço em segundo plano — no Linux, macOS e Windows.

| 👵 Iniciante | 🎓 Aprendiz | 🧑‍💻 Desenvolvedor |
|---|---|---|
| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-ptlang.md#the-oma-modus-beginner-shortcut) : basta escrever uma palavra, Aura faz o resto | Aprenda com Koans — um conceito de cada vez | Script completo em Python, plugins, chamadas de API |
| 🗄️ Gerenciamento de Estado | Orquestração Trino + Airflow, fzf, CopyQ, comandos de voz/terminal, UIs de navegador |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **~2,87 J** por teste (39 testes sem LanguageTool em mais de 800 mapas @ 0,07s aquecido / 0,36s frio 🌿 medido com [Eco-CI](https://metrics.green-coding.io/index.html)) · sem computação em nuvem

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **Conjunto completo de testes:** 94 testes com LanguageTool em mais de 800 mapas @ 0,07s aquecido / 0,46s frio · sem computação em nuvem

<details>
<summary>Início Rápido</summary>

## Início Rápido

## # Opção A: Instalador de 1 & Web (Recomendado)

Comando de linha única ou instalador independente para Linux, macOS e Windows:
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-ptlang.md)**

---

## # Opção B: Instalação Manual (Desenvolvedores / Git)

1. Transferir ou clonar este repositório
2. Execute o script de configuração para o seu sistema operacional (veja a pasta `setup/`):
   - Linux (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
   - Linux (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
   - Linux (openSUSE): `bash setup/suse_setup.sh`
   - Linux (NixOS): `nix-shell setup/shell.nix` e `bash setup/nixos_setup.sh`
   == Ver também ==== Ligações externas ==   
   - macOS: `bash setup/macos_setup.sh`
   - Janelas: `setup/windows11_setup_with_ahk_copyq.bat`
3. Iniciar Aura: `./scripts/restart_venv_and_run-server.sh`
4. Pressione a tecla de atalho e fale - **[full guide →](../docs/GettingStarted.i18n/GettingStarted-ptlang.md) *

---

Desinstalação
Para remover os serviços de fundo SL5 Aura, entradas de inicialização automática e ambientes virtuais:
- **Linux / macOS:** `bash setup/uninstall.sh`
- **Windows (PowerShell):** `powershell -File setup/uninstall.ps1`
*(Suas regras personalizadas no `config/maps/` são mantidas seguras por padrão, a menos que você especifique `--purge`).

---


Requisitos do sistema e compatibilidade * *

*   **Windows:** □ Totalmente suportado (usa AutoHotkey/PowerShell).
*   ** macOS:** □ Totalmente suportado (usa AppleScript).
*   **Linux (X11/Xorg):** Totalmente apoiado.
*   **Linux (Wayland): ** Totalmente suportado (testado no KDE Plasma 6 / Wayland).
*   **Linux (CachyOS / lançamento de rolamento baseado em arco):** Totalmente apoiado.
    Requer mimaloc (`sudo pacman -S mimalloc`) devido à compatibilidade glibc 2.43.
*   **Linux (NixOS):** ** Experimental — configuração da comunidade, ainda não testada.
    Se você tentar, por favor abra um problema ou RP com suas descobertas!    
*   **Linux (Manjaro):** Novo : Uma tecla de atalho ampla do sistema abre uma interface fzf-like, orientada pelo teclado para que você possa executar comandos Aura de qualquer lugar no desktop (completamente dissociado da janela ativa). Este lançador orientado por teclas de atalho está atualmente implementado e testado no Linux (Manjaro); Outras distribuições podem funcionar, mas requerem a configuração. Ver em [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-ptlang.md)    


    
SL5 Aura é um assistente de voz completo, **offline** construído em **Vosk** (para Speech-to-Text) e **LanguageTool** (para Grammar/Style), apresentando um opcional **Local LLM (Ollama) Fallback** para respostas criativas e correspondência fuzzy avançada. Transforma sua voz em ações e texto precisos, projetados para personalização final através de um sistema de regras plugáveis e um motor de script dinâmico.
    
Traduções: Este documento também existe no [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Nota: Muitos textos são traduções geradas por máquina da documentação original em inglês e destinam-se apenas a orientação geral. Em caso de discrepâncias ou ambiguidades, a versão inglesa sempre prevalece. Congratulamo-nos com a ajuda da comunidade para melhorar esta tradução!

</details>

<details>
<summary>Demonstração</summary>

## # # Demonstração Terminal

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **Dica: ** Para uma melhor experiência terminal, consulte [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-ptlang.md).

# # # Vídeo Tutorial
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Link alternativo: [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw)) *

</details>

<details>
<summary>Principais funcionalidades</summary>

# # Principais características

*   **Offline & Private:** 100% local. Nenhum dado sai da sua máquina.
*   ** Motor de Programação Dinâmica:** Vai além da substituição de texto. As regras podem executar scripts Python personalizados (`on_match_exec`) para executar ações avançadas como chamar APIs (por exemplo, pesquisar Wikipedia), interagir com arquivos (por exemplo, gerenciar uma lista de tarefas), ou gerar conteúdo dinâmico (por exemplo, uma saudação de e-mail consciente de contexto).
*   ** Regras de Contexto-Aware:** Restrinja regras para aplicações específicas. Usando `only_in_windows`, você pode garantir que uma regra só aciona se um título específico da janela (por exemplo, "Terminal", "Código VS" ou "Browser") estiver ativo. Isso funciona multi-plataforma (Linux, Windows, macOS).
*  ** Motor de Transformação de Alto Controle:** Implementa um pipeline de processamento de configuração altamente personalizável. Prioridade de regra, detecção de comandos e transformações de texto são determinadas puramente pela ordem sequencial das regras nos mapas fuzzy, exigindo ** configuração, não codificação**.
*   ** Uso conservador da RAM:** Gerencia inteligentemente a memória, pré-carregando modelos apenas se houver RAM livre suficiente, garantindo que outros aplicativos (como seus jogos de PC) sempre tenham prioridade.
*   ** Plataforma Cruzada:** Funciona em Linux, macOS e Windows.
*   **Fully Automated:** Gerencia seu próprio servidor LanguageTool (mas você também pode usar um externo).
*   **Blazing Fast:** Caching inteligente garante notificações instantâneas de "Ouvir..." e processamento rápido.
*   **Gestão de Estado dinâmica via Trino:** Motor de configuração de interface
    separa as configurações para `speech`, `terminal` e `web` — mude uma sem
    Afectando os outros. Inclui um painel em tempo real **Admin Dashboard** (port 8084).
</details>

<details>
<summary>Integrações prontas a utilizar</summary>
    
Integrações prontas a utilizar

SL5-Aura vem com um vasto ecossistema de mais de **100+ plugins pré-configurados**. Aqui estão alguns destaques:

OculiX / SikuliX IDE Controle de Voz
SL5-Aura fornece suporte de voz de primeira classe para o **OculiX** e **SikuliX IDE**. Esta integração permite-lhe "falar" o seu código de automação.

*   ** Voz- a- Snippet: ** Diga "clique", "esperar" ou "encontrar tudo", e o serviço digita instantaneamente o código Python correto (por exemplo, `click("image.png")`) no IDE.
*   ** Window- Aware: ** O plug-in é sensível ao contexto; ele só ativa quando a janela OculiX/SikuliX está focada.
*   **Smart English Support:** Otimizado para `en-US` com um foco especial em sotaques não nativos (por exemplo, fonética alemã-inglês), garantindo alta precisão de reconhecimento para a comunidade global.
*   **Extensível:** Utiliza o formato fácil de editar `FUZZY_MAP_pre.py`.

> ** Status: ** Reconhecida como um plug-in comunitário pela equipe OculiX (ver [Issue #204](https://github.com/oculix-org/Oculix/issues/204)).

LibreOffice IDE Controle de Voz

0 A.D. Controle de Voz

---

</details>


<details>
<summary>Documentação</summary>

## Documentação

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=pt)

Para uma referência técnica completa, incluindo todos os módulos e scripts, por favor visite nossa página oficial de documentação. Ela é gerada automaticamente e está sempre atualizada.

[🇬🇧 English](https://sl5net.github.io/SL5-aura-service/README.html) | [🇸🇦 العربية](https://sl5net.github.io/SL5-aura-service/README.i18n/README-arlang.html) | [🇩🇪 Deutsch](https://sl5net.github.io/SL5-aura-service/README.i18n/README-delang.html) | [🇪🇸 Español](https://sl5net.github.io/SL5-aura-service/README.i18n/README-eslang.html) | [🇫🇷 Français](https://sl5net.github.io/SL5-aura-service/README.i18n/README-frlang.html) | [🇮🇳 हिन्दी](https://sl5net.github.io/SL5-aura-service/README.i18n/README-hilang.html) | [🇯🇵 日本語](https://sl5net.github.io/SL5-aura-service/README.i18n/README-jalang.html) | [🇰🇷 한국어](https://sl5net.github.io/SL5-aura-service/README.i18n/README-kolang.html) | [🇵🇱 Polski](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pllang.html) | [🇵🇹 Português](https://sl5net.github.io/SL5-aura-service/README.i18n/README-ptlang.html) | [🇧🇷 Português Brasil](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pt-BRlang.html) | [🇨🇳 简体中文](https://sl5net.github.io/SL5-aura-service/README.i18n/README-zh-CNlang.html)

## # Spotlights de recurso
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-ptlang.md) — Pesquisa de regras de painel duplo `fzf`, pré-visualizações de contexto ao vivo, execução instantânea de comandos via `Enter`/`Ctrl+R` e integração de editor via `Ctrl+E`. Suportado por uma tecla de atalho global (`Super+S`) e vários ambientes de pesquisa dedicados pré-configurados através de comandos de voz.

### Status da Construção

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

👉 **Leia isto em outros idiomas:**

[🇬🇧 English](https://sl5net.github.io/SL5-aura-service/README.html) | [🇸🇦 العربية](https://sl5net.github.io/SL5-aura-service/README.i18n/README-arlang.html) | [🇩🇪 Deutsch](https://sl5net.github.io/SL5-aura-service/README.i18n/README-delang.html) | [🇪🇸 Español](https://sl5net.github.io/SL5-aura-service/README.i18n/README-eslang.html) | [🇫🇷 Français](https://sl5net.github.io/SL5-aura-service/README.i18n/README-frlang.html) | [🇮🇳 हिन्दी](https://sl5net.github.io/SL5-aura-service/README.i18n/README-hilang.html) | [🇯🇵 日本語](https://sl5net.github.io/SL5-aura-service/README.i18n/README-jalang.html) | [🇰🇷 한국어](https://sl5net.github.io/SL5-aura-service/README.i18n/README-kolang.html) | [🇵🇱 Polski](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pllang.html) | [🇵🇹 Português](https://sl5net.github.io/SL5-aura-service/README.i18n/README-ptlang.html) | [🇧🇷 Português Brasil](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pt-BRlang.html) | [🇨🇳 简体中文](https://sl5net.github.io/SL5-aura-service/README.i18n/README-zh-CNlang.html)

---

<details>
<summary>Instalação</summary>

Instalação

Instalação rápida sem moderação (Manjaro/Arch Video)
Assista ao processo completo de configuração de 6 minutos:
* ** Baixar: ~3 minutos
* ** Setup & Primeiro Início:** ~ 3 minutos (incluindo Assistente de Boas-vindas)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


A configuração é um processo em duas etapas:
1.  Baixe o mais recente Release ou master ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) ou clone este repositório para o seu computador.
2.  Execute o script de configuração única para o seu sistema operacional.

Os scripts de configuração lidam com tudo: dependências do sistema, ambiente Python e baixando os modelos e ferramentas necessários (~4GB) diretamente de nossos lançamentos GitHub para a velocidade máxima.


#### Para Linux, macOS e Windows (com exclusão de idioma opcional)

Para economizar espaço em disco e largura de banda, você pode excluir modelos de linguagem específicos (`de`, `en`) ou todos os modelos opcionais (`all`) durante a configuração. **Componentes principais (LanguageTool, lid.176) estão sempre incluídos.**

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
   * *O script irá pedir automaticamente privilégios de administrador. *
   * * Instala o Sistema Core, Modelos de Linguagem, **AutoHotkey v2**, e **CopyQ**.
3. Uma vez concluída a instalação, **Aura Dictation** será lançada automaticamente.

> **Nota:** Você não precisa instalar Python ou Git de antemão; O guião trata de tudo.

---

#### Instalação Avançada / Personalizada
Se você preferir não instalar as ferramentas do cliente (AHK/CopyQ) ou quiser economizar espaço em disco excluindo idiomas específicos, você pode executar o script principal via linha de comando:

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
<summary>Uso</summary>

## Uso

### 1. Inicie os Serviços

#### No Linux e macOS
Um único script cuida de tudo. Ele inicia o serviço principal de ditado e o observador de arquivos automaticamente em segundo plano.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

#### No Windows
Iniciar o serviço é um **processo manual em duas etapas**:

1.  **Inicie o Serviço Principal:** Execute `start_aura.bat`. ou inicie a partir de `.venv` o serviço com `python3`

### 2. Configure sua tecla de atalho

Para ativar a ditadura, você precisa de um atalho global que crie um arquivo específico. Recomendamos fortemente a ferramenta multiplataforma [CopyQ](https://github.com/hluk/CopyQ).

#### Nossa Recomendação: CopyQ

Crie um novo comando no CopyQ com um atalho global.

**Comando para Linux/macOS:**
```bash
touch /tmp/sl5_record.trigger
```

**Comando para Windows ao usar [CopyQ](https://github.com/hluk/CopyQ):**
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


**Comando para Windows ao usar [AutoHotkey](https://AutoHotkey.com):**
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


### 3. Comece a ditar!
Clique em qualquer campo de texto, pressione sua tecla de atalho e uma notificação "Ouvindo..." aparecerá. Fale claramente, então faça uma pausa. O texto corrigido será digitado para você.

</details>

---


<details>
<summary>Configuração Avançada (Opcional)</summary>

# # Configuração Avançada (Opcional)

Você pode personalizar o comportamento da aplicação criando um arquivo de configurações locais.

1.  Navegue para o diretório `config/`.
2.  Crie uma cópia do `config/settings_local.py_Example.txt` e mude o nome para `config/settings_local.py`.
3.  Editar `config/settings_local.py` (ele substitui qualquer configuração do arquivo principal `config/settings.py`).

Este arquivo `config/settings_local.py` é ignorado pelo Git por padrão, então suas alterações pessoais não serão sobrescritas por atualizações.

Plug-in Estrutura e Lógica

A modularidade do sistema permite uma extensão robusta através dos plugins/diretório.

O motor de processamento adere estritamente a uma ** Cadeia Prioritária Hierárquica ***:

1. ** Ordem de carregamento do módulo (alta prioridade): ** As regras carregadas dos pacotes de idiomas principais (de-DE, en-US) têm precedência sobre as regras carregadas dos plugins/diretório (que carregam por último alfabeticamente).
    
2. **In-File Order (Micro Priority):** Dentro de qualquer arquivo de mapa (FUZZY MAP pre.py), as regras são processadas estritamente por **line number** (top-to-bottom).
    

Esta arquitetura garante que as regras do sistema principal são protegidas, enquanto as regras específicas do projeto ou do contexto (como aquelas para controles CodeIgniter ou jogo) podem ser facilmente adicionadas como extensões de baixa prioridade através de plug-ins.

</details>

<details>
<summary>Scripts chave para usuários do Windows</summary>






## Scripts Principais para Usuários do Windows

Aqui está uma lista dos scripts mais importantes para configurar, atualizar e executar o aplicativo em um sistema Windows.

### Configuração & Atualização

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat`: O script principal para a **configuração inicial única** do ambiente.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : Execute isso a partir da pasta do projeto para **obter o código e as dependências mais recentes**.

### Executando o Aplicativo
*   `start_aura.bat`: Um script principal para **iniciar o serviço de ditado**.

### Scripts Principais e Auxiliares
*   `aura_engine.py`: O serviço principal do Python (geralmente iniciado por um dos scripts acima).
*   `get_suggestions.py`: Um script auxiliar para funcionalidades específicas.

</details>



## 🚀 Principais Recursos e Compatibilidade com SO

<details>
<summary>Legenda para Compatibilidade com OS</summary>

Legenda para compatibilidade de SO:  
*   🐧 **Linux** (por exemplo, Arch, Ubuntu)  
    *   🍏 **macOS**  
*   🪟 **Janelas**  
*   📱 **Android** (para recursos específicos de dispositivos móveis)  

---

</details>



# # ** Motor de Fala-Texto (Aura) #
    Nosso motor primário para reconhecimento de fala offline e processamento de áudio.

    
<details>
<summary>Núcleo Aura</summary>

** Aura- Core/ ** 🐧 🍏 🪟  
├─ `aura_engine.py` (serviço Python principal que orquestra Aura) 🐧 🍏 🪟  
├┬ **Live Hot-Reload** (Config & Maps) 🐧 🍏 🪟  
│├ **Secure Private Map Loading (Integrity-First)** 🔒  🐧 🍏 🪟  
││ * ** Fluxo de trabalho:** Carrega arquivos ZIP protegidos por senha.   
│├ ** Processamento e Correção de Texto/** Agrupado por Língua (por exemplo, `de-DE`, `en-US`, ... )   
│├ 1. `normalize_punctuation.py` (Standardiza pontuação pós-transcrição) 🐧 🍏 🪟  
│├ 2. **Precorreção inteligente** (`FuzzyMap Pre` - [The Primary Command Layer](../docs/CreatingNewPluginModules.i18n/CreatingNewPluginModules-ptlang.md)) 🐧 🍏 🪟  
││ * ** Execução de script dinâmico: Regras podem ativar scripts Python personalizados (`on_match_exec`) para executar ações avançadas como chamadas de API, arquivos de I/O ou gerar respostas dinâmicas.  
││ * ** Execução em cascata:** As regras são processadas sequencialmente e seus efeitos são ** cumulativos **. Regras posteriores aplicam-se ao texto modificado por regras anteriores.  
││ * **Critério de Paragem de Prioridade mais Alta:**Se uma regra atingir um **Full Match** (^...$), todo o oleoduto de processamento para esse token para imediatamente. Este mecanismo é fundamental para implementar comandos de voz confiáveis.  
│├ 3. `correct_text_by_languagetool.py` (Integra Linguagem para correção gramatical/estilo) 🐧 🍏 🪟  
│├ **4. Motor Hierárquico RegEx regra com Ollama AI Fallback * 🐧 🍏 🪟  
││ * ** Controle determinístico:** Usa o RegEx Rule Engine para comando preciso, de alta prioridade e controle de texto.  
│├ *Plugin Vector-Search** (Carregamento preguiçoso): Activa a Busca Semântica conectando incorporações Vector locais com a camada de retorno Ollama/LLM 🐧  
││ * ** Ollama AI (LLM Local) Serve como uma verificação opcional, de baixa prioridade para ** respostas criativas, Q&A, e Fuzzy Matching avançado** quando nenhuma regra determinística é cumprida.  
││ * ** Status:** Integração LLM local.
│└ 5. ** Pós-correcção inteligente** (`FuzzyMap`)**– Refinamento pós-LT * 🐧 🍏 🪟  
││ * Aplicado após LinguagemTool para corrigir saídas específicas de LT. Segue a mesma lógica de prioridade em cascata estrita que a camada de pré-correção.  
││ * * Execução de script dinâmico: Regras podem ativar scripts Python personalizados ([on_match_exec](../docs/advanced-scripting.i18n/advanced-scripting-ptlang.md)) para executar ações avançadas, como chamadas de API, E/S de arquivo ou gerar respostas dinâmicas.  
││ * ** Fuzzy Fallback:** O **Fuzzy Semelhance Check** (controlado por um limiar, por exemplo, 85%) atua como a camada de correção de erro de menor prioridade. Ele só é executado se toda a regra determinística/em cascata anterior falhar em encontrar uma correspondência (a regra atual é falsa), otimizando o desempenho evitando verificações lentas e fuzzy sempre que possível.  
├┬ **Model Management/ **   
│├─ `prioritize_model.py` (Otimiza carregamento/descarregamento do modelo baseado no uso) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (Configura a configuração do modelo pela primeira vez) 🐧 🍏 🪟  
├─ ** VAD adaptado Tempo limite * 🐧 🍏 🪟  
├─ ** Tecla de atalho adaptativa (Iniciar/Parar) 🐧 🍏 🪟  
├─ ** Interruptor de linguagem instantânea** (Experimental via pré-carregamento do modelo) 🐧 🍏         
├─ **Airflow Orchestration** (Automação de fluxo de trabalho baseada em DAG) 🐧 🍏 🪟
│   Requer Docker · UI: `http://localhost:8081` 🐧 🍏 🪟  
├─ **Trino State Engine** (configuração de interface por fala/terminal/web) 🐧 🍏 🪟
└─  Requer Docker · Admin UI: `http://localhost:8084` 🐧 🍏 🪟  

**SystemUtilities/**   
├┬ **LanguageTool Server Management/**   
│├─ `start_languagetool_server.py` (Inicializa o servidor local da Linguagem) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py` (Desliga o servidor LanguageTool) 🐧 🍏 
├─ `monitor_mic.sh` (por exemplo, para uso com fone de ouvido sem teclado de uso e monitor) 🐧 🍏 🪟  

### **Gerenciamento de Modelos e Pacotes**  
    Ferramentas para o manuseio robusto de grandes modelos de linguagem.  

**GerenciamentoDeModelos/** 🐧 🍏 🪟  
├─ **Downloadador de Modelos Robusto** (pedaços de lançamento do GitHub) 🐧 🍏 🪟  
├─ `split_and_hash.py` (Utilitário para proprietários de repositórios dividir arquivos grandes e gerar somas de verificação) 🐧 🍏 🪟  
└─ `download_all_packages.py` (Ferramenta para usuários finais baixarem, verificarem e remontarem arquivos multipartes) 🐧 🍏 🪟  

</details>


<details>
<summary>Helpers de Desenvolvimento e Implantação</summary>

### **Auxiliadores de desenvolvimento e implantação#  
    Scripts para configuração de ambiente, testes e execução de serviço.  

*Dica: glogg permite que você use expressões regulares para procurar eventos interessantes em seus arquivos de log. *     
Por favor, verifique a caixa de seleção ao instalar para associar com arquivos de log.    
https://glogg.bonnefon.org/     
    
Dica: Depois de definir seus padrões de regex, execute `python3 tools/map_tagger.py` para gerar automaticamente exemplos pesquisáveis para as ferramentas CLI. Consulte [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-ptlang.md) para detalhes. *

Então talvez um duplo clique
`log/aura_engine.log`
    
**DevHelpers/**  
├┬ ** Gestão Virtual do Ambiente/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ ** Integração de Ditação por Sistema/*  
│├ Integração com o Ouvinte do Sistema Vosk 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (monitoramento de microfone específico para Linux) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey escuta para texto reconhecido e digita-lo em todo o sistema) 🪟  
└─ **CI/CD Automation/**  
    └─ Fluxos de trabalho expandidos do GitHub (instalação, teste, implantação de documentos)  

</details>

<details>
<summary>Características experimentais</summary>
    
# # ** A chegar / Características experimentais *  
    Características atualmente em desenvolvimento ou em status de esboço.  

** Características experimentais / **  
├─ **ENTER APÓS DICTAÇÃO REGEX** Regra de ativação de exemplo "(ExemploAplication ThatNotExist'Pi, your personal AI)" 🐧  
├┬Plug-ins  
│Recarregamento de Preguiçoso ao Vivo** (*) 🐧 🍏 🪟  
(*Alterações para ativação/desativação do Plugin, e suas configurações, são aplicadas na próxima execução de processamento sem reiniciar o serviço.*)  
│ ├ **Git commands* (Controle de voz para enviar comandos git) 🐧 🍏 🪟  
│ ├ **wannweil** (Mapa para a localização Alemanha-Wannweil) 🐧 🍏 🪟  
│ ├ **Poker Plugin (Draft)** (Controlo de voz para aplicações de poker) 🐧 🍏 🪟  
│ └ **0 A.D. Plugin (Draft)** (Controlo de voz para 0 A.D. jogo) 🐧   
├─ ** Saída do Som quando iniciar ou terminar uma sessão** (Descrição pendente) 🐧   
├─ ** Saída de fala para deficientes visuais** (Descrição pendente) 🐧 🍏 🪟  
└─ *SL5 Aura Android Prototype** (Ainda não totalmente offline) 📱  

---

*(Nota: As distribuições específicas do Linux como Arch (ARL) ou Ubuntu (UBT) são cobertas pelo símbolo geral do Linux. Distinções detalhadas podem ser cobertas em guias de instalação. *
</details>

<details>
<summary>Carregue para ver o comando usado para gerar esta lista de programas</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>Uma visão gráfica da arquitetura</summary>

### Uma visão geral gráfica da arquitetura:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>Modelos usados</summary>

## Modelos Usados:

Recomendação: use modelos do Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (provavelmente mais rápido)

Esses modelos compactados devem ser salvos na pasta `models/`

`mv vosk-model-*.zip models/`


□ Modelo : Tamanho : Taxa de erro do Word / Velocidade Notas
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
* [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) * 1.8G * 5.69 (librispeech test-clean) XHTMLTAG 0X6.05 (télio) <br/>29.78 (callcenter) * Accurate generic US English model * Apache 2.0 *
<br/>24.00 (podcast)<br/>12.82 (cv-test)<br/>12.42 (mls)<br/>33.26 (mtedx)

Esta tabela fornece uma visão geral dos diferentes modelos Vosk, incluindo seu tamanho, taxa de erro de palavras ou velocidade, observações e informações de licença.


- **Modelos Vosk:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **LanguageTool:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**Licença do LanguageTool:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

## Apoie o Projeto
Se você achar esta ferramenta útil, por favor, considere nos comprar um café! Seu apoio ajuda a impulsionar futuras melhorias.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

