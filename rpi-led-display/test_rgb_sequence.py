#!/usr/bin/env python3
"""
Test pour identifier quel canal RGB fonctionne
et tester différentes séquences RGB
"""

import sys
import os
import time

# Argument : séquence à tester
sequence = "RGB"  # Défaut
if len(sys.argv) > 1:
    sequence = sys.argv[1].upper()
    if len(sequence) != 3 or not all(c in "RGB" for c in sequence):
        print("❌ La séquence doit contenir R, G, et B (ex: RGB, GRB, BRG)")
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
║   TEST SÉQUENCE RGB : {sequence}                                ║
║   Pour identifier quel canal RGB fonctionne               ║
╚════════════════════════════════════════════════════════════╝
""")

print(f"Test avec led_rgb_sequence = '{sequence}'")
print("")
print("Ce test va afficher ROUGE, puis VERT, puis BLEU.")
print("Notez quelle VRAIE couleur apparaît pour chaque test.")
print("")

try:
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 128
    options.chain_length = 1
    options.parallel = 1
    options.row_address_type = 5  # On sait que c'est correct
    options.multiplexing = 0
    options.gpio_slowdown = 2
    options.hardware_mapping = 'regular'
    options.brightness = 80
    options.led_rgb_sequence = sequence  # ← TEST DE LA SÉQUENCE
    options.pwm_bits = 7
    options.pwm_lsb_nanoseconds = 50

    print(f"Création de la matrice avec séquence '{sequence}'...")
    matrix = RGBMatrix(options=options)

    width = matrix.width
    height = matrix.height

    print(f"✓ Matrice créée : {width}×{height}")
    print("")

    # Test ROUGE
    print("="*70)
    print("TEST 1 : Envoi de ROUGE (255, 0, 0)")
    print("="*70)
    print("Quelle couleur voyez-vous s'afficher ?")
    print("")

    matrix.Clear()
    for y in range(height):
        for x in range(width):
            matrix.SetPixel(x, y, 255, 0, 0)  # ROUGE

    time.sleep(3)

    couleur_vue_rouge = input("Quelle couleur apparaît ? (R=rouge, V=vert, B=bleu, A=autre) : ").upper()

    # Test VERT
    print("")
    print("="*70)
    print("TEST 2 : Envoi de VERT (0, 255, 0)")
    print("="*70)
    print("Quelle couleur voyez-vous s'afficher ?")
    print("")

    matrix.Clear()
    for y in range(height):
        for x in range(width):
            matrix.SetPixel(x, y, 0, 255, 0)  # VERT

    time.sleep(3)

    couleur_vue_vert = input("Quelle couleur apparaît ? (R=rouge, V=vert, B=bleu, A=autre) : ").upper()

    # Test BLEU
    print("")
    print("="*70)
    print("TEST 3 : Envoi de BLEU (0, 0, 255)")
    print("="*70)
    print("Quelle couleur voyez-vous s'afficher ?")
    print("")

    matrix.Clear()
    for y in range(height):
        for x in range(width):
            matrix.SetPixel(x, y, 0, 0, 255)  # BLEU

    time.sleep(3)

    couleur_vue_bleu = input("Quelle couleur apparaît ? (R=rouge, V=vert, B=bleu, A=autre) : ").upper()

    matrix.Clear()

    # Analyse
    print("")
    print("="*70)
    print("ANALYSE DES RÉSULTATS")
    print("="*70)
    print("")
    print(f"Séquence testée : {sequence}")
    print("")
    print(f"  Envoi ROUGE (255,0,0) → Vous avez vu : {couleur_vue_rouge}")
    print(f"  Envoi VERT (0,255,0)  → Vous avez vu : {couleur_vue_vert}")
    print(f"  Envoi BLEU (0,0,255)  → Vous avez vu : {couleur_vue_bleu}")
    print("")

    # Déterminer la bonne séquence
    mapping = {
        'R': couleur_vue_rouge,
        'V': couleur_vue_vert,
        'B': couleur_vue_bleu
    }

    if couleur_vue_rouge == 'R' and couleur_vue_vert == 'V' and couleur_vue_bleu == 'B':
        print("✅ PARFAIT ! La séquence RGB est correcte !")
        print(f"   Utilisez : options.led_rgb_sequence = '{sequence}'")

        with open('CONFIG_RGB_SEQUENCE.txt', 'w') as f:
            f.write(f"# Séquence RGB correcte trouvée\n")
            f.write(f"options.led_rgb_sequence = '{sequence}'\n")

        print("")
        print("Configuration sauvegardée dans CONFIG_RGB_SEQUENCE.txt")
    else:
        print("❌ Les couleurs ne sont PAS correctes.")
        print("")
        print("Séquences suggérées à tester :")

        sequences_a_tester = ["RGB", "RBG", "GRB", "GBR", "BRG", "BGR"]
        for seq in sequences_a_tester:
            if seq != sequence:
                print(f"  sudo python3 test_rgb_sequence.py {seq}")

    print("")
    print("="*70)

except Exception as e:
    print(f"\n✗ Erreur : {e}")
    import traceback
    traceback.print_exc()

print("")
print("TOUTES LES SÉQUENCES POSSIBLES :")
print("  sudo python3 test_rgb_sequence.py RGB  # Défaut")
print("  sudo python3 test_rgb_sequence.py RBG  # Rouge/Bleu inversés")
print("  sudo python3 test_rgb_sequence.py GRB  # Vert en premier")
print("  sudo python3 test_rgb_sequence.py GBR")
print("  sudo python3 test_rgb_sequence.py BRG")
print("  sudo python3 test_rgb_sequence.py BGR  # Tout inversé")
print("")
