#Mac OS

## carpeta mkdir y compilar el archivo Plist:

```sh

mkdir -p ~/Library/LaunchAgents
cat > ~/Library/LaunchAgents/com.sl5.aura-engine.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sl5.aura-engine</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura &amp;&amp; touch /tmp/sl5_aura/sl5net_aura_project_root; /Users/USERNAME/SL5-aura-service/scripts/restart_venv_and_run-server.sh; fi</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/Users/USERNAME/SL5-aura-service/aura_engine.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/USERNAME/SL5-aura-service/aura_engine.log</string>
</dict>
</plist>
EOF

```

```sh
launchctl load ~/Library/LaunchAgents/com.sl5.aura-engine.plist
```

## prueba


```
launchctl start com.sl5.aura-engine
tail -f ~/SL5-aura-service/aura_engine.log
```

## prueba
```
launchctl list | grep sl5
```

## cambiar
```
launchctl unload ~/Library/LaunchAgents/com.sl5.aura-engine.plist
```