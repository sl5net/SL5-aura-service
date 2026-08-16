# Guía de comunicación: firmas y marca

Para ayudar a difundir el conocimiento de **Aura** sin ser intrusivos, utilizamos una estrategia de "marca pasiva" a través de firmas de chat. Esto permite a los usuarios encontrar el proyecto fácilmente mientras mantienen la conversación centrada en el contenido.

## 1. La firma del aura
Al utilizar las funciones de traducción o automatización en un chat, Aura puede agregar una pequeña firma a sus mensajes.

**Formato recomendado:**
> `🗣SL5net ⟫ Aura`

### Desglose de los símbolos:
* **`🗣` (Cabeza parlante):** Un indicador visual de que este mensaje fue procesado o traducido. Señala "Comunicación/Lenguaje".
* **`SL5net`:** El espacio de nombres único. Esto es crucial para la capacidad de búsqueda.
* **`⟫` (Doble corchete derecho):** Un símbolo técnico de "tubería" que parece un operador CLI/Shell, lo que refuerza que se trata de una herramienta técnica.
* **`Aura`:** El nombre del proyecto.

---

## 2. ¿Por qué "SL5net Aura" en lugar de un Enlace?
Muchas plataformas de chat (Matrix, Discord, Telegram, etc.) tienen filtros estrictos contra URL o estructuras similares a dominios.
* **Capacidad de búsqueda:** La búsqueda de `SL5net Aura` en Google o GitHub produce una tasa de éxito del 100% para encontrar el repositorio.
* **Filter-Safe:** Al utilizar un término de búsqueda único en lugar de un enlace `.com`, evitamos que los moderadores automáticos nos marquen como "spam" o "ad-bots".
* **Baja fricción:** Es fácil de leer y de escribir en una barra de búsqueda.

---

## 3. Etiqueta de firma (Preguntas frecuentes)
Cómo utilizar firmas de forma eficaz sin molestar a tus compañeros de chat:

### P: ¿Debo tener la firma en cada mensaje?
**R:** No. Las firmas constantes pueden percibirse como spam en chats de ritmo rápido.
* **Práctica recomendada:** Habilite la firma solo para el primer mensaje de una conversación nueva o para mensajes traducidos específicos de "alto valor".
* **Configuración:** Utilice la opción `# signatur` en su configuración para desactivarla en reuniones de negocios privadas o muy formales.

### P: ¿Por qué no utilizar Braille o caracteres Unicode complejos?
**R:** Probamos símbolos como `⠠de╱Aura`. Si bien parecen únicos, a otros les resulta difícil copiarlos y pegarlos o escribirlos manualmente en un motor de búsqueda. `SL5net Aura` es el puente "humano-motor de búsqueda" más robusto.

### P: ¿El Emoji (🗣) es lo suficientemente profesional?
**R:** En el 95% de los entornos de desarrollo modernos (GitHub, Discord, Slack), los emojis son estándar. Si se encuentra en un entorno corporativo de alto cumplimiento (por ejemplo, banca), le recomendamos una versión más limpia:
`[ SL5net Aura ]`

---

## 4. Ejemplos de configuración (en config/settings.py o config/settings_local.py)
Aura admite diferentes estilos para adaptarse a tu personalidad:

```bash
# Professional/Technical
signatur='🗣SL5net ⟫ Aura'

# Discreet/Official
signatur='🗣[ SL5net Aura ]'

# Minimalist
signatur='🗣SL5net Aura'
```

---

### Consejo profesional para desarrolladores:
Al incluir esta guía en su repositorio, demuestra **"Inteligencia social".** No solo está creando una herramienta; está creando una herramienta que comprende el contexto social del lugar donde se utiliza. Esta es una calificación de alto nivel que a menudo se busca en **Gerentes de pruebas sénior** y **Propietarios de productos**.

**🗣SL5net ⟫ Aura**