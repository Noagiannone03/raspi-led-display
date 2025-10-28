#!/bin/bash

echo "======================================"
echo "Installation LED Matrix pour Raspberry Pi"
echo "======================================"
echo ""

# Mise à jour du système
echo "[1/6] Mise à jour du système..."
sudo apt-get update

# Installation des dépendances
echo "[2/6] Installation des dépendances..."
sudo apt-get install -y python3-dev python3-pillow

# Désactivation du son (nécessaire pour la matrice LED)
echo "[3/6] Désactivation du module son..."
sudo bash -c 'echo "blacklist snd_bcm2835" > /etc/modprobe.d/alsa-blacklist.conf'

# Clonage de la bibliothèque rpi-rgb-led-matrix
echo "[4/6] Téléchargement de rpi-rgb-led-matrix..."
if [ ! -d "rpi-rgb-led-matrix" ]; then
    git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
else
    echo "Bibliothèque déjà téléchargée"
fi

# Compilation de la bibliothèque
echo "[5/6] Compilation de la bibliothèque..."
cd rpi-rgb-led-matrix
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
cd ..

# Installation de Pillow si nécessaire
echo "[6/6] Installation de Pillow..."
pip3 install Pillow

echo ""
echo "======================================"
echo "Installation terminée !"
echo "======================================"
echo ""
echo "IMPORTANT: Redémarrez le Raspberry Pi pour que les changements prennent effet"
echo "Commande: sudo reboot"
echo ""
echo "Après le redémarrage, testez avec:"
echo "  sudo python3 test_display.py"
echo ""
