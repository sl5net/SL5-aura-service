# Introdução ao SL5 Aura

> **Pré-requisitos:** Você concluiu o script de configuração e configurou sua tecla de atalho.
> Caso contrário, consulte o [Installation section in README.md](../../README.i18n/README-pt-BRlang.md#installation).

---

## Etapa 1: seu primeiro ditado

1. Inicie o Aura (se ainda não estiver em execução):
   ```bash
   ./scripts/restart_venv_and_run-server.sh
   ```
Aguarde o som de inicialização – isso significa que o Aura está pronto.

2. Clique em qualquer campo de texto (editor, navegador, terminal).
3. Pressione a tecla de atalho, diga **"Hello World"** e pressione a tecla de atalho novamente.
4. Observe o texto aparecer.

> **Nada aconteceu?** Verifique se há erros em `log/aura_engine.log`.
> Correção comum para CachyOS/Arch: `sudo pacman -S mimalloc`

---

## Etapa 2: Escreva sua primeira regra

A maneira mais rápida de adicionar uma regra pessoal:

1. Abra `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. Adicione uma regra dentro de `FUZZY_MAP_pre = [...]`:
   ```python
   ('Hello World', r'hello world', 0, {'flags': re.IGNORECASE})
   #  ^ output        ^ pattern        ^ threshold (ignored for regex)
   ```
3. **Salvar** — Aura recarrega automaticamente. Não é necessário reiniciar.
4. Dite `hello world` e observe-o se tornar `Hello World`.

> Consulte `docs/FuzzyMapRuleGuide.md` para obter a referência completa da regra.

### The Oma-Modus (atalho para iniciantes)

Ainda não conhece regex? Sem problemas.

1. Abra qualquer `FUZZY_MAP_pre.py` vazio na sandbox
2. Escreva apenas uma palavra simples em sua própria linha (sem aspas, sem tupla):
   ```
   raspberry
   ```
3. Salvar — o sistema Auto-Fix detecta a palavra simples e automaticamente
converte-o em uma entrada de regra válida.
4. Você pode então editar o texto de substituição manualmente.

Isso é chamado de **Oma-Modus** — projetado para usuários que desejam resultados sem
aprendendo regex primeiro.

---

## Etapa 3: Aprenda com Koans

Koans são pequenos exercícios em que cada um ensina um conceito.
Eles vivem em `configmaps/koans deutsch/` e `configmaps/koans english/`.

Comece aqui:

| Pasta | O que você aprende |
|---|---|
| `00_koan_oma-modus` | Auto-Fix, primeira regra sem regex |
| `01_koan_erste_schritte` | Sua primeira regra, noções básicas de pipeline |
| `02_koan_listen` | Trabalhando com listas |
| `03_koan_schwierige_namen` | Correspondência difusa para nomes difíceis de reconhecer |
| `04_koan_kleine_helfer` | Atalhos úteis |

Cada pasta koan contém um `FUZZY_MAP_pre.py` com exemplos comentados.
Remova o comentário de uma regra, salve, dite a frase-gatilho - pronto.

---

## Etapa 4: Vá além

| O que | Onde |
|---|---|
| Referência completa da regra | `docs/FuzzyMapRuleGuide.md` |
| Crie seu próprio plugin | `docs/CreatingNewPluginModules.md` |
| Execute scripts Python a partir de regras | `docs/advanced-scripting.md` |
| DEV_MODE + configuração do filtro de log | `docs/Developer_Guide/dev_mode_setup.md` |
| Regras sensíveis ao contexto (`only_in_windows`) | `docs/FuzzyMapRuleGuide.md` |