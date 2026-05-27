# Interfaz de usuario de administración de Aura

La interfaz de usuario del administrador le permite ver y cambiar la configuración de Aura en su navegador.

## Abierto

http://localhost:8084

## Qué puedes hacer

- Ver el estado de la traducción para cada interfaz (voz, terminal, web)
- Activar o desactivar la traducción por interfaz
- Elija el idioma de destino (inglés, francés, español, etc.)

## Interfaces

| Interfaz | Descripción |
|-----------|------------------------------------|
| discurso | Entrada de voz (micrófono) |
| terminales | Línea de comando (comando `s`) |
| web | Chat web Streamlit (puerto 8831) |

## Ejemplo

Para traducir solo usuarios web al inglés: deje la voz y la terminal apagadas,
habilitar web con idioma `en`.