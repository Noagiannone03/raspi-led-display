#!/usr/bin/env python3
"""
Test final pour panneau 128×64-32S
On sait que row_address_type=5 fonctionne partiellement
Maintenant on teste avec différents multiplexing et parallel
"""

import sys
import os
import time

# Argument : numéro de config à tester
config_num = 0
if len(sys.argv) > 1:
    try:
        config_num = int(sys.argv[1])
    except ValueError:
        pass

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
║   TEST FINAL PANNEAU 128×64-32S                           ║
║   row_address_type = 5 (confirmé)                         ║
║   Teste maintenant multiplexing + parallel                ║
╚════════════════════════════════════════════════════════════╝
""")

# Configurations à tester avec row_address_type=5
configs = [
    # rows=64, différents multiplexing
    {"rows": 64, "cols": 128, "parallel": 1, "multiplex": 0, "slowdown": 2, "name": "rows=64, parallel=1, mux=0"},
    {"rows": 64, "cols": 128, "parallel": 1, "multiplex": 1, "slowdown": 2, "name": "rows=64, parallel=1, mux=1"},
    {"rows": 64, "cols": 128, "parallel": 1, "multiplex": 2, "slowdown": 2, "name": "rows=64, parallel=1, mux=2"},

    # parallel=2 (peut-être le panneau utilise 2 lignes en parallèle)
    {"rows": 32, "cols": 128, "parallel": 2, "multiplex": 0, "slowdown": 2, "name": "rows=32, parallel=2, mux=0"},
    {"rows": 32, "cols": 128, "parallel": 2, "multiplex": 1, "slowdown": 2, "name": "rows=32, parallel=2, mux=1"},
    {"rows": 32, "cols": 128, "parallel": 2, "multiplex": 2, "slowdown": 2, "name": "rows=32, parallel=2, mux=2"},

    # Autres multiplexing importants
    {"rows": 64, "cols": 128, "parallel": 1, "multiplex": 8, "slowdown": 2, "name": "rows=64, parallel=1, mux=8 (ZStripeUneven)"},
    {"rows": 64, "cols": 128, "parallel": 1, "multiplex": 11, "slowdown": 2, "name": "rows=64, parallel=1, mux=11 (InversedZStripe)"},

    # Avec slowdown plus élevé
    {"rows": 64, "cols": 128, "parallel": 1, "multiplex": 0, "slowdown": 3, "name": "rows=64, parallel=1, mux=0, slowdown=3"},
    {"rows": 64, "cols": 128, "parallel": 1, "multiplex": 0, "slowdown": 4, "name": "rows=64, parallel=1, mux=0, slowdown=4"},

    # rows=16, parallel=4 (panneau divisé en 4 sections)
    {"rows": 16, "cols": 128, "parallel": 4, "multiplex": 0, "slowdown": 2, "name": "rows=16, parallel=4, mux=0"},
]

if config_num >= len(configs):
    print(f"❌ Config {config_num} n'existe pas (max = {len(configs) - 1})")
    print("\nUtilisation: sudo python3 test_32S_final.py [numéro]")
    print("\nConfigurations disponibles:")
    for i, c in enumerate(configs):
        print(f"  {i}: {c['name']}")
    sys.exit(1)

config = configs[config_num]

print(f"Configuration {config_num}/{len(configs) - 1} : {config['name']}")
print("")

try:
    options = RGBMatrixOptions()
    options.rows = config['rows']
    options.cols = config['cols']
    options.chain_length = 1
    options.parallel = config['parallel']
    options.row_address_type = 5  # ← Confirmé comme correct
    options.multiplexing = config['multiplex']
    options.gpio_slowdown = config['slowdown']
    options.hardware_mapping = 'regular'
    options.brightness = 80
    options.disable_hardware_pulsing = False

    # PWM settings pour scan 1/32
    options.pwm_bits = 7
    options.pwm_lsb_nanoseconds = 50
    options.pwm_dither_bits = 1

    print("Paramètres:")
    print(f"  rows = {options.rows}")
    print(f"  cols = {options.cols}")
    print(f"  parallel = {options.parallel}")
    print(f"  row_address_type = 5 (shift register)")
    print(f"  multiplexing = {config['multiplex']}")
    print(f"  gpio_slowdown = {config['slowdown']}")
    print("")

    print("Création de la matrice...")
    matrix = RGBMatrix(options=options)

    width = matrix.width
    height = matrix.height

    print(f"✓ Matrice créée : {width}×{height}")
    print("")

    # Test 1 : Tout en blanc
    print("1️⃣  Remplir TOUT l'écran en BLANC (3 secondes)")
    for y in range(min(64, height)):
        for x in range(min(128, width)):
            matrix.SetPixel(x, y, 255, 255, 255)
    time.sleep(3)

    # Test 2 : 4 bandes verticales
    print("2️⃣  4 bandes de couleur : ROUGE | VERT | BLEU | BLANC (3 secondes)")
    matrix.Clear()

    for y in range(min(64, height)):
        for x in range(0, min(32, width)):
            matrix.SetPixel(x, y, 255, 0, 0)  # Rouge
        for x in range(32, min(64, width)):
            matrix.SetPixel(x, y, 0, 255, 0)  # Vert
        for x in range(64, min(96, width)):
            matrix.SetPixel(x, y, 0, 0, 255)  # Bleu
        for x in range(96, min(128, width)):
            matrix.SetPixel(x, y, 255, 255, 255)  # Blanc

    time.sleep(3)

    # Test 3 : Bandes horizontales de couleurs
    print("3️⃣  4 bandes HORIZONTALES de couleur (3 secondes)")
    matrix.Clear()

    for y in range(0, min(16, height)):
        for x in range(min(128, width)):
            matrix.SetPixel(x, y, 255, 0, 0)  # Rouge
    for y in range(16, min(32, height)):
        for x in range(min(128, width)):
            matrix.SetPixel(x, y, 0, 255, 0)  # Vert
    for y in range(32, min(48, height)):
        for x in range(min(128, width)):
            matrix.SetPixel(x, y, 0, 0, 255)  # Bleu
    for y in range(48, min(64, height)):
        for x in range(min(128, width)):
            matrix.SetPixel(x, y, 255, 255, 255)  # Blanc

    time.sleep(3)

    # Test 4 : Damier
    print("4️⃣  Damier (2 secondes)")
    matrix.Clear()
    for y in range(min(64, height)):
        for x in range(min(128, width)):
            if (x // 8 + y // 8) % 2 == 0:
                matrix.SetPixel(x, y, 255, 255, 0)  # Jaune

    time.sleep(2)

    # Test 5 : Bordure
    print("5️⃣  Bordure rouge (2 secondes)")
    matrix.Clear()

    for x in range(min(128, width)):
        matrix.SetPixel(x, 0, 255, 0, 0)
        if height > 1:
            matrix.SetPixel(x, min(63, height - 1), 255, 0, 0)

    for y in range(min(64, height)):
        matrix.SetPixel(0, y, 255, 0, 0)
        if width > 1:
            matrix.SetPixel(min(127, width - 1), y, 255, 0, 0)

    time.sleep(2)

    matrix.Clear()

    print("")
    print("="*80)
    print("RÉSULTATS À VÉRIFIER :")
    print("="*80)
    print("  1. TOUT l'écran (128×64) était-il rempli ?")
    print("  2. Les couleurs étaient-elles CORRECTES (pas tout en vert) ?")
    print("  3. Les bandes verticales : ROUGE, VERT, BLEU, BLANC ?")
    print("  4. Les bandes horizontales apparaissaient-elles correctement ?")
    print("  5. La bordure faisait-elle le tour COMPLET de l'écran ?")
    print("="*80)
    print("")

    response = input("TOUT était PARFAIT ? (o/N) : ")

    if response.lower() == 'o':
        print("")
        print("="*80)
        print("🎉🎉🎉 CONFIGURATION TROUVÉE ! 🎉🎉🎉")
        print("="*80)
        print("")
        print("Configuration pour votre panneau 128×64-32S :")
        print("")
        print("options = RGBMatrixOptions()")
        print(f"options.rows = {options.rows}")
        print(f"options.cols = {options.cols}")
        print(f"options.chain_length = 1")
        print(f"options.parallel = {options.parallel}")
        print(f"options.row_address_type = 5  # Shift register pour 32S")
        print(f"options.multiplexing = {config['multiplex']}")
        print(f"options.gpio_slowdown = {config['slowdown']}")
        print(f"options.hardware_mapping = 'regular'")
        print(f"options.brightness = 80")
        print(f"options.pwm_bits = 7")
        print(f"options.pwm_lsb_nanoseconds = 50")
        print(f"options.pwm_dither_bits = 1")
        print("")
        print("="*80)

        # Sauvegarder
        with open('CONFIG_FINALE_32S.txt', 'w') as f:
            f.write("# Configuration FINALE pour panneau 128×64-32S\n")
            f.write("# DV08-210519 128x64-32S-V1.0\n\n")
            f.write("options = RGBMatrixOptions()\n")
            f.write(f"options.rows = {options.rows}\n")
            f.write(f"options.cols = {options.cols}\n")
            f.write(f"options.chain_length = 1\n")
            f.write(f"options.parallel = {options.parallel}\n")
            f.write(f"options.row_address_type = 5\n")
            f.write(f"options.multiplexing = {config['multiplex']}\n")
            f.write(f"options.gpio_slowdown = {config['slowdown']}\n")
            f.write(f"options.hardware_mapping = 'regular'\n")
            f.write(f"options.brightness = 80\n")
            f.write(f"options.pwm_bits = 7\n")
            f.write(f"options.pwm_lsb_nanoseconds = 50\n")
            f.write(f"options.pwm_dither_bits = 1\n")

        print("✓ Configuration sauvegardée dans CONFIG_FINALE_32S.txt")
        print("")
    else:
        print("")
        print("Décrivez ce que vous avez vu :")
        print("  - Combien de lignes/pixels allumés ?")
        print("  - Quelles couleurs ?")
        print("  - Où sur l'écran ?")
        print("")
        print(f"Pour tester la config suivante, lancez :")
        print(f"  sudo python3 test_32S_final.py {config_num + 1}")

except Exception as e:
    print(f"\n✗ Erreur : {e}")
    import traceback
    traceback.print_exc()

print("")
print("="*80)
print("LISTE DES CONFIGURATIONS À TESTER :")
print("="*80)
for i, c in enumerate(configs):
    marker = "←" if i == config_num else ""
    print(f"  sudo python3 test_32S_final.py {i:2d}  # {c['name']} {marker}")
print("="*80)
