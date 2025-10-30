#!/usr/bin/env python3
"""
Test pour panneau P3 128×64 avec SEULEMENT A, B, C (pas de D ni E)
Ce type de panneau utilise un scan 1/8 avec multiplexage
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
║     TEST PANNEAU 128×64 avec scan 1/8                      ║
║     (Seulement A, B, C - pas de D ni E)                   ║
╚════════════════════════════════════════════════════════════╝
""")

# Configurations spécifiques pour panneau avec seulement 3 bits d'adressage
configurations = [
    {
        "name": "Config 1: 2×64×32, multiplexing=0 (scan 1/8 standard)",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 2: 2×64×32, multiplexing=1 (stripe)",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 1,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 3: 2×64×32, multiplexing=2 (checker)",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 2,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 4: 2×64×32, multiplexing=3 (spiral)",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 3,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 5: 2×64×32, multiplexing=4 (Z-strip)",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 4,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 6: Single 128×32 panel",
        "rows": 32,
        "cols": 128,
        "chain": 1,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 7: 2×64×32 avec adafruit-hat mapping",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 0,
        "hw_map": "adafruit-hat"
    },
    {
        "name": "Config 8: 2×64×16, scan 1/4",
        "rows": 16,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 9: 2×64×64 (au cas où)",
        "rows": 64,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 0,
        "hw_map": "regular"
    },
    {
        "name": "Config 10: 2×64×32, multiplexing=8 (Coreman)",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 8,
        "row_addr": 0,
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

        width = matrix.width
        height = matrix.height

        # Test 1: Bandes verticales
        print("Test 1: 4 bandes verticales (Rouge, Vert, Bleu, Blanc) - 3 sec...")

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

        # Test 2: Tout blanc pour vérifier la couverture
        print("Test 2: Écran tout blanc (2 sec)...")
        for y in range(height):
            for x in range(width):
                matrix.SetPixel(x, y, 255, 255, 255)

        time.sleep(2)

        # Test 3: Damier pour vérifier l'adressage
        print("Test 3: Damier (2 sec)...")
        for y in range(height):
            for x in range(width):
                if (x // 8 + y // 8) % 2 == 0:
                    matrix.SetPixel(x, y, 255, 0, 0)
                else:
                    matrix.SetPixel(x, y, 0, 0, 0)

        time.sleep(2)

        matrix.Clear()

        print("")
        print("✓ Configuration testée !")
        print("")
        print("Est-ce que tu as vu :")
        print("  1. Les 4 bandes de couleur correctement")
        print("  2. L'écran ENTIER est allumé (128 pixels de large)")
        print("  3. Le damier est régulier (pas de lignes bizarres)")
        print("")
        response = input("Est-ce que tout était correct ? (o/N) : ")

        if response.lower() == 'o':
            print("")
            print("="*70)
            print("🎉 CONFIGURATION TROUVÉE ! 🎉")
            print("="*70)
            print(f"\n👉 Copie ces paramètres dans ton script :")
            print("")
            print("options = RGBMatrixOptions()")
            print(f"options.rows = {options.rows}")
            print(f"options.cols = {options.cols}")
            print(f"options.chain_length = {options.chain_length}")
            print(f"options.parallel = {options.parallel}")
            print(f"options.multiplexing = {options.multiplexing}")
            print(f"options.row_address_type = {options.row_address_type}")
            print(f"options.hardware_mapping = '{options.hardware_mapping}'")
            print(f"options.brightness = 60")
            print(f"options.disable_hardware_pulsing = False")
            print("")
            print("="*70)
            return True

    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

    return False

# Test toutes les configs
print("On va tester 10 configurations différentes.")
print("Ton panneau a seulement A, B, C (pas de D ni E),")
print("donc il utilise un scan 1/8 avec multiplexage.")
print("")
print("Pour chaque test, vérifie que :")
print("  - Les couleurs sont bonnes")
print("  - L'affichage couvre TOUT l'écran (128 pixels de large)")
print("  - Le motif est régulier (pas de lignes dupliquées ou manquantes)")
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
print("Aucune configuration n'a parfaitement fonctionné.")
print("")
print("Si tu as vu quelque chose s'afficher (même partiellement),")
print("envoie-moi une photo ou décris ce que tu vois.")
print("")
print("Sinon, vérifie le câblage avec: sudo python3 test_wiring.py")
print("="*70)
