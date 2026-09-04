__KOD_BLOKU_0__
modele płyt CD
wget -q --show-progress https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
rozpakuj -q vosk-model-small-de-0.15.zip
rm vosk-model-small-de-0.15.zip
płyta CD ..
__KOD_BLOKU_1__
echo "vosk-model-small-de-0.15" > config/nazwa_modelu.txt
__KOD_BLOKU_2__
PRELOAD_MODELS = ["model-vosk .. "]
__KOD_BLOKU_3__
zamiana sudo -a
sudo fallocate -l 8G /plik wymiany
sudo chmod 600 / plik wymiany
sudo mkswap /plik wymiany
sudo zamiana/plik wymiany
echo '/swapfile brak wymiany SW 0 0' | sudo tee -a /etc/fstab
__KOD_BLOKU_4__
sysctl vm.swapusage
__KOD_BLOKU_5__