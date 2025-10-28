#!/usr/bin/env python3
"""
Test de TOUTES les configurations possibles
Pour trouver celle qui affiche correctement les couleurs
"""

import sys
import time
import os

# Configuration des chemins
script_dir = os.path.dirname(os.path.abspath(__file__))
rgb_matrix_path = os.path.join(script_dir, 'rpi-rgb-led-matrix', 'bindings', 'python')
sys.path.insert(0, rgb_matrix_path)

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError as e:
    print("ERREUR: Module rgbmatrix non trouvé")
    sys.exit(1)

print("""
╔════════════════════════════════════════════════════════════╗
║     TEST DE TOUTES LES CONFIGURATIONS                      ║
║     Pour trouver celle qui affiche les bonnes couleurs    ║
╚════════════════════════════════════════════════════════════╝
""")

configurations = [
    {"name": "Config 1: Standard, row_addr=0", "rows": 64, "cols": 64, "row_addr": 0, "hw_map": "regular"},
    {"name": "Config 2: row_addr=1", "rows": 64, "cols": 64, "row_addr": 1, "hw_map": "regular"},
    {"name": "Config 3: row_addr=2", "rows": 64, "cols": 64, "row_addr": 2, "hw_map": "regular"},
    {"name": "Config 4: row_addr=0, adafruit-hat", "rows": 64, "cols": 64, "row_addr": 0, "hw_map": "adafruit-hat"},
    {"name": "Config 5: row_addr=1, adafruit-hat", "rows": 64, "cols": 64, "row_addr": 1, "hw_map": "adafruit-hat"},
    {"name": "Config 6: 2 panels 32x64", "rows": 32, "cols": 64, "row_addr": 0, "hw_map": "regular"},
]

def test_config(config):
    """Teste une configuration"""
    print(f"\n{'='*60}")
    print(f"TEST: {config['name']}")
    print(f"{'='*60}")

    try:
        # Configuration
        options = RGBMatrixOptions()
        options.rows = config['rows']
        options.cols = config['cols']
        options.chain_length = 1
        options.parallel = 1
        options.row_address_type = config['row_addr']
        options.hardware_mapping = config['hw_map']
        options.brightness = 80
        options.disable_hardware_pulsing = False

        print(f"Rows: {options.rows}, Cols: {options.cols}")
        print(f"Row addr type: {options.row_address_type}")
        print(f"Hardware mapping: {options.hardware_mapping}")
        print("")

        matrix = RGBMatrix(options=options)

        # Test SANS double buffering - affichage direct
        print("Affichage ROUGE (2 sec)...")
        for y in range(matrix.height):
            for x in range(matrix.width):
                matrix.SetPixel(x, y, 255, 0, 0)
        time.sleep(2)

        print("Affichage VERT (2 sec)...")
        for y in range(matrix.height):
            for x in range(matrix.width):
                matrix.SetPixel(x, y, 0, 255, 0)
        time.sleep(2)

        print("Affichage BLEU (2 sec)...")
        for y in range(matrix.height):
            for x in range(matrix.width):
                matrix.SetPixel(x, y, 0, 0, 255)
        time.sleep(2)

        print("Affichage BLANC (2 sec)...")
        for y in range(matrix.height):
            for x in range(matrix.width):
                matrix.SetPixel(x, y, 255, 255, 255)
        time.sleep(2)

        # Motif de test
        print("Motif de test (3 sec)...")
        matrix.Clear()

        # Bande rouge à gauche
        for y in range(matrix.height):
            for x in range(0, 16):
                matrix.SetPixel(x, y, 255, 0, 0)

        # Bande verte au milieu-gauche
        for y in range(matrix.height):
            for x in range(16, 32):
                matrix.SetPixel(x, y, 0, 255, 0)

        # Bande bleue au milieu-droit
        for y in range(matrix.height):
            for x in range(32, 48):
                matrix.SetPixel(x, y, 0, 0, 255)

        # Bande blanche à droite
        for y in range(matrix.height):
            for x in range(48, 64):
                matrix.SetPixel(x, y, 255, 255, 255)

        time.sleep(3)

        matrix.Clear()

        print("")
        print("✓ Configuration testée !")
        print("")
        response = input("Est-ce que tu as vu les 4 couleurs correctement ? (o/N) : ")

        if response.lower() == 'o':
            print("")
            print("="*60)
            print("🎉 CONFIGURATION TROUVÉE ! 🎉")
            print("="*60)
            print(f"Utilise ces paramètres :")
            print(f"  rows = {options.rows}")
            print(f"  cols = {options.cols}")
            print(f"  row_address_type = {options.row_address_type}")
            print(f"  hardware_mapping = '{options.hardware_mapping}'")
            print("="*60)
            return True

    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False

    return False

# Test toutes les configs
print("On va tester 6 configurations différentes.")
print("Pour chaque test, regarde l'écran et dis si les couleurs sont bonnes.")
print("")
input("Appuie sur ENTRÉE pour commencer...")

for i, config in enumerate(configurations, 1):
    print(f"\n[Test {i}/{len(configurations)}]")

    found = test_config(config)

    if found:
        print("\n✓ On a trouvé la bonne configuration !")
        sys.exit(0)

    if i < len(configurations):
        input("\nAppuie sur ENTRÉE pour le test suivant...")

print("")
print("="*60)
print("Aucune configuration standard n'a fonctionné.")
print("")
print("Ton écran nécessite peut-être des paramètres spéciaux.")
print("Essaie de chercher sur l'écran un modèle ou une référence.")
print("="*60)
