#!/usr/bin/env python3
"""
Test spécifique pour panneau DV08-210519 128x64-32S V1.0

IMPORTANT : Ce panneau nécessite une alimentation 5V 10A minimum !
Si tu n'as que 0.3A, ça ne marchera JAMAIS correctement.
"""

from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time
import sys

def test_configuration(config_name, options_dict):
    """Teste une configuration spécifique"""
    print(f"\n{'='*60}")
    print(f"TEST : {config_name}")
    print(f"{'='*60}")

    try:
        # Créer les options
        options = RGBMatrixOptions()

        # Appliquer la configuration
        for key, value in options_dict.items():
            setattr(options, key, value)

        # Afficher la config
        print(f"Configuration testée :")
        for key, value in options_dict.items():
            print(f"  {key}: {value}")

        # Créer la matrice
        print("\nInitialisation de la matrice...")
        matrix = RGBMatrix(options=options)
        canvas = matrix.CreateFrameCanvas()

        print("✓ Matrice initialisée avec succès !")

        # Test 1 : Remplir en rouge (faible luminosité pour économiser l'alimentation)
        print("\nTest 1/4 : Rouge complet...")
        canvas.Fill(50, 0, 0)  # Rouge faible (50 au lieu de 255)
        matrix.SwapOnVSync(canvas)
        time.sleep(2)

        # Test 2 : Vert
        print("Test 2/4 : Vert complet...")
        canvas.Fill(0, 50, 0)
        matrix.SwapOnVSync(canvas)
        time.sleep(2)

        # Test 3 : Bleu
        print("Test 3/4 : Bleu complet...")
        canvas.Fill(0, 0, 50)
        matrix.SwapOnVSync(canvas)
        time.sleep(2)

        # Test 4 : Dégradé horizontal
        print("Test 4/4 : Dégradé horizontal...")
        canvas.Clear()
        for x in range(128):
            color_val = int((x / 128.0) * 50)
            for y in range(64):
                canvas.SetPixel(x, y, color_val, color_val, color_val)
        matrix.SwapOnVSync(canvas)
        time.sleep(3)

        # Effacer
        canvas.Clear()
        matrix.SwapOnVSync(canvas)

        print(f"\n✓✓✓ CONFIGURATION RÉUSSIE : {config_name} ✓✓✓")
        print(f"Cette configuration fonctionne correctement !")

        return True

    except Exception as e:
        print(f"\n✗ Erreur avec cette configuration : {str(e)}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  Test pour panneau DV08-210519 128x64-32S V1.0             ║
╚══════════════════════════════════════════════════════════════╝

⚠️  IMPORTANT : Ton alimentation actuelle (0.3A) est INSUFFISANTE

    Ce panneau nécessite minimum 5V 10A (50W)

    Avec 0.3A, le test peut :
    - Ne rien afficher
    - Afficher des lignes bizarres
    - Afficher partiellement
    - Faire redémarrer le Raspberry Pi

    Tu DOIS changer l'alimentation pour avoir un résultat correct.

Appuie sur ENTER pour continuer quand même (ou Ctrl+C pour annuler)...
""")

    try:
        input()
    except KeyboardInterrupt:
        print("\nTest annulé.")
        return

    # Configurations à tester spécifiquement pour le DV08-210519 128x64-32S
    configurations = [
        {
            "name": "Config 1 : Standard 128x64 avec scan 1/32",
            "options": {
                "rows": 32,
                "cols": 64,
                "chain_length": 2,
                "parallel": 1,
                "hardware_mapping": "regular",
                "multiplexing": 0,
                "pwm_bits": 11,
                "brightness": 30,  # Faible pour économiser l'alim
                "pwm_lsb_nanoseconds": 130,
                "led_rgb_sequence": "RGB",
                "row_address_type": 0,
                "gpio_slowdown": 4,
            }
        },
        {
            "name": "Config 2 : Avec multiplexing type 1",
            "options": {
                "rows": 32,
                "cols": 64,
                "chain_length": 2,
                "parallel": 1,
                "hardware_mapping": "regular",
                "multiplexing": 1,  # Différent !
                "pwm_bits": 11,
                "brightness": 30,
                "pwm_lsb_nanoseconds": 130,
                "led_rgb_sequence": "RGB",
                "row_address_type": 0,
                "gpio_slowdown": 4,
            }
        },
        {
            "name": "Config 3 : Mode stripe",
            "options": {
                "rows": 32,
                "cols": 64,
                "chain_length": 2,
                "parallel": 1,
                "hardware_mapping": "regular",
                "multiplexing": 4,  # Stripe mode
                "pwm_bits": 11,
                "brightness": 30,
                "pwm_lsb_nanoseconds": 130,
                "led_rgb_sequence": "RGB",
                "row_address_type": 0,
                "gpio_slowdown": 4,
            }
        },
        {
            "name": "Config 4 : Panel unique 128x64 (pas de chain)",
            "options": {
                "rows": 64,
                "cols": 128,
                "chain_length": 1,
                "parallel": 1,
                "hardware_mapping": "regular",
                "multiplexing": 0,
                "pwm_bits": 11,
                "brightness": 30,
                "pwm_lsb_nanoseconds": 130,
                "led_rgb_sequence": "RGB",
                "row_address_type": 0,
                "gpio_slowdown": 4,
            }
        },
        {
            "name": "Config 5 : Avec FM6126A panel type",
            "options": {
                "rows": 32,
                "cols": 64,
                "chain_length": 2,
                "parallel": 1,
                "hardware_mapping": "regular",
                "multiplexing": 0,
                "pwm_bits": 11,
                "brightness": 30,
                "pwm_lsb_nanoseconds": 130,
                "led_rgb_sequence": "RGB",
                "row_address_type": 0,
                "gpio_slowdown": 4,
                "panel_type": "FM6126A",  # Important pour certains panneaux
            }
        },
        {
            "name": "Config 6 : Hardware mapping Adafruit",
            "options": {
                "rows": 32,
                "cols": 64,
                "chain_length": 2,
                "parallel": 1,
                "hardware_mapping": "adafruit-hat",  # Parfois marche même sans HAT
                "multiplexing": 0,
                "pwm_bits": 11,
                "brightness": 30,
                "pwm_lsb_nanoseconds": 130,
                "led_rgb_sequence": "RGB",
                "row_address_type": 0,
                "gpio_slowdown": 2,  # Différent pour Adafruit
            }
        }
    ]

    successful_configs = []

    for i, config in enumerate(configurations, 1):
        print(f"\n\nTest {i}/{len(configurations)}")

        if test_configuration(config["name"], config["options"]):
            successful_configs.append(config["name"])

        time.sleep(2)  # Pause entre les tests

    # Résumé
    print("\n\n" + "="*60)
    print("RÉSUMÉ DES TESTS")
    print("="*60)

    if successful_configs:
        print(f"\n✓ {len(successful_configs)} configuration(s) réussie(s) :")
        for config in successful_configs:
            print(f"  • {config}")
    else:
        print("\n✗ Aucune configuration n'a fonctionné.")
        print("\nCauses possibles :")
        print("  1. Alimentation INSUFFISANTE (0.3A → besoin de 10A)")
        print("  2. Câblage incorrect")
        print("  3. Panneau défectueux")
        print("  4. Incompatibilité du chip driver")
        print("\nVérifie en priorité l'ALIMENTATION !")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrompu par l'utilisateur.")
        sys.exit(0)
