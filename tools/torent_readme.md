Das ist ein bekanntes Problem — libtorrent ist kein reines Python-Paket, es braucht die C++-Bibliothek als Unterbau. Auf Arch (und Arch-basierten Distros wie Manjaro) läuft das anders als pip:
bashsudo pacman -S python-libtorrent
Das installiert sowohl die C++-Bibliothek (libtorrent-rasterbar) als auch die Python-Bindings in einem Schritt über den offiziellen Paketmanager.

sudo pacman -S python-libtorrent

Danach testen:
bashpython3 -c "import libtorrent; print(libtorrent.version)"


###########################################

i want offer Repo Github sl5net aura via BitTorrent

    (BitTorrent client, Deluge, qBittorrent ... any client you like). 
    

Why does 0 A.D. use torrents?

The easiest way to distribute a file is by putting it on a central server. Then all users can download it from that server. But when there are many people downloading the files, one server is not sufficient, and placing different servers around the world is costly. As a free game, we’re not able to pay for these costs.

Ich habe es leider nirgendwo online gespeichert (vermutlich die Models zu groß) 

hast du eine Idee was ich machen kann
