#!/usr/bin/env python3
"""
Test avec UNE SEULE valeur de gpio_slowdown
Usage: sudo python3 test_slowdown_single.py [slowdown_value]
"""

import sys
import os
import time

# Récupérer la valeur slowdown depuis les arguments
if len(sys.argv) > 1:
    try:
        slowdown = int(sys.argv[1])
        if slowdown < 0 or slowdown > 4:
            print("❌ slowdown doit être entre 0 et 4")
            sys.exit(1)
    except ValueError:
        print("❌ slowdown doit être un nombre entier")
        sys.exit(1)
else:
    print("Usage: sudo python3 test_slowdown_single.py [slowdown_value]")
    print("Exemple: sudo python3 test_slowdown_single.py 2")
    sys.exit(1)

script_dir = os.path.dirname(os.path.abspath(__file__))
rgb_matrix_path = os.path.join(script_dir, 'rpi-rgb-led-matrix', 'bindings', 'python')
sys.path.insert(0, rgb_matrix_path)

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError as e:
    print("ERREUR: Module rgbmatrix non trouvé")
    print(f"Détail: {e}")
    sys.exit(1)

print(f"""
╔════════════════════════════════════════════════════════════╗
║       TEST avec gpio_slowdown = {slowdown}                          ║
╚════════════════════════════════════════════════════════════╝
""")

try:
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 2
    options.parallel = 1
    options.hardware_mapping = 'regular'
    options.gpio_slowdown = slowdown  # ← PARAMÈTRE CLÉ
    options.brightness = 80
    options.disable_hardware_pulsing = False

    print(f"Création de la matrice avec slowdown={slowdown}...")
    matrix = RGBMatrix(options=options)

    width = matrix.width
    height = matrix.height

    print(f"✓ Matrice créée : {width}×{height}")
    print("\n1️⃣  Test : 3 bandes de couleur verticales...")
    print("    Gauche=ROUGE, Centre=VERT, Droite=BLEU")

    # Rouge
    for y in range(height):
        for x in range(0, width // 3):
            matrix.SetPixel(x, y, 255, 0, 0)

    # Vert
    for y in range(height):
        for x in range(width // 3, 2 * width // 3):
            matrix.SetPixel(x, y, 0, 255, 0)

    # Bleu
    for y in range(height):
        for x in range(2 * width // 3, width):
            matrix.SetPixel(x, y, 0, 0, 255)

    time.sleep(3)

    # Test ligne par ligne
    print("\n2️⃣  Test : Lignes horizontales blanches ligne par ligne...")
    matrix.Clear()

    for line in [0, height // 4, height // 2, 3 * height // 4, height - 1]:
        matrix.Clear()
        print(f"    Ligne {line}...")
        for x in range(width):
            matrix.SetPixel(x, line, 255, 255, 255)
        time.sleep(1)

    # Damier
    print("\n3️⃣  Test : Damier...")
    matrix.Clear()
    for y in range(height):
        for x in range(width):
            if (x // 8 + y // 8) % 2 == 0:
                matrix.SetPixel(x, y, 255, 255, 255)

    time.sleep(3)

    matrix.Clear()

    print("\n" + "="*70)
    print("VÉRIFIEZ L'AFFICHAGE :")
    print("="*70)
    print("  1. Les 3 bandes couvraient TOUT l'écran (128 pixels) ?")
    print("  2. Les lignes blanches apparaissaient UNE PAR UNE ?")
    print("  3. Le damier était régulier sur tout l'écran ?")
    print("  4. Pas de lignes qui se répètent bizarrement ?")
    print("="*70)

    response = input(f"\nAvec slowdown={slowdown}, TOUT était parfait ? (o/N) : ")

    if response.lower() == 'o':
        print("\n" + "="*70)
        print("🎉 SOLUTION TROUVÉE ! 🎉")
        print("="*70)
        print(f"\n✓ Le paramètre qui fonctionne : gpio_slowdown = {slowdown}")
        print("\n👉 AJOUTEZ CE PARAMÈTRE dans tous vos scripts :\n")
        print("options = RGBMatrixOptions()")
        print(f"options.gpio_slowdown = {slowdown}  # ← IMPORTANT !")
        print("options.hardware_mapping = 'regular'")
        print("options.rows = 32")
        print("options.cols = 64")
        print("options.chain_length = 2")
        print("# ... autres paramètres")
        print("\n" + "="*70)

        # Sauvegarder
        with open('CONFIGURATION_SLOWDOWN.txt', 'w') as f:
            f.write(f"# Configuration trouvée\n")
            f.write(f"options.gpio_slowdown = {slowdown}\n")
            f.write(f"options.hardware_mapping = 'regular'\n")
            f.write(f"options.rows = 32\n")
            f.write(f"options.cols = 64\n")
            f.write(f"options.chain_length = 2\n")

        print("✓ Configuration sauvegardée dans CONFIGURATION_SLOWDOWN.txt")
    else:
        print(f"\n❌ slowdown={slowdown} ne fonctionne pas.")
        print("\nPour tester la valeur suivante, lancez :")
        print(f"sudo python3 test_slowdown_single.py {slowdown + 1}")

except Exception as e:
    print(f"\n✗ Erreur avec slowdown={slowdown} : {e}")
