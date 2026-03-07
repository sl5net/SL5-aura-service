# Matemáticos famosos - Guía de corrección STT

## El problema

Los sistemas de reconocimiento de voz (STT) como Vosk a menudo escuchan mal o escriben mal los nombres de matemáticos famosos.
Esto es especialmente común en los nombres alemanes que contienen caracteres especiales (ß, ü, ä, ö).
o nombres tomados prestados de otros idiomas.

## Errores comunes de STT

| Salida hablada/STT | Ortografía correcta | Notas |
|---|---|---|
| gaus, gauss | Gauss | Matemático alemán, ß a menudo desaparecido |
| engrasador, oyler | Euler | Suizo, su nombre suena como "engrasador" en alemán |
| leibnitz, lipnitz | Leibniz | z al final, error ortográfico común |
| riman, riemann | Riemann | doble n a menudo se pierde |
| Hilberto | Hilberto | generalmente correcto, solo mayúsculas |
| cantor | Cantor | generalmente correcto, solo mayúsculas |
| poincaré, poincaré | Poincaré | a menudo falta el acento |
| noether, nöter | Nada más | diéresis a menudo se pasa por alto |

## Reglas de ejemplo

```python
FUZZY_MAP_pre = [
    ('Gauß', r'\bgau[sß]{1,2}\b', 0, {'flags': re.IGNORECASE}),
    ('Euler', r'\b(oiler|oyler|euler)\b', 0, {'flags': re.IGNORECASE}),
    ('Leibniz', r'\bleib(nitz|niz|nits)\b', 0, {'flags': re.IGNORECASE}),
    ('Riemann', r'\bri{1,2}e?mann?\b', 0, {'flags': re.IGNORECASE}),
    ('Noether', r'\bn[oö]e?th?er\b', 0, {'flags': re.IGNORECASE}),
]
```

## ¿Por qué Pre-LanguageTool?

Estas correcciones deberían realizarse en `FUZZY_MAP_pre.py` (antes de LanguageTool),
porque LanguageTool podría "corregir" un nombre mal escrito con una palabra incorrecta diferente.
Es mejor solucionarlo primero y luego dejar que LanguageTool revise la gramática.

## Pruebas

Después de agregar una regla, pruebe con la consola Aura:
```
s euler hat die formel e hoch i pi plus eins gleich null bewiesen
```
Se esperaba: `Euler hat die Formel e hoch i pi plus eins gleich null bewiesen`