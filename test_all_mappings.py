#!/usr/bin/env python3
"""
Test TOUS les mappings hardware possibles pour trouver celui qui fonctionne
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
║     TEST DE TOUS LES MAPPINGS HARDWARE                    ║
║                                                            ║
║  Ce script va tester tous les mappings GPIO possibles     ║
║  pour trouver celui qui correspond à votre câblage        ║
╚════════════════════════════════════════════════════════════╝
""")

# Tous les mappings hardware possibles
mappings = [
    "regular",
    "adafruit-hat",
    "adafruit-hat-pwm",
    "regular-pi1",
    "classic",
    "classic-pi1"
]

# Configurations à tester pour panneau 128×64
configurations = [
    {
        "name": "128×64 - 2 panneaux 64×32 en chaîne",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 0
    },
    {
        "name": "128×64 - 2 panneaux 64×32 en chaîne (multiplexing=1)",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
        "multiplexing": 1,
        "row_addr": 0
    },
    {
        "name": "128×64 - Un seul panneau 128×32",
        "rows": 32,
        "cols": 128,
        "chain": 1,
        "parallel": 1,
        "multiplexing": 0,
        "row_addr": 0
    }
]

def test_mapping(hw_map, config):
    """Teste un mapping hardware avec une configuration"""
    print(f"\n{'='*70}")
    print(f"TEST: {hw_map} + {config['name']}")
    print(f"{'='*70}")

    try:
        # Configuration
        options = RGBMatrixOptions()
        options.rows = config['rows']
        options.cols = config['cols']
        options.chain_length = config['chain']
        options.parallel = config['parallel']
        options.multiplexing = config['multiplexing']
        options.row_address_type = config['row_addr']
        options.hardware_mapping = hw_map
        options.brightness = 70
        options.disable_hardware_pulsing = False

        print(f"\nParamètres:")
        print(f"  hardware_mapping = '{hw_map}'")
        print(f"  rows = {options.rows}")
        print(f"  cols = {options.cols}")
        print(f"  chain_length = {options.chain_length}")
        print(f"  multiplexing = {options.multiplexing}")
        print(f"  → Résolution: {options.cols * options.chain_length}×{options.rows}")

        matrix = RGBMatrix(options=options)

        width = matrix.width
        height = matrix.height

        print(f"\n✓ Matrice créée: {width}×{height}")
        print("\nAffichage d'un test visuel (4 secondes)...")
        print("  - Quart gauche: ROUGE")
        print("  - Centre-gauche: VERT")
        print("  - Centre-droite: BLEU")
        print("  - Quart droit: BLANC")

        # Quart gauche rouge
        for y in range(height):
            for x in range(0, width // 4):
                matrix.SetPixel(x, y, 255, 0, 0)

        # Centre-gauche vert
        for y in range(height):
            for x in range(width // 4, width // 2):
                matrix.SetPixel(x, y, 0, 255, 0)

        # Centre-droite bleu
        for y in range(height):
            for x in range(width // 2, 3 * width // 4):
                matrix.SetPixel(x, y, 0, 0, 255)

        # Quart droit blanc
        for y in range(height):
            for x in range(3 * width // 4, width):
                matrix.SetPixel(x, y, 255, 255, 255)

        time.sleep(4)

        # Test damier
        print("\nAffichage d'un damier (2 secondes)...")
        matrix.Clear()
        for y in range(height):
            for x in range(width):
                if (x // 8 + y // 8) % 2 == 0:
                    matrix.SetPixel(x, y, 255, 255, 0)
                else:
                    matrix.SetPixel(x, y, 0, 0, 0)

        time.sleep(2)

        matrix.Clear()

        print("\n✓ Test terminé !")
        print("\n" + "="*70)
        print("Est-ce que l'affichage était correct ?")
        print("  - Les 4 bandes de couleur étaient bien séparées ?")
        print("  - L'affichage couvrait TOUT l'écran (128 pixels) ?")
        print("  - Le damier était régulier (pas de lignes bizarres) ?")
        print("="*70)

        response = input("\nEst-ce que tout était PARFAIT ? (o/N) : ")

        if response.lower() == 'o':
            print("\n" + "="*70)
            print("🎉 CONFIGURATION TROUVÉE ! 🎉")
            print("="*70)
            print(f"\n👉 Utilisez ces paramètres dans vos scripts :\n")
            print("options = RGBMatrixOptions()")
            print(f"options.hardware_mapping = '{hw_map}'  # ← IMPORTANT !")
            print(f"options.rows = {options.rows}")
            print(f"options.cols = {options.cols}")
            print(f"options.chain_length = {options.chain_length}")
            print(f"options.parallel = {options.parallel}")
            print(f"options.multiplexing = {options.multiplexing}")
            print(f"options.row_address_type = {options.row_address_type}")
            print(f"options.brightness = 70")
            print(f"options.disable_hardware_pulsing = False")
            print("\n" + "="*70)
            return True

    except Exception as e:
        print(f"\n✗ Erreur avec ce mapping: {e}")
        return False

    return False

# Programme principal
print("Ce script va tester TOUS les mappings hardware possibles.")
print("Pour chaque test, vous verrez 4 bandes de couleur puis un damier.")
print("\nSi l'affichage est parfait, tapez 'o' et ENTRÉE.")
print("Sinon, appuyez juste sur ENTRÉE pour passer au suivant.")
print("")
input("Appuyez sur ENTRÉE pour commencer...\n")

found = False
test_count = 0

for hw_map in mappings:
    if found:
        break

    for config in configurations:
        test_count += 1
        print(f"\n[Test {test_count}/{len(mappings) * len(configurations)}]")

        found = test_mapping(hw_map, config)

        if found:
            print("\n✓ Configuration trouvée ! Vous pouvez maintenant l'utiliser.")
            sys.exit(0)

        if test_count < len(mappings) * len(configurations):
            input("\nAppuyez sur ENTRÉE pour le test suivant...")

print("\n" + "="*70)
print("Aucune configuration n'a parfaitement fonctionné.")
print("")
print("Si vous avez vu QUELQUE CHOSE s'afficher (même partiellement),")
print("re-lancez ce script et notez quel mapping donnait le meilleur résultat.")
print("")
print("Ensuite, on pourra ajuster les autres paramètres (multiplexing, etc.)")
print("="*70)
