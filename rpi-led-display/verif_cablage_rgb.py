#!/usr/bin/env python3
"""
Vérification DÉTAILLÉE du câblage RGB
Pour identifier si R1, B1 sont bien branchés
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
║   VÉRIFICATION CÂBLAGE RGB - Test de CHAQUE canal        ║
╚════════════════════════════════════════════════════════════╝
""")

print("Ce test va vérifier CHAQUE canal RGB individuellement.")
print("Si un canal ne s'allume pas, on saura exactement lequel.")
print("")

try:
    options = RGBMatrixOptions()

    # Configuration de base pour 128×64-32S (on sait que ça marche partiellement)
    options.rows = 64
    options.cols = 128
    options.chain_length = 1
    options.parallel = 1
    options.row_address_type = 5
    options.multiplexing = 0
    options.gpio_slowdown = 2
    options.hardware_mapping = 'regular'
    options.brightness = 100  # Max pour voir même les signaux faibles
    options.pwm_bits = 7
    options.pwm_lsb_nanoseconds = 50

    print("Création de la matrice...")
    matrix = RGBMatrix(options=options)

    width = matrix.width
    height = matrix.height

    print(f"✓ Matrice créée : {width}×{height}")
    print("")

    # Test INDIVIDUEL de chaque canal
    tests = [
        {"name": "R1 (Rouge supérieur)", "color": (255, 0, 0), "canal": "R1", "gpio": "GPIO 17 (Pin 11)"},
        {"name": "G1 (Vert supérieur)", "color": (0, 255, 0), "canal": "G1", "gpio": "GPIO 18 (Pin 12)"},
        {"name": "B1 (Bleu supérieur)", "color": (0, 0, 255), "canal": "B1", "gpio": "GPIO 22 (Pin 15)"},
        {"name": "R2 (Rouge inférieur)", "color": (128, 0, 0), "canal": "R2", "gpio": "GPIO 23 (Pin 16)"},
        {"name": "G2 (Vert inférieur)", "color": (0, 128, 0), "canal": "G2", "gpio": "GPIO 24 (Pin 18)"},
        {"name": "B2 (Bleu inférieur)", "color": (0, 0, 128), "canal": "B2", "gpio": "GPIO 25 (Pin 22)"},
    ]

    resultats = {}

    for test in tests:
        print("="*70)
        print(f"TEST : {test['name']}")
        print(f"Canal : {test['canal']} ({test['gpio']})")
        print(f"Couleur envoyée : RGB{test['color']}")
        print("="*70)

        matrix.Clear()

        # Remplir tout l'écran avec cette couleur
        for y in range(min(64, height)):
            for x in range(min(128, width)):
                matrix.SetPixel(x, y, test['color'][0], test['color'][1], test['color'][2])

        print("")
        print(f"L'écran devrait être rempli avec : {test['name']}")
        print("")
        print("Que voyez-vous ?")
        print("  1. Rien (noir)")
        print("  2. La bonne couleur (rouge/vert/bleu)")
        print("  3. Une autre couleur")
        print("  4. Quelques LEDs seulement")
        print("")

        time.sleep(3)

        reponse = input("Choisissez (1/2/3/4) : ").strip()

        if reponse == "1":
            resultats[test['canal']] = "❌ RIEN - Canal ne fonctionne PAS"
        elif reponse == "2":
            resultats[test['canal']] = "✅ OK - Bonne couleur"
        elif reponse == "3":
            autre = input("  Quelle couleur voyez-vous ? (R/V/B) : ").upper()
            resultats[test['canal']] = f"⚠️  Mauvaise couleur (vu {autre})"
        elif reponse == "4":
            resultats[test['canal']] = "⚠️  Partiel - Quelques LEDs seulement"
        else:
            resultats[test['canal']] = "? Réponse inconnue"

        print("")

    matrix.Clear()

    # Résumé
    print("")
    print("="*70)
    print("RÉSUMÉ DES TESTS")
    print("="*70)
    print("")

    for canal, resultat in resultats.items():
        print(f"{canal:4s} : {resultat}")

    print("")
    print("="*70)
    print("ANALYSE")
    print("="*70)
    print("")

    # Analyse des résultats
    canaux_ok = [c for c, r in resultats.items() if "✅" in r]
    canaux_ko = [c for c, r in resultats.items() if "❌" in r]

    print(f"Canaux qui fonctionnent : {', '.join(canaux_ok) if canaux_ok else 'AUCUN'}")
    print(f"Canaux qui ne fonctionnent PAS : {', '.join(canaux_ko) if canaux_ko else 'AUCUN'}")
    print("")

    # Diagnostic
    if "G1" in canaux_ok and "R1" in canaux_ko and "B1" in canaux_ko:
        print("🔍 DIAGNOSTIC :")
        print("")
        print("Seulement G1 fonctionne → Vérifiez le CÂBLAGE de R1 et B1 !")
        print("")
        print("Vérifications à faire :")
        print("  1. R1 (Pin HUB75) → GPIO 17 (Pin physique 11 du RPi)")
        print("  2. B1 (Pin HUB75) → GPIO 22 (Pin physique 15 du RPi)")
        print("")
        print("Possibilités :")
        print("  - Les fils R1 et B1 ne sont PAS branchés")
        print("  - Les fils sont sur les MAUVAIS GPIO")
        print("  - Les fils sont mal insérés dans le connecteur HUB75")
        print("")

    elif all("✅" in r for r in resultats.values()):
        print("🎉 EXCELLENT ! Tous les canaux RGB fonctionnent !")
        print("")
        print("Le problème n'est donc PAS le câblage RGB.")
        print("C'est probablement la configuration (multiplexing, row_address_type, etc.)")
        print("")

    elif "G1" in canaux_ok and "G2" in canaux_ok:
        print("🔍 DIAGNOSTIC :")
        print("")
        print("Seulement les canaux VERTS fonctionnent.")
        print("")
        print("Soit :")
        print("  1. Problème de câblage : R1, R2, B1, B2 mal branchés")
        print("  2. Problème de niveau logique : Panneau ne détecte pas les 3.3V")
        print("     (mais on peut exclure ça car G1 et G2 marchent)")
        print("")
        print("→ VÉRIFIEZ LE CÂBLAGE des pins rouges et bleues !")

    else:
        print("🔍 Résultats mixtes...")
        print("")
        print("Vérifiez le câblage de tous les canaux qui ne fonctionnent pas.")

    print("")
    print("="*70)
    print("PROCHAINES ÉTAPES")
    print("="*70)
    print("")

    if canaux_ko:
        print("1. Vérifiez physiquement le câblage :")
        print("")
        print("   Connecteur HUB75 du panneau (ordre des pins) :")
        print("   R1  ──  G1")
        print("   B1  ──  GND")
        print("   R2  ──  G2")
        print("   B2  ──  GND")
        print("   ...")
        print("")
        print("   Raspberry Pi GPIO :")
        for test in tests:
            if test['canal'] in canaux_ko:
                print(f"   {test['canal']} → {test['gpio']}")
        print("")
        print("2. Une fois le câblage vérifié, relancez ce test")
        print("3. Si tous les canaux fonctionnent, le problème sera la config logicielle")
    else:
        print("Tous les canaux fonctionnent !")
        print("Le problème est dans la configuration logicielle.")
        print("")
        print("Essayez différentes configurations de multiplexing, row_address_type, etc.")

    print("")

except Exception as e:
    print(f"\n✗ Erreur : {e}")
    import traceback
    traceback.print_exc()
