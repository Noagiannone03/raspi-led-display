# 🔌 Câblage EXACT pour TON panneau

## Ton connecteur HUB75 (16 pins)

```
R1  ──  G1
B1  ──  GND
R2  ──  G2
B2  ──  GND
A   ──  B
C   ──  GND
CLK ──  LAT
OE  ──  GND
```

**Important** : Tu n'as que **A, B, C** (3 bits d'adressage), pas de D ni E.
Ça signifie que ton panneau utilise un **scan 1/8** avec multiplexage interne.

---

## Câblage EXACT Raspberry Pi 4 ↔ Ton panneau

### 🔴 Signaux de données RGB

| Pin HUB75 | → | GPIO RPi | Pin Physique |
|-----------|---|----------|--------------|
| **R1** | → | GPIO 17 | Pin 11 |
| **G1** | → | GPIO 18 | Pin 12 |
| **B1** | → | GPIO 22 | Pin 15 |
| **R2** | → | GPIO 23 | Pin 16 |
| **G2** | → | GPIO 24 | Pin 18 |
| **B2** | → | GPIO 25 | Pin 22 |

### 🎯 Adressage (SEULEMENT 3 bits pour ton panneau)

| Pin HUB75 | → | GPIO RPi | Pin Physique |
|-----------|---|----------|--------------|
| **A** | → | GPIO 15 | Pin 10 |
| **B** | → | GPIO 16 | Pin 36 |
| **C** | → | GPIO 20 | Pin 38 |

**⚠️ PAS de D ni E sur ton panneau !**

### ⚙️ Signaux de contrôle

| Pin HUB75 | → | GPIO RPi | Pin Physique |
|-----------|---|----------|--------------|
| **CLK** | → | GPIO 11 | Pin 23 |
| **LAT** | → | GPIO 27 | Pin 13 |
| **OE** | → | GPIO 4 | Pin 7 |

### ⚫ Masse

| Pin HUB75 | → | Raspberry Pi |
|-----------|---|--------------|
| **GND** (tous les 4) | → | GND (n'importe quel pin GND du RPi) |

Pins GND disponibles sur le RPi : **6, 9, 14, 20, 25, 30, 34, 39**

---

## 📋 Liste de câblage simplifiée

Branche dans cet ordre :

```
1. R1  → GPIO 17 (Pin 11)
2. G1  → GPIO 18 (Pin 12)
3. B1  → GPIO 22 (Pin 15)
4. R2  → GPIO 23 (Pin 16)
5. G2  → GPIO 24 (Pin 18)
6. B2  → GPIO 25 (Pin 22)
7. A   → GPIO 15 (Pin 10)
8. B   → GPIO 16 (Pin 36)
9. C   → GPIO 20 (Pin 38)
10. CLK → GPIO 11 (Pin 23)
11. LAT → GPIO 27 (Pin 13)
12. OE  → GPIO 4  (Pin 7)
13. GND → GND (tous ensemble)
```

**Total : 13 connexions** (12 signaux + GND)

---

## 🔌 Schéma visuel du Raspberry Pi 4

```
    3V3  (1) (2)  5V
  GPIO2  (3) (4)  5V
  GPIO3  (5) (6)  GND ← GND
  GPIO4  (7) (8)  GPIO14
        ← OE
    GND  (9) (10) GPIO15 ← A
 GPIO17 (11) (12) GPIO18 ← G1
        ← R1
 GPIO27 (13) (14) GND
        ← LAT
 GPIO22 (15) (16) GPIO23 ← R2
        ← B1
    3V3 (17) (18) GPIO24 ← G2
 GPIO10 (19) (20) GND
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
    GND (39) (40) GPIO21
```

---

## ⚡ ALIMENTATION (CRUCIAL)

**NE JAMAIS** alimenter le panneau via le Raspberry Pi !

1. Utilise une **alimentation 5V externe** (5-10A)
2. Branche l'alimentation au connecteur d'alimentation du panneau (séparé du HUB75)
3. **IMPORTANT** : Relie le GND de l'alimentation au GND du Raspberry Pi

```
[Alim 5V/10A] ─────→ [Panneau LED - Connecteur alimentation]
                          |
                         GND ─────→ [Raspberry Pi GND]
```

---

## 🧪 Test du câblage

Une fois tout branché, lance :

```bash
sudo python3 test_wiring.py
```

Ce script va tester chaque couleur séparément et te dire exactement quelle pin est mal branchée si il y a un problème.

---

## 🎯 Configuration logicielle pour ton panneau

Avec seulement A, B, C, ton panneau utilise probablement ces paramètres :

**Option 1 : Scan 1/8 (le plus probable)**
```python
options.rows = 32
options.cols = 64
options.chain_length = 2
options.multiplexing = 0  # ou 1
options.row_address_type = 0
options.hardware_mapping = 'regular'
```

**Option 2 : Scan 1/16 avec multiplexage**
```python
options.rows = 32
options.cols = 64
options.chain_length = 2
options.multiplexing = 1  # Important !
options.row_address_type = 0
options.hardware_mapping = 'regular'
```

Le script `test_p3_128x64.py` va tester ces configurations automatiquement.

---

## ✅ Checklist avant de tester

- [ ] R1, G1, B1 branchés (GPIO 17, 18, 22)
- [ ] R2, G2, B2 branchés (GPIO 23, 24, 25)
- [ ] A, B, C branchés (GPIO 15, 16, 20) ← **Seulement ces 3 !**
- [ ] CLK, LAT, OE branchés (GPIO 11, 27, 4)
- [ ] Tous les GND connectés
- [ ] Alimentation 5V externe branchée au panneau
- [ ] GND de l'alimentation relié au GND du RPi

---

## 🚀 Prochaines étapes

1. **Branche tout comme indiqué ci-dessus**
2. **Lance** : `sudo python3 test_wiring.py`
3. **Si tout est OK, lance** : `sudo python3 test_p3_128x64.py`
4. **Note la configuration qui marche**

---

## 🐛 Si ça ne marche toujours pas

Les traits verticaux que tu vois indiquent que :
- ✅ Les pins RGB (R1, G1, B1, R2, G2, B2) fonctionnent partiellement
- ❌ Les signaux de contrôle (CLK, LAT, OE) ou l'adressage (A, B, C) sont mal configurés

**Essaie ça** :
1. Vérifie bien CLK, LAT, OE (ce sont les plus critiques)
2. Vérifie que le GND est bien connecté
3. Essaie avec `hardware_mapping = 'adafruit-hat'` même sans HAT (parfois ça marche)
