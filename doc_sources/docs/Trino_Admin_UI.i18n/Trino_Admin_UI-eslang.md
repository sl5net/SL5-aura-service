# Interfaz de usuario de administración de Aura

La interfaz de usuario del administrador le permite ver y cambiar la configuración de Aura en su navegador sin costo alguno de recursos inactivos. El servidor del panel no se ejecuta durante el arranque; se inicia bajo demanda solo cuando se solicita.

## Cómo abrir (bajo demanda)

Puede iniciar y abrir el Panel de administración dinámicamente utilizando cualquiera de los tres métodos siguientes:

### 1. Comando de voz
Simplemente hable por su micrófono:
* *"administración del aura"

### 2. Comando de terminal/consola
Si está trabajando en la terminal, ejecute este comando para activar el iniciador directamente:
```bash
s aura administration
```

*⚠️ **Nota de plataforma para usuarios de Windows/macOS:** El contenedor de comando `s` corto está configurado principalmente para entornos Linux. Por favor lea el documento para eso. Si está ejecutando Windows o macOS, es posible que el comando `s` no funcione de fábrica. Consulte nuestra documentación oficial de configuración de CLI para aprender cómo configurar e implementar el alias del comando `s` para su sistema operativo.*


### 3. Acceso directo al escritorio
Para crear un icono de escritorio específico de la plataforma, ejecute este script de configuración una vez:
```bash
python scripts/py/chat/install_shortcut.py
```
Luego, simplemente haga doble clic en el ícono **Aura Admin Dashboard** en su escritorio.

---

## Acceso directo al navegador
Una vez que el servidor se haya iniciado mediante cualquiera de los métodos bajo demanda anteriores, podrá acceder a la interfaz directamente en su navegador en cualquier momento:

http://localhost:8084

*(¡No dudes en marcar este enlace como favorito en tu navegador!)*

---

## Qué puedes hacer

- Ver el estado de traducción de cada interfaz (voz, terminal, web).
- Activar o desactivar la traducción por interfaz.
- Elija el idioma de destino (inglés, francés, español, etc.).

## Interfaces

| Interfaz | Descripción |
|-----------|------------------------------------|
| discurso | Entrada de voz (micrófono) |
| terminales | Línea de comando (comando `s`) |
| web | Chat web Streamlit (puerto 8831) |

## Ejemplo

Para traducir solo usuarios web al inglés: deje la voz y la terminal apagadas, habilite la web con el idioma "en".