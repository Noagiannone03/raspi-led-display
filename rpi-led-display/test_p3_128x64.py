#!/usr/bin/env python3
"""
Test spécifique pour panneau P3 128×64-32S (DV08-210519)
Ce panneau a des caractéristiques particulières
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
    print(f"Détail: {e}")
    sys.exit(1)

print("""
╔════════════════════════════════════════════════════════════╗
║     TEST PANNEAU P3 128×64-32S                             ║
║     DV08-210519                                            ║
╚════════════════════════════════════════════════════════════╝
""")

# Configurations spécifiques pour ce type de panneau
configurations = [
    {
        "name": "Config 1: 2×64×64 panels chained (Standard)",
        "rows": 64,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 2: 2×64×32 panels (32S = scan 1/32)",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 3: Single 128×64 panel",
        "rows": 64,
        "cols": 128,
        "chain": 1,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 4: 2×64×32 with row_addr=1",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 1,
        "hw_map": "regular"
    },
    {
        "name": "Config 5: 2×64×32 with multiplexing=1",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 1,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 6: 4×64×32 parallel (alternative wiring)",
        "rows": 32,
        "cols": 64,
        "chain": 1,
        "parallel": 2,
        "multiplexing": 0,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 7: adafruit-hat mapping",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 0,
        "hw_map": "adafruit-hat"
    },
    {
        "name": "Config 8: 2×64×64 with row_addr=2 (E-line)",
        "rows": 64,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 2,
        "hw_map": "regular"
    },
]

def test_config(config):
    """Teste une configuration"""
    print(f"\n{'='*70}")
    print(f"TEST: {config['name']}")
    print(f"{'='*70}")

    try:
        # Configuration
        options = RGBMatrixOptions()
        options.rows = config['rows']
        options.cols = config['cols']
        options.chain_length = config['chain']
        options.parallel = config['parallel']
        options.multiplexing = config['multiplexing']
        options.row_address_type = config['row_addr']
        options.hardware_mapping = config['hw_map']
        options.brightness = 60
        options.disable_hardware_pulsing = False

        print(f"Paramètres:")
        print(f"  rows = {options.rows}")
        print(f"  cols = {options.cols}")
        print(f"  chain_length = {options.chain_length}")
        print(f"  parallel = {options.parallel}")
        print(f"  multiplexing = {options.multiplexing}")
        print(f"  row_address_type = {options.row_address_type}")
        print(f"  hardware_mapping = '{options.hardware_mapping}'")
        print(f"\n  → Résolution totale: {options.cols * options.chain_length}×{options.rows * options.parallel}")
        print()

        matrix = RGBMatrix(options=options)

        # Motif de test TRÈS visible
        print("Test 1: Bandes de couleur verticales (3 sec)...")

        width = matrix.width
        height = matrix.height

        # Rouge à gauche
        for y in range(height):
            for x in range(0, width // 4):
                matrix.SetPixel(x, y, 255, 0, 0)

        # Vert
        for y in range(height):
            for x in range(width // 4, width // 2):
                matrix.SetPixel(x, y, 0, 255, 0)

        # Bleu
        for y in range(height):
            for x in range(width // 2, 3 * width // 4):
                matrix.SetPixel(x, y, 0, 0, 255)

        # Blanc à droite
        for y in range(height):
            for x in range(3 * width // 4, width):
                matrix.SetPixel(x, y, 255, 255, 255)

        time.sleep(3)

        # Test 2: Bandes horizontales
        print("Test 2: Bandes de couleur horizontales (3 sec)...")
        matrix.Clear()

        # Rouge en haut
        for y in range(0, height // 4):
            for x in range(width):
                matrix.SetPixel(x, y, 255, 0, 0)

        # Vert
        for y in range(height // 4, height // 2):
            for x in range(width):
                matrix.SetPixel(x, y, 0, 255, 0)

        # Bleu
        for y in range(height // 2, 3 * height // 4):
            for x in range(width):
                matrix.SetPixel(x, y, 0, 0, 255)

        # Blanc en bas
        for y in range(3 * height // 4, height):
            for x in range(width):
                matrix.SetPixel(x, y, 255, 255, 255)

        time.sleep(3)

        # Test 3: Damier
        print("Test 3: Motif en damier (3 sec)...")
        matrix.Clear()

        for y in range(height):
            for x in range(width):
                if (x // 8 + y // 8) % 2 == 0:
                    matrix.SetPixel(x, y, 255, 255, 255)
                else:
                    matrix.SetPixel(x, y, 255, 0, 0)

        time.sleep(3)

        # Test 4: Tout blanc
        print("Test 4: Écran tout blanc (2 sec)...")
        for y in range(height):
            for x in range(width):
                matrix.SetPixel(x, y, 255, 255, 255)

        time.sleep(2)

        matrix.Clear()

        print("")
        print("✓ Configuration testée !")
        print("")
        response = input("Est-ce que l'affichage était correct et couvrait tout l'écran ? (o/N) : ")

        if response.lower() == 'o':
            print("")
            print("="*70)
            print("🎉 CONFIGURATION TROUVÉE ! 🎉")
            print("="*70)
            print(f"Utilise ces paramètres :")
            print(f"  options.rows = {options.rows}")
            print(f"  options.cols = {options.cols}")
            print(f"  options.chain_length = {options.chain_length}")
            print(f"  options.parallel = {options.parallel}")
            print(f"  options.multiplexing = {options.multiplexing}")
            print(f"  options.row_address_type = {options.row_address_type}")
            print(f"  options.hardware_mapping = '{options.hardware_mapping}'")
            print("="*70)
            return True

    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

    return False

# Test toutes les configs
print("On va tester 8 configurations différentes pour ton panneau 128×64.")
print("Pour chaque test, regarde si l'affichage couvre TOUT l'écran (128 pixels de large).")
print("")
input("Appuie sur ENTRÉE pour commencer...")

for i, config in enumerate(configurations, 1):
    print(f"\n[Test {i}/{len(configurations)}]")

    found = test_config(config)

    if found:
        print("\n✓ Configuration trouvée !")
        sys.exit(0)

    if i < len(configurations):
        input("\nAppuie sur ENTRÉE pour le test suivant...")

print("")
print("="*70)
print("Aucune configuration standard n'a fonctionné.")
print("Il faut peut-être ajuster d'autres paramètres.")
print("Envoie-moi une photo de ce que tu vois sur l'écran.")
print("="*70)
