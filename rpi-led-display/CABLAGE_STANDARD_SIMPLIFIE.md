# 🔌 Câblage STANDARD pour panneau 128×64 (avec seulement A, B, C)

## ⚡ Ce câblage fonctionne avec `hardware_mapping = 'regular'`

### 📋 Liste complète des connexions

Branchez **EXACTEMENT** ces pins :

```
HUB75 → Raspberry Pi
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 COULEURS RGB (6 signaux)
───────────────────────────
R1  →  Pin 11  (GPIO 17)
G1  →  Pin 12  (GPIO 18)
B1  →  Pin 15  (GPIO 22)
R2  →  Pin 16  (GPIO 23)
G2  →  Pin 18  (GPIO 24)
B2  →  Pin 22  (GPIO 25)

🎯 ADRESSAGE (3 bits seulement pour ton panneau)
─────────────────────────────────────────────────
A   →  Pin 10  (GPIO 15)
B   →  Pin 36  (GPIO 16)
C   →  Pin 38  (GPIO 20)

⚙️ SIGNAUX DE CONTRÔLE (3 signaux)
───────────────────────────────────────
CLK →  Pin 23  (GPIO 11)
LAT →  Pin 13  (GPIO 27)
OE  →  Pin 7   (GPIO 4)

⚫ MASSE (GND)
──────────────
GND →  Pin 6, 9, 14, 20, 25, 30, 34 ou 39
       (n'importe lequel, tous les GND ensemble)
```

---

## 🎨 Schéma visuel simplifié

```
         RASPBERRY PI 4

         [USB] [USB]
           ┌─────┐
     3V3 ○ │ 1  2│ ○ 5V
   GPIO2 ○ │ 3  4│ ○ 5V
   GPIO3 ○ │ 5  6│ ● GND ←─── GND
   GPIO4 ○ │ 7  8│ ○ GPIO14
      OE ─┘ 9 10│ └─ A
     GND ● │11 12│ ○ GPIO18
  GPIO17 ○─┘    └─● G1
      R1   13 14│ ● GND
  GPIO27 ○─┘    │
     LAT   15 16│ └─○ GPIO23
  GPIO22 ○─┘    └──● R2
      B1   17 18│ ○ GPIO24
     3V3 ○ │    └─● G2
 GPIO10  ○ │19 20│ ● GND
  GPIO9  ○ │21 22│ ○ GPIO25
 GPIO11  ○─┘    └─● B2
     CLK   23 24│ ○ GPIO8
     GND ● │25 26│ ○ GPIO7
  GPIO0  ○ │27 28│ ○ GPIO1
  GPIO5  ○ │29 30│ ● GND
  GPIO6  ○ │31 32│ ○ GPIO12
 GPIO13  ○ │33 34│ ● GND
 GPIO19  ○ │35 36│ ○ GPIO16
 GPIO26  ○ │37 38│ ○─● B
     GND ● │39 40│ ○ GPIO20
           └─────┘    └──● C
        [Ethernet]
```

---

## ✅ Checklist de câblage

Cochez au fur et à mesure :

- [ ] R1  → Pin 11
- [ ] G1  → Pin 12
- [ ] B1  → Pin 15
- [ ] R2  → Pin 16
- [ ] G2  → Pin 18
- [ ] B2  → Pin 22
- [ ] A   → Pin 10
- [ ] B   → Pin 36
- [ ] C   → Pin 38
- [ ] CLK → Pin 23
- [ ] LAT → Pin 13
- [ ] OE  → Pin 7
- [ ] GND → N'importe quel GND

**Total : 13 connexions**

---

## 🧪 Test après câblage

Une fois câblé, lancez :

```bash
sudo python3 test_wiring.py
```

Puis :

```bash
sudo python3 test_all_mappings.py
```

Le mapping qui devrait fonctionner : **`regular`**

---

## 💡 Pourquoi ce câblage ?

C'est le câblage **par défaut** de la librairie `rpi-rgb-led-matrix`.

Si vous utilisez un câblage différent, la librairie ne saura pas où chercher les signaux et l'affichage sera incorrect ou absent.

---

## 🆚 Comparaison avec votre câblage actuel

Vous utilisez : **35,37,39,40,29,25,23,26,19,20,18,16,15,11,12,9,7**

Le standard utilise : **11,12,15,16,18,22,10,36,38,23,13,7 + GND**

→ C'est pour ça que ça ne fonctionne pas ! Les GPIO ne correspondent pas.
