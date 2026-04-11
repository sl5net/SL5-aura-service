البداية التلقائية Eintrag über dein grafische Benutzeroberfläche لـ:

                         Restart_venv_and_run-server.sh.desktop XSPACEكسرX

                                         aura_engine.log.desktopXSPACEكسرX

                         قم بإنشاء الملف: `~/.config/autostart/`

                                                     öffne في المحرر

                         Restart_venv_and_run-server.sh.desktop XSPACEكسرX
                                         aura_engine.log.desktopXSPACEكسرX

                                  دن بيفيل مانويل أنباسين

                                                            **انستات:**
                                             `Exec=/pfad/zu/deinem/script.sh`

                                             **بيسبييلي شريبي:**

Exec=xfce4-terminal -e \'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'

`Exec=xfce4-terminal -e \'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"''

Exec=konsole -e \'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"' XSPACEbreakX

                  Exec=Exec=kate /home/me/projects/py/STT/log/aura_engine.log

Exec=kate /home/me/projects/py/STT/config/filters/settings_local_log_filter.py





         ### ماذا عن الرسم البياني الذي لا يعمل؟

تعد Plasma 6 مشكلة رائعة بسبب "المحطات الافتراضية" في مرحلة بدء الأنظمة. سيتم إرسال "وحدة التحكم" (das Standard-Terminal von KDE) مباشرة إلى "Exec"--Seile schreiben، وسنقوم بعد ذلك بالتبديل التلقائي والبدء في البداية.


                                                 26.3.\'26 08:16 الخميس