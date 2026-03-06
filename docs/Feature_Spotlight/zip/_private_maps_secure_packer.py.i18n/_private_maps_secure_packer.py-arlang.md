استيراد نظام التشغيل
                                 عملية الاستيراد الفرعية
                                                تسجيل الاستيراد
                                                        استيراد Shutil
                                         من مسار استيراد pathlib

                       المسجل = logging.getLogger(__name__)

                              التنفيذ المؤكد (البيانات):
                                                                       يمر

                                                      تعريف on_reload():
                                                                          """
                                                 إنشاء "Matryoshka-ZIP":
                   أوردنر ->inner.zip (aura_secure.blob) ->password.zip
                                   Versteckt die Complete Verzeichnistruktur.
                                                                          """
        logger.info("🔒 SecurePacker (Matryoshka): بدء الأمان...")

                      current_dir = المسار(__file__).parent
                                              parent_dir = current_dir.parent

                                                    # Name des äußeren ZIPs
                      zip_name_outer = current_dir.name.lstrip(\'_') + ".zip"
                                   zip_path_outer =parent_dir /zip_name_outer

                          # 1. كلمة المرور من هذا القبيل
                       key_file = next(parent_dir.glob(".*.py"), لا شيء)
                                          إذا لم يكن ملف key_file:
                                    logger.error("❌مفتاح الملف!")
                                                                     يعود

                          كلمة المرور = _extract_password(key_file)
                                    إذا لم يكن كلمة المرور:
                 logger.error("❌ كلمة المرور غير متاحة!")
                                                                     يعود

                                      # 2. INNERES ZIP erstellen (Der "Blob")
# نحن ننشئ مؤقتًا في دليل الوالدين لـ Schreibzugriffe في نظام المراقبة الخاص بنا لتقليله
               temp_inner_zip =parent_dir / "aura_secure_temp" # wird zu .zip

                                                                  يحاول:
                                               # Erzeugt aura_secure_temp.zip
           Shutil.make_archive(str(temp_inner_zip), \'zip', str(current_dir))
                     temp_inner_zip_file =parent_dir / "aura_secure_temp.zip"

                                     # Umbenennen in den Neutralen Blob-Namen
                                               blob_name = "aura_secure.blob"
                                            blob_path =parent_dir / blob_name
                        Shutil.move(str(temp_inner_zip_file), str(blob_path))

                                # 3. ÄUßERES ZIP erstellen (Verschlüsselt)
إذا subprocess.call("command -v zip"، shell=True، stdout=subprocess.DEVNULL) != 0:
                                     logger.error("❌ \'zip' Befehl fehlt.")
                                                                     يعود

                                         # Wir packen NUR den Blob in das ZIP
                                                                   كمد = [
\'zip', '-j', # -j: المسارات غير المرغوب فيها (keine Pfade speichern, nur Dateiname)
                                               "-P"، كلمة المرور،
                                                  شارع (zip_path_outer)،
                                                         شارع (blob_path)
                                                                            ]

  العملية = subprocess.run (cmd، Capture_output = True، text = True)

                                                       # Aufräumen des Blobs
                               نظام التشغيل.إزالة (blob_path)

                  إذا كانت العملية. رمز الإرجاع == 0:
logger.info(f"✔ SecurePacker: Struktur versteckt in {zip_name_outer} Gespeichert.")
                                                                      آخر:
                            logger.error(f"❌ ZIP Fehler: {process.stderr}")

                                  باستثناء الاستثناء كـ e:
                                    logger.error(f"❌ حزمة Fehler: {e}")

                                       تعريف_extract_password(key_path):
                                                                  يحاول:
                          مع open(key_path, \'r', encoding='utf-8') كـ f:
                                                             للخط في f:
                              إذا كان الخط.strip().startswith("#"):
                                  نظيف = line.strip().lstrip("#").strip()
                            فإذا كان نظيفاً: رجع نظيفاً
                                                                إلا : مر
                                                         عودة لا شيء