# 🚀 Démarrage Rapide - Panneau P3 128×64-32S

Guide pas à pas pour faire fonctionner ton panneau LED avec le Raspberry Pi 4.

---

## 📋 Ce que tu as
- **Panneau**: P3 128×64-32S-V1.0 (DV08-210519)
- **Type**: HUB75 avec connecteur 16 pins
- **Résolution**: 128×64 pixels
- **Raspberry Pi**: 4 Model B

---

## ⚡ Étape 1: Alimentation (IMPORTANT !)

**NE PAS alimenter le panneau via le Raspberry Pi !**

1. Utilise une **alimentation 5V externe** (minimum 5A, recommandé 10A)
2. Branche l'alimentation au connecteur d'alimentation du panneau
3. **Connecte le GND de l'alimentation au GND du Raspberry Pi** (masse commune obligatoire)

```
[Alim 5V] ─→ [Panneau LED]
                  ↓
                 GND ─→ [Raspberry Pi GND]
```

---

## 🔌 Étape 2: Câblage HUB75 → Raspberry Pi

### Option A: Avec un HAT Adafruit (RECOMMANDÉ) ✅

Si tu as un [Adafruit RGB Matrix HAT](https://www.adafruit.com/product/2345):
1. Installe le HAT sur le Raspberry Pi
2. Branche le câble HUB75 sur le HAT
3. Dans les scripts, utilise: `hardware_mapping = 'adafruit-hat'`

### Option B: Câblage direct ⚠️

Si tu câbles directement, suis **EXACTEMENT** ce mapping:

| Signal HUB75 | GPIO RPi | Pin Physique | Câble |
|--------------|----------|--------------|-------|
| R1 | GPIO 17 | Pin 11 | Rouge partie haute |
| G1 | GPIO 18 | Pin 12 | Vert partie haute |
| B1 | GPIO 22 | Pin 15 | Bleu partie haute |
| R2 | GPIO 23 | Pin 16 | Rouge partie basse |
| G2 | GPIO 24 | Pin 18 | Vert partie basse |
| B2 | GPIO 25 | Pin 22 | Bleu partie basse |
| A | GPIO 15 | Pin 10 | Adressage ligne |
| B | GPIO 16 | Pin 36 | Adressage ligne |
| C | GPIO 20 | Pin 38 | Adressage ligne |
| D | GPIO 21 | Pin 40 | Adressage ligne |
| E | GPIO 26 | Pin 37 | Adressage ligne (pour scan 1/32) |
| CLK | GPIO 11 | Pin 23 | Clock |
| LAT | GPIO 27 | Pin 13 | Latch |
| OE | GPIO 4 | Pin 7 | Output Enable |
| GND | GND | Pins 6,9,14,20,25,30,34,39 | Masse |

**📘 Guide complet**: Lis `CABLAGE_RASPBERRY_PI.md` pour les détails.

---

## 🧪 Étape 3: Test du câblage

Une fois tout branché, teste que le câblage est bon:

```bash
cd /Users/noagiannone/Documents/moduleair-pro-tests/rpi-led-display
sudo python3 test_wiring.py
```

Ce script va:
1. Afficher chaque couleur séparément (R1, G1, B1, R2, G2, B2)
2. Montrer un motif de test
3. Tester l'adressage des lignes
4. Te dire exactement quel câble est mal branché si il y a un problème

**✓ Si toutes les couleurs s'affichent correctement**, passe à l'étape suivante.

**✗ Si des couleurs manquent ou que c'est bizarre**, vérifie le câblage des pins concernées (le script te dit lesquelles).

---

## 🎯 Étape 4: Trouver la bonne configuration

Maintenant qu'on sait que le câblage est bon, il faut trouver les bons paramètres logiciels:

```bash
sudo python3 test_p3_128x64.py
```

Le script va tester **8 configurations différentes**. Pour chaque test:

1. Regarde l'écran LED
2. Vérifie que les couleurs sont bonnes (rouge, vert, bleu, blanc)
3. **Vérifie surtout que l'affichage couvre TOUT l'écran (128 pixels de large)**

Quand tu vois un affichage correct qui couvre tout l'écran:
- Tape `o` puis ENTRÉE
- **Note les paramètres affichés** (tu en auras besoin après)

---

## 📝 Étape 5: Utiliser la bonne configuration

Une fois la bonne config trouvée, ouvre le fichier `display_text_128x64.py`:

```bash
nano display_text_128x64.py
```

Trouve la section marquée `CONFIGURATION À AJUSTER` (vers la ligne 40) et remplace avec les paramètres trouvés.

Par exemple, si le test a trouvé:
```python
rows = 32
cols = 64
chain_length = 2
row_address_type = 0
hardware_mapping = 'regular'
```

Remplace dans `display_text_128x64.py` avec ces valeurs.

---

## 🎨 Étape 6: Tester l'affichage de texte

Teste l'affichage de texte:

```bash
# Texte simple
sudo python3 display_text_128x64.py "HELLO"

# Texte en rouge
sudo python3 display_text_128x64.py "MODULEAIR" --color 255,0,0

# Texte défilant
sudo python3 display_text_128x64.py "HELLO WORLD" --scroll

# Avec luminosité réduite
sudo python3 display_text_128x64.py "TEST" --brightness 40
```

---

## 🎉 C'est bon !

Si tout fonctionne, tu peux maintenant:

1. Utiliser `display_text_128x64.py` pour afficher du texte
2. Créer tes propres scripts en utilisant la même configuration
3. Consulter les exemples de la librairie:
   ```bash
   cd rpi-rgb-led-matrix/examples-api-use
   ls *.py
   ```

---

## 🐛 Dépannage

### Rien ne s'affiche
1. Lance avec `sudo` (obligatoire pour accéder aux GPIO)
2. Vérifie l'alimentation 5V du panneau
3. Vérifie que les GND sont bien connectés
4. Lance `test_wiring.py` pour diagnostiquer

### Des traits verticaux blanc/rouge/vert sur la gauche
→ C'est un problème de **câblage** ou de **configuration**
- Si câblage direct: vérifie le mapping des GPIO (suis `CABLAGE_RASPBERRY_PI.md`)
- Essaie avec `hardware_mapping = 'adafruit-hat'` si tu as un HAT

### Les couleurs sont bizarres
→ Problème de câblage des pins RGB
- Lance `test_wiring.py` pour identifier quelle pin est mal branchée
- Vérifie R1, G1, B1, R2, G2, B2

### Seulement la moitié du panneau fonctionne
→ Vérifier `chain_length` (devrait être 2 pour un panneau 128×64)

### L'image est décalée/bizarre
→ Mauvais paramètres d'adressage
- Essaie différents `row_address_type` (0, 1, 2)
- Vérifie le câblage de A, B, C, D, E

---

## 📚 Fichiers du projet

- `DEMARRAGE_RAPIDE.md` ← Tu es ici
- `CABLAGE_RASPBERRY_PI.md` - Guide détaillé du câblage
- `PANNEAU_P3_128x64.md` - Documentation technique du panneau
- `test_wiring.py` - Test du câblage
- `test_p3_128x64.py` - Recherche de la bonne configuration
- `display_text_128x64.py` - Affichage de texte

---

## 🆘 Besoin d'aide ?

1. Relis les guides dans l'ordre:
   - `CABLAGE_RASPBERRY_PI.md` (câblage)
   - `PANNEAU_P3_128x64.md` (configuration)

2. Lance les scripts de test:
   ```bash
   sudo python3 test_wiring.py      # Test du câblage
   sudo python3 test_p3_128x64.py   # Test de la configuration
   ```

3. Envoie une photo de ce que tu vois sur l'écran pour diagnostiquer le problème
