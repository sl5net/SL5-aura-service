# Guia do desenvolvedor: Gerando o gráfico de chamada de serviço

Este documento descreve o método robusto e seguro para gerar um gráfico de chamada visual do `aura_engine.py` de longa duração. Usamos o profiler `yappi` (para suporte multi-threading) e `gprof2dot` para visualização.

### Pré-requisitos

Certifique-se de ter as ferramentas necessárias instaladas globalmente ou em seu ambiente virtual:

```bash
# Required Python libraries for profiling
pip install yappi gprof2dot

# Required system library for visualization
# Linux: sudo apt install graphviz 
```

### Etapa 1: Modificando o serviço para criação de perfil

O script `aura_engine.py` deve ser modificado para iniciar manualmente o criador de perfil `yappi` e salvar normalmente os dados de perfil após a interrupção (`Ctrl+C`).

**Principais mudanças em `aura_engine.py`:**

1. **Importações e manipulador de sinais:** Importe `yappi` e defina a função `generate_graph_on_interrupt` (conforme implementado anteriormente) para chamar `yappi.stop()` e `stats.save(...)`.
2. **Iniciar/Parar:** Adicione `yappi.start()` e `signal.signal(signal.SIGINT, ...)` dentro do bloco `if __name__ == "__main__":` para encerrar a execução de `main(...)`.

### Etapa 2: Executando o serviço e coletando dados

Execute o script modificado diretamente e permita que ele processe os dados por um tempo suficiente (por exemplo, 10 a 20 segundos) para garantir que todas as funções principais, incluindo as encadeadas (como correção do LanguageTool), sejam chamadas.

```bash
# Execute the service directly (do NOT use the pycallgraph wrapper)
python3 aura_engine.py
```

Pressione **Ctrl+C** uma vez para acionar o manipulador de sinal. Isso interromperá o criador de perfil e salvará os dados brutos em:

`\mathbf{yappi\_profile\_data.prof`

### Etapa 3: Gerando e Filtrando o Gráfico Visual

Usamos `gprof2dot` para converter os dados brutos `pstats` para o formato SVG. Como opções de filtragem avançada como `--include` e `--threshold` podem não ser suportadas por nosso ambiente específico, usamos o filtro básico **`--strip`** para limpar as informações do caminho e reduzir a desordem interna do sistema.

**Execute o comando de visualização:**

```bash
python3 -m gprof2dot -f pstats yappi_profile_data.prof --strip | dot -Tsvg -o yappi_call_graph_stripped.svg
```

### Etapa 4: Documentação (corte manual)

O arquivo `yappi_call_graph_stripped.svg` (ou `.png`) resultante será grande, mas contém com precisão o fluxo de execução completo, incluindo todos os threads.

Para fins de documentação, **corte manualmente a imagem** para focar na lógica central (os 10-20 nós principais e suas conexões) para criar um Call Graph focado e legível para a documentação do repositório.

### Arquivamento

O arquivo de configuração modificado e a visualização final do Call Graph devem ser arquivados no diretório de origem da documentação:

| Artefato | Localização |
| :--- | :--- |
| **Arquivo de serviço modificado** | `doc_sources/profiling/aura_engine_profiling_base.py` |
| **Imagem recortada final** | `doc_sources/profiling/core_logic_call_graph.svg` |
| **Dados brutos de perfil** | *(Opcional: Deve ser excluído da documentação final do repositório)* |


![yappi_call_graph](../yappi_call_graph_stripped.svg_20251024_010459.png "yappi_call_graph_stripped.svg_20251024_010459.png")