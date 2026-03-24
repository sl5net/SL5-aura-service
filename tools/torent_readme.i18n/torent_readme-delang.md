Das ist ein bekanntes Problem — libtorrent ist kein reines Python-Paket, es braucht die C++-Bibliothek als Unterbau. Auf Arch (und Arch-basierten Distros wie Manjaro) läuft das anders als pip:
bashsudo pacman -S python-libtorrent
Das installiert sowohl die C++-Bibliothek (libtorrent-rasterbar) als auch die Python-Bindings in einem Schritt über den offiziellen Paketmanager.

sudo pacman -S python-libtorrent

Danach testen:
bashpython3 -c „libtorrent importieren; drucken(libtorrent.version)“


#########################################

Ich möchte Repo Github sl5net Aura über BitTorrent anbieten

(BitTorrent-Client, Deluge, qBittorrent ... jeder Client, den Sie mögen).
  

Warum verwendet 0 n. Chr. Torrents?

Der einfachste Weg, eine Datei zu verteilen, besteht darin, sie auf einem zentralen Server abzulegen. Dann können alle Benutzer es von diesem Server herunterladen. Wenn aber viele Leute die Dateien herunterladen, reicht ein Server nicht aus und die Platzierung verschiedener Server auf der ganzen Welt ist kostspielig. Da es sich um ein kostenloses Spiel handelt, können wir diese Kosten nicht übernehmen.

Ich habe es leider nirgendwo online gespeichert (vermutlich die Models zu groß)

Hast du eine Idee was ich machen kann