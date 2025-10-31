#!/usr/bin/env python3
"""
Test EXHAUSTIF pour trouver la configuration exacte de votre panneau
Ce script teste TOUS les paramètres possibles : hardware_mapping, row_address_type, multiplexing
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
║         TEST EXHAUSTIF DE TOUTES LES CONFIGURATIONS       ║
║                                                            ║
║  Ce script teste TOUS les paramètres possibles pour       ║
║  trouver la configuration exacte de votre panneau 128×64   ║
╚════════════════════════════════════════════════════════════╝
""")

# Tous les mappings hardware possibles
hardware_mappings = [
    "regular",
    "adafruit-hat",
    "adafruit-hat-pwm",
    "regular-pi1",
    "classic",
    "classic-pi1"
]

# Tous les row_address_type possibles (CRUCIAL pour panneau avec A,B,C seulement)
row_address_types = [
    0,  # Direct (défaut)
    1,  # AB-addressed panels
    2,  # Direct row select
    3,  # ABC-addressed panels  ← PROBABLEMENT CELUI-CI pour votre panneau
    4,  # ABC Shift + DE direct
]

# Tous les multiplexing possibles
multiplexing_modes = [
    0,   # Direct (défaut)
    1,   # Stripe
    2,   # Checkered
    3,   # Spiral
    4,   # ZStripe (uneven Z-stripe)
    5,   # ZnMirrorZStripe
    6,   # coreman
    7,   # Kaler2Scan
    8,   # ZStripeUneven
    9,   # P10-128x4-Z
    10,  # QiangLiQ8
    11,  # InversedZStripe
]

# Configurations de base à tester
base_configs = [
    {
        "name": "128×64 - 2 panneaux 64×32 en chaîne",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
    },
    {
        "name": "128×64 - 4 panneaux 64×32 en parallèle",
        "rows": 32,
        "cols": 64,
        "chain": 1,
        "parallel": 2,
    },
]

