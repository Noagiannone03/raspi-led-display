#!/bin/bash
# Installation rapide et simple de rpi-rgb-led-matrix

echo "========================================"
echo "INSTALLATION SIMPLE RGB LED MATRIX"
echo "========================================"
echo ""

# Aller au home
cd ~

# Cloner si pas déjà fait
if [ ! -d "rpi-rgb-led-matrix" ]; then
    echo "1. Clonage de la bibliothèque officielle..."
    git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
else
    echo "1. La bibliothèque existe déjà, on l'utilise."
fi

cd rpi-rgb-led-matrix

# Compiler
echo ""
echo "2. Compilation (ça peut prendre 2-3 minutes)..."
make build-python HARDWARE_DESC=adafruit-hat
sudo make install-python

echo ""
echo "========================================"
echo "✓ INSTALLATION TERMINÉE !"
echo "========================================"
echo ""
echo "TESTE MAINTENANT avec les exemples fournis:"
echo ""
echo "1. TEST SIMPLE (carré):"
echo "   cd ~/rpi-rgb-led-matrix/bindings/python/samples"
echo "   sudo python3 simple-square.py --led-rows=32 --led-cols=64 --led-chain=2 --led-gpio-mapping=adafruit-hat --led-row-addr-type=3"
echo ""
echo "2. TEXTE DÉFILANT:"
echo "   cd ~/rpi-rgb-led-matrix/bindings/python/samples"
echo "   sudo python3 runtext.py --led-rows=32 --led-cols=64 --led-chain=2 --led-gpio-mapping=adafruit-hat --led-row-addr-type=3 --text='HELLO'"
echo ""
echo "3. HORLOGE:"
echo "   cd ~/rpi-rgb-led-matrix/bindings/python/samples"
echo "   sudo python3 clock.py --led-rows=32 --led-cols=64 --led-chain=2 --led-gpio-mapping=adafruit-hat --led-row-addr-type=3"
echo ""
echo "Si ça ne marche pas, essaie --led-row-addr-type=5 au lieu de 3"
echo ""
