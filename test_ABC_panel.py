#!/usr/bin/env python3
"""
Test SPÉCIFIQUE pour panneaux avec adressage ABC uniquement
(DV08-210519 128x64-32S V1.0)

CE PANNEAU N'A QUE 3 LIGNES D'ADRESSAGE : A, B, C
(pas de D ou E)

DONC il faut ABSOLUMENT utiliser row_address_type = 3 ou 5 !
"""

import sys
import os
import time

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

def test_config(name, row_addr_type, gpio_slow, multiplex=0, panel_type=None):
    """Teste une configuration spécifique"""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}")
    print(f"  row_address_type: {row_addr_type}")
    print(f"  gpio_slowdown: {gpio_slow}")
    print(f"  multiplexing: {multiplex}")
    if panel_type:
        print(f"  panel_type: {panel_type}")

    try:
        options = RGBMatrixOptions()

        # Configuration de base pour 128x64 (2 panneaux de 64x32)
        options.rows = 32
        options.cols = 64
        options.chain_length = 2
        options.parallel = 1

        # Hardware Adafruit
        options.hardware_mapping = 'adafruit-hat'

        # PARAMÈTRES CRITIQUES POUR ABC
        options.row_address_type = row_addr_type  # CRITIQUE !
        options.gpio_slowdown = gpio_slow
        options.multiplexing = multiplex

        # Qualité d'affichage
        options.pwm_bits = 11
        options.brightness = 60
        options.led_rgb_sequence = "RGB"

        # Panel type si spécifié
        if panel_type:
            options.panel_type = panel_type

        # Créer la matrice
        print("\nInitialisation...")
        matrix = RGBMatrix(options=options)
        print(f"✓ Matrice créée: {matrix.width}x{matrix.height}")

        # Test 1: Écran blanc complet
        print("\nTest 1: Blanc complet...")
        for y in range(matrix.height):
            for x in range(matrix.width):
                matrix.SetPixel(x, y, 80, 80, 80)
        time.sleep(2)

        # Test 2: Damier
        print("Test 2: Damier...")
        matrix.Clear()
        for y in range(matrix.height):
            for x in range(matrix.width):
                if (x // 8 + y // 8) % 2 == 0:
                    matrix.SetPixel(x, y, 100, 100, 100)
        time.sleep(2)

        # Test 3: Dégradé horizontal
        print("Test 3: Dégradé horizontal...")
        matrix.Clear()
        for x in range(matrix.width):
            color = int((x / matrix.width) * 100)
            for y in range(matrix.height):
                matrix.SetPixel(x, y, color, color, color)
        time.sleep(2)

        # Test 4: Couleurs RGB
        print("Test 4: Rouge...")
        matrix.Clear()
        for y in range(matrix.height):
            for x in range(matrix.width):
                matrix.SetPixel(x, y, 100, 0, 0)
        time.sleep(1.5)

        print("Test 5: Vert...")
        matrix.Clear()
        for y in range(matrix.height):
            for x in range(matrix.width):
                matrix.SetPixel(x, y, 0, 100, 0)
        time.sleep(1.5)

        print("Test 6: Bleu...")
        matrix.Clear()
        for y in range(matrix.width):
            for x in range(matrix.width):
                matrix.SetPixel(x, y, 0, 0, 100)
        time.sleep(1.5)

        # Test 5: Lignes horizontales (test adressage)
        print("Test 7: Lignes horizontales (crucial pour ABC)...")
        matrix.Clear()
        for y in range(0, matrix.height, 4):
            for x in range(matrix.width):
                matrix.SetPixel(x, y, 100, 100, 100)
        time.sleep(3)

        matrix.Clear()

        print(f"\n✓✓✓ SUCCÈS avec cette configuration ! ✓✓✓")
        return True

    except Exception as e:
        print(f"\n✗ Échec: {e}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  TEST PANNEAUX ABC - DV08-210519 128x64-32S                      ║
╚══════════════════════════════════════════════════════════════════╝

⚠️  TON PANNEAU A SEULEMENT 3 LIGNES D'ADRESSAGE (A, B, C)

Les configurations par défaut ne marchent PAS avec ce type de panneau !
On va tester les configurations spécifiques ABC.

IMPORTANT: Tu dois avoir :
  • Une alimentation 5V 10A minimum (0.3A ne suffit PAS)
  • Le bonnet Adafruit bien connecté
  • Sudo pour exécuter ce script

Appuie sur ENTER pour continuer...
""")

    try:
        input()
    except KeyboardInterrupt:
        print("\nAnnulé.")
        return

    successful = []

    # TEST 1: row_address_type = 3 (méthode ABC standard)
    if test_config(
        "Config 1: ABC Standard (type 3), slowdown 2",
        row_addr_type=3,
        gpio_slow=2
    ):
        successful.append("ABC type 3, slowdown 2")

    time.sleep(2)

    # TEST 2: row_address_type = 3 avec slowdown 3
    if test_config(
        "Config 2: ABC Standard (type 3), slowdown 3",
        row_addr_type=3,
        gpio_slow=3
    ):
        successful.append("ABC type 3, slowdown 3")

    time.sleep(2)

    # TEST 3: row_address_type = 5 (méthode ABC rapide)
    if test_config(
        "Config 3: ABC Rapide (type 5), slowdown 2",
        row_addr_type=5,
        gpio_slow=2
    ):
        successful.append("ABC type 5, slowdown 2")

    time.sleep(2)

    # TEST 4: row_address_type = 3 avec multiplexing 1
    if test_config(
        "Config 4: ABC type 3, slowdown 2, multiplexing 1",
        row_addr_type=3,
        gpio_slow=2,
        multiplex=1
    ):
        successful.append("ABC type 3, slowdown 2, multiplex 1")

    time.sleep(2)

    # TEST 5: Avec FM6126A panel type
    if test_config(
        "Config 5: ABC type 3 + FM6126A chip",
        row_addr_type=3,
        gpio_slow=2,
        panel_type="FM6126A"
    ):
        successful.append("ABC type 3 + FM6126A")

    time.sleep(2)

    # TEST 6: row_address_type = 5 avec slowdown 1
    if test_config(
        "Config 6: ABC type 5, slowdown 1 (plus rapide)",
        row_addr_type=5,
        gpio_slow=1
    ):
        successful.append("ABC type 5, slowdown 1")

    # RÉSUMÉ
    print("\n\n" + "="*70)
    print("RÉSUMÉ DES TESTS")
    print("="*70)

    if successful:
        print(f"\n✓ {len(successful)} configuration(s) réussie(s):")
        for i, config in enumerate(successful, 1):
            print(f"  {i}. {config}")

        print("\n📝 UTILISE LA PREMIÈRE CONFIG QUI A MARCHÉ pour ton code final !")
    else:
        print("\n✗ Aucune configuration n'a fonctionné.")
        print("\nPROBLÈMES POSSIBLES:")
        print("  1. ⚡ ALIMENTATION INSUFFISANTE (tu as 0.3A, il faut 10A !)")
        print("     → C'est probablement LE problème principal")
        print("  2. 🔌 Câblage incorrect")
        print("  3. 💔 Panneau défectueux")
        print("  4. 🎛️  Bonnet mal connecté")
        print("\n👉 CHANGE L'ALIMENTATION EN PRIORITÉ !")

    print("\n" + "="*70)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️  Ce script doit être exécuté avec sudo:")
        print("   sudo python3 test_ABC_panel.py")
        sys.exit(1)

    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrompu par l'utilisateur.")
        sys.exit(0)
