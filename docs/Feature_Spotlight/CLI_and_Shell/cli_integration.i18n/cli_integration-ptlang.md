# Recurso em destaque: integração de interface de linha de comando (CLI)

**Dedicado ao meu amigo muito importante, Lub.**

A nova interface de linha de comando (CLI) baseada em FastAPI fornece uma maneira limpa e síncrona de interagir com nosso serviço principal de processamento de texto em execução a partir de qualquer shell local ou remoto. Esta é uma solução robusta projetada para integrar a lógica central em ambientes shell.

---

## 1. Arquitetura e conceito de CLI síncrona

O serviço é alimentado pelo servidor **Uvicorn/FastAPI** e usa um endpoint personalizado (`/process_cli`) para entregar um resultado síncrono (bloqueio) de um processo em segundo plano baseado em arquivo inerentemente assíncrono.

### Estratégia de pesquisa de esperar e ler

1. **Substituição de saída exclusiva:** A API cria um diretório temporário exclusivo para cada solicitação.
2. **Início do processo:** Ele chama `process_text_in_background` para executar a lógica principal em um thread sem bloqueio, gravando o resultado em um arquivo `tts_output_*.txt` dentro dessa pasta exclusiva.
3. **Espera síncrona:** A função API então **bloqueia** e pesquisa a pasta exclusiva até que o arquivo de saída seja criado ou um tempo limite seja atingido.
4. **Entrega de resultados:** A API lê o conteúdo do arquivo, realiza a limpeza necessária (excluindo o arquivo e o diretório temporário) e retorna o texto final processado no campo `result_text` da resposta JSON.

Isso garante que o cliente CLI só receba uma resposta *após* a conclusão do processamento de texto, garantindo uma experiência de shell confiável.

## 2. Acesso remoto e mapeamento de porta de rede

Para permitir o acesso de clientes remotos como o terminal de Lub, foi necessária a seguinte configuração de rede, abordando a restrição comum de disponibilidade limitada de portas externas:

### Solução: Mapeamento de porta externa

Como o serviço é executado internamente na **Porta 8000** e nosso ambiente de rede limita o acesso externo a um intervalo de portas específico (por exemplo, `88__-8831`), implementamos o **Mapeamento de portas** no roteador (Fritz!Box).

| Ponto final | Protocolo | Porto | Descrição |
| :--- | :--- | :--- | :--- |
| **Externo/Público** | TCP | `88__` (Exemplo) | A porta que o cliente (Lub) deve usar. |
| **Interno/Local** | TCP | `8000` | A porta em que o serviço FastAPI realmente escuta (`--port 8000`). |

O roteador converte qualquer conexão de entrada na porta externa (`88__`) para a porta interna (`8000`) da máquina host, tornando o serviço acessível globalmente sem alterar a configuração do servidor principal.

## 3. Uso do cliente CLI

O cliente deve ser configurado com o endereço IP público, a porta externa e a API-Key correta.

### Sintaxe do Comando Final

__CODE_BLOCK_0__