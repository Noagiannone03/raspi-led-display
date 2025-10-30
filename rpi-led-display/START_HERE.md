# ⚡ START HERE - Guide pour TON panneau exact

## 📌 Ton panneau
- **Type** : P3 128×64-32S (DV08-210519)
- **Connecteur** : HUB75 avec **seulement A, B, C** (pas de D ni E)
- **Raspberry Pi** : 4 Model B

---

## 🔌 ÉTAPE 1 : Câblage

Lis et suis **EXACTEMENT** ce guide :
```
📄 CABLAGE_EXACT.md
```

**Résumé ultra-rapide** :
- R1, G1, B1, R2, G2, B2 → GPIO 17, 18, 22, 23, 24, 25
- A, B, C → GPIO 15, 16, 20 (⚠️ **seulement ces 3 !**)
- CLK, LAT, OE → GPIO 11, 27, 4
- GND → GND (tous ensemble)
- **Alimentation 5V externe pour le panneau (pas le RPi !)**

---

## 🧪 ÉTAPE 2 : Test du câblage

Clone le repo sur ton RPi :
```bash
cd ~
git clone <ton_repo>
cd rpi-led-display
```

Lance le test de câblage :
```bash
sudo python3 test_wiring.py
```

Ce script va afficher chaque couleur séparément. Si une couleur ne s'affiche pas, il te dira exactement quelle pin vérifier.

**✓ Continue seulement si toutes les couleurs s'affichent correctement.**

---

## 🎯 ÉTAPE 3 : Trouver la bonne configuration

Maintenant que le câblage est bon, trouve les bons paramètres logiciels :

```bash
sudo python3 test_exact_panel.py
```

Ce script va tester **10 configurations** adaptées à ton panneau (avec seulement A, B, C).

Pour chaque test, vérifie :
1. Les couleurs sont bonnes (rouge, vert, bleu, blanc)
2. L'affichage couvre **TOUT l'écran** (128 pixels de large)
3. Le motif est régulier (pas de lignes bizarres)

Quand tout est bon, tape **`o`** puis ENTRÉE.

Le script va afficher les paramètres exacts à utiliser. **COPIE-LES !**

---

## 📝 ÉTAPE 4 : Utiliser la configuration

Édite le fichier `display_text_128x64.py` :

```bash
nano display_text_128x64.py
```

Trouve la section **"CONFIGURATION À AJUSTER"** (ligne ~35) et remplace avec les paramètres trouvés.

Exemple :
```python
options.rows = 32
options.cols = 64
options.chain_length = 2
options.multiplexing = 1  # ← Ce paramètre est crucial !
options.hardware_mapping = 'regular'
```

---

## 🎨 ÉTAPE 5 : Teste l'affichage

```bash
sudo python3 display_text_128x64.py "HELLO"
```

Si ça marche, essaie :
```bash
# Texte en rouge
sudo python3 display_text_128x64.py "MODULEAIR" --color 255,0,0

# Texte défilant
sudo python3 display_text_128x64.py "BONJOUR" --scroll
```

---

## 🎉 C'est tout !

Si ça marche, tu as terminé !

Si ça ne marche pas, vérifie :
1. Tu lances bien avec `sudo`
2. Le câblage est correct (teste avec `test_wiring.py`)
3. L'alimentation 5V du panneau est branchée
4. Les GND sont bien connectés ensemble

---

## 📚 Autres fichiers utiles

- `CABLAGE_EXACT.md` - Guide détaillé du câblage pour TON panneau
- `test_wiring.py` - Test du câblage (affiche chaque couleur séparément)
- `test_exact_panel.py` - Teste 10 configurations adaptées à ton panneau
- `display_text_128x64.py` - Affiche du texte une fois configuré

---

## 🐛 Problème : "Traits verticaux blanc/rouge/vert"

C'est ce que tu as actuellement. Ça signifie que :
- ✅ Les pins RGB fonctionnent partiellement
- ❌ Le problème est dans les signaux de contrôle (CLK, LAT, OE) ou la configuration logicielle

**Solution** :
1. Vérifie bien que CLK, LAT, OE sont sur les bons GPIO (11, 27, 4)
2. Lance `test_exact_panel.py` qui va tester différents modes de multiplexage
3. Le paramètre **`multiplexing`** est probablement la clé pour ton panneau

---

## ⚡ TL;DR (résumé ultra-court)

```bash
# 1. Clone le repo
git clone <repo> && cd rpi-led-display

# 2. Branche selon CABLAGE_EXACT.md

# 3. Test le câblage
sudo python3 test_wiring.py

# 4. Trouve la config
sudo python3 test_exact_panel.py

# 5. Édite display_text_128x64.py avec la config trouvée

# 6. Teste
sudo python3 display_text_128x64.py "HELLO"
```

---

**Questions ? Relis `CABLAGE_EXACT.md` et assure-toi que le câblage est correct.**
