# Diretório inicial e tratamento de caminho entre plataformas

O Aura foi projetado para ser executado em vários sistemas operacionais. Para garantir que os comandos de navegação do sistema de arquivos funcionem independentemente de você estar executando Linux, macOS ou Windows, as strings de caminho são analisadas dinamicamente antes de serem registradas nos mapas difusos ativos.

---

## Lógica de normalização de caminho (`FUZZY_MAP_pre.py`)

A lógica de mapeamento de caminho dinâmico depende das seguintes práticas padrão:

### 1. Redução de til (POSIX)
Em sistemas compatíveis com POSIX (Linux e macOS), os caminhos absolutos que correspondem ao diretório inicial do usuário (por exemplo, `/home/username/`) são convertidos em caminhos relativos `~` na inicialização. Isso mantém o comprimento das strings mais curto e torna as regras geradas portáveis entre diferentes usuários no mesmo sistema operacional:

```python
# Replaces '/home/username/projects' with '~/projects'
if sys.platform != 'win32' and project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_FOR_MAP = project_root_str_full.replace(home_dir_str, '~', 1)
```

### 2. Preservação absoluta do caminho (Windows)
O Windows não avalia de forma confiável o caractere `~` no prompt de comando padrão (`cmd.exe`) ou em ambientes PowerShell. Portanto, quando o plugin detecta um ambiente Windows (`sys.platform == 'win32'`), ele preserva o caminho absoluto totalmente qualificado (por exemplo, `C:\Users\username\...`) para garantir que a execução do comando não falhe.

### 3. Normalização de barra (`as_posix()`)
Aura usa barras no estilo POSIX (`/`) internamente para mapas de configuração. O script normaliza todos os separadores de caminho dependentes do sistema operacional utilizando o método `pathlib.Path.as_posix()` do Python, que limpa automaticamente as barras invertidas (`\`) em ambientes Windows.