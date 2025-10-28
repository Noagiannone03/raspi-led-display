#!/bin/bash
#
# Script de démarrage rapide pour l'écran LED
# Usage: ./quick_start.sh "Votre texte"
#

TEXT="${1:-HELLO LED}"

echo "╔════════════════════════════════════════╗"
echo "║   QUICK START - LED MATRIX 64x64       ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "Texte: $TEXT"
echo ""

# Vérifie si on est root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Ce script doit être exécuté avec sudo"
    echo "Commande: sudo ./quick_start.sh \"$TEXT\""
    exit 1
fi

# Vérifie si la lib est installée
if [ ! -d "rpi-rgb-led-matrix" ]; then
    echo "❌ La bibliothèque n'est pas installée"
    echo "Exécutez d'abord: sudo bash install.sh"
    exit 1
fi

echo "✓ Lancement de l'affichage..."
echo ""

python3 display_text.py "$TEXT" --scroll

echo ""
echo "✓ Terminé !"
