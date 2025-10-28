#!/bin/bash

echo "======================================"
echo "Installation LED Matrix pour Raspberry Pi"
echo "======================================"
echo ""

# Vérifie si on est root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Ce script doit être exécuté avec sudo"
    echo "Commande: sudo bash install.sh"
    exit 1
fi

# Mise à jour du système
echo "[1/8] Mise à jour du système..."
apt-get update

# Installation des dépendances
echo "[2/8] Installation des dépendances..."
apt-get install -y python3-dev python3-pillow python3-pip python3-setuptools cython3 git build-essential

# Désactivation du son (nécessaire pour la matrice LED)
echo "[3/8] Désactivation du module son..."
bash -c 'echo "blacklist snd_bcm2835" > /etc/modprobe.d/alsa-blacklist.conf'

# Clonage de la bibliothèque rpi-rgb-led-matrix
echo "[4/8] Téléchargement de rpi-rgb-led-matrix..."
if [ ! -d "rpi-rgb-led-matrix" ]; then
    git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
else
    echo "Bibliothèque déjà téléchargée"
    cd rpi-rgb-led-matrix
    git pull
    cd ..
fi

# Compilation de la bibliothèque C++
echo "[5/8] Compilation de la bibliothèque C++..."
cd rpi-rgb-led-matrix
make clean
make

# Compilation du module Python
echo "[6/8] Compilation du module Python..."
cd bindings/python
make clean
make build-python PYTHON=$(which python3)

# Installation du module Python (globalement avec sudo)
echo "[7/8] Installation du module Python..."
python3 setup.py install

cd ../../..

# Installation de Pillow si nécessaire
echo "[8/8] Installation de Pillow..."
pip3 install --break-system-packages Pillow 2>/dev/null || pip3 install Pillow

echo ""
echo "======================================"
echo "Vérification de l'installation..."
echo "======================================"
echo ""

# Test d'import
python3 -c "import sys; sys.path.insert(0, 'rpi-rgb-led-matrix/bindings/python'); from rgbmatrix import RGBMatrix; print('✓ Module importé avec succès!')" 2>&1
IMPORT_RESULT=$?

if [ $IMPORT_RESULT -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "Installation terminée avec succès !"
    echo "======================================"
    echo ""
    echo "IMPORTANT: Redémarrez le Raspberry Pi pour que les changements prennent effet"
    echo "Commande: sudo reboot"
    echo ""
    echo "Après le redémarrage, testez avec:"
    echo "  sudo python3 test_display.py"
    echo ""
else
    echo ""
    echo "⚠️  AVERTISSEMENT ⚠️"
    echo "L'installation s'est terminée mais le module ne peut pas être importé."
    echo ""
    echo "Essayez de redémarrer et testez à nouveau."
    echo "Si le problème persiste, exécutez:"
    echo "  bash verify_installation.sh"
    echo ""
fi
