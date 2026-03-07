### مستند تخفيض السعر: `STT/settings/maps/plugins/standard_actions/path_navigator/CLI_Workflow_Tools.md`

```markdown
CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY

# CLI Workflow Tools: FZF to Kate Integration

This document describes a high-efficiency command-line workflow that leverages the fuzzy file search implemented in the `path_navigator` plugin to quickly open files in the Kate editor.

## 1. Fast File Selection (Aura Command)

The `path_navigator` action uses the following Git-aware `fzf` command. Its purpose is to output a file path directly into the system clipboard.

**Command Logic:**
- Uses `git ls-files` inside a Git repository (excludes ignored files).
- Falls back to `find . -type f` outside a Git repository.
- Outputs the selected path to the clipboard using `xclip -selection clipboard`.

## 2. Fast File Execution (The 'k' Function)

To complete the loop, the custom shell function `k` is used. This function takes the path from the clipboard and instantly opens the file in `kate`.

### Implementation

Add the following function to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
# وظيفة فتح مسار الملف من حافظة النظام في كيت
                                                              وظيفة ك {
                           # تحقق مما إذا كان xclip متاحًا
                                لو ! الأمر -v xclip &> /dev/null; ثم
         صدى "خطأ: xclip مطلوب ولكن لم يتم تثبيته."
                                                               العودة 1
                                                                       فاي
                                              اكس سبيس بريك اكس
                               # 1. احصل على محتوى الحافظة
               CLIPBOARD_CONTENT=$(xclip -selection clipboard -o 2>/dev/null)
                                              اكس سبيس بريك اكس
                  # تحقق مما إذا كانت الحافظة فارغة
                                  إذا [ -z "${CLIPBOARD_CONTENT}" ]؛ ثم
 صدى "خطأ: الحافظة فارغة. لا يوجد شيء لفتحه."
                                                               العودة 1
                                                                       فاي

# 2. التحقق من وجود محتوى متعدد الأسطر (يضمن استخدام مسار ملف واحد فقط)
                          LINE_COUNT=$(صدى "${CLIPBOARD_CONTENT}" | wc -l)
                                              اكس سبيس بريك اكس
                                       إذا [ "${LINE_COUNT}" -gt 1 ]; ثم
صدى "خطأ: تحتوي الحافظة على ${LINE_COUNT} من الأسطر. يتم دعم مسارات الملفات ذات السطر الواحد فقط."
                                                               العودة 1
                                                                       فاي
                                              اكس سبيس بريك اكس
# 3. اطبع الأمر قبل التنفيذ (ملاحظات المستخدم)
                                     صدى "كيت \"${CLIPBOARD_CONTENT}\""
                                              اكس سبيس بريك اكس
                                           # 4. التنفيذ النهائي
# تتعامل علامات الاقتباس المزدوجة حول المحتوى مع أسماء الملفات بمسافات بشكل صحيح.
# يقوم "&" بتشغيل الأمر في الخلفية، مما يؤدي إلى تحرير الوحدة الطرفية.
                                              كيت "${CLIPBOARD_CONTENT}" &
                                                                            }
```

### Usage

1.  Use the `path_navigator` command (e.g., type `search file` in your trigger tool).
2.  Find and select the desired file (e.g., `src/main/config.py`).
3.  In your terminal, type `k` and press **ENTER**.
4.  The file opens instantly in Kate.
```