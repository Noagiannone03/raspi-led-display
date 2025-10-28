#!/bin/bash
#
# Exemples d'utilisation de l'écran LED
# Exécutez ce script pour voir différents exemples
#

echo "╔════════════════════════════════════════════════════════╗"
echo "║         EXEMPLES D'UTILISATION LED MATRIX              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Vérifie si on est root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Ce script doit être exécuté avec sudo"
    echo "Commande: sudo bash examples.sh"
    exit 1
fi

echo "Cet exemple va montrer différents affichages."
echo "Appuyez sur Ctrl+C à tout moment pour arrêter."
echo ""
read -p "Appuyez sur ENTRÉE pour commencer..."

# Exemple 1: Texte simple blanc
echo ""
echo "[Exemple 1/8] Texte simple blanc"
python3 display_text.py "HELLO LED!" --duration 5

# Exemple 2: Texte rouge
echo ""
echo "[Exemple 2/8] Texte rouge"
python3 display_text.py "ROUGE" --color 255,0,0 --duration 5

# Exemple 3: Texte vert
echo ""
echo "[Exemple 3/8] Texte vert"
python3 display_text.py "VERT" --color 0,255,0 --duration 5

# Exemple 4: Texte bleu
echo ""
echo "[Exemple 4/8] Texte bleu"
python3 display_text.py "BLEU" --color 0,0,255 --duration 5

# Exemple 5: Texte cyan
echo ""
echo "[Exemple 5/8] Texte cyan"
python3 display_text.py "CYAN" --color 0,255,255 --duration 5

# Exemple 6: Texte jaune
echo ""
echo "[Exemple 6/8] Texte jaune"
python3 display_text.py "JAUNE" --color 255,255,0 --duration 5

# Exemple 7: Heure actuelle
echo ""
echo "[Exemple 7/8] Heure actuelle"
CURRENT_TIME=$(date +"%H:%M:%S")
python3 display_text.py "$CURRENT_TIME" --color 255,255,0 --duration 5

# Exemple 8: Texte défilant
echo ""
echo "[Exemple 8/8] Texte défilant (10 secondes)"
timeout 10 python3 display_text.py "Ceci est un exemple de texte qui défile sur l'écran LED!" --scroll --color 0,255,255 --speed 0.04

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                  EXEMPLES TERMINÉS                     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Pour créer vos propres affichages, utilisez:"
echo "  sudo python3 display_text.py \"Votre texte\" [options]"
echo ""
echo "Consultez le README.md pour plus d'informations !"
