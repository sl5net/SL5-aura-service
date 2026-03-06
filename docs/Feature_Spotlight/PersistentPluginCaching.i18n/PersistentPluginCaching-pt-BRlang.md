# 💡 Destaque de recurso: cache de plug-in persistente

## 💾 Armazenamento em cache para desempenho, confiabilidade e eficiência de rede

O sistema agora oferece um mecanismo de cache central e persistente (`simple_plugin_cache`) projetado para reduzir a carga da rede externa (por exemplo, clima, APIs de tradução) e acelerar a execução. O cache é **persistente**, o que significa que as entradas sobrevivem às reinicializações do serviço.

**Objetivo:** reduzir o tráfego de rede, evitar abusos de API e fornecer respostas alternativas rápidas durante interrupções de serviços externos.

---

### 1. Implementação básica de cache (orientada por TTL)

Para armazenar em cache o resultado de uma função, você precisa implementar a lógica principal em três blocos: **Check**, **Execute** e **Store**.

#### 1.1 Importações e configuração

Adicione as importações necessárias e defina uma constante Time-To-Live (TTL) no script do seu plugin (por exemplo, `weather.py`):

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
from pathlib import Path

# Define the Time-To-Live for successful data
WEATHER_TTL = 300 # 5 minutes
```

#### 1.2 Lógica de cache no bloco `execute`

A função `executar` deve primeiro tentar recuperar o resultado armazenado em cache antes de fazer qualquer chamada de rede.

```python
def execute(match_data, logger):
    # ASSUMPTION: BASE_DIR_FOR_CACHE points to a stable, persistent directory (e.g., TMP_DIR)
    BASE_DIR_FOR_CACHE = Path(...) 
    
    # The cache key must be a tuple of all arguments that affect the function's result.
    cache_key_args = (city, lang) 
    
    # --- BLOCK A: PRIMARY CACHE CHECK (TTL-Driven) ---
    cached_response = get_cached_result(
        BASE_DIR_FOR_CACHE,
        'plugin_get_weather',      # Unique name for this function/operation
        cache_key_args,
        WEATHER_TTL,               # The TTL for this entry
        logger=logger
    )
    if cached_response:
        return cached_response # <-- CACHE HIT: Return immediately
        
    # --- BLOCK B: NETWORK EXECUTION (ONLY on Cache Miss) ---
    try:
        # Execute your CURL/Requests/External API call here.
        response = "Successful API response..." 

        # --- SUCCESS: STORE RESULT ---
        set_cached_result(BASE_DIR_FOR_CACHE, 'plugin_get_weather', cache_key_args, response)
        
        return response

    # --- BLOCK C: EXCEPTION & FAILOVER (Stale Cache Strategy) ---
    except Exception as e:
        logger.warning(f"API call failed ({type(e).__name__}). Attempting stale cache fallback...")
        
        # SECOND CACHE CHECK: Retrieve the last stored entry, ignoring its age (ttl_seconds=None).
        stale_response = get_cached_result(
            BASE_DIR_FOR_CACHE, 
            'plugin_get_weather', 
            cache_key_args,
            logger=logger # Important: TTL is explicitly omitted (None) here
        )
        
        if stale_response:
            logger.warning("Delivering STALE cache as fallback.")
            return stale_response
        
        # NO FALLBACK AVAILABLE: Return the original error message.
        # Ensure you handle all specific exceptions as defined in your plugin.
        if isinstance(e, FileNotFoundError):
             return "Error: 'curl' program not found."
        # ... (other exception handlers) ...
        return f"Error: Could not fetch data and no fallback available. Cause: {e}"
```

---

### 2. Modos de cache avançados

#### A. Cache Permanente (Eterno)

Se um resultado **nunca expirar** (por exemplo, pesquisa de configuração estática), omita totalmente o parâmetro `ttl_seconds`.

```python
# The entry will be considered valid forever until manually overwritten.
cached_result = get_cached_result(BASE_DIR_FOR_CACHE, 'static_config', ('my_key',), logger=logger) 
```

#### B. Requisitos de chave de cache (`key_args`)

* `key_args` deve ser uma **tupla** contendo todas as variáveis que definem o resultado (por exemplo, `(cidade, idioma, sistema_unidade)`).
* O mecanismo de cache converte automaticamente objetos Python comuns não serializáveis por JSON, como **`pathlib.Path`**, em strings para geração de chave.