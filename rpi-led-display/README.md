# Panneau LED DV08-210519 128x64-32S

Configuration pour panneau LED HUB75 128x64 - **DV08-210519 128x64-32S V1.0**

Raspberry Pi

**Plus complexe, nécessite bonne alimentation**

**Matériel requis:**
- Raspberry Pi 4
- Panneau DV08-210519 128x64-32S
- **Alimentation 5V 10A MINIMUM** pour le panneau (obligatoire)
- Câblage GPIO direct

**Installation:**
```bash
# Installer la lib rpi-rgb-led-matrix
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.sh >rgb-matrix.sh
sudo bash rgb-matrix.sh

# Installer les dépendances Python
sudo pip3 install Pillow
```

**Test:**
```bash
sudo python3 test_DV08_128x64_32S.py
```

Ce script teste 6 configurations différentes. Une devrait marcher.

**Avantages:**
- Plus de puissance de calcul
- Système complet Linux
- Réseau, serveur web, etc.

**Inconvénients:**
- Configuration complexe
- Nécessite alimentation puissante (5V 10A min)
- Plus cher

**Fichier:** `test_DV08_128x64_32S.py`

---

## Câblage standard HUB75

**Pour ESP32:**
```
R1 -> GPIO 25    G1 -> GPIO 26    B1 -> GPIO 27
R2 -> GPIO 14    G2 -> GPIO 12    B2 -> GPIO 13
A  -> GPIO 23    B  -> GPIO 19    C  -> GPIO 5
D  -> GPIO 17    E  -> GPIO 18
LAT-> GPIO 4     OE -> GPIO 15    CLK-> GPIO 16
GND-> GND
```

**Pour Raspberry Pi:**
Voir les fichiers de configuration dans `test_DV08_128x64_32S.py`

---

## Alimentation

**ESP32:** 5V 3A suffit pour usage normal

**Raspberry Pi:** 5V 10A MINIMUM
- Sans ça, rien ne marchera correctement
- Symptômes d'alimentation faible:
  - Affichage instable
  - Couleurs bizarres
  - Lignes verticales
  - RPi qui redémarre

---

## Dépannage

### Rien ne s'affiche

**ESP32:**
1. Vérifie le câblage HUB75
2. Vérifie l'alimentation 5V
3. Ouvre le moniteur série (115200 baud)
4. Décommente la ligne `FM6126A` dans le code si nécessaire

**Raspberry Pi:**
1. Vérifie l'alimentation (10A minimum)
2. Lance le script de test: `sudo python3 test_DV08_128x64_32S.py`
3. Essaye les 6 configurations

### Affichage bizarre

- Vérifie l'alimentation en premier
- Puis vérifie le câblage
- Regarde le moniteur série pour les erreurs

---

## Quelle solution choisir ?

**Choisis ESP32 si:**
- Tu veux juste afficher des trucs
- Tu veux que ça marche facilement
- Budget limité pour l'alimentation

**Choisis Raspberry Pi si:**
- Tu as besoin d'un serveur web
- Tu fais du traitement vidéo/image
- Tu veux un système Linux complet
- Tu as une bonne alimentation 5V 10A

---

## Fichiers du projet

- `esp32_dv08_128x64.ino` - Code ESP32 complet
- `test_DV08_128x64_32S.py` - Script de test Raspberry Pi
- `requirements.txt` - Dépendances Python
- `.gitignore` - Config Git

---

## Librairies utilisées

**ESP32:**
- ESP32-HUB75-MatrixPanel-DMA
- https://github.com/mrfaptastic/ESP32-HUB75-MatrixPanel-DMA

**Raspberry Pi:**
- rpi-rgb-led-matrix (Hzeller)
- https://github.com/hzeller/rpi-rgb-led-matrix

---

## Support

**Pour ESP32:**
- Regarde le code dans `esp32_dv08_128x64.ino`
- Tous les exemples sont dedans
- Moniteur série pour debug

**Pour Raspberry Pi:**
- Lance `sudo python3 test_DV08_128x64_32S.py`
- Les 6 configs vont se tester automatiquement
- Note celle qui marche

---

**Bon courage !**
