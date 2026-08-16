# Notificaciones de flujo de trabajo (alertas de audio)

Para mejorar la productividad, puede configurar un alias de Git local que envíe su código y le avise automáticamente (por voz o sonido) tan pronto como finalice el flujo de trabajo de GitHub Actions. Esto evita la "fatiga de observación de GitHub" y le permite concentrarse en otras tareas.

### Requisitos previos

Necesita **GitHub CLI** y un motor de texto a voz o un reproductor de sonido instalado en su sistema.

**Para Manjaro/Arch Linux:**
```bash
sudo pacman -S github-cli espeak-ng
gh auth login
```

### Configuración

Ejecute el siguiente comando en su terminal para crear un alias global de Git llamado `pushsound`:

```bash
git config --global alias.pushsound '!git push && sleep 3 && gh run watch $(gh run list --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "all github workflow has finished"'
```

### Uso

En lugar de "git push", simplemente ejecute:
```bash
git pushsound
```
Su terminal esperará a que se complete el flujo de trabajo y luego anunciará: *"todo el flujo de trabajo de github ha finalizado"*.

---

### Personalización y alternativas

Dependiendo de sus preferencias, es posible que desee utilizar un nombre de alias o un método de notificación diferente.

#### 1. Nombres de alias recomendados
Si "pushsound" es demasiado largo para escribirlo, considere estas alternativas:
* `git pw` (Push & Watch) — **Recomendado por velocidad.**
* `git sync` (Implica presionar y esperar la "luz verde")
* `git palert` (alerta push)

#### 2. Estilos de notificación
Puedes cambiar la parte `espeak-ng` por otros tipos de alertas:

* **Notificación de escritorio:**
`... && notificar-enviar "Acción de GitHub" "¡Flujo de trabajo finalizado!"`
* **Sonido del sistema (campana):**
`... && paplay /usr/share/sounds/freedesktop/stereo/complete.oga`
* **Combinación (Sonido + Voz):**
`... && paplay /usr/share/sounds/freedesktop/stereo/message.oga && espeak-ng "Listo"`

#### 3. Avanzado: versión segura para equipos
Si varios desarrolladores ingresan al mismo repositorio simultáneamente, el comando predeterminado podría rastrear la ejecución incorrecta. Utilice esta versión "Branch-Safe" para ver únicamente su propia rama actual:

##### comprueba solo el primer flujo de trabajo:

```bash
git config --global alias.pw '!git push && sleep 3 && gh run watch $(gh run list --branch $(git branch --show-current) --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "Workflow finished"'

git config --global alias.pushsound '!git push && sleep 3 && (gh run watch $(gh run list --limit 1 --json databaseId --jq ".[0].databaseId") --exit-status && espeak-ng "workflow successful" || espeak-ng "workflow failed")'

```

##### comprueba todos los flujos de trabajo registrados en GitHub

git config --global alias.pushsound '!f() { git push && echo "Esperando a que GitHub registre flujos de trabajo..." && sleep 5 && SHA=$(git rev-parse HEAD) && SUCCESS=0 && for id in $(gh run list --commit $SHA --json DatabaseId -q ".[].databaseId"); hacer echo "Observando el flujo de trabajo $id..." && gh ejecutar watch $id --exit-status || ÉXITO=1; hecho; [ $SUCCESS -eq 0 ] && espeak-ng "todos los flujos de trabajo exitosos" || espeak-ng "al menos un flujo de trabajo falló"; }; F'


### Solución de problemas
* **"No se encontraron ejecuciones":** Incluimos un `sleep 3` porque GitHub se toma un momento para registrar el envío e iniciar el flujo de trabajo. Si tiene una conexión muy lenta, es posible que deba aumentarla a "suspensión 5".
* **Pitidos del terminal:** Si `espeak-ng` no funciona, asegúrese de que el audio no esté silenciado y que el paquete esté instalado correctamente.