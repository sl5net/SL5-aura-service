#!/bin/bash
# keep_lieve.sh
# test Okay it's good to see me online today and oh, and it's in English okay English is also nice
#  I can understand a little bit British English You need from the United States that can speak so well But sometimes need to listen to British or am I correct in English Undies from the United States It's And Trump is also from the United States

echo "keep_lieve.sh checks if dictation_service is running and restarts it when not"

while true
do
    # ps aux | grep dictation_service

    if pgrep -f dictation_service > /dev/null; then
        nothing=0
        # echo "dictation_service is running"
    else
        echo "dictation_service is not running, starting..."
        ./dictation_service
        sleep 10
    fi
    #time.sleep(0.40)
    sleep 0.41
done

