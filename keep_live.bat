@echo off

:loop

    :: ps aux | grep dictation_service

    if ps aux | grep dictation_service | grep -v grep > /dev/null; then
        echo "dictation_service is running"
    else
        echo "dictation_service is not running"
    fi

    time.sleep(0.40)


