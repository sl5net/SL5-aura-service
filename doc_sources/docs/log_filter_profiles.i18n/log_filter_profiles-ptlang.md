# Perfis de filtro de log

O filtro de log ativo é sempre `config/filters/settings_local_log_filter.py`.

## Perfis

Perfis predefinidos são armazenados em `config/filters/.backlock/`:

| Perfil | Descrição |
|---|---|
| `primeira_execução` | Saída mínima – apenas erros e status. Aplicado automaticamente na primeira partida. |
| `normal` | Filtro padrão para uso diário. |

## Alternar perfil manualmente

```bash
cp config/filters/.backlock/first_run/settings_local_log_filter.py config/filters/settings_local_log_filter.py
cp config/filters/.backlock/normal/settings_local_log_filter.py config/filters/settings_local_log_filter.py
```

## Adicione um perfil personalizado

1. Crie uma nova pasta em `config/filters/.backlock/my_profile/`
2. Copie um `settings_local_log_filter.py` existente nele e edite de acordo com suas necessidades
3. Aplique-o com `cp` como mostrado acima

## Troca automática de perfil

Na primeira inicialização, o Aura detecta que o diretório `log/` ainda não existe e
copia automaticamente o perfil `first_run` como o filtro ativo.