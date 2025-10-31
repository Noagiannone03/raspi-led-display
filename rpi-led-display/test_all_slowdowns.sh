#!/bin/bash
# Script pour tester automatiquement tous les slowdowns

echo "╔════════════════════════════════════════════════════════════╗"
echo "║       TEST AUTOMATIQUE DE TOUS LES SLOWDOWNS               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Ce script va tester slowdown 0, 1, 2, 3, 4"
echo "Pour chaque valeur, vérifiez l'affichage."
echo ""
read -p "Appuyez sur ENTRÉE pour commencer..."

for slowdown in 0 1 2 3 4
do
    echo ""
    echo "======================================================================="
    echo "TEST ${slowdown}/4 : gpio_slowdown = ${slowdown}"
    echo "======================================================================="
    echo ""

    sudo python3 test_slowdown_single.py $slowdown

    result=$?

    if [ $result -eq 0 ]; then
        echo ""
        echo "✓ Vous avez trouvé une configuration qui fonctionne !"
        exit 0
    fi

    if [ $slowdown -lt 4 ]; then
        echo ""
        read -p "Appuyez sur ENTRÉE pour tester slowdown=$((slowdown + 1))..."
    fi
done

echo ""
echo "======================================================================="
echo "AUCUN SLOWDOWN N'A RÉSOLU LE PROBLÈME"
echo "======================================================================="
echo ""
echo "Si aucune valeur de slowdown n'a fonctionné, cela signifie que"
echo "votre panneau nécessite des signaux 5V (pas 3.3V)."
echo ""
echo "📋 SOLUTION : Vous avez besoin d'un HAT avec level shifter"
echo ""
echo "HATs recommandés :"
echo "  1. Adafruit RGB Matrix HAT/Bonnet (~20€)"
echo "     → https://www.adafruit.com/product/2345"
echo ""
echo "  2. Electrodragon RGB LED Matrix Panel Driver (~10€)"
echo ""
echo "  3. Waveshare RGB Matrix Driver HAT"
echo ""
echo "Le HAT convertit les signaux 3.3V du Raspberry Pi en 5V"
echo "que votre panneau peut détecter correctement."
echo ""
echo "Une fois le HAT installé, utilisez :"
echo "  options.hardware_mapping = 'adafruit-hat'"
echo "  options.gpio_slowdown = 1"
echo ""
echo "======================================================================="
echo ""
echo "Lisez PROBLEME_NIVEAU_LOGIQUE.md pour plus de détails."
echo "======================================================================="
