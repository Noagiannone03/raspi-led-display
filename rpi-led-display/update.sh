#!/bin/bash
#
# Script de mise à jour rapide
# Lance ce script si tu as déjà fait git pull pour récupérer les dernières modifications
#

echo "╔════════════════════════════════════════╗"
echo "║   MISE À JOUR DES SCRIPTS              ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Rend les scripts exécutables
echo "Mise à jour des permissions..."
chmod +x install.sh
chmod +x quick_start.sh
chmod +x examples.sh
chmod +x test_display.py
chmod +x display_text.py
chmod +x troubleshoot.py

echo ""
echo "✓ Mise à jour terminée !"
echo ""
echo "Vous pouvez maintenant utiliser:"
echo "  sudo python3 display_text.py \"BONJOUR\""
echo ""
