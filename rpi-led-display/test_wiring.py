#!/usr/bin/env python3
"""
Test du câblage du panneau HUB75 sur Raspberry Pi
Teste chaque signal individuellement pour diagnostiquer les problèmes
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
    print("\nAssure-toi que la librairie rpi-rgb-led-matrix est installée.")
    sys.exit(1)

print("""
╔════════════════════════════════════════════════════════════╗
║     TEST DU CÂBLAGE HUB75                                  ║
║     Diagnostic des connexions Raspberry Pi → Panneau LED  ║
╚════════════════════════════════════════════════════════════╝

Ce script va tester ton câblage en affichant:
1. Chaque couleur séparément (R1, G1, B1, R2, G2, B2)
2. Des motifs pour tester l'adressage des lignes
3. Des signaux de contrôle (CLK, LAT, OE)

Si une couleur ou un motif ne s'affiche pas correctement,
cela indique quel câble est mal branché.
""")

print("Quelle est la résolution de ton panneau ?")
print("1. 64×64 (un panneau carré)")
print("2. 128×64 (panneau rectangulaire, le plus probable)")
print("3. 64×32")

choice = input("\nChoix (1/2/3) [2]: ").strip() or "2"

if choice == "1":
    rows, cols, chain = 64, 64, 1
elif choice == "3":
    rows, cols, chain = 32, 64, 1
else:  # 2 par défaut
    rows, cols, chain = 32, 64, 2

print(f"\nConfiguration: {cols * chain}×{rows} pixels")
print("\nQuel mapping hardware utilises-tu ?")
print("1. regular (câblage direct)")
print("2. adafruit-hat (si tu as un HAT Adafruit)")

hw_choice = input("\nChoix (1/2) [1]: ").strip() or "1"
hw_map = "adafruit-hat" if hw_choice == "2" else "regular"

print(f"\nUtilisation du mapping: {hw_map}")
input("\nAppuie sur ENTRÉE pour commencer les tests...")

# Configuration de la matrice
options = RGBMatrixOptions()
options.rows = rows
options.cols = cols
options.chain_length = chain
options.parallel = 1
options.multiplexing = 0
options.row_address_type = 0
options.hardware_mapping = hw_map
options.brightness = 70
options.disable_hardware_pulsing = False

print("\nInitialisation de la matrice...")
try:
    matrix = RGBMatrix(options=options)
    print(f"✓ Matrice créée: {matrix.width}×{matrix.height}")
except Exception as e:
    print(f"✗ Erreur lors de l'initialisation: {e}")
    print("\nCauses possibles:")
    print("- Tu n'as pas lancé avec 'sudo'")
    print("- Un autre processus utilise déjà les GPIO")
    print("- La librairie n'est pas correctement installée")
    sys.exit(1)

def clear_screen():
    """Efface l'écran"""
    matrix.Clear()

def wait_and_clear(seconds=2):
    """Attend et efface"""
    time.sleep(seconds)
    clear_screen()

print("\n" + "="*70)
print("TEST 1: COULEURS PRIMAIRES")
print("="*70)

