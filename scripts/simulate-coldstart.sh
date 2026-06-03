# end Engine & end Trino, end Docker
fuser -k 8830/tcp 8084/tcp
pkill -f aura_engine.py
docker stop trino

# stat aura
~/projects/py/STT/scripts/restart_venv_and_run-server.sh &
