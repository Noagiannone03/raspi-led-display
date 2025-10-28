#!/bin/bash

echo "╔════════════════════════════════════════════════════════╗"
echo "║   CORRECTION DES PERMISSIONS (OPTIONNEL)               ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Vérifie si on est root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Ce script doit être exécuté avec sudo"
    echo "Commande: sudo bash fix_permissions.sh"
    exit 1
fi

echo "Ce script corrige l'avertissement sur les permissions temps réel."
echo ""
echo "Avertissement actuel :"
echo "  'Can't set realtime thread priority=99: Operation not permitted'"
echo ""
echo "Cela n'empêche pas l'écran de fonctionner, mais peut causer"
echo "un léger scintillement. Cette correction améliore la stabilité."
echo ""

read -p "Voulez-vous appliquer la correction ? (o/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Oo]$ ]]; then
    echo "Correction annulée."
    exit 0
fi

echo ""
echo "[1/2] Application de la capacité cap_sys_nice à Python..."
setcap 'cap_sys_nice=eip' $(which python3)

if [ $? -eq 0 ]; then
    echo "✓ Capacité appliquée"
else
    echo "✗ Échec de l'application"
    exit 1
fi

echo ""
echo "[2/2] Vérification..."
getcap $(which python3)

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                 CORRECTION TERMINÉE                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "L'avertissement ne devrait plus apparaître."
echo "Testez avec:"
echo "  sudo python3 test_display.py"
echo ""