# Test R1 (partie haute du panneau en rouge)
print("\nTest R1 (Rouge - partie haute)...")
print("→ Si tu vois du rouge sur la MOITIÉ HAUTE du panneau, R1 est OK")
clear_screen()
for y in range(0, matrix.height // 2):
    for x in range(matrix.width):
        matrix.SetPixel(x, y, 255, 0, 0)
input("Appuie sur ENTRÉE pour continuer...")
wait_and_clear(0.5)

# Test G1 (partie haute du panneau en vert)
print("\nTest G1 (Vert - partie haute)...")
print("→ Si tu vois du vert sur la MOITIÉ HAUTE du panneau, G1 est OK")
for y in range(0, matrix.height // 2):
    for x in range(matrix.width):
        matrix.SetPixel(x, y, 0, 255, 0)
input("Appuie sur ENTRÉE pour continuer...")
wait_and_clear(0.5)

# Test B1 (partie haute du panneau en bleu)
print("\nTest B1 (Bleu - partie haute)...")
print("→ Si tu vois du bleu sur la MOITIÉ HAUTE du panneau, B1 est OK")
for y in range(0, matrix.height // 2):
    for x in range(matrix.width):
        matrix.SetPixel(x, y, 0, 0, 255)
input("Appuie sur ENTRÉE pour continuer...")
wait_and_clear(0.5)

# Test R2 (partie basse du panneau en rouge)
print("\nTest R2 (Rouge - partie basse)...")
print("→ Si tu vois du rouge sur la MOITIÉ BASSE du panneau, R2 est OK")
for y in range(matrix.height // 2, matrix.height):
    for x in range(matrix.width):
        matrix.SetPixel(x, y, 255, 0, 0)
input("Appuie sur ENTRÉE pour continuer...")
wait_and_clear(0.5)

# Test G2 (partie basse du panneau en vert)
print("\nTest G2 (Vert - partie basse)...")
print("→ Si tu vois du vert sur la MOITIÉ BASSE du panneau, G2 est OK")
for y in range(matrix.height // 2, matrix.height):
    for x in range(matrix.width):
        matrix.SetPixel(x, y, 0, 255, 0)
input("Appuie sur ENTRÉE pour continuer...")
wait_and_clear(0.5)

# Test B2 (partie basse du panneau en bleu)
print("\nTest B2 (Bleu - partie basse)...")
print("→ Si tu vois du bleu sur la MOITIÉ BASSE du panneau, B2 est OK")
for y in range(matrix.height // 2, matrix.height):
    for x in range(matrix.width):
        matrix.SetPixel(x, y, 0, 0, 255)
input("Appuie sur ENTRÉE pour continuer...")
wait_and_clear(0.5)

print("\n" + "="*70)
print("TEST 2: MOTIF COMPLET")
print("="*70)
print("\nAffichage d'un motif avec toutes les couleurs...")
print("→ Tu devrais voir 4 bandes verticales: Rouge, Vert, Bleu, Blanc")

# Rouge à gauche
for y in range(matrix.height):
    for x in range(0, matrix.width // 4):
        matrix.SetPixel(x, y, 255, 0, 0)

# Vert
for y in range(matrix.height):
    for x in range(matrix.width // 4, matrix.width // 2):
        matrix.SetPixel(x, y, 0, 255, 0)

# Bleu
for y in range(matrix.height):
    for x in range(matrix.width // 2, 3 * matrix.width // 4):
        matrix.SetPixel(x, y, 0, 0, 255)

# Blanc à droite
for y in range(matrix.height):
    for x in range(3 * matrix.width // 4, matrix.width):
        matrix.SetPixel(x, y, 255, 255, 255)

input("\nAppuie sur ENTRÉE pour continuer...")
wait_and_clear(0.5)

print("\n" + "="*70)
print("TEST 3: ADRESSAGE DES LIGNES")
print("="*70)
print("\nTest des lignes horizontales...")
print("→ Tu devrais voir des lignes blanches horizontales qui balayent l'écran")

for y in range(matrix.height):
    clear_screen()
    # Affiche une seule ligne blanche
    for x in range(matrix.width):
        matrix.SetPixel(x, y, 255, 255, 255)
    time.sleep(0.05)

input("\nAppuie sur ENTRÉE pour continuer...")
wait_and_clear(0.5)

print("\n" + "="*70)
print("TEST 4: DAMIER")
print("="*70)
print("\nAffichage d'un damier...")
print("→ Tu devrais voir un motif en damier régulier")

for y in range(matrix.height):
    for x in range(matrix.width):
        if (x // 4 + y // 4) % 2 == 0:
            matrix.SetPixel(x, y, 255, 255, 255)
        else:
            matrix.SetPixel(x, y, 255, 0, 0)

input("\nAppuie sur ENTRÉE pour continuer...")
wait_and_clear(0.5)

print("\n" + "="*70)
print("TEST TERMINÉ")
print("="*70)

print("\n📊 DIAGNOSTIC:")
print("")
print("Si TU AS VU:")
print("✓ Toutes les couleurs (rouge, vert, bleu) sur les deux moitiés")
print("✓ Les 4 bandes verticales correctement")
print("✓ Les lignes horizontales qui balayent l'écran")
print("✓ Le damier régulier")
print("")
print("→ Ton câblage est BON ! 🎉")
print("→ Lance maintenant: sudo python3 test_p3_128x64.py")

print("\n" + "-"*70)

print("\nSi TU N'AS PAS VU certaines couleurs:")
print("")
print("❌ Pas de rouge partie haute → Vérifie R1 (GPIO 17 / Pin 11)")
print("❌ Pas de vert partie haute → Vérifie G1 (GPIO 18 / Pin 12)")
print("❌ Pas de bleu partie haute → Vérifie B1 (GPIO 22 / Pin 15)")
print("❌ Pas de rouge partie basse → Vérifie R2 (GPIO 23 / Pin 16)")
print("❌ Pas de vert partie basse → Vérifie G2 (GPIO 24 / Pin 18)")
print("❌ Pas de bleu partie basse → Vérifie B2 (GPIO 25 / Pin 22)")

print("\n" + "-"*70)

print("\nSi les MOTIFS sont bizarres:")
print("")
print("❌ Lignes décalées/bizarres → Vérifie A,B,C,D,E (adressage)")
print("   A = GPIO 15 (Pin 10)")
print("   B = GPIO 16 (Pin 36)")
print("   C = GPIO 20 (Pin 38)")
print("   D = GPIO 21 (Pin 40)")
print("   E = GPIO 26 (Pin 37) - uniquement pour scan 1/32")

print("\n" + "-"*70)

print("\nSi RIEN ne s'affiche ou que c'est très faible:")
print("")
print("❌ Vérifie CLK (Clock) → GPIO 11 (Pin 23)")
print("❌ Vérifie LAT (Latch) → GPIO 27 (Pin 13)")
print("❌ Vérifie OE (Output Enable) → GPIO 4 (Pin 7)")
print("❌ Vérifie que tous les GND sont connectés")
print("❌ Vérifie l'alimentation 5V du panneau (externe, pas le RPi!)")

print("\n" + "="*70)

matrix.Clear()
print("\n✓ Fin des tests")
