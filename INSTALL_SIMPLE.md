# INSTALLATION SIMPLE - Méthode officielle

## Étape 1: Cloner la bibliothèque

```bash
cd ~
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
```

## Étape 2: Compiler

```bash
make build-python HARDWARE_DESC=adafruit-hat
sudo make install-python
```

## Étape 3: Tester avec les exemples fournis

### Test 1: Runtext (texte défilant)
```bash
cd examples-api-use
sudo ./demo -D0 --led-rows=32 --led-cols=64 --led-chain=2 --led-gpio-mapping=adafruit-hat --led-row-addr-type=3
```

### Test 2: Image
```bash
cd examples-api-use
sudo ./led-image-viewer --led-rows=32 --led-cols=64 --led-chain=2 --led-gpio-mapping=adafruit-hat --led-row-addr-type=3 ../examples-api-use/runtext.ppm
```

## Étape 4: Exemples Python déjà prêts

### Test Python 1: Texte défilant simple
```bash
cd bindings/python/samples
sudo python3 runtext.py --led-rows=32 --led-cols=64 --led-chain=2 --led-gpio-mapping=adafruit-hat --led-row-addr-type=3 --text="HELLO WORLD"
```

### Test Python 2: Image
```bash
cd bindings/python/samples
sudo python3 image-viewer.py --led-rows=32 --led-cols=64 --led-chain=2 --led-gpio-mapping=adafruit-hat --led-row-addr-type=3 ../../examples-api-use/runtext.ppm
```

### Test Python 3: Horloge
```bash
cd bindings/python/samples
sudo python3 clock.py --led-rows=32 --led-cols=64 --led-chain=2 --led-gpio-mapping=adafruit-hat --led-row-addr-type=3
```

## IMPORTANT: Le paramètre critique

**`--led-row-addr-type=3`** est OBLIGATOIRE pour ton panneau ABC !

Si ça ne marche pas avec 3, essaie:
- `--led-row-addr-type=5`
- `--led-gpio-slowdown=2` ou `3`

## Exemples complets disponibles dans le repo

Tous dans `rpi-rgb-led-matrix/bindings/python/samples/`:
- `runtext.py` - Texte défilant
- `image-viewer.py` - Affichage d'images
- `clock.py` - Horloge
- `pulsing-colors.py` - Couleurs pulsantes
- `rotating-block-generator.py` - Animation
- `simple-square.py` - Carré simple

## Commande minimale pour tester

```bash
cd ~/rpi-rgb-led-matrix/bindings/python/samples
sudo python3 simple-square.py --led-rows=32 --led-cols=64 --led-chain=2 --led-gpio-mapping=adafruit-hat --led-row-addr-type=3
```

C'est tout !
