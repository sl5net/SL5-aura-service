البداية التلقائية Eintrag über dein grafische Benutzeroberfläche لـ:

                         Restart_venv_and_run-server.sh.desktop XSPACEكسرX

                                         aura_engine.log.desktopXSPACEكسرX

                         قم بإنشاء الملف: `~/.config/autostart/`

                                                     öffne في المحرر

                         Restart_venv_and_run-server.sh.desktop XSPACEكسرX
                                         aura_engine.log.desktopXSPACEكسرX

                                    دن بيفيل مانويل أنباسن

                                                            **انستات:**
                                             `Exec=/pfad/zu/deinem/script.sh`

                                             **بيسبييلي شريبي:**

                                             [إدخال سطح المكتب]
                                                           تعليق[ar_GB]=
                                                              التعليق=
Exec=konsole -e bash -c \'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; ثم ردد "الهالة تعمل بالفعل."; وإلا المس /tmp/sl5_aura/sl5net_aura_project_root; /home/......../projects/py/STT/scripts/restart_venv_and_run-server.sh; فاي؛ إكسيك زش'
                                                الاسم العام[en_GB]=
                                                       الاسم العام=
                                                    أيقونة = نص-x-log
                                                                 نوع Mime=
                                                الاسم[en_GB]=aura_engine
                                                       الاسم=aura_engine
                                                                المسار=
                                                           StartupNotify=true
                                                        المحطة = خطأ
                                                    النوع=التطبيق
                                               X-KDE-AutostartScript=صحيح
                                                   X-KDE-SubstituteUID=خطأ
                                               X-KDE-اسم المستخدم=


         ### ماذا عن الرسم البياني الذي لا يعمل؟

تعد Plasma 6 مشكلة رائعة بسبب "المحطات الافتراضية" في مرحلة بدء الأنظمة. سيتم إرسال "وحدة التحكم" (das Standard-Terminal von KDE) مباشرة إلى "Exec"--Seile schreiben، وسنقوم بعد ذلك بالتبديل التلقائي والبدء في البداية.


                                                 26.3.\'26 08:16 الخميس