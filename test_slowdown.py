#!/usr/bin/env python3
"""
Test avec différentes valeurs de gpio_slowdown
pour voir si ça résout le problème de niveau logique
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
║       TEST AVEC DIFFÉRENTS GPIO SLOWDOWN                  ║
║                                                            ║
║  Le slowdown ralentit les signaux GPIO pour aider         ║
║  le panneau à détecter les signaux 3.3V                   ║
╚════════════════════════════════════════════════════════════╝
""")

print("Ce test va essayer différentes valeurs de gpio_slowdown.")
print("Le slowdown ralentit les signaux pour aider le panneau à les détecter.")
print("")
print("Valeurs à tester : 0 (défaut), 1, 2, 3, 4")
print("Plus le nombre est élevé, plus les signaux sont lents.")
print("")
input("Appuyez sur ENTRÉE pour commencer...\n")

# Testez différentes valeurs de slowdown
for slowdown in [0, 1, 2, 3, 4]:
    print(f"\n{'='*70}")
    print(f"TEST {slowdown + 1}/5 : gpio_slowdown = {slowdown}")
    print(f"{'='*70}")

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

        print(f"\nCréation de la matrice avec slowdown={slowdown}...")
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

        lines_ok = True
        for line in [0, height // 4, height // 2, 3 * height // 4, height - 1]:
            matrix.Clear()
            for x in range(width):
                matrix.SetPixel(x, line, 255, 255, 255)
            time.sleep(0.5)

        # Damier
        print("\n3️⃣  Test : Damier...")
        matrix.Clear()
        for y in range(height):
            for x in range(width):
                if (x // 8 + y // 8) % 2 == 0:
                    matrix.SetPixel(x, y, 255, 255, 255)

        time.sleep(2)

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
            sys.exit(0)

    except Exception as e:
        print(f"\n✗ Erreur avec slowdown={slowdown} : {e}")

    if slowdown < 4:
        input("\nAppuyez sur ENTRÉE pour le test suivant...")

print("\n" + "="*70)
print("AUCUN SLOWDOWN N'A RÉSOLU LE PROBLÈME")
print("="*70)
print("\nSi aucune valeur de slowdown n'a fonctionné, cela signifie que")
print("votre panneau nécessite des signaux 5V (pas 3.3V).")
print("")
print("📋 SOLUTION : Vous avez besoin d'un HAT avec level shifter")
print("")
print("HATs recommandés :")
print("  1. Adafruit RGB Matrix HAT/Bonnet (~20€)")
print("     → https://www.adafruit.com/product/2345")
print("")
print("  2. Electrodragon RGB LED Matrix Panel Driver (~10€)")
print("")
print("  3. Waveshare RGB Matrix Driver HAT")
print("")
print("Le HAT convertit les signaux 3.3V du Raspberry Pi en 5V")
print("que votre panneau peut détecter correctement.")
print("")
print("Une fois le HAT installé, utilisez :")
print("  options.hardware_mapping = 'adafruit-hat'")
print("  options.gpio_slowdown = 1")
print("")
print("="*70)
print("\nLisez PROBLEME_NIVEAU_LOGIQUE.md pour plus de détails.")
print("="*70)
