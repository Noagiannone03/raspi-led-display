#!/usr/bin/env python3
"""
Test EXHAUSTIF pour panneau 128×64 unique avec toutes les configurations possibles
pour résoudre le problème des "16 lignes du bas seulement"
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
║   TEST EXHAUSTIF PANNEAU 128×64 UNIQUE                    ║
║   (Résolution problème "16 lignes du bas seulement")     ║
╚════════════════════════════════════════════════════════════╝
""")

print("Ce script va tester TOUTES les configurations pour panneau 128×64")
print("avec seulement A, B, C (3 bits d'adressage).")
print("")
print("Configurations à tester :")
print("  - row_address_type : 0, 3, 5 (le 5 est crucial pour 128×64 ABC)")
print("  - multiplexing : 0 à 11")
print("  - parallel : 1, 2, 3")
print("  - panel_type : None, FM6126A")
print("")

mode = input("Mode:\n  1. RAPIDE (teste seulement row_addr 3 et 5)\n  2. COMPLET (teste tout)\nChoix (1/2): ")

if mode == "1":
    row_address_types = [3, 5]
    multiplexing_modes = [0, 1, 2]
    parallel_values = [1, 2, 3]
else:
    row_address_types = [0, 1, 2, 3, 4, 5]
    multiplexing_modes = list(range(12))
    parallel_values = [1, 2, 3]

# Configurations de base possibles pour 128×64
base_configs = [
    {
        "name": "128×64 direct (rows=64, cols=128)",
        "rows": 64,
        "cols": 128,
    },
    {
        "name": "128×64 comme 32 rows (rows=32, cols=128)",
        "rows": 32,
        "cols": 128,
    },
    {
        "name": "128×64 comme 16 rows (rows=16, cols=128)",
        "rows": 16,
        "cols": 128,
    },
]

panel_types = [None, "FM6126A"]

input("\nAppuyez sur ENTRÉE pour commencer...\n")

test_count = 0
found = False

for panel_type in panel_types:
    if found:
        break

    for base_config in base_configs:
        if found:
            break

        for parallel in parallel_values:
            if found:
                break

            for row_addr in row_address_types:
                if found:
                    break

                for multiplex in multiplexing_modes:
                    test_count += 1

                    config_name = f"panel={panel_type or 'None'} | rows={base_config['rows']} | parallel={parallel} | row_addr={row_addr} | mux={multiplex}"

                    print(f"\n{'='*80}")
                    print(f"TEST {test_count} : {config_name}")
                    print(f"{'='*80}")

                    try:
                        options = RGBMatrixOptions()
                        options.rows = base_config['rows']
                        options.cols = base_config['cols']
                        options.chain_length = 1
                        options.parallel = parallel
                        options.hardware_mapping = 'regular'
                        options.row_address_type = row_addr
                        options.multiplexing = multiplex
                        options.gpio_slowdown = 1
                        options.brightness = 80
                        options.disable_hardware_pulsing = False

                        # Panel type si spécifié
                        if panel_type:
                            options.panel_type = panel_type

                        print(f"\nParamètres:")
                        print(f"  panel_type = {panel_type or 'None'}")
                        print(f"  rows = {options.rows}")
                        print(f"  cols = {options.cols}")
                        print(f"  parallel = {options.parallel}")
                        print(f"  row_address_type = {row_addr}")
                        print(f"  multiplexing = {multiplex}")

                        matrix = RGBMatrix(options=options)
                        width = matrix.width
                        height = matrix.height

                        print(f"\n✓ Matrice créée : {width}×{height}")

                        # Test simple et rapide
                        print("\nTest visuel (3 secondes)...")
                        print("  Vous devriez voir TOUT l'écran en blanc")

                        # Remplir tout en blanc
                        for y in range(min(64, height)):
                            for x in range(min(128, width)):
                                matrix.SetPixel(x, y, 255, 255, 255)

                        time.sleep(3)

                        # Bordure rouge
                        matrix.Clear()
                        print("  Bordure rouge (2 secondes)...")

                        # Lignes haut et bas
                        for x in range(min(128, width)):
                            matrix.SetPixel(x, 0, 255, 0, 0)
                            if height > 1:
                                matrix.SetPixel(x, min(63, height - 1), 255, 0, 0)

                        # Lignes gauche et droite
                        for y in range(min(64, height)):
                            matrix.SetPixel(0, y, 255, 0, 0)
                            if width > 1:
                                matrix.SetPixel(min(127, width - 1), y, 255, 0, 0)

                        time.sleep(2)

                        matrix.Clear()

                        print("\n" + "="*80)
                        print("VÉRIFIEZ :")
                        print("  1. TOUT l'écran (128×64) était-il rempli en blanc ?")
                        print("  2. La bordure rouge faisait-elle le tour COMPLET ?")
                        print("  3. Pas juste 16 lignes du bas ?")
                        print("="*80)

                        response = input("\nTOUT était parfait (tout l'écran allumé) ? (o/N) : ")

                        if response.lower() == 'o':
                            print("\n" + "="*80)
                            print("🎉🎉🎉 CONFIGURATION TROUVÉE ! 🎉🎉🎉")
                            print("="*80)
                            print(f"\n✓ Configuration pour votre panneau :\n")
                            print("options = RGBMatrixOptions()")
                            if panel_type:
                                print(f"options.panel_type = '{panel_type}'  # ← IMPORTANT !")
                            print(f"options.rows = {options.rows}")
                            print(f"options.cols = {options.cols}")
                            print(f"options.chain_length = 1")
                            print(f"options.parallel = {options.parallel}")
                            print(f"options.row_address_type = {row_addr}  # ← CRUCIAL !")
                            print(f"options.multiplexing = {multiplex}")
                            print(f"options.hardware_mapping = 'regular'")
                            print(f"options.gpio_slowdown = 1")
                            print(f"options.brightness = 80")
                            print("\n" + "="*80)

                            # Sauvegarder
                            with open('CONFIGURATION_FINALE_128x64.txt', 'w') as f:
                                f.write("# Configuration FINALE pour panneau 128×64 unique\n\n")
                                f.write("options = RGBMatrixOptions()\n")
                                if panel_type:
                                    f.write(f"options.panel_type = '{panel_type}'\n")
                                f.write(f"options.rows = {options.rows}\n")
                                f.write(f"options.cols = {options.cols}\n")
                                f.write(f"options.chain_length = 1\n")
                                f.write(f"options.parallel = {options.parallel}\n")
                                f.write(f"options.row_address_type = {row_addr}\n")
                                f.write(f"options.multiplexing = {multiplex}\n")
                                f.write(f"options.hardware_mapping = 'regular'\n")
                                f.write(f"options.gpio_slowdown = 1\n")
                                f.write(f"options.brightness = 80\n")

                            print("✓ Configuration sauvegardée dans CONFIGURATION_FINALE_128x64.txt")
                            found = True
                            break

                    except Exception as e:
                        print(f"\n✗ Erreur : {e}")

                    if not found and test_count < 1000:
                        input("\nAppuyez sur ENTRÉE pour le test suivant (ou Ctrl+C pour arrêter)...")

if not found:
    print("\n" + "="*80)
    print("AUCUNE CONFIGURATION PARFAITE TROUVÉE")
    print("="*80)
    print("\nSi vous avez vu une configuration qui donnait un meilleur résultat")
    print("(même pas parfait), notez les paramètres.")
    print("")
    print("Possibilités :")
    print("  1. Votre panneau nécessite un HAT avec level shifter")
    print("  2. Le câblage n'est pas encore 100% correct")
    print("  3. Un paramètre spécial est nécessaire")
    print("="*80)
