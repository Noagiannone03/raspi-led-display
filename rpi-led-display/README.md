# 🎮 Affichage LED Matrix HUB75 pour Raspberry Pi

Projet complet pour afficher du texte et des graphiques sur un panneau LED HUB75 avec Raspberry Pi.

**✨ Spécialement configuré pour panneau P3 128×64-32S (DV08-210519)**

## 🔧 Matériel requis

- **Raspberry Pi 4 Model B** (ou Pi 3, Zero W)
- **Panneau LED P3 128×64-32S** HUB75 (référence DV08-210519 ou similaire)
- **Alimentation 5V externe** minimum **5A** (recommandé **10A** pour un panneau 128×64)
- **Câbles de connexion** ou **Adafruit RGB Matrix HAT** (recommandé)

## 📦 Installation sur le Raspberry Pi

### 1. Cloner le projet

```bash
cd ~
git clone <URL_DE_TON_REPO>
cd rpi-led-display
```

### 2. Lancer l'installation automatique

```bash
chmod +x install.sh
sudo bash install.sh
```

**IMPORTANT:** Après l'installation, redémarrez le Raspberry Pi :

```bash
sudo reboot
```

### 3. Tester l'écran

Après le redémarrage, testez différentes configurations pour trouver celle qui fonctionne avec votre écran :

```bash
cd ~/rpi-led-display
sudo python3 test_display.py
```

Ce script va tester 4 configurations différentes. Notez celle qui fonctionne !

## 🎨 Utilisation

### Afficher du texte simple

```bash
sudo python3 display_text.py "HELLO WORLD"
```

### Afficher du texte qui défile

```bash
sudo python3 display_text.py "Ceci est un texte qui défile" --scroll
```

### Options avancées

```bash
# Texte rouge
sudo python3 display_text.py "ROUGE" --color 255,0,0

# Texte vert avec défilement lent
sudo python3 display_text.py "VERT" --color 0,255,0 --scroll --speed 0.1

# Texte bleu, luminosité 50%
sudo python3 display_text.py "BLEU" --color 0,0,255 --brightness 50

# Configuration spécifique du type d'adressage
sudo python3 display_text.py "TEST" --row-addr-type 1
```

### Paramètres disponibles

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|-------------------|
| `text` | Texte à afficher | "HELLO LED!" |
| `--scroll` | Active le défilement | Non |
| `--color R,G,B` | Couleur RGB (0-255) | 255,255,255 (blanc) |
| `--duration N` | Durée d'affichage (secondes) | 10 |
| `--speed N` | Vitesse de défilement | 0.05 |
| `--brightness N` | Luminosité (0-100) | 70 |
| `--row-addr-type N` | Type d'adressage (0, 1, 2) | 0 |

## 🔌 Câblage

### Connexion standard (sans HAT)

L'écran LED se connecte au GPIO du Raspberry Pi. Voici les connexions principales :

| Pin écran | Pin GPIO | Description |
|-----------|----------|-------------|
| R1 | GPIO 11 | Rouge données 1 |
| G1 | GPIO 27 | Vert données 1 |
| B1 | GPIO 7 | Bleu données 1 |
| R2 | GPIO 8 | Rouge données 2 |
| G2 | GPIO 9 | Vert données 2 |
| B2 | GPIO 10 | Bleu données 2 |
| A | GPIO 22 | Adresse ligne A |
| B | GPIO 23 | Adresse ligne B |
| C | GPIO 24 | Adresse ligne C |
| D | GPIO 25 | Adresse ligne D |
| E | GPIO 15 | Adresse ligne E (64x64) |
| CLK | GPIO 17 | Clock |
| LAT | GPIO 4 | Latch |
| OE | GPIO 18 | Output Enable |
| GND | GND | Masse |

**⚠️ IMPORTANT :**
- Ne connectez PAS les pins d'alimentation 5V de l'écran au Raspberry Pi !
- Utilisez une alimentation externe 5V/4A minimum
- Reliez uniquement les GND ensemble

### Avec Adafruit RGB Matrix HAT

Si vous utilisez un HAT Adafruit, modifiez dans `display_text.py` :

```python
options.hardware_mapping = 'adafruit-hat'
```

Et soudez le jumper **E** sur le HAT pour les matrices 64x64.

## 🐛 Dépannage

