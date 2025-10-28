#!/bin/bash

echo "╔════════════════════════════════════════════════════════╗"
echo "║     VÉRIFICATION DÉTAILLÉE DE L'INSTALLATION           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

echo "[1/6] Vérification du dossier rpi-rgb-led-matrix..."
if [ -d "rpi-rgb-led-matrix" ]; then
    echo "✓ Dossier trouvé"
else
    echo "✗ Dossier non trouvé"
    echo "   Exécutez: sudo bash install.sh"
    exit 1
fi

echo ""
echo "[2/6] Vérification de la compilation..."
if [ -f "rpi-rgb-led-matrix/lib/librgbmatrix.so.1" ]; then
    echo "✓ Bibliothèque C++ compilée"
else
    echo "✗ Bibliothèque C++ non compilée"
fi

echo ""
echo "[3/6] Vérification du module Python..."
cd rpi-rgb-led-matrix/bindings/python

# Vérifie si rgbmatrix.so existe
if [ -f "rgbmatrix/core.so" ]; then
    echo "✓ Module Python trouvé: rgbmatrix/core.so"
    ls -lh rgbmatrix/core.so
elif [ -f "build/lib.linux-armv7l-3.*/rgbmatrix/core.so" ] || [ -f "build/lib.linux-aarch64-3.*/rgbmatrix/core.so" ]; then
    echo "✓ Module Python compilé mais pas installé"
    echo "   Chemin: $(find build -name core.so 2>/dev/null | head -1)"
else
    echo "✗ Module Python non trouvé"
fi

cd ../../..

echo ""
echo "[4/6] Test d'import Python (utilisateur normal)..."
python3 -c "import sys; sys.path.insert(0, 'rpi-rgb-led-matrix/bindings/python'); from rgbmatrix import RGBMatrix" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Import réussi pour l'utilisateur normal"
else
    echo "✗ Import échoué pour l'utilisateur normal"
fi

echo ""
echo "[5/6] Test d'import Python (root/sudo)..."
sudo python3 -c "import sys; sys.path.insert(0, 'rpi-rgb-led-matrix/bindings/python'); from rgbmatrix import RGBMatrix" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Import réussi pour root"
else
    echo "✗ Import échoué pour root"
    echo "   C'est probablement le problème !"
fi

echo ""
echo "[6/6] Vérification des fichiers nécessaires..."
FILES=(
    "rpi-rgb-led-matrix/lib/librgbmatrix.so.1"
    "rpi-rgb-led-matrix/bindings/python/rgbmatrix/__init__.py"
    "rpi-rgb-led-matrix/bindings/python/setup.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file manquant"
    fi
done

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                   RÉSULTAT                             ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Si l'import échoue pour root, la solution est :"
echo ""
echo "  cd rpi-rgb-led-matrix/bindings/python"
echo "  sudo python3 setup.py install"
echo "  cd ../../.."
echo ""
echo "Ou relancez l'installation complète :"
echo ""
echo "  sudo bash install.sh"
echo ""
