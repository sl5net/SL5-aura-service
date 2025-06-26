exit 0

# list running
pgrep -f live_transcribe.py
1223

ps aux | grep '[l]ive_transcribe.py'

# kill the service. option 1
kill 1223


# kill the service. option 2
pkill -f live_transcribe.py

# start
python3 ~/projects/py/speak_server/live_transcribe.py &
/scripts/activate-venv_and_run-server.sh &





