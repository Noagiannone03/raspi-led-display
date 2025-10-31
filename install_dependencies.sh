#!/bin/bash

echo "╔════════════════════════════════════════════════════════╗"
echo "║   INSTALLATION DES DÉPENDANCES PYTHON                  ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Vérifie si on est root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Ce script doit être exécuté avec sudo"
    echo "Commande: sudo bash install_dependencies.sh"
    exit 1
fi

echo "Installation des outils Python nécessaires..."
echo ""

echo "[1/4] Mise à jour des paquets..."
apt-get update

echo ""
echo "[2/4] Installation de setuptools et pip..."
apt-get install -y python3-pip python3-setuptools

echo ""
echo "[3/4] Installation de Cython..."
apt-get install -y cython3

echo ""
echo "[4/4] Installation de Pillow..."
apt-get install -y python3-pillow

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║              VÉRIFICATION                              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Vérifie setuptools
python3 -c "import setuptools; print('✓ setuptools OK')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "✗ setuptools non installé"
else
    echo "✓ setuptools installé"
fi

# Vérifie cython
which cython3 >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "✗ cython3 non installé"
else
    echo "✓ cython3 installé"
fi

# Vérifie pip
which pip3 >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "✗ pip3 non installé"
else
    echo "✓ pip3 installé"
fi

# Vérifie PIL
python3 -c "from PIL import Image; print('✓ Pillow OK')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "✗ Pillow non installé"
else
    echo "✓ Pillow installé"
fi

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                 TERMINÉ !                              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Vous pouvez maintenant lancer :"
echo "  sudo bash install.sh"
echo ""
