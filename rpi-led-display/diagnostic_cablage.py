#!/usr/bin/env python3
"""
Diagnostic détaillé du câblage pour identifier les problèmes
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
║            DIAGNOSTIC DÉTAILLÉ DU CÂBLAGE                  ║
║                                                            ║
║  Ce script va tester chaque signal individuellement       ║
║  pour identifier exactement quel câble pose problème      ║
╚════════════════════════════════════════════════════════════╝
""")

def create_matrix():
    """Crée une matrice avec configuration de base"""
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 2
    options.parallel = 1
    options.hardware_mapping = 'regular'
    options.row_address_type = 0
    options.multiplexing = 0
    options.brightness = 80
    options.disable_hardware_pulsing = False

    return RGBMatrix(options=options)

print("\n1️⃣  TEST DES SIGNAUX RGB")
print("="*70)

matrix = create_matrix()
width = matrix.width
height = matrix.height

print(f"Matrice initialisée: {width}×{height}")

# Test R1 (première moitié en rouge)
print("\n🔴 Test R1 (haut en rouge)...")
matrix.Clear()
for y in range(0, height // 2):
    for x in range(width):
        matrix.SetPixel(x, y, 255, 0, 0)
time.sleep(2)

input("\n❓ Voyez-vous la MOITIÉ SUPÉRIEURE en rouge ? (appuyez sur ENTRÉE)")

# Test G1 (première moitié en vert)
print("\n🟢 Test G1 (haut en vert)...")
matrix.Clear()
for y in range(0, height // 2):
    for x in range(width):
        matrix.SetPixel(x, y, 0, 255, 0)
time.sleep(2)

input("\n❓ Voyez-vous la MOITIÉ SUPÉRIEURE en vert ? (appuyez sur ENTRÉE)")

# Test B1 (première moitié en bleu)
print("\n🔵 Test B1 (haut en bleu)...")
matrix.Clear()
for y in range(0, height // 2):
    for x in range(width):
        matrix.SetPixel(x, y, 0, 0, 255)
time.sleep(2)

input("\n❓ Voyez-vous la MOITIÉ SUPÉRIEURE en bleu ? (appuyez sur ENTRÉE)")

# Test R2 (deuxième moitié en rouge)
print("\n🔴 Test R2 (bas en rouge)...")
matrix.Clear()
for y in range(height // 2, height):
    for x in range(width):
        matrix.SetPixel(x, y, 255, 0, 0)
time.sleep(2)

input("\n❓ Voyez-vous la MOITIÉ INFÉRIEURE en rouge ? (appuyez sur ENTRÉE)")

# Test G2 (deuxième moitié en vert)
print("\n🟢 Test G2 (bas en vert)...")
matrix.Clear()
for y in range(height // 2, height):
    for x in range(width):
        matrix.SetPixel(x, y, 0, 255, 0)
time.sleep(2)

input("\n❓ Voyez-vous la MOITIÉ INFÉRIEURE en vert ? (appuyez sur ENTRÉE)")

# Test B2 (deuxième moitié en bleu)
print("\n🔵 Test B2 (bas en bleu)...")
matrix.Clear()
for y in range(height // 2, height):
    for x in range(width):
        matrix.SetPixel(x, y, 0, 0, 255)
time.sleep(2)

input("\n❓ Voyez-vous la MOITIÉ INFÉRIEURE en bleu ? (appuyez sur ENTRÉE)")

print("\n" + "="*70)
print("2️⃣  TEST D'ADRESSAGE (A, B, C)")
print("="*70)
print("\nCe test va allumer des LIGNES INDIVIDUELLES.")
print("Si vous voyez plusieurs lignes en même temps,")
print("c'est que A, B, ou C ne sont pas bien branchés.\n")

# Test ligne par ligne
print("🎯 Allumage ligne par ligne...")
matrix.Clear()

for line in range(min(8, height)):  # Teste les 8 premières lignes
    matrix.Clear()
    print(f"\n  → Allumage LIGNE {line} uniquement (blanche)...")

    for x in range(width):
        matrix.SetPixel(x, line, 255, 255, 255)

    time.sleep(1.5)

    response = input(f"    Voyez-vous UNE SEULE ligne blanche (ligne {line}) ? (o/N) : ")
    if response.lower() != 'o':
        print(f"    ⚠️  PROBLÈME DÉTECTÉ sur ligne {line} !")
        print(f"    → Vérifiez les connexions A, B, C (GPIO 15, 16, 20)")

matrix.Clear()

print("\n" + "="*70)
print("3️⃣  TEST COMPLET DU PANNEAU")
print("="*70)

# Damier
print("\n🏁 Affichage d'un damier complet...")
matrix.Clear()
for y in range(height):
    for x in range(width):
        if (x // 4 + y // 4) % 2 == 0:
            matrix.SetPixel(x, y, 255, 255, 255)

time.sleep(3)

print("\n❓ Questions sur le damier :")
print("  1. Le damier couvre-t-il TOUT l'écran (128×64) ?")
print("  2. Les carrés sont-ils réguliers ?")
print("  3. Voyez-vous des lignes qui se répètent bizarrement ?")

input("\nAppuyez sur ENTRÉE pour continuer...")

# Test des 4 coins
print("\n📍 Test des 4 COINS de l'écran...")
matrix.Clear()

# Coin supérieur gauche (rouge)
for y in range(8):
    for x in range(8):
        matrix.SetPixel(x, y, 255, 0, 0)

# Coin supérieur droit (vert)
for y in range(8):
    for x in range(width - 8, width):
        matrix.SetPixel(x, y, 0, 255, 0)

# Coin inférieur gauche (bleu)
for y in range(height - 8, height):
    for x in range(8):
        matrix.SetPixel(x, y, 0, 0, 255)

# Coin inférieur droit (blanc)
for y in range(height - 8, height):
    for x in range(width - 8, width):
        matrix.SetPixel(x, y, 255, 255, 255)

time.sleep(3)

print("\n❓ Voyez-vous 4 carrés de couleur dans les 4 COINS ?")
print("  Coin haut-gauche: ROUGE")
print("  Coin haut-droit: VERT")
print("  Coin bas-gauche: BLEU")
print("  Coin bas-droit: BLANC")

input("\nAppuyez sur ENTRÉE pour continuer...")

matrix.Clear()

print("\n" + "="*70)
print("📋 RÉSUMÉ DU DIAGNOSTIC")
print("="*70)
print("\nSi vous avez vu :")
print("\n✅ Les couleurs fonctionnent MAIS...")
print("❌ Plusieurs lignes s'allument en même temps")
print("❌ Seulement 3 traits horizontaux")
print("")
print("→ PROBLÈME AVEC LES SIGNAUX D'ADRESSAGE (A, B, C)")
print("")
print("VÉRIFICATIONS À FAIRE:")
print("  1. Pin A  → GPIO 15 (Pin physique 10)")
print("  2. Pin B  → GPIO 16 (Pin physique 36)")
print("  3. Pin C  → GPIO 20 (Pin physique 38)")
print("")
print("  4. Pin CLK → GPIO 11 (Pin physique 23)")
print("  5. Pin LAT → GPIO 27 (Pin physique 13)")
print("  6. Pin OE  → GPIO 4  (Pin physique 7)")
print("")
print("  7. Tous les GND bien connectés ensemble")
print("")
print("="*70)
print("\n💡 CONSEIL:")
print("Si les lignes d'adressage (A, B, C) sont bien branchées,")
print("le problème vient de la configuration logicielle.")
print("")
print("Dans ce cas, essayez de tester avec différents")
print("'hardware_mapping' dans test_exhaustive.py")
print("="*70)
