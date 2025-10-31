#!/usr/bin/env python3
"""
Test pour panneau 128×64-32S (scan 1/32)
Configuration spécifique pour DV08-210519 128x64-32S-V1.0
"""

import sys
import os
import time

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
║   TEST PANNEAU 128×64-32S (scan 1/32)                    ║
║   DV08-210519 128x64-32S-V1.0                            ║
╚════════════════════════════════════════════════════════════╝
""")

print("Panneau identifié : 128×64-32S")
print("  - Résolution : 128×64 pixels")
print("  - Scan : 1/32 (32S)")
print("  - Adressage : ABC (3 bits) avec shift register")
print("")
print("Configuration recommandée pour ce type de panneau :")
print("  - rows = 64")
print("  - cols = 128")
print("  - row_address_type = 5 (shift register)")
print("  - gpio_slowdown = 2 ou 3")
print("")

# Configurations spécifiques pour panneau 32S
configs_to_test = [
    {
        "name": "Config 1 : row_addr=5, slowdown=2 (RECOMMANDÉ)",
        "rows": 64,
        "cols": 128,
        "chain": 1,
        "parallel": 1,
        "row_addr": 5,
        "multiplex": 0,
        "slowdown": 2,
        "panel_type": None
    },
    {
        "name": "Config 2 : row_addr=5, slowdown=3",
        "rows": 64,
        "cols": 128,
        "chain": 1,
        "parallel": 1,
        "row_addr": 5,
        "multiplex": 0,
        "slowdown": 3,
        "panel_type": None
    },
    {
        "name": "Config 3 : row_addr=3, slowdown=2",
        "rows": 64,
        "cols": 128,
        "chain": 1,
        "parallel": 1,
        "row_addr": 3,
        "multiplex": 0,
        "slowdown": 2,
        "panel_type": None
    },
    {
        "name": "Config 4 : row_addr=5, slowdown=2, FM6126A",
        "rows": 64,
        "cols": 128,
        "chain": 1,
        "parallel": 1,
        "row_addr": 5,
        "multiplex": 0,
        "slowdown": 2,
        "panel_type": "FM6126A"
    },
    {
        "name": "Config 5 : row_addr=5, slowdown=4",
        "rows": 64,
        "cols": 128,
        "chain": 1,
        "parallel": 1,
        "row_addr": 5,
        "multiplex": 0,
        "slowdown": 4,
        "panel_type": None
    },
]

input("Appuyez sur ENTRÉE pour commencer les tests...\n")

for i, config in enumerate(configs_to_test):
    print(f"\n{'='*80}")
    print(f"TEST {i+1}/{len(configs_to_test)} : {config['name']}")
    print(f"{'='*80}")

    try:
        options = RGBMatrixOptions()
        options.rows = config['rows']
        options.cols = config['cols']
        options.chain_length = config['chain']
        options.parallel = config['parallel']
        options.row_address_type = config['row_addr']
        options.multiplexing = config['multiplex']
        options.gpio_slowdown = config['slowdown']
        options.hardware_mapping = 'regular'
        options.brightness = 80
        options.disable_hardware_pulsing = False

        # PWM settings recommandés pour scan 1/32
        options.pwm_bits = 7
        options.pwm_lsb_nanoseconds = 50
        options.pwm_dither_bits = 1

        if config['panel_type']:
            options.panel_type = config['panel_type']

        print(f"\nParamètres:")
        print(f"  panel_type = {config['panel_type'] or 'None'}")
        print(f"  rows = {options.rows}")
        print(f"  cols = {options.cols}")
        print(f"  row_address_type = {config['row_addr']}  ← CRUCIAL pour 32S")
        print(f"  gpio_slowdown = {config['slowdown']}")
        print(f"  pwm_bits = {options.pwm_bits}")
        print(f"  pwm_lsb_nanoseconds = {options.pwm_lsb_nanoseconds}")

        print(f"\nCréation de la matrice...")
        matrix = RGBMatrix(options=options)

        width = matrix.width
        height = matrix.height

        print(f"✓ Matrice créée : {width}×{height}")

        # Test 1 : Tout en blanc
        print("\n1️⃣  Test : Remplir TOUT l'écran en BLANC (3 secondes)")
        print("    Vous devriez voir les 128×64 pixels TOUS allumés en blanc")

        for y in range(height):
            for x in range(width):
                matrix.SetPixel(x, y, 255, 255, 255)

        time.sleep(3)

        # Test 2 : 4 bandes verticales
        print("\n2️⃣  Test : 4 bandes de couleur verticales (3 secondes)")
        print("    ROUGE | VERT | BLEU | BLANC")

        matrix.Clear()

        for y in range(height):
            for x in range(0, width // 4):
                matrix.SetPixel(x, y, 255, 0, 0)  # Rouge
            for x in range(width // 4, width // 2):
                matrix.SetPixel(x, y, 0, 255, 0)  # Vert
            for x in range(width // 2, 3 * width // 4):
                matrix.SetPixel(x, y, 0, 0, 255)  # Bleu
            for x in range(3 * width // 4, width):
                matrix.SetPixel(x, y, 255, 255, 255)  # Blanc

        time.sleep(3)

        # Test 3 : Bordure
        print("\n3️⃣  Test : Bordure rouge autour de l'écran (2 secondes)")

        matrix.Clear()

        # Haut et bas
        for x in range(width):
            matrix.SetPixel(x, 0, 255, 0, 0)
            matrix.SetPixel(x, height - 1, 255, 0, 0)

        # Gauche et droite
        for y in range(height):
            matrix.SetPixel(0, y, 255, 0, 0)
            matrix.SetPixel(width - 1, y, 255, 0, 0)

        time.sleep(2)

        # Test 4 : Damier
        print("\n4️⃣  Test : Damier (2 secondes)")

        matrix.Clear()

        for y in range(height):
            for x in range(width):
                if (x // 8 + y // 8) % 2 == 0:
                    matrix.SetPixel(x, y, 255, 255, 0)  # Jaune

        time.sleep(2)

        matrix.Clear()

        print("\n" + "="*80)
        print("VÉRIFIEZ L'AFFICHAGE :")
        print("="*80)
        print("  1. TOUT l'écran (128×64) était rempli en blanc ?")
        print("  2. Les 4 bandes couvraient TOUT l'écran ?")
        print("  3. La bordure faisait le tour COMPLET ?")
        print("  4. Le damier couvrait TOUT l'écran ?")
        print("  5. PAS seulement 16 lignes du bas ?")
        print("="*80)

        response = input(f"\nTOUT était PARFAIT ? (o/N) : ")

        if response.lower() == 'o':
            print("\n" + "="*80)
            print("🎉🎉🎉 CONFIGURATION TROUVÉE ! 🎉🎉🎉")
            print("="*80)
            print(f"\n✓ Configuration pour votre panneau 128×64-32S :\n")
            print("options = RGBMatrixOptions()")
            if config['panel_type']:
                print(f"options.panel_type = '{config['panel_type']}'")
            print(f"options.rows = {options.rows}")
            print(f"options.cols = {options.cols}")
            print(f"options.chain_length = {options.chain_length}")
            print(f"options.parallel = {options.parallel}")
            print(f"options.row_address_type = {config['row_addr']}  # ← CRUCIAL pour scan 1/32")
            print(f"options.multiplexing = {config['multiplex']}")
            print(f"options.gpio_slowdown = {config['slowdown']}  # ← Important")
            print(f"options.hardware_mapping = 'regular'")
            print(f"options.brightness = 80")
            print(f"options.pwm_bits = 7")
            print(f"options.pwm_lsb_nanoseconds = 50")
            print(f"options.pwm_dither_bits = 1")
            print("\n" + "="*80)

            # Sauvegarder
            with open('CONFIGURATION_128x64_32S.txt', 'w') as f:
                f.write("# Configuration pour panneau 128×64-32S (scan 1/32)\n")
                f.write("# DV08-210519 128x64-32S-V1.0\n\n")
                f.write("options = RGBMatrixOptions()\n")
                if config['panel_type']:
                    f.write(f"options.panel_type = '{config['panel_type']}'\n")
                f.write(f"options.rows = {options.rows}\n")
                f.write(f"options.cols = {options.cols}\n")
                f.write(f"options.chain_length = {options.chain_length}\n")
                f.write(f"options.parallel = {options.parallel}\n")
                f.write(f"options.row_address_type = {config['row_addr']}\n")
                f.write(f"options.multiplexing = {config['multiplex']}\n")
                f.write(f"options.gpio_slowdown = {config['slowdown']}\n")
                f.write(f"options.hardware_mapping = 'regular'\n")
                f.write(f"options.brightness = 80\n")
                f.write(f"options.pwm_bits = 7\n")
                f.write(f"options.pwm_lsb_nanoseconds = 50\n")
                f.write(f"options.pwm_dither_bits = 1\n")

            print("✓ Configuration sauvegardée dans CONFIGURATION_128x64_32S.txt")
            sys.exit(0)

    except Exception as e:
        print(f"\n✗ Erreur : {e}")

    if i < len(configs_to_test) - 1:
        input("\nAppuyez sur ENTRÉE pour le test suivant...")

print("\n" + "="*80)
print("AUCUNE CONFIGURATION N'A PARFAITEMENT FONCTIONNÉ")
print("="*80)
print("\nSi l'une des configurations donnait un meilleur résultat")
print("(même pas parfait), notez laquelle et on pourra ajuster.")
print("")
print("Possibilités :")
print("  1. Essayez avec un slowdown plus élevé (5, 6, 7, 8)")
print("  2. Votre panneau nécessite peut-être un HAT avec level shifter")
print("="*80)
