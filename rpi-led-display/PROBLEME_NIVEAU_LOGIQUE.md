# ⚡ Problème de niveau logique 3.3V vs 5V

## 🔍 Votre problème : Les signaux A, B, C ne fonctionnent pas

**Symptôme confirmé par le diagnostic :**
- ✅ Les couleurs RGB fonctionnent (R1, G1, B1, R2, G2, B2)
- ❌ Les signaux d'adressage A, B, C ne fonctionnent PAS
- ❌ Toujours les mêmes 3 lignes qui s'allument

---

## 🎯 Cause probable : NIVEAU LOGIQUE INSUFFISANT

### Le problème

Votre panneau LED **ne détecte pas les signaux 3.3V** du Raspberry Pi !

| Composant | Niveau logique | Explication |
|-----------|----------------|-------------|
| **Raspberry Pi GPIO** | 3.3V | Les GPIO sortent du 3.3V |
| **Votre panneau LED** | **Nécessite 5V** | Les chips 74HC245 nécessitent >4V pour détecter un signal HIGH |

**Résultat :** Le panneau ne "voit" pas les changements sur A, B, C car le signal 3.3V est trop faible !

---

## 📊 Pourquoi ça affecte seulement A, B, C ?

C'est étrange mais logique :

| Signaux | Pourquoi ça marche / ça marche pas |
|---------|-------------------------------------|
| **R1, G1, B1, R2, G2, B2** | ✅ Fonctionnent partiellement car ce sont des signaux **statiques** (maintenu HIGH ou LOW longtemps) |
| **A, B, C** | ❌ Ne fonctionnent PAS car ce sont des signaux **rapides** qui changent constamment et nécessitent une détection précise |
| **CLK, LAT, OE** | ❓ Fonctionnent partiellement mais pas optimalement |

---

## 🔧 Solutions possibles

### ✅ SOLUTION 1 : Utiliser un HAT avec level shifter (RECOMMANDÉ)

Un HAT (Hardware Attached on Top) se branche sur le GPIO et convertit les 3.3V en 5V.

**HATs recommandés :**

1. **Adafruit RGB Matrix HAT ou Bonnet** (~15-25€)
   - Inclut un level shifter 74HCT245
   - Convertit 3.3V → 5V
   - Plug & play
   - Lien : https://www.adafruit.com/product/2345

2. **Electrodragon RGB LED Matrix Panel Driver Board** (~10€)
   - Alternative moins chère
   - Level shifter intégré

3. **Waveshare RGB Matrix Driver HAT**
   - Compatible Raspberry Pi
   - Level shifter intégré

**Avec un HAT :**
```python
options.hardware_mapping = 'adafruit-hat'  # Important !
```

---

### ⚙️ SOLUTION 2 : Tester avec --led-slowdown-gpio (GRATUIT, À TESTER D'ABORD)

Ralentir les signaux GPIO peut aider certains panneaux à détecter les signaux 3.3V.

**Créez ce fichier de test :**

```python
#!/usr/bin/env python3
# test_slowdown.py

import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
rgb_matrix_path = os.path.join(script_dir, 'rpi-rgb-led-matrix', 'bindings', 'python')
sys.path.insert(0, rgb_matrix_path)

from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time

# Testez différentes valeurs de slowdown
for slowdown in [0, 1, 2, 3, 4]:
    print(f"\n{'='*70}")
    print(f"TEST avec --led-slowdown-gpio={slowdown}")
    print(f"{'='*70}")

    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 2
    options.hardware_mapping = 'regular'
    options.gpio_slowdown = slowdown  # ← IMPORTANT
    options.brightness = 80

    try:
        matrix = RGBMatrix(options=options)

        # Test simple : 3 bandes de couleur
        width = matrix.width
        height = matrix.height

        print(f"Matrice : {width}×{height}")
        print("Affichage de 3 bandes de couleur...")

        # Rouge
        for y in range(height):
            for x in range(0, width // 3):
                matrix.SetPixel(x, y, 255, 0, 0)

        # Vert
        for y in range(height):
            for x in range(width // 3, 2 * width // 3):
                matrix.SetPixel(x, y, 0, 255, 0)

        # Bleu
        for y in range(height):
            for x in range(2 * width // 3, width):
                matrix.SetPixel(x, y, 0, 0, 255)

        time.sleep(3)

        matrix.Clear()

        print("✓ Test terminé")
        response = input(f"\nAvec slowdown={slowdown}, l'affichage était-il correct ? (o/N) : ")

        if response.lower() == 'o':
            print(f"\n🎉 SOLUTION TROUVÉE : gpio_slowdown = {slowdown}")
            print(f"\nUtilisez ce paramètre dans vos scripts :")
            print(f"options.gpio_slowdown = {slowdown}")
            break

    except Exception as e:
        print(f"Erreur : {e}")

    if slowdown < 4:
        input("\nAppuyez sur ENTRÉE pour le test suivant...")
```

