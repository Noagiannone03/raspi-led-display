#!/bin/bash

echo "╔════════════════════════════════════════════════════════╗"
echo "║     CORRECTION AUTOMATIQUE DU BUG PILLOW               ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Vérifie si on est dans le bon dossier
if [ ! -f "test_display.py" ]; then
    echo "✗ Erreur: Vous devez être dans le dossier rpi-led-display"
    echo "Commande: cd ~/raspi-led-display/rpi-led-display"
    exit 1
fi

echo "Ce script va corriger l'erreur :"
echo "  'ImagingCore' object has no attribute 'getim'"
echo ""
echo "Correction en cours..."
echo ""

# Sauvegarde des fichiers originaux
echo "[1/4] Sauvegarde des fichiers originaux..."
cp test_display.py test_display.py.backup
cp display_text.py display_text.py.backup
echo "✓ Sauvegardes créées"

# Correction de test_display.py
echo ""
echo "[2/4] Correction de test_display.py..."
sed -i 's/matrix\.SetImage(image)$/matrix.SetImage(image.convert('\''RGB'\''))/g' test_display.py
LINES_CHANGED=$(grep -c "image.convert('RGB')" test_display.py)
echo "✓ $LINES_CHANGED lignes corrigées"

# Correction de display_text.py
echo ""
echo "[3/4] Correction de display_text.py..."
sed -i 's/matrix\.SetImage(image)$/matrix.SetImage(image.convert('\''RGB'\''))/g' display_text.py
sed -i 's/matrix\.SetImage(cropped)$/matrix.SetImage(cropped.convert('\''RGB'\''))/g' display_text.py
LINES_CHANGED2=$(grep -c "convert('RGB')" display_text.py)
echo "✓ $LINES_CHANGED2 lignes corrigées"

# Vérification
echo ""
echo "[4/4] Vérification des corrections..."
if grep -q "image.convert('RGB')" test_display.py; then
    echo "✓ test_display.py corrigé"
else
    echo "✗ test_display.py non corrigé - essai manuel..."

    # Correction manuelle plus agressive
    python3 << 'EOF'
import re

# Correction de test_display.py
with open('test_display.py', 'r') as f:
    content = f.read()

# Remplace toutes les occurrences
content = re.sub(r'matrix\.SetImage\(image\)(?!\.)' , "matrix.SetImage(image.convert('RGB'))", content)

with open('test_display.py', 'w') as f:
    f.write(content)

print("✓ Correction Python appliquée à test_display.py")
EOF
fi

if grep -q "convert('RGB')" display_text.py; then
    echo "✓ display_text.py corrigé"
else
    echo "✗ display_text.py non corrigé - essai manuel..."

    # Correction manuelle plus agressive
    python3 << 'EOF'
import re

# Correction de display_text.py
with open('display_text.py', 'r') as f:
    content = f.read()

# Remplace les occurrences
content = re.sub(r'matrix\.SetImage\(image\)(?!\.)' , "matrix.SetImage(image.convert('RGB'))", content)
content = re.sub(r'matrix\.SetImage\(cropped\)(?!\.)' , "matrix.SetImage(cropped.convert('RGB'))", content)

with open('display_text.py', 'w') as f:
    f.write(content)

print("✓ Correction Python appliquée à display_text.py")
EOF
fi

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                 CORRECTION TERMINÉE                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Testez maintenant avec :"
echo "  sudo python3 test_display.py"
echo ""
echo "Si vous voyez encore l'erreur, les fichiers de sauvegarde sont :"
echo "  test_display.py.backup"
echo "  display_text.py.backup"
echo ""
