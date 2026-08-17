# Security Architecture: Protection of Private Data (7.8.'26 13:22 Fri)

The source code of `service_api.py` implements a triple-layered, mutually independent security architecture to protect private data.

## Overview

| Layer | Mechanism | Component | Protection Goal |
|-------|-----------|-----------|-----------------|
| 1 | Underscore-Rule Middleware | `service_api.py` | Block access to hidden paths |
| 2 | API-Key Authentication | `service_api.py` | Access control for endpoints |
| 3 | Privacy Masking & Cache Isolation | `service_api.py`, `aura_cache.py` | Data obfuscation & cache separation |

---

## Layer 1: Underscore-Rule Middleware

Any request to paths or folders with a leading underscore (such as `_privat`) is hard-blocked by the middleware with **HTTP 403 Forbidden**.

**Error message:**
```
Access to hidden folders (starting with '_') is forbidden.
```

This rule operates at the path/routing level and prevents any access to directories marked as private.

---

## Layer 2: API-Key Authentication

All API endpoints are protected by `Depends(verify_api_key)`.

Requests without a valid `X-API-Key` header are immediately rejected before reaching any business logic.

---

## Layer 3: Privacy Masking & Cache Isolation

### Masking
Via the API, `unmasked = False` is the default. Sensitive data in API responses is therefore automatically masked.

### Cache Isolation
The `cache_id` hash in `aura_cache.py` is separated by the active window title (`_active_window_title`).

**Consequence:** Cache entries created in the local terminal cannot be read via the API, because they possess a different `cache_id` hash.

---

## Summary

Your confidential data in `_privat` is thus protected on all three language and path levels against unauthorized API access:

1. **Path Level** — Access to `_` folders is blocked
2. **Authentication Level** — Only valid API keys are granted access
3. **Data Level** — Masking and cache isolation prevent data exfiltration
