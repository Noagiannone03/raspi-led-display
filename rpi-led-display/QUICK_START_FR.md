# 🚀 DÉMARRAGE RAPIDE - LED Matrix 64x64

Guide ultra-rapide pour faire fonctionner ton écran LED !

## 📋 Ce qu'il te faut

- Raspberry Pi (3, 4, ou Zero W)
- Écran LED 64x64 (ton DV08-210519)
- Alimentation 5V/4A ou plus puissante
- Carte SD avec Raspberry Pi OS

## ⚡ Installation en 3 étapes

### 1️⃣ Sur ton Raspberry Pi, clone le projet

```bash
cd ~
git clone <URL_DU_REPO>
cd rpi-led-display
```

### 2️⃣ Lance l'installation (prend 5-10 min)

```bash
chmod +x install.sh
sudo bash install.sh
```

**Attend que l'installation soit terminée, puis redémarre :**

```bash
sudo reboot
```

### 3️⃣ Teste ton écran !

Après le redémarrage, connecte-toi en SSH et teste :

```bash
cd ~/rpi-led-display
sudo python3 test_display.py
```

Ce script va tester 4 configurations différentes. **Regarde ton écran et note celle qui fonctionne !**

## ✅ Si ça marche

Super ! Tu peux maintenant afficher ce que tu veux :

```bash
# Texte simple
sudo python3 display_text.py "HELLO !"

# Texte qui défile
sudo python3 display_text.py "Ceci défile !" --scroll

# Texte en couleur
sudo python3 display_text.py "ROUGE" --color 255,0,0
sudo python3 display_text.py "VERT" --color 0,255,0
sudo python3 display_text.py "BLEU" --color 0,0,255

# Voir tous les exemples
sudo bash examples.sh
```

## ❌ Si ça ne marche pas

### Problème 1 : Rien ne s'affiche

```bash
# Teste avec un type d'adressage différent
sudo python3 display_text.py "TEST" --row-addr-type 1
sudo python3 display_text.py "TEST" --row-addr-type 2
```

### Problème 2 : Image coupée en deux

C'est le row_addr_type ! Utilise :

```bash
sudo python3 display_text.py "TEST" --row-addr-type 1
```

Si ça marche, édite `display_text.py` ligne 36 et change :

```python
options.row_address_type = 1  # au lieu de 0
```

### Problème 3 : Seul le rouge s'affiche

Ton alimentation est trop faible ! Utilise une alim 5V/4A minimum (6A c'est mieux).

### Diagnostic complet

```bash
sudo python3 troubleshoot.py
```

## 🔌 Câblage important

**⚠️ ATTENTION ⚠️**
- N'alimente PAS l'écran depuis le Raspberry Pi !
- Utilise une alimentation externe 5V/4A
- Relie UNIQUEMENT les GND ensemble

Pour voir le câblage complet :

```bash
cat wiring_guide.txt
```

## 📱 Commandes utiles

```bash
# Afficher l'heure
sudo python3 display_text.py "$(date +%H:%M)" --color 255,255,0

# Message défilant rapide
sudo python3 display_text.py "NEWS DU JOUR" --scroll --speed 0.03

# Texte avec luminosité réduite
sudo python3 display_text.py "NUIT" --brightness 30

# Démarrage rapide
sudo ./quick_start.sh "TON TEXTE"
```

## 🆘 Besoin d'aide ?

1. Lis le `README.md` complet
2. Regarde `wiring_guide.txt` pour le câblage
3. Lance `sudo python3 troubleshoot.py`
4. Vérifie que le pin **E** est bien connecté (critique pour 64x64 !)

## 🎯 Configurations qui marchent généralement

La plupart des écrans 64x64 fonctionnent avec :

```bash
# Configuration 1 (la plus courante)
sudo python3 display_text.py "TEST" --row-addr-type 0

# Configuration 2 (si coupé en deux)
sudo python3 display_text.py "TEST" --row-addr-type 1
```

---

**C'est tout ! Si tu suis ces étapes, ton écran devrait fonctionner en moins de 15 minutes ! 🎉**
