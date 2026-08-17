# Arquitetura de segurança: proteção de dados privados (7.8.'26 13:22 sex)

O código-fonte de `service_api.py` implementa uma arquitetura de segurança de camada tripla e mutuamente independente para proteger dados privados.

## Visão geral

| Camada | Mecanismo | Componente | Meta de Proteção |
|-------|-----------|-----------|-----------------|
| 1 | Middleware com regra de sublinhado | `service_api.py` | Bloquear o acesso a caminhos ocultos |
| 2 | Autenticação de chave API | `service_api.py` | Controle de acesso para endpoints |
| 3 | Mascaramento de privacidade e isolamento de cache | `service_api.py`, `aura_cache.py` | Ofuscação de dados e separação de cache |

---

## Camada 1: Middleware de regra de sublinhado

Qualquer solicitação para caminhos ou pastas com um sublinhado inicial (como `_privat`) é bloqueada pelo middleware com **HTTP 403 Forbidden**.

**Mensagem de erro:**
```
Access to hidden folders (starting with '_') is forbidden.
```

Esta regra opera no nível de caminho/roteamento e impede qualquer acesso a diretórios marcados como privados.

---

## Camada 2: Autenticação de chave API

Todos os endpoints da API são protegidos por `Depends(verify_api_key)`.

Solicitações sem um cabeçalho `X-API-Key` válido são imediatamente rejeitadas antes de atingir qualquer lógica de negócios.

---

## Camada 3: Máscara de privacidade e isolamento de cache

### Mascaramento
Através da API, `unmasked = False` é o padrão. Os dados confidenciais nas respostas da API são, portanto, automaticamente mascarados.

### Isolamento de cache
O hash `cache_id` em `aura_cache.py` é separado pelo título da janela ativa (`_active_window_title`).

**Consequência:** As entradas de cache criadas no terminal local não podem ser lidas pela API, pois possuem um hash `cache_id` diferente.

---

## Resumo

Seus dados confidenciais em `_privat` são protegidos em todos os três níveis de idioma e caminho contra acesso não autorizado à API:

1. **Nível de caminho** — O acesso às pastas `_` está bloqueado
2. **Nível de autenticação** — Somente chaves de API válidas têm acesso
3. **Nível de dados** — O mascaramento e o isolamento de cache evitam a exfiltração de dados