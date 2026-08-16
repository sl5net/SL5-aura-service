# search_rules.sh – التعديل التفاعلي مع fzf

    > ⚠️ نور لينكس/ماك. Kein Windows-Support (fzf + xdg-open).

                                                  ## كان وفاق ماخت

`search_rules.sh` يستخدم جميع بيانات الخريطة في `config/maps/` التفاعل مع `fzf`.
يمكن أن يتم النقل مباشرة من خلال المحرر المتوفر أو من خلال GitHub.

                                                           ## Dateien im Repo

```
scripts/search_rules/search_rules.sh   ← offizielle Version
tools/search_rules.sh                  ← veraltet, hat hardcodierten Pfad-Bug
```

تم استبدال الإصدار الموجود في "الأدوات/" أو من خلال رابط رمزي واحد:
```bash
rm ~/projects/py/STT/tools/search_rules.sh
ln -s ../scripts/search_rules/search_rules.sh ~/projects/py/STT/tools/search_rules.sh
```

                                                ## فوراوسيتزونجن

```bash
# fzf installieren (falls nicht vorhanden)
sudo apt install fzf        # Debian/Ubuntu
sudo pacman -S fzf          # Arch
brew install fzf            # macOS
```

                                                             ##نوتزونج

```bash
cd ~/projects/py/STT
bash scripts/search_rules/search_rules.sh
```

                                                         ## fzf Tastenkürzel

                                                        | ذوق | اكشن |
                                                                    |---|---|
                             | تيبن | سوشانفراج إينجبين |
                            | `أدخل` | Datei im Editor öffnen (كيت) |
        | `السيطرة+G` | قم بتشغيل GitHub في المتصفح |
                   | `السيطرة+Z` | Vorherige suchanfrage aus History |
                    | `السيطرة+Y` | Nächste suchanfrage aus History |
        | `السيطرة+P` | تاريخ فورهيرجير-اينتراغ |
                      | `السيطرة + N` | تاريخ Nächster-Eintrag |
                               | `السيطرة+أ` | كل ما تريده |
                                        | `السيطرة+C` | ابريشن |
                           | `Ctrl+←/←` | الملاحة الرائعة |
          | `Ctrl+مسافة للخلف` | نبتة لوسشن (روابط) |
                 | `التحكم + الحذف` | نبتة لوسشن (حق) |

                                                            ## التكوين

                                             Am Anfang des Scripts anpassbar:

```bash
PREFERRED_EDITOR="kate"          # Editor für Ctrl+Enter
HISTORY_FILE="$HOME/.search_rules_history"  # Suchverlauf
DEFAULT_QUERY=".py pre # EXAMPLE:"          # Startsuche beim ersten Aufruf
REPO_URL="https://github.com/sl5net/SL5-aura-service/blob/master"
```

                                                 ## معاينة فينستر

    أصبح FZF-Fenster (50%) واحدًا من مزارعي الأشجار:
                                            - 5 Zeilen vor und nach dem Match
                                     - Die Treffer-Zeile ist mit `>` markiert
                                             - Zeilennummern werden angezeigt

                                                         ##سوفيرلاوف

سيتم استخدام هذه اللقطة تلقائيًا كبداية بعد أن يتم استخدامها.
                           يقع Der Verlauf في `~/.search_rules_history`.

                                                     ## Typische suchanfragen

```
FUZZY_MAP_pre                    # alle pre-Map Regeln
# TODO                           # auskommentierte Aufgaben
^.*$                             # Fullmatch-Regeln (Pipeline-Stopper)
re.IGNORECASE                    # alle Regex-Regeln mit Flag
koans                            # alle Koan-Dateien
```

                                                 ## Bekannte Einschränkungen

- نور Linux/macOS (على الرغم من وجود Windows `fzf` و`xdg-open`)
- محرر مضمن على `kate` - محرر آخر `PREFERRED_EDITOR` ändern
- لم يتم العثور على أي شيء في `config/maps/` - لا يوجد أي خلل في الريبو