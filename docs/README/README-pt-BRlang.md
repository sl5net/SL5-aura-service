# Voz offline em todo o sistema para comandos ou texto, sistema conectável

# Serviço SL5 Aura - Recursos e compatibilidade de sistema operacional

Bem-vindo ao Serviço SL5 Aura! Este documento fornece uma visão geral rápida dos nossos principais recursos e da compatibilidade do sistema operacional.

Aura não é apenas uma transcritora; é um poderoso mecanismo de processamento off-line que transforma sua voz em ações e textos precisos.

É um assistente offline completo baseado em Vosk e LanguageTool, projetado para personalização definitiva por meio de um sistema de regras conectável e um mecanismo de script dinâmico.
  
  
Traduções: Este documento também existe em [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/docs).

Nota: Muitos textos são traduções geradas automaticamente da documentação original em inglês e destinam-se apenas a orientação geral. Em caso de discrepâncias ou ambiguidades, prevalece sempre a versão em inglês. Agradecemos a ajuda da comunidade para melhorar esta tradução!


[![SL5 Aura (v0.7.0.2): A Deep Dive Under the Hood – Live Coding & Core Concepts](https://img.youtube.com/vi/tEijy8WRFCI/maxresdefault.jpg)](https://www.youtube.com/watch?v=tEijy8WRFCI)
( https://skipvids.com/?v=tEijy8WRFCI )

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

[🇬🇧 English](README.md) | [🇸🇦 العربية](docs/README/README-arlang.md) | [🇩🇪 Deutsch](docs/README/README-delang.md) | [🇪🇸 Español](docs/README/README-eslang.md) | [🇫🇷 Français](docs/README/README-frlang.md) | [🇮🇳 हिन्दी](docs/README/README-hilang.md) | [🇯🇵 日本語](docs/README/README-jalang.md) | [🇰🇷 한국어](docs/README/README-kolang.md) | [🇵🇱 Polski](docs/README/README-pllang.md) | [🇵🇹 Português](docs/README/README-ptlang.md) | [🇧🇷 Português Brasil](docs/README/README-pt-BRlang.md) | [🇨🇳 简体中文](docs/README/README-zh-CNlang.md)

---

## Instalação

A configuração é um processo de duas etapas:
1. Clone este repositório em seu computador.
2. Execute o script de configuração único para seu sistema operacional.

Os scripts de configuração cuidam de tudo: dependências do sistema, ambiente Python e download dos modelos e ferramentas necessários (~ 4 GB) diretamente de nossas versões do GitHub para velocidade máxima.

#### Para Linux e macOS e Windows
Abra um terminal no diretório raiz do projeto e execute o script para o seu sistema:
```bash
# For Ubuntu/Debian, Manjaro/Arch, macOs  or other derivatives

bash setup/{your-os}_setup.sh

# For Windows in Admin-Powershell

setup/windows11_setup.ps1
```

#### Para Windows
Execute o script de configuração com privilégios de administrador **"Executar com PowerShell"**.

**Instale uma ferramenta para leitura e execução, por exemplo. [CopyQ](https://github.com/hluk/CopyQ) ou [AutoHotkey v2](https://www.autohotkey.com/)**. Isso é necessário para o observador de digitação de texto.

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
```bash
touch /tmp/sl5_record.trigger
```

**Comando para Windows ao usar [CopyQ](https://github.com/hluk/CopyQ):**
__CODE_BLOCO_3__


**Comando para Windows ao usar [AutoHotkey](https://AutoHotkey.com):**
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


### 3. Comece a ditar!
Clique em qualquer campo de texto, pressione a tecla de atalho e uma notificação "Ouvindo..." aparecerá. Fale claramente e depois faça uma pausa. O texto corrigido será digitado para você.

---


## Configuração avançada (opcional)

Você pode personalizar o comportamento do aplicativo criando um arquivo de configurações locais.

1. Navegue até o diretório `config/`.
2. Crie uma cópia de `settings_local.py_Example.txt` e renomeie-a para `settings_local.py`.
3. Edite `settings_local.py` para substituir qualquer configuração do arquivo principal `config/settings.py`.

Este arquivo `settings_local.py` é (talvez) ignorado pelo Git, então suas alterações pessoais (talvez) não serão substituídas por atualizações.

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
│├ **Processamento e correção de texto/** Agrupado por idioma (por exemplo, `de-DE`, `en-US`, ...)   
│├ 1. `normalize_punctuation.py` (padroniza a pontuação pós-transcrição) 🐧 🍏 🪟  
│├ 2. **Pré-correção inteligente** (`FuzzyMap Pre` - [The Primary Command Layer](../CreatingNewPluginModules-pt-BRlang.md)) 🐧 🍏 🪟  
││ * **Execução dinâmica de script:** As regras podem acionar scripts Python personalizados (on_match_exec) para executar ações avançadas como chamadas de API, E/S de arquivo ou gerar respostas dinâmicas.  
││ * **Execução em Cascata:** As regras são processadas sequencialmente e seus efeitos são **cumulativos**. Regras posteriores se aplicam ao texto modificado por regras anteriores.  
││ * **Critério de parada de prioridade mais alta:** Se uma regra atingir uma **Correspondência completa** (^...$), todo o pipeline de processamento desse token será interrompido imediatamente. Este mecanismo é fundamental para implementar comandos de voz confiáveis.  
│├ 3. `correct_text_by_languagetool.py` (Integra o LanguageTool para correção de gramática/estilo) 🐧 🍏 🪟  
│└ 4. **Pós-Correção Inteligente** (`FuzzyMap`)**– Refinamento Pós-LT** 🐧 🍏 🪟  
││ * Aplicado após o LanguageTool para corrigir saídas específicas do LT. Segue a mesma lógica estrita de prioridade em cascata da camada de pré-correção.  
││ * **Execução dinâmica de script:** As regras podem acionar scripts Python personalizados ([on_match_exec](../advanced-scripting-pt-BRlang.md)) para executar ações avançadas, como chamadas de API, E/S de arquivo ou gerar respostas dinâmicas.  
││ * **Fuzzy Fallback:** A **Verificação de similaridade difusa** (controlada por um limite, por exemplo, 85%) atua como a camada de correção de erros de prioridade mais baixa. Ele só será executado se toda a execução anterior da regra determinística/em cascata não conseguir encontrar uma correspondência (current_rule_matched é False), otimizando o desempenho evitando verificações difusas lentas sempre que possível.  
├┬ **Gerenciamento de modelo/**   
│├─ `prioritize_model.py` (otimiza o carregamento/descarregamento do modelo com base no uso) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (configura a configuração inicial do modelo) 🐧 🍏 🪟  
├─ **Tempo limite do VAD adaptável** 🐧 🍏 🪟  
├─ **Tecla de atalho adaptativa (Iniciar/Parar)** 🐧 🍏 🪟  
└─ **Troca instantânea de idioma** (Experimental via pré-carregamento de modelo) 🐧 🍏   

**Utilitários do Sistema/**   
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
├─ **Saída de som ao iniciar ou encerrar uma sessão** (descrição pendente) 🐧   
├─ **Saída de fala para deficientes visuais** (Descrição pendente) 🐧 🍏 🪟  
└─ **Protótipo SL5 Aura Android** (Ainda não totalmente offline) 📱  

---

*(Nota: Distribuições específicas do Linux como Arch (ARL) ou Ubuntu (UBT) são cobertas pelo símbolo geral do Linux 🐧. Distinções detalhadas podem ser abordadas nos guias de instalação.)*









<detalhes>
<summary>Clique para ver o comando usado para gerar esta lista de scripts</summary>

__CODE_BLOCO_5__
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