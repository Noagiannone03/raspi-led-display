# Guide de câblage HUB75 → Raspberry Pi 4

## IMPORTANT: Tu as 2 options

### Option 1: Utiliser un HAT Adafruit (RECOMMANDÉ) ✅
C'est **beaucoup plus simple** et évite les erreurs de câblage.
- [Adafruit RGB Matrix HAT](https://www.adafruit.com/product/2345)
- Tu branches le connecteur HUB75 directement sur le HAT
- Dans le code, tu utilises: `hardware_mapping = 'adafruit-hat'`

### Option 2: Câblage direct (plus complexe) ⚠️
Si tu veux câbler directement, voici les connexions exactes.

---

## Câblage Direct pour Raspberry Pi 4 Model B

### Ton connecteur HUB75 a ces pins:
```
R1    G1       (données couleur - partie haute du panneau)
B1    GND
R2    G2       (données couleur - partie basse du panneau)
B2    GND
A     B        (adressage des lignes)
C     D        (adressage des lignes)
CLK   LAT      (signaux de contrôle)
OE    GND      (output enable)
```

Pour un panneau 1/32 scan, tu as aussi une pin **E** pour l'adressage.

---

## Mapping des GPIO (Raspberry Pi → HUB75)

### 🔴 MAPPING "REGULAR" (par défaut)

Voici le câblage exact pour le mapping `hardware_mapping = 'regular'`:

| Signal HUB75 | GPIO Raspberry Pi | Pin Physique |
|--------------|-------------------|--------------|
| **R1** (Rouge 1) | GPIO 17 | Pin 11 |
| **G1** (Vert 1) | GPIO 18 | Pin 12 |
| **B1** (Bleu 1) | GPIO 22 | Pin 15 |
| **R2** (Rouge 2) | GPIO 23 | Pin 16 |
| **G2** (Vert 2) | GPIO 24 | Pin 18 |
| **B2** (Bleu 2) | GPIO 25 | Pin 22 |
| **A** (Row A) | GPIO 15 | Pin 10 |
| **B** (Row B) | GPIO 16 | Pin 36 |
| **C** (Row C) | GPIO 20 | Pin 38 |
| **D** (Row D) | GPIO 21 | Pin 40 |
| **E** (Row E)* | GPIO 26 | Pin 37 |
| **CLK** (Clock) | GPIO 11 | Pin 23 |
| **LAT** (Latch) | GPIO 27 | Pin 13 |
| **OE** (Output Enable) | GPIO 4 | Pin 7 |
| **GND** | GND | Pin 6, 9, 14, 20, 25, 30, 34, 39 |

**Note**: La pin **E** n'est utilisée que pour les panneaux avec plus de 16 lignes (scan 1/32 ou 1/64).

---

## Schéma visuel du Raspberry Pi 4

```
    3V3  (1) (2)  5V
  GPIO2  (3) (4)  5V
  GPIO3  (5) (6)  GND ← GND
  GPIO4  (7) (8)  GPIO14
    GND  (9) (10) GPIO15 ← A
 GPIO17 (11) (12) GPIO18 ← G1
        ← R1
 GPIO27 (13) (14) GND ← GND
        ← LAT
 GPIO22 (15) (16) GPIO23 ← R2
        ← B1
    3V3 (17) (18) GPIO24 ← G2
 GPIO10 (19) (20) GND ← GND
  GPIO9 (21) (22) GPIO25 ← B2
 GPIO11 (23) (24) GPIO8
        ← CLK
    GND (25) (26) GPIO7
  GPIO0 (27) (28) GPIO1
  GPIO5 (29) (30) GND
  GPIO6 (31) (32) GPIO12
 GPIO13 (33) (34) GND
 GPIO19 (35) (36) GPIO16 ← B
 GPIO26 (37) (38) GPIO20 ← C
        ← E
    GND (39) (40) GPIO21 ← D
```

---

## 🔧 Câblage étape par étape

### 1. **Signaux de données (RGB)**

Relie les câbles de couleur:

```bash
HUB75         Raspberry Pi 4
------        ---------------
R1    →       GPIO 17 (Pin 11)
G1    →       GPIO 18 (Pin 12)
B1    →       GPIO 22 (Pin 15)

R2    →       GPIO 23 (Pin 16)
G2    →       GPIO 24 (Pin 18)
B2    →       GPIO 25 (Pin 22)
```

### 2. **Adressage des lignes (Row Select)**

Pour ton panneau 1/32 scan, tu as besoin de A, B, C, D, **et E**:

```bash
HUB75         Raspberry Pi 4
------        ---------------
A     →       GPIO 15 (Pin 10)
B     →       GPIO 16 (Pin 36)
C     →       GPIO 20 (Pin 38)
D     →       GPIO 21 (Pin 40)
E     →       GPIO 26 (Pin 37)  ← IMPORTANT pour scan 1/32 !
```

### 3. **Signaux de contrôle**

```bash
HUB75         Raspberry Pi 4
------        ---------------
CLK   →       GPIO 11 (Pin 23)
LAT   →       GPIO 27 (Pin 13)
OE    →       GPIO 4  (Pin 7)
```

### 4. **Masse (GND)**

Connecte **TOUS les GND ensemble**:
```bash
HUB75 GND → Raspberry Pi GND (utilise plusieurs pins GND pour la stabilité)
```

Pins GND disponibles: 6, 9, 14, 20, 25, 30, 34, 39

---

## ⚡ ATTENTION - Alimentation

**NE PAS** alimenter le panneau LED via le Raspberry Pi !

1. Le panneau LED a besoin d'une **alimentation 5V externe** (5-10A minimum)
2. Relie l'alimentation directement au panneau LED (connecteur d'alimentation séparé)
3. **Relie le GND de l'alimentation au GND du Raspberry Pi** (masse commune obligatoire)

