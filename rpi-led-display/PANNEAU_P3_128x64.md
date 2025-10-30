# Configuration pour Panneau P3 128×64-32S

## Identification du panneau
- **Modèle**: P3 128×64-32S-V1.0
- **Référence**: DV08-210519
- **Type**: HUB75
- **Résolution**: 128×64 pixels
- **Pitch**: P3 (3mm entre les LEDs)

## Le problème
Les scripts précédents étaient configurés pour un panneau **64×64** au lieu de **128×64**. C'est pour ça que l'affichage ne fonctionnait pas correctement.

## Solution

### Étape 1: Trouver la bonne configuration

Lance ce script sur le Raspberry Pi:
```bash
sudo python3 test_p3_128x64.py
```

Ce script va tester **8 configurations différentes**. Pour chaque test:
1. Regarde l'écran LED
2. Vérifie que les couleurs sont correctes
3. **Vérifie surtout que l'affichage couvre TOUT l'écran (128 pixels de large)**

Quand tu vois un affichage qui couvre tout l'écran avec les bonnes couleurs, tape `o` puis ENTRÉE.

### Configurations testées

Le script teste ces configurations dans l'ordre:

1. **2×64×64 panels chained (Standard)**
   - Deux panneaux de 64×64 chaînés
   - `rows=64, cols=64, chain=2`

2. **2×64×32 panels (32S = scan 1/32)** ← **PROBABLEMENT LA BONNE**
   - Deux panneaux de 64×32 avec scan 1/32
   - `rows=32, cols=64, chain=2`
   - Le "32S" dans le nom suggère cette config

3. **Single 128×64 panel**
   - Un seul grand panneau
   - `rows=64, cols=128, chain=1`

4-8. Variations avec différents paramètres de scan

### Étape 2: Mettre à jour le script d'affichage

Une fois la bonne configuration trouvée:

1. Ouvre `display_text_128x64.py`
2. Remplace les paramètres dans la section marquée `CONFIGURATION À AJUSTER`
3. Teste:
```bash
sudo python3 display_text_128x64.py "TEST"
```

## Paramètres importants

Pour le panneau P3 128×64-32S, voici les paramètres clés:

### `rows` et `cols`
- Définissent la taille d'UN panneau physique
- Pour un scan 1/32: `rows=32, cols=64`
- Pour un scan 1/64: `rows=64, cols=64`

### `chain_length`
- Nombre de panneaux chaînés horizontalement
- Pour 128 pixels de large: `chain=2` (si cols=64)

### `parallel`
- Nombre de chaînes parallèles (vertical)
- Généralement `parallel=1` pour ce panneau

### `row_address_type`
- Type d'adressage des lignes
- `0` = direct (4 lignes A,B,C,D)
- `1` = direct (5 lignes A,B,C,D,E)
- `2` = autre mapping

### `multiplexing`
- Mode de multiplexage du scan
- `0` = direct (standard)
- `1` = stripe
- Autres valeurs pour panels spéciaux

### `hardware_mapping`
- Mapping du GPIO vers les pins du panneau
- `'regular'` = connexion standard
- `'adafruit-hat'` = pour Adafruit RGB Matrix HAT

## Commandes utiles

### Test rapide
```bash
sudo python3 test_p3_128x64.py
```

### Affichage de texte
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

## Diagnostic

Si rien ne s'affiche:
1. Vérifie que tu lances avec `sudo`
2. Vérifie les connexions du panneau
3. Essaie avec `--brightness 80` pour augmenter la luminosité
4. Lance `test_p3_128x64.py` pour tester toutes les configs

Si les couleurs sont incorrectes:
- C'est un problème de configuration
- Essaie les différents paramètres de `row_address_type` (0, 1, 2)
- Essaie différents `multiplexing` (0, 1, 2)

Si seulement la moitié de l'écran s'allume:
- Vérifie `chain_length` (devrait être 2)
- Vérifie que le câble entre les deux moitiés est bien branché

## Ressources

- [Documentation rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix)
- [Options de configuration](https://github.com/hzeller/rpi-rgb-led-matrix#changing-parameters-via-command-line-flags)