**Lancez :**
```bash
sudo python3 test_slowdown.py
```

**Si ça marche avec slowdown=2 ou 3 :**
→ Ajoutez `options.gpio_slowdown = 2` dans tous vos scripts !

---

### 🔨 SOLUTION 3 : Construire un level shifter DIY (AVANCÉ)

Si vous ne voulez pas acheter de HAT, vous pouvez construire un level shifter avec des chips 74HCT245.

**Composants nécessaires :**
- 2× 74HCT245 (level shifter)
- Breadboard ou PCB prototype
- Fils de connexion

**Schéma :**
```
Raspberry Pi (3.3V)  →  74HCT245  →  Panneau LED (5V)
                          ↑
                       Alimenté en 5V
```

**Pins à convertir :**
- R1, G1, B1, R2, G2, B2 (6 pins)
- A, B, C (3 pins)
- CLK, LAT, OE (3 pins)
- **Total : 12 signaux**

**Note :** C'est technique, je recommande plutôt d'acheter un HAT.

---

### 🧪 SOLUTION 4 : Essayer d'autres GPIO (SI LES GPIO SONT GRILLÉS)

Si les GPIO 15, 16, 20 sont endommagés, vous pouvez essayer d'autres pins.

**GPIO disponibles sur Raspberry Pi 4 :**
- GPIO 5, 6, 12, 13, 19, 21, 26

**ATTENTION :** Cela nécessite de modifier le code source de rpi-rgb-led-matrix pour remapper les pins.

---

## 🧪 Test des GPIO (pour diagnostiquer si les GPIO sont grillés)

J'ai créé un script pour tester si les GPIO fonctionnent :

```bash
# DÉBRANCHEZ le panneau LED d'abord !
sudo python3 test_gpio_signals.py
```

Ce script :
1. Teste si les GPIO 15, 16, 20 peuvent envoyer des signaux
2. Alterne entre HIGH (3.3V) et LOW (0V)
3. Vous dit si un GPIO est probablement grillé

**Si vous avez un multimètre :**
- Mesurez les pins 10, 36, 38 pendant le test
- Vous devriez voir ~3.3V qui alterne avec 0V
- Si une pin reste à 0V constant → GPIO grillé

---

## 📋 Plan d'action recommandé

### Étape 1 : Tester avec gpio_slowdown (GRATUIT)

```bash
sudo python3 test_slowdown.py
```

**Si ça marche :** Problème résolu ! Ajoutez `options.gpio_slowdown = X` dans vos scripts.

**Si ça ne marche pas :** Passez à l'étape 2.

---

### Étape 2 : Tester les GPIO (vérifier s'ils sont grillés)

```bash
# Débranchez le panneau LED !
sudo python3 test_gpio_signals.py
```

**Si un GPIO ne fonctionne pas :** Vous devrez utiliser d'autres pins (solution 4).

**Si tous les GPIO fonctionnent :** Le problème est le niveau logique → Achetez un HAT.

---

### Étape 3 : Acheter un HAT avec level shifter (SOLUTION DÉFINITIVE)

**Recommandation :** Adafruit RGB Matrix HAT/Bonnet (~20€)

**Où acheter :**
- Adafruit : https://www.adafruit.com/product/2345
- Amazon
- Boutiques électronique locales

**Une fois installé :**
```python
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 1  # Souvent nécessaire même avec HAT
```

---

## 🎯 Résumé du problème

```
Raspberry Pi GPIO → 3.3V (trop faible pour votre panneau)
                      ↓
Panneau LED chips → Nécessite >4V pour détecter HIGH
                      ↓
Signaux A, B, C → Ne sont PAS détectés
                      ↓
Résultat → Toujours les mêmes lignes qui s'allument
```

---

## ✅ Solution rapide à tester MAINTENANT

Créez le fichier `test_slowdown.py` que j'ai fourni ci-dessus et lancez-le :

```bash
sudo python3 test_slowdown.py
```

**Testez avec slowdown 0, 1, 2, 3, 4 et voyez si l'affichage s'améliore.**

Si slowdown=2 ou 3 résout le problème → Vous avez de la chance, pas besoin d'acheter de HAT !

Si aucun slowdown ne fonctionne → Vous aurez besoin d'un HAT avec level shifter.

---

## 📚 Références

- Issue GitHub similaire : https://github.com/hzeller/rpi-rgb-led-matrix/issues/360
- Documentation level shifter : https://github.com/hzeller/rpi-rgb-led-matrix#readme
- HAT Adafruit : https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi

---

**🚀 Commencez par tester avec `test_slowdown.py` - c'est gratuit et ça peut marcher !**
