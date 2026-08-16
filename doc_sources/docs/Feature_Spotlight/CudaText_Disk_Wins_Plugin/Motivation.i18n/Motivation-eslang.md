# Motivación: ¿Por qué "el disco gana"?

## El problema en el modo abuela Aura

En [Aura Oma Mode](../../../GettingStarted.i18n/GettingStarted-eslang.md) (ver línea 67), Aura opera en gran medida de forma autónoma:
el usuario pronuncia comandos y Aura escribe archivos por sí sola.
configuraciones, scripts, entradas de registro, texto generado.

El siguiente escenario ocurre constantemente:

1. El usuario tiene un archivo abierto en el editor (por ejemplo, un archivo de reglas o un script).
2. Olvidan que el editor todavía está activo y pronuncian un comando de Aura.
3. Aura cambia el archivo en el disco.
4. El editor detecta el cambio externo y **pregunta**.

Este mensaje es **espectacular** en el modo Oma:
- El usuario puede estar sentado en el sofá, utilizando la entrada de voz,
y no puedo ver ni acceder al cuadro de diálogo.
- O presionaron accidentalmente una tecla en el editor, el búfer ahora está
"modificado", y cada cambio externo se bloquea con un
"¿Recargar? / ¿Mantener local?" diálogo.
- El resultado: Aura sigue funcionando, pero el editor muestra una versión obsoleta.
El usuario cree que está viendo el archivo actual, pero lo edita según
en un viejo Estado: el caos está garantizado.

## Lo que necesitamos

Comportamiento del editor que **siempre prioriza el disco**.
Cuando Aura (o cualquier otra herramienta) cambia el archivo, el editor debe
inmediatamente y **sin ningún aviso** mostrar el nuevo contenido.
Las entradas no guardadas en el editor pueden descartarse silenciosamente, porque en
Modo Oma, Aura es la fuente de la verdad, no la entrada del teclado humano.

## Por qué fallan los editores estándar

Casi todos los editores comunes (Kate, VS Code, Sublime Text, Notepad++,
Emacs, Vim, CudaText listos para usar) tienen un mecanismo de protección:
tan pronto como el búfer contiene cambios no guardados, **siempre** preguntan
cuando ocurre un cambio externo. Esta es una característica normal.
trabajo de desarrollador, pero un error para el modo Aura Oma.

Este complemento cierra exactamente esa brecha para CudaText.

## Público objetivo

- Usuarios del modo Aura Oma que ven archivos en un editor en paralelo.
- Escenarios de automatización donde un proceso escribe archivos y un editor.
sirve sólo como espectador en vivo.
- Cualquiera para quien "el disco siempre gana" es el comportamiento deseado.