```
[Alimentation 5V] → [Panneau LED]
                       ↓
                      GND → [Raspberry Pi GND]
```

---

## 🧪 Test du câblage

J'ai créé un script pour tester ton câblage:

```bash
sudo python3 test_wiring.py
```

Ce script va:
1. Tester chaque GPIO individuellement
2. Allumer les LEDs une couleur à la fois
3. Te dire si le câblage est correct

---

## 🔧 Mapping alternatif: Adafruit HAT

Si tu as un Adafruit RGB Matrix HAT, utilise plutôt:

```python
options.hardware_mapping = 'adafruit-hat'
```

Le HAT gère automatiquement tout le câblage.

---

## 🐛 Problèmes courants

### "Je vois juste des traits verticaux"
→ Le câblage des **signaux de contrôle** (CLK, LAT, OE) est incorrect.

### "Les couleurs sont bizarres"
→ Les **pins RGB** (R1, G1, B1, R2, G2, B2) sont mal branchées.

### "Rien ne s'affiche"
→ Vérifie:
- Les GND sont bien connectés
- L'alimentation 5V du panneau
- Les permissions (`sudo`)

### "Seulement la moitié du panneau fonctionne"
→ Les pins **R2, G2, B2** ne sont pas connectées.

### "L'image est décalée/bizarre"
→ Les pins d'**adressage** (A, B, C, D, E) sont mal branchées.

---

## 📝 Checklist avant de tester

- [ ] R1, G1, B1 branchés sur GPIO 17, 18, 22
- [ ] R2, G2, B2 branchés sur GPIO 23, 24, 25
- [ ] A, B, C, D, E branchés sur GPIO 15, 16, 20, 21, 26
- [ ] CLK, LAT, OE branchés sur GPIO 11, 27, 4
- [ ] Tous les GND connectés ensemble
- [ ] Alimentation 5V externe pour le panneau
- [ ] GND de l'alimentation relié au GND du RPi
- [ ] Lance les scripts avec `sudo`

---

## 🚀 Une fois le câblage fait

Lance le test complet:
```bash
sudo python3 test_p3_128x64.py
```

Si le câblage est bon, tu verras les 4 bandes de couleur s'afficher correctement !
