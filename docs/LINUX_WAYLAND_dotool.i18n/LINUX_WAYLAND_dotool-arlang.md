# Aura unter Wayland (Manjaro / Arch / CachyOS)

Damit Aura يمكن كتابة نص في نوافذ أخرى، وهو موجود في Wayland `dotool`.

                                                ### Wichtige Voraussetzungen:
1. **البرنامج الخفي:** `dotoold` muss im Hintergrund laufen (Aura startet diesen automatisch).
            2. **Berechtigungen:** Dein User muss in der Gruppe `input` sein.
3. **Uinput:** يجب أن يتم تجميع البيانات `/dev/uinput` للمجموعة `input`.

                                         ### مانويل ريباراتور:
لا تعمل شلالات Tippen، فهي تتدفق من الأسفل إلى الأعلى:
                                                             __CODE_BLOCK_0__