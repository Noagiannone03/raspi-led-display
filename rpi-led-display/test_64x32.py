#!/usr/bin/env python3
"""
Test pour panneau 64×32 (plus tolérant aux signaux 3.3V)
Ces panneaux fonctionnent souvent SANS level shifter !
"""

import sys
import os
import time

# Argument : numéro de config
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
║   TEST PANNEAU 64×32                                      ║
║   Ces panneaux sont plus tolérants aux signaux 3.3V !    ║
╚════════════════════════════════════════════════════════════╝
""")

print("Les panneaux 64×32 utilisent souvent des chips 74HCT245")
print("qui acceptent mieux les signaux 3.3V que les 128×64.")
print("")
print("Si votre panneau 64×32 a des chips 74HCT245 → Devrait marcher !")
print("Si il a des chips 74HC245 → Peut avoir des problèmes...")
print("")

# Configurations pour 64×32
configs = [
    # Configurations standard 64×32
    {"name": "64×32 standard, scan 1/16", "rows": 32, "cols": 64, "chain": 1, "parallel": 1, "row_addr": 0, "multiplex": 0, "slowdown": 1},
    {"name": "64×32 standard, scan 1/16, slowdown=2", "rows": 32, "cols": 64, "chain": 1, "parallel": 1, "row_addr": 0, "multiplex": 0, "slowdown": 2},
    {"name": "64×32 standard, scan 1/8", "rows": 16, "cols": 64, "chain": 1, "parallel": 2, "row_addr": 0, "multiplex": 0, "slowdown": 1},

    # Avec multiplexing
    {"name": "64×32, mux=1 (Stripe)", "rows": 32, "cols": 64, "chain": 1, "parallel": 1, "row_addr": 0, "multiplex": 1, "slowdown": 2},
    {"name": "64×32, mux=2 (Checkered)", "rows": 32, "cols": 64, "chain": 1, "parallel": 1, "row_addr": 0, "multiplex": 2, "slowdown": 2},

    # Avec différents row_address_type
    {"name": "64×32, row_addr=1", "rows": 32, "cols": 64, "chain": 1, "parallel": 1, "row_addr": 1, "multiplex": 0, "slowdown": 2},
    {"name": "64×32, row_addr=2", "rows": 32, "cols": 64, "chain": 1, "parallel": 1, "row_addr": 2, "multiplex": 0, "slowdown": 2},

    # Slowdown élevé pour aider la détection 3.3V
    {"name": "64×32, slowdown=3", "rows": 32, "cols": 64, "chain": 1, "parallel": 1, "row_addr": 0, "multiplex": 0, "slowdown": 3},
    {"name": "64×32, slowdown=4", "rows": 32, "cols": 64, "chain": 1, "parallel": 1, "row_addr": 0, "multiplex": 0, "slowdown": 4},
]

if config_num >= len(configs):
    print(f"❌ Config {config_num} n'existe pas (max = {len(configs) - 1})")
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
    options.chain_length = config['chain']
    options.parallel = config['parallel']
    options.row_address_type = config['row_addr']
    options.multiplexing = config['multiplex']
    options.gpio_slowdown = config['slowdown']
    options.hardware_mapping = 'regular'
    options.brightness = 80
    options.disable_hardware_pulsing = False

    print("Paramètres:")
    print(f"  rows = {options.rows}")
    print(f"  cols = {options.cols}")
    print(f"  chain_length = {options.chain_length}")
    print(f"  parallel = {options.parallel}")
    print(f"  row_address_type = {config['row_addr']}")
    print(f"  multiplexing = {config['multiplex']}")
    print(f"  gpio_slowdown = {config['slowdown']}")
    print("")

    print("Création de la matrice...")
    matrix = RGBMatrix(options=options)

    width = matrix.width
    height = matrix.height

    print(f"✓ Matrice créée : {width}×{height}")
    print("")

    # Test 1 : TOUT en blanc
    print("1️⃣  Remplir TOUT l'écran en BLANC (3 secondes)")
    for y in range(height):
        for x in range(width):
            matrix.SetPixel(x, y, 255, 255, 255)
    time.sleep(3)

    # Test 2 : 3 bandes verticales RGB
    print("2️⃣  3 bandes verticales : ROUGE | VERT | BLEU (3 secondes)")
    matrix.Clear()

    for y in range(height):
        for x in range(0, width // 3):
            matrix.SetPixel(x, y, 255, 0, 0)  # ROUGE
        for x in range(width // 3, 2 * width // 3):
            matrix.SetPixel(x, y, 0, 255, 0)  # VERT
        for x in range(2 * width // 3, width):
            matrix.SetPixel(x, y, 0, 0, 255)  # BLEU

    time.sleep(3)

    # Test 3 : Bandes horizontales
    print("3️⃣  3 bandes HORIZONTALES : ROUGE | VERT | BLEU (3 secondes)")
    matrix.Clear()

    for y in range(0, height // 3):
        for x in range(width):
            matrix.SetPixel(x, y, 255, 0, 0)  # ROUGE
    for y in range(height // 3, 2 * height // 3):
        for x in range(width):
            matrix.SetPixel(x, y, 0, 255, 0)  # VERT
    for y in range(2 * height // 3, height):
        for x in range(width):
            matrix.SetPixel(x, y, 0, 0, 255)  # BLEU

    time.sleep(3)

    # Test 4 : Damier
    print("4️⃣  Damier (2 secondes)")
    matrix.Clear()
    for y in range(height):
        for x in range(width):
            if (x // 4 + y // 4) % 2 == 0:
                matrix.SetPixel(x, y, 255, 255, 0)  # JAUNE

    time.sleep(2)

    # Test 5 : Bordure
    print("5️⃣  Bordure rouge (2 secondes)")
    matrix.Clear()

    for x in range(width):
        matrix.SetPixel(x, 0, 255, 0, 0)
        if height > 1:
            matrix.SetPixel(x, height - 1, 255, 0, 0)

    for y in range(height):
        matrix.SetPixel(0, y, 255, 0, 0)
        if width > 1:
            matrix.SetPixel(width - 1, y, 255, 0, 0)

    time.sleep(2)

    matrix.Clear()

    print("")
    print("="*80)
    print("RÉSULTATS À VÉRIFIER :")
    print("="*80)
    print("  1. TOUT l'écran (64×32) était-il rempli en BLANC ?")
    print("  2. Les 3 couleurs (ROUGE, VERT, BLEU) s'affichaient-elles TOUTES ?")
    print("  3. Les bandes verticales ET horizontales étaient correctes ?")
    print("  4. Le damier couvrait tout l'écran ?")
    print("  5. La bordure faisait le tour complet ?")
    print("="*80)
    print("")

    response = input("TOUT était PARFAIT ? (o/N) : ")

    if response.lower() == 'o':
        print("")
        print("="*80)
        print("🎉🎉🎉 CONFIGURATION TROUVÉE ! 🎉🎉🎉")
        print("="*80)
        print("")
        print("Configuration pour votre panneau 64×32 :")
        print("")
        print("options = RGBMatrixOptions()")
        print(f"options.rows = {options.rows}")
        print(f"options.cols = {options.cols}")
        print(f"options.chain_length = {options.chain_length}")
        print(f"options.parallel = {options.parallel}")
        print(f"options.row_address_type = {config['row_addr']}")
        print(f"options.multiplexing = {config['multiplex']}")
        print(f"options.gpio_slowdown = {config['slowdown']}")
        print(f"options.hardware_mapping = 'regular'")
        print(f"options.brightness = 80")
        print("")
        print("="*80)

        # Sauvegarder
        with open('CONFIG_64x32_SANS_HAT.txt', 'w') as f:
            f.write("# Configuration pour panneau 64×32 SANS HAT (3.3V direct)\n\n")
            f.write("options = RGBMatrixOptions()\n")
            f.write(f"options.rows = {options.rows}\n")
            f.write(f"options.cols = {options.cols}\n")
            f.write(f"options.chain_length = {options.chain_length}\n")
            f.write(f"options.parallel = {options.parallel}\n")
            f.write(f"options.row_address_type = {config['row_addr']}\n")
            f.write(f"options.multiplexing = {config['multiplex']}\n")
            f.write(f"options.gpio_slowdown = {config['slowdown']}\n")
            f.write(f"options.hardware_mapping = 'regular'\n")
            f.write(f"options.brightness = 80\n")

        print("✓ Configuration sauvegardée dans CONFIG_64x32_SANS_HAT.txt")
        print("")
    else:
        print("")
        print("Décrivez ce que vous avez vu :")
        print("  - Toutes les couleurs (R, V, B) s'affichent ?")
        print("  - Ou seulement une couleur (comme avec le 128×64) ?")
        print("  - Tout l'écran s'allume ?")
        print("")
        print(f"Pour tester la config suivante : sudo python3 test_64x32.py {config_num + 1}")

except Exception as e:
    print(f"\n✗ Erreur : {e}")
    import traceback
    traceback.print_exc()

print("")
print("="*80)
print("CONFIGURATIONS À TESTER (dans l'ordre) :")
print("="*80)
for i, c in enumerate(configs):
    marker = "←" if i == config_num else ""
    print(f"  sudo python3 test_64x32.py {i}  # {c['name']} {marker}")
print("="*80)
print("")
print("💡 CONSEIL : Commencez par config 0 (standard)")
print("   Si tout VERT comme avec le 128×64 → Essayez config 7 et 8 (slowdown élevé)")