### Rien ne s'affiche

1. **Vérifiez l'alimentation** : L'écran a besoin de beaucoup de courant (5V/4A min)
2. **Testez différents row_addr_type** :
   ```bash
   sudo python3 display_text.py "TEST" --row-addr-type 1
   sudo python3 display_text.py "TEST" --row-addr-type 2
   ```
3. **Vérifiez le câblage** : Toutes les connexions doivent être bien enfoncées
4. **Permissions** : Exécutez toujours avec `sudo`

### Image coupée en deux ou lignes manquantes

C'est un problème de configuration. Testez :

```bash
sudo python3 display_text.py "TEST" --row-addr-type 1
```

Si ça ne marche pas, essayez avec `--row-addr-type 2`.

### Seule la couleur rouge s'affiche

Problème d'alimentation ! Utilisez une alimentation plus puissante (5V/4A ou 5V/6A).

### Couleurs incorrectes

Vérifiez les connexions R1, G1, B1, R2, G2, B2 sur le GPIO.

### Permission denied

Vous devez exécuter les scripts avec `sudo` :

```bash
sudo python3 display_text.py "TEST"
```

## 📝 Configuration avancée

### Modifier la configuration par défaut

Éditez le fichier `display_text.py` et modifiez les valeurs dans la fonction `create_matrix()` :

```python
# Exemple de configuration qui a marché lors du test
options.rows = 64
options.cols = 64
options.row_address_type = 1  # Changez selon vos tests !
options.brightness = 70
```

### Lancer au démarrage

Pour lancer automatiquement un message au démarrage du Raspberry Pi :

1. Créez un service systemd :

```bash
sudo nano /etc/systemd/system/led-display.service
```

2. Ajoutez :

```ini
[Unit]
Description=LED Matrix Display
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/pi/rpi-led-display/display_text.py "HELLO WORLD" --scroll
WorkingDirectory=/home/pi/rpi-led-display
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

3. Activez le service :

```bash
sudo systemctl enable led-display.service
sudo systemctl start led-display.service
```

## 🎯 Exemples d'utilisation

### Messages simples

```bash
# Message d'accueil
sudo python3 display_text.py "BIENVENUE"

# Température
sudo python3 display_text.py "Temp: 22C" --color 0,255,255

# Heure
sudo python3 display_text.py "$(date +%H:%M)" --color 255,255,0
```

### Messages défilants

```bash
# Actualités
sudo python3 display_text.py "Dernières news: Il fait beau aujourd'hui!" --scroll --speed 0.04

# Publicité
sudo python3 display_text.py "PROMO -50% sur tout!" --scroll --color 255,0,0
```

### Boucle infinie avec différents messages

Créez un fichier `messages.sh` :

```bash
#!/bin/bash
while true; do
    sudo python3 display_text.py "MESSAGE 1" --duration 5
    sudo python3 display_text.py "MESSAGE 2" --color 255,0,0 --duration 5
    sudo python3 display_text.py "MESSAGE 3" --color 0,255,0 --scroll
done
```

Exécutez :

```bash
chmod +x messages.sh
./messages.sh
```

## 📚 Ressources

- [Bibliothèque rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix)
- [Guide de câblage détaillé](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/wiring.md)
- [Adafruit RGB Matrix HAT](https://www.adafruit.com/product/2345)

## ⚡ Problèmes courants résolus

### Le son ne fonctionne plus

C'est normal ! Le module son est désactivé car il utilise les mêmes ressources que la matrice LED. Si vous avez besoin du son, vous devrez faire un choix.

### Performance lente

Essayez d'augmenter la priorité :

```bash
sudo nice -n -20 python3 display_text.py "TEST"
```

### Scintillement

Ajustez le paramètre PWM dans `display_text.py` :

```python
options.pwm_lsb_nanoseconds = 130  # Essayez 100, 130, 200
```

## 🤝 Support

Si vous rencontrez des problèmes :

1. Vérifiez que vous avez bien redémarré après l'installation
2. Testez toutes les configurations avec `test_display.py`
3. Vérifiez votre alimentation (5V/4A minimum)
4. Assurez-vous d'exécuter avec `sudo`

## 📄 Licence

Projet open source - Utilisez et modifiez librement !

---

**Fait avec ❤️ pour ton Raspberry Pi et ton écran LED 64x64**
