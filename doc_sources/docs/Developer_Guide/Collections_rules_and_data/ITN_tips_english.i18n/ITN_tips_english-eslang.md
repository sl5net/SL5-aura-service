El término técnico es **Normalización de texto inverso (ITN)**.

Si lo busca, encontrará enormes colecciones de reglas y datos.

Estos son los mejores recursos para completar mapas sin tener que escribir todo usted mismo:

### 1. Colecciones de reglas ITN (el “estándar de oro”)
* **[itnpy](https://github.com/barseghyanartur/itnpy):** Una herramienta Python simple y determinista diseñada para este mismo propósito. Utiliza archivos CSV para convertir palabras habladas en caracteres escritos (números, monedas, fechas). Puede copiar los archivos CSV casi 1:1 en su mapa.

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** Muy potente. Tienen enormes archivos gramaticales para casi todos los idiomas. Allí encontrará listas de unidades de medida, títulos y formatos de fecha.

### 2. Fuentes de datos para puntuación y mayúsculas y minúsculas
* **[Vosk recasepunc](https://github.com/benob/recasepunc):** Esta es la herramienta estándar para Vosk. Utiliza modelos, pero el código fuente suele contener listas de abreviaturas y nombres propios que se pueden extraer.

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** Un enorme conjunto de datos (creado para un desafío de Kaggle) que contiene millones de ejemplos de cómo el lenguaje hablado se convierte en lenguaje escrito.

### 3. Bibliotecas de “ayuda de dictado”
* **[num2words](https://github.com/savoirfairelinux/num2words):** Si necesita mapeo de números, puede encontrar listas de “uno” a “un millón” aquí.