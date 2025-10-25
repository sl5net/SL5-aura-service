# Configuración de ganchos Git previos al envío y herramientas Python en Linux

Este proyecto utiliza un enlace Git previo al envío para actualizar automáticamente `requirements.txt` desde sus scripts de Python.
Para utilizar este flujo de trabajo, necesita tener la herramienta `pipreqs` instalada y disponible para Git.

## Recomendado: Instalar pipreqs con pipx

1. **Instalar pipx (si aún no está instalado):**
```golpecito
sudo pacman -S python-pipx
```

2. **Instale pipreqs usando pipx:**
```golpecito
pipx instalar pipreqs
```

3. **Verifique que pipreqs funcione:**
```golpecito
pipreqs --versión
```

## Alternativa: utilizar un entorno virtual Python

Si prefiere o está utilizando un entorno virtual para su proyecto:

1. **Crea y activa un entorno virtual:**
```golpecito
python -m venv .venv
fuente .venv/bin/activate
```

2. **Instale pipreqs dentro de virtualenv:**
```golpecito
pip instalar pipreqs
```

3. **Edite el gancho de git** para llamar a pipreqs usando la ruta completa:
```golpecito
.venv/bin/pipreqs "$TMPDIR" --fuerza
```

## ¿Por qué no utilizar la instalación de pip simple?

Las distribuciones modernas de Linux restringen las instalaciones de pip en todo el sistema para evitar que se rompan los paquetes del sistema operativo.
**NO** use `sudo pip install pipreqs` o `pip install pipreqs` globalmente.

## Solución de problemas

- Si ve `pipreqs: comando no encontrado`, asegúrese de haberlo instalado con pipx y que `~/.local/bin` esté en su `$PATH`.
- Puedes consultar tu ruta con:
```golpecito
eco $ RUTA
```

## ¿Necesitas ayuda?

¡Abra un problema o pregunte en la discusión del proyecto!
