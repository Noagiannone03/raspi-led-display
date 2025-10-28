#!/bin/bash

echo "╔════════════════════════════════════════════════════════╗"
echo "║     RÉPARATION DE L'INSTALLATION                       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Vérifie si on est root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Ce script doit être exécuté avec sudo"
    echo "Commande: sudo bash fix_install.sh"
    exit 1
fi

# Vérifie si le dossier existe
if [ ! -d "rpi-rgb-led-matrix" ]; then
    echo "✗ Le dossier rpi-rgb-led-matrix n'existe pas"
    echo "   Exécutez d'abord: sudo bash install.sh"
    exit 1
fi

echo "Ce script va réparer l'installation du module Python."
echo ""
echo "Étapes :"
echo "  1. Nettoyage des fichiers compilés"
echo "  2. Recompilation du module Python"
echo "  3. Installation globale du module"
echo ""
read -p "Appuyez sur ENTRÉE pour continuer..."

echo ""
echo "[1/5] Nettoyage..."
cd rpi-rgb-led-matrix/bindings/python
make clean
rm -rf build dist *.egg-info

echo ""
echo "[2/5] Compilation du module Python..."
make build-python PYTHON=$(which python3)

echo ""
echo "[3/5] Installation du module Python (globalement)..."
python3 setup.py install

echo ""
echo "[4/5] Vérification de l'installation..."
cd ../../..

# Test simple
python3 -c "from rgbmatrix import RGBMatrix; print('✓ Import réussi!')" 2>&1
RESULT=$?

echo ""
echo "[5/5] Test avec le chemin du script..."
python3 -c "import sys; sys.path.insert(0, 'rpi-rgb-led-matrix/bindings/python'); from rgbmatrix import RGBMatrix; print('✓ Import avec chemin réussi!')" 2>&1
RESULT2=$?

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                   RÉSULTAT                             ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

if [ $RESULT -eq 0 ] || [ $RESULT2 -eq 0 ]; then
    echo "✓ Réparation réussie !"
    echo ""
    echo "Vous pouvez maintenant tester avec :"
    echo "  sudo python3 test_display.py"
    echo ""
else
    echo "✗ La réparation a échoué"
    echo ""
    echo "Essayez une installation complète :"
    echo "  cd .."
    echo "  rm -rf rpi-led-display"
    echo "  git clone <VOTRE_REPO>"
    echo "  cd rpi-led-display"
    echo "  sudo bash install.sh"
    echo ""
fi
