#!/bin/bash
# Standalone fzf transform reload test script

INIT_LIST="file1:1 | hello\nfile1:2 | world\nfile2:1 | foo\nfile2:2 | bar"

echo -e "$INIT_LIST" | fzf \
    --bind="start:execute-silent(echo empty > /tmp/fzf_test_state)" \
    --bind="change:transform:
        q='{q}'
        state=\$(cat /tmp/fzf_test_state 2>/dev/null || echo empty)
        if [ -n \"\$q\" ] && [ \"\$state\" = \"empty\" ]; then
            echo \"non-empty\" > /tmp/fzf_test_state
            echo 'reload(echo -e \"FULL LIST:\nfile1:1 | hello\nfile1:2 | world\nfile2:1 | foo\nfile2:2 | bar\")'
        elif [ -z \"\$q\" ] && [ \"\$state\" = \"non-empty\" ]; then
            echo \"empty\" > /tmp/fzf_test_state
            echo 'reload(echo -e \"SCOPED LIST:\nfile1:1 | hello\n〃:2 | world\nfile2:1 | foo\n〃:2 | bar\")'
        fi"