def test_configuration(hw_map, row_addr, multiplex, base_config):
    """Teste une configuration complète"""

    config_name = f"{hw_map} | row_addr={row_addr} | mux={multiplex} | {base_config['name']}"

    print(f"\n{'='*80}")
    print(f"TEST: {config_name}")
    print(f"{'='*80}")

    try:
        # Configuration
        options = RGBMatrixOptions()
        options.rows = base_config['rows']
        options.cols = base_config['cols']
        options.chain_length = base_config['chain']
        options.parallel = base_config['parallel']
        options.hardware_mapping = hw_map
        options.row_address_type = row_addr
        options.multiplexing = multiplex
        options.brightness = 70
        options.disable_hardware_pulsing = False
        options.pwm_lsb_nanoseconds = 130  # Aide à réduire le scintillement

        print(f"\nParamètres:")
        print(f"  hardware_mapping = '{hw_map}'")
        print(f"  row_address_type = {row_addr}")
        print(f"  multiplexing = {multiplex}")
        print(f"  rows = {options.rows}")
        print(f"  cols = {options.cols}")
        print(f"  chain_length = {options.chain_length}")
        print(f"  parallel = {options.parallel}")
        print(f"  → Résolution attendue: {options.cols * options.chain_length}×{options.rows}")

        matrix = RGBMatrix(options=options)

        width = matrix.width
        height = matrix.height

        print(f"\n✓ Matrice créée: {width}×{height}")

        # Test simple et rapide
        print("\nAffichage test (3 secondes)...")
        print("  - Gauche: ROUGE")
        print("  - Centre: VERT")
        print("  - Droite: BLEU")

        # Gauche rouge
        for y in range(height):
            for x in range(0, width // 3):
                matrix.SetPixel(x, y, 255, 0, 0)

        # Centre vert
        for y in range(height):
            for x in range(width // 3, 2 * width // 3):
                matrix.SetPixel(x, y, 0, 255, 0)

        # Droite bleu
        for y in range(height):
            for x in range(2 * width // 3, width):
                matrix.SetPixel(x, y, 0, 0, 255)

        time.sleep(3)

        # Test ligne blanche en haut et en bas
        matrix.Clear()
        print("\nTest lignes blanches haut/bas (2 secondes)...")

        # Ligne en haut
        for x in range(width):
            matrix.SetPixel(x, 0, 255, 255, 255)

        # Ligne en bas
        for x in range(width):
            matrix.SetPixel(x, height - 1, 255, 255, 255)

        time.sleep(2)

        matrix.Clear()

        print("\n✓ Test terminé !")
        print("\n" + "="*80)
        print("VÉRIFIEZ:")
        print("  1. Les 3 bandes de couleur couvraient TOUT l'écran (128 pixels de large)?")
        print("  2. Les couleurs étaient correctes (rouge, vert, bleu)?")
        print("  3. Les lignes blanches étaient bien en HAUT et en BAS?")
        print("  4. Pas de lignes bizarres ou répétées?")
        print("="*80)

        response = input("\nTout était PARFAIT ? (o/N) : ")

        if response.lower() == 'o':
            print("\n" + "="*80)
            print("🎉🎉🎉 CONFIGURATION TROUVÉE ! 🎉🎉🎉")
            print("="*80)
            print(f"\n👉 COPIEZ ET UTILISEZ CES PARAMÈTRES:\n")
            print("options = RGBMatrixOptions()")
            print(f"options.hardware_mapping = '{hw_map}'")
            print(f"options.row_address_type = {row_addr}  # ← CRUCIAL !")
            print(f"options.multiplexing = {multiplex}  # ← IMPORTANT !")
            print(f"options.rows = {options.rows}")
            print(f"options.cols = {options.cols}")
            print(f"options.chain_length = {options.chain_length}")
            print(f"options.parallel = {options.parallel}")
            print(f"options.brightness = 70")
            print(f"options.disable_hardware_pulsing = False")
            print(f"options.pwm_lsb_nanoseconds = 130")
            print("\n" + "="*80)

            # Sauvegarder dans un fichier
            with open('CONFIGURATION_TROUVEE.txt', 'w') as f:
                f.write("# Configuration trouvée pour votre panneau LED\n\n")
                f.write("options = RGBMatrixOptions()\n")
                f.write(f"options.hardware_mapping = '{hw_map}'\n")
                f.write(f"options.row_address_type = {row_addr}\n")
                f.write(f"options.multiplexing = {multiplex}\n")
                f.write(f"options.rows = {options.rows}\n")
                f.write(f"options.cols = {options.cols}\n")
                f.write(f"options.chain_length = {options.chain_length}\n")
                f.write(f"options.parallel = {options.parallel}\n")
                f.write(f"options.brightness = 70\n")
                f.write(f"options.disable_hardware_pulsing = False\n")
                f.write(f"options.pwm_lsb_nanoseconds = 130\n")

            print("✓ Configuration sauvegardée dans CONFIGURATION_TROUVEE.txt")
            return True

    except Exception as e:
        print(f"\n✗ Erreur: {e}")
        return False

    return False

# Programme principal
print("Ce script va tester TOUTES les combinaisons possibles.")
print("Pour chaque test, vous verrez 3 bandes de couleur puis des lignes blanches.")
print("\nCela peut prendre du temps (plusieurs minutes).")
print("")
print("CONSEIL: Concentrez-vous sur les configurations avec row_address_type=3")
print("         car votre panneau a seulement A, B, C (3 bits d'adressage).")
print("")

mode = input("Mode de test:\n  1. RAPIDE (teste uniquement row_address_type=2,3 et mux=0,1)\n  2. COMPLET (teste tout, peut prendre 30+ min)\nChoix (1/2): ")

if mode == "1":
    # Mode rapide - teste seulement les plus probables
    print("\nMode RAPIDE activé")
    row_address_types_to_test = [2, 3]
    multiplexing_modes_to_test = [0, 1]
    hardware_mappings_to_test = ["regular", "adafruit-hat"]
else:
    # Mode complet
    print("\nMode COMPLET activé - cela peut prendre du temps...")
    row_address_types_to_test = row_address_types
    multiplexing_modes_to_test = multiplexing_modes
    hardware_mappings_to_test = hardware_mappings

input("\nAppuyez sur ENTRÉE pour commencer...\n")

found = False
test_count = 0
total_tests = len(hardware_mappings_to_test) * len(row_address_types_to_test) * len(multiplexing_modes_to_test) * len(base_configs)

for hw_map in hardware_mappings_to_test:
    if found:
        break

    for row_addr in row_address_types_to_test:
        if found:
            break

        for multiplex in multiplexing_modes_to_test:
            if found:
                break

            for base_config in base_configs:
                test_count += 1
                print(f"\n[Test {test_count}/{total_tests}]")

                found = test_configuration(hw_map, row_addr, multiplex, base_config)

                if found:
                    print("\n✓ Configuration trouvée ! Fin des tests.")
                    sys.exit(0)

                if test_count < total_tests:
                    input("\nAppuyez sur ENTRÉE pour le test suivant (ou Ctrl+C pour arrêter)...")

print("\n" + "="*80)
print("Aucune configuration parfaite trouvée.")
print("")
print("Si vous avez vu quelque chose de PRESQUE correct:")
print("  - Notez les paramètres qui donnaient le meilleur résultat")
print("  - On pourra ajuster manuellement après")
print("="*80)
