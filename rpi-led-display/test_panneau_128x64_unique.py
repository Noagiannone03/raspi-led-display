#!/usr/bin/env python3
"""
Test pour UN SEUL panneau 128×64 (pas deux panneaux en chaîne)
Usage: sudo python3 test_panneau_128x64_unique.py [slowdown]
"""

import sys
import os
import time

# Récupérer la valeur slowdown depuis les arguments
slowdown = 1  # Valeur par défaut
if len(sys.argv) > 1:
    try:
        slowdown = int(sys.argv[1])
    except ValueError:
        print("❌ slowdown doit être un nombre entier")
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
║       TEST PANNEAU UNIQUE 128×64                          ║
║       (pas deux panneaux en chaîne)                       ║
╚════════════════════════════════════════════════════════════╝
""")

print("Configuration pour UN SEUL panneau 128×64 :")
print("  - rows = 64 (pas 32 !)")
print("  - cols = 128")
print("  - chain_length = 1 (un seul panneau)")
print(f"  - gpio_slowdown = {slowdown}")
print("")

try:
    options = RGBMatrixOptions()

    # CONFIGURATION POUR UN SEUL PANNEAU 128×64
    options.rows = 64          # ← 64 lignes !
    options.cols = 128         # ← 128 colonnes !
    options.chain_length = 1   # ← UN SEUL panneau !
    options.parallel = 1

    options.hardware_mapping = 'regular'
    options.gpio_slowdown = slowdown
    options.brightness = 80
    options.disable_hardware_pulsing = False

    # Paramètres pour panneau avec A, B, C seulement
    options.row_address_type = 0  # On va tester différentes valeurs
    options.multiplexing = 0

    print(f"Création de la matrice...")
    matrix = RGBMatrix(options=options)

    width = matrix.width
    height = matrix.height

    print(f"✓ Matrice créée : {width}×{height}")

    if width != 128 or height != 64:
        print(f"⚠️  ATTENTION : La matrice devrait être 128×64, pas {width}×{height}")
        print("    Il y a peut-être un problème de configuration.")

    print("\n" + "="*70)
    print("TEST 1 : Remplir TOUT l'écran en BLANC")
    print("="*70)
    print("Si tout fonctionne, vous devriez voir TOUT l'écran en blanc.")
    print("")

    # Remplir tout en blanc
    for y in range(height):
        for x in range(width):
            matrix.SetPixel(x, y, 255, 255, 255)

    time.sleep(3)

    # Test des bandes
    print("\n" + "="*70)
    print("TEST 2 : 4 bandes de couleur verticales")
    print("="*70)
    print("De gauche à droite : ROUGE, VERT, BLEU, BLANC")
    print("")

    matrix.Clear()

    # 4 bandes verticales
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

    # Test des lignes
    print("\n" + "="*70)
    print("TEST 3 : Lignes horizontales")
    print("="*70)
    print("5 lignes blanches horizontales : haut, 1/4, milieu, 3/4, bas")
    print("")

    matrix.Clear()

    lines_to_test = [0, height // 4, height // 2, 3 * height // 4, height - 1]

    for line in lines_to_test:
        matrix.Clear()
        print(f"  Ligne {line}...")
        for x in range(width):
            matrix.SetPixel(x, line, 255, 255, 255)
        time.sleep(1)

    # Damier
    print("\n" + "="*70)
    print("TEST 4 : Damier complet")
    print("="*70)
    print("")

    matrix.Clear()
    for y in range(height):
        for x in range(width):
            if (x // 8 + y // 8) % 2 == 0:
                matrix.SetPixel(x, y, 255, 255, 0)  # Jaune

    time.sleep(3)

    # Bordure
    print("\n" + "="*70)
    print("TEST 5 : Bordure rouge autour de l'écran")
    print("="*70)
    print("Vous devriez voir un cadre rouge tout autour de l'écran.")
    print("")

    matrix.Clear()

    # Ligne du haut
    for x in range(width):
        matrix.SetPixel(x, 0, 255, 0, 0)

    # Ligne du bas
    for x in range(width):
        matrix.SetPixel(x, height - 1, 255, 0, 0)

    # Ligne de gauche
    for y in range(height):
        matrix.SetPixel(0, y, 255, 0, 0)

    # Ligne de droite
    for y in range(height):
        matrix.SetPixel(width - 1, y, 255, 0, 0)

    time.sleep(3)

    matrix.Clear()

    print("\n" + "="*70)
    print("RÉSULTATS À VÉRIFIER :")
    print("="*70)
    print("\n1. L'écran ENTIER (128×64) était-il rempli en blanc ?")
    print("2. Les 4 bandes de couleur couvraient-elles TOUT l'écran ?")
    print("3. Les lignes horizontales s'affichaient-elles correctement ?")
    print("4. Le damier couvrait-il TOUT l'écran ?")
    print("5. La bordure rouge faisait-elle le tour COMPLET de l'écran ?")
    print("")
    print("="*70)

    response = input(f"\nTOUT fonctionnait parfaitement ? (o/N) : ")

    if response.lower() == 'o':
        print("\n" + "="*70)
        print("🎉🎉🎉 CONFIGURATION TROUVÉE ! 🎉🎉🎉")
        print("="*70)
        print(f"\n✓ Configuration pour votre panneau 128×64 unique :\n")
        print("options = RGBMatrixOptions()")
        print("options.rows = 64          # 64 lignes")
        print("options.cols = 128         # 128 colonnes")
        print("options.chain_length = 1   # UN SEUL panneau")
        print("options.parallel = 1")
        print("options.hardware_mapping = 'regular'")
        print(f"options.gpio_slowdown = {slowdown}")
        print("options.brightness = 80")
        print("options.disable_hardware_pulsing = False")
        print("options.row_address_type = 0")
        print("options.multiplexing = 0")
        print("\n" + "="*70)

        # Sauvegarder
        with open('CONFIGURATION_128x64_UNIQUE.txt', 'w') as f:
            f.write("# Configuration pour panneau 128×64 unique\n")
            f.write("options.rows = 64\n")
            f.write("options.cols = 128\n")
            f.write("options.chain_length = 1\n")
            f.write("options.parallel = 1\n")
            f.write("options.hardware_mapping = 'regular'\n")
            f.write(f"options.gpio_slowdown = {slowdown}\n")
            f.write("options.brightness = 80\n")
            f.write("options.disable_hardware_pulsing = False\n")
            f.write("options.row_address_type = 0\n")
            f.write("options.multiplexing = 0\n")

        print("✓ Configuration sauvegardée dans CONFIGURATION_128x64_UNIQUE.txt")
    else:
        print("\n❌ L'affichage n'est pas encore parfait.")
        print("\nQu'avez-vous vu exactement ?")
        print("  - Seulement une partie de l'écran s'allume ?")
        print("  - Les couleurs sont mélangées ?")
        print("  - Les lignes se répètent ?")
        print("")
        print("Décrivez le problème pour que je puisse vous aider.")

except Exception as e:
    print(f"\n✗ Erreur : {e}")
    import traceback
    traceback.print_exc()
