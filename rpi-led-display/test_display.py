#!/usr/bin/env python3
"""
Script de test pour écran LED 64x64
Ce script teste différentes configurations pour trouver celle qui fonctionne
"""

import sys
import time

# Configuration des chemins
sys.path.append('rpi-rgb-led-matrix/bindings/python')

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print("ERREUR: Impossible d'importer les modules nécessaires")
    print(f"Détail: {e}")
    print("\nVeuillez d'abord exécuter: sudo bash install.sh")
    sys.exit(1)

# Configurations à tester
CONFIGURATIONS = [
    {
        "name": "Config 1: Standard 64x64",
        "rows": 64,
        "cols": 64,
        "chain_length": 1,
        "parallel": 1,
        "row_addr_type": 0,
        "multiplexing": 0,
    },
    {
        "name": "Config 2: 64x64 avec row_addr_type=1",
        "rows": 64,
        "cols": 64,
        "chain_length": 1,
        "parallel": 1,
        "row_addr_type": 1,
        "multiplexing": 0,
    },
    {
        "name": "Config 3: 64x64 avec row_addr_type=2",
        "rows": 64,
        "cols": 64,
        "chain_length": 1,
        "parallel": 1,
        "row_addr_type": 2,
        "multiplexing": 0,
    },
    {
        "name": "Config 4: 32x64 chainé (2 panneaux)",
        "rows": 32,
        "cols": 64,
        "chain_length": 2,
        "parallel": 1,
        "row_addr_type": 0,
        "multiplexing": 0,
    },
]

def test_configuration(config):
    """Teste une configuration spécifique"""
    print(f"\n{'='*60}")
    print(f"Test: {config['name']}")
    print(f"{'='*60}")

    try:
        # Configuration de la matrice
        options = RGBMatrixOptions()
        options.rows = config['rows']
        options.cols = config['cols']
        options.chain_length = config['chain_length']
        options.parallel = config['parallel']
        options.row_address_type = config['row_addr_type']
        options.multiplexing = config['multiplexing']
        options.hardware_mapping = 'regular'
        options.brightness = 50
        options.pwm_lsb_nanoseconds = 130
        options.disable_hardware_pulsing = False

        print(f"Paramètres:")
        print(f"  - Rows: {options.rows}")
        print(f"  - Cols: {options.cols}")
        print(f"  - Chain: {options.chain_length}")
        print(f"  - Row addr type: {options.row_address_type}")
        print(f"  - Multiplexing: {options.multiplexing}")

        # Création de la matrice
        matrix = RGBMatrix(options=options)

        # Test 1: Rectangle rouge
        print("\nTest 1: Rectangle rouge (3 secondes)...")
        image = Image.new('RGB', (matrix.width, matrix.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, matrix.width, matrix.height), fill=(255, 0, 0))
        matrix.SetImage(image)
        time.sleep(3)

        # Test 2: Rectangle vert
        print("Test 2: Rectangle vert (3 secondes)...")
        draw.rectangle((0, 0, matrix.width, matrix.height), fill=(0, 255, 0))
        matrix.SetImage(image)
        time.sleep(3)

        # Test 3: Rectangle bleu
        print("Test 3: Rectangle bleu (3 secondes)...")
        draw.rectangle((0, 0, matrix.width, matrix.height), fill=(0, 0, 255))
        matrix.SetImage(image)
        time.sleep(3)

        # Test 4: Texte
        print("Test 4: Affichage de texte (3 secondes)...")
        draw.rectangle((0, 0, matrix.width, matrix.height), fill=(0, 0, 0))
        draw.text((5, 5), "HELLO", fill=(255, 255, 255))
        draw.text((5, 25), "MATRIX", fill=(0, 255, 255))
        draw.text((5, 45), "64x64", fill=(255, 255, 0))
        matrix.SetImage(image)
        time.sleep(3)

        # Clear
        matrix.Clear()

        print(f"\n✓ Configuration testée avec succès!")
        print(f"Si l'affichage était correct, utilisez cette configuration.")

        return True

    except Exception as e:
        print(f"\n✗ Erreur avec cette configuration:")
        print(f"  {str(e)}")
        return False

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║     TEST DE CONFIGURATION LED MATRIX 64x64                 ║
║                                                            ║
║  Ce script va tester différentes configurations pour      ║
║  trouver celle qui fonctionne avec votre écran.           ║
║                                                            ║
║  IMPORTANT: Ce script doit être exécuté en root:          ║
║  sudo python3 test_display.py                             ║
╚════════════════════════════════════════════════════════════╝
    """)

    input("Appuyez sur ENTRÉE pour commencer les tests...")

    successful_configs = []

    for i, config in enumerate(CONFIGURATIONS, 1):
        print(f"\n\n[Test {i}/{len(CONFIGURATIONS)}]")

        try:
            success = test_configuration(config)
            if success:
                successful_configs.append(config)
        except KeyboardInterrupt:
            print("\n\nInterruption par l'utilisateur.")
            break
        except Exception as e:
            print(f"\nErreur inattendue: {e}")

        if i < len(CONFIGURATIONS):
            print("\n" + "-"*60)
            input("Appuyez sur ENTRÉE pour tester la configuration suivante...")

    # Résumé
    print("\n\n" + "="*60)
    print("RÉSUMÉ DES TESTS")
    print("="*60)

    if successful_configs:
        print(f"\n✓ {len(successful_configs)} configuration(s) ont fonctionné:\n")
        for config in successful_configs:
            print(f"  - {config['name']}")
            print(f"    Paramètres: rows={config['rows']}, cols={config['cols']}, "
                  f"row_addr_type={config['row_addr_type']}")
    else:
        print("\n✗ Aucune configuration n'a fonctionné.")
        print("\nProblèmes possibles:")
        print("  1. Câblage incorrect - vérifiez les connexions GPIO")
        print("  2. Alimentation insuffisante - utilisez une alim 5V/4A minimum")
        print("  3. Type de panneau spécial - essayez avec --led-panel-type")
        print("  4. Le module n'est pas installé correctement")

if __name__ == "__main__":
    main()
