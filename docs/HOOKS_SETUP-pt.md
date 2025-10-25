# Configurando Git Hooks Pre-Push e Ferramentas Python no Linux

Este projeto usa um gancho Git pré-push para atualizar automaticamente `requirements.txt` de seus scripts Python.
Para usar este fluxo de trabalho, você precisa ter a ferramenta `pipreqs` instalada e disponível para Git.

## Recomendado: Instale pipreqs com pipx

1. **Instale o pipx (se ainda não estiver instalado):**
```bash
sudo pacman -S python-pipx
```

2. **Instale pipreqs usando pipx:**
```bash
pipx instalar pipreqs
```

3. **Verifique se o pipreqs funciona:**
```bash
pipreqs --versão
```

## Alternativa: use um ambiente virtual Python

Se você preferir ou estiver usando um virtualenv para seu projeto:

1. **Crie e ative um virtualenv:**
```bash
python -m venv.venv
fonte .venv/bin/activate
```

2. **Instale o pipreqs dentro do virtualenv:**
```bash
pip instalar pipreqs
```

3. **Edite o git hook** para chamar pipreqs usando o caminho completo:
```bash
.venv/bin/pipreqs "$TMPDIR" --force
```

## Por que não usar a instalação simples do pip?

As distribuições modernas do Linux restringem as instalações de pip em todo o sistema para evitar a quebra de pacotes do sistema operacional.
**NÃO** use `sudo pip install pipreqs` ou `pip install pipreqs` globalmente.

## Solução de problemas

- Se você vir `pipreqs: comando não encontrado`, certifique-se de instalá-lo com pipx e que `~/.local/bin` esteja em seu `$PATH`.
- Você pode verificar seu caminho com:
```bash
echo $PATH
```

## Precisa de ajuda?

Abra um problema ou pergunte na discussão do projeto!
