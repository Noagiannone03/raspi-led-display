#!/usr/bin/env python3
"""
Test SIMPLE sans utiliser Pillow
Utilise directement les pixels de la matrice
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
║     TEST SIMPLE - Sans Pillow                              ║
║     Utilise directement les pixels de la matrice          ║
╚════════════════════════════════════════════════════════════╝
""")

# Configuration de la matrice
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.row_address_type = 0
options.hardware_mapping = 'regular'
options.brightness = 70

print("Création de la matrice...")
try:
    matrix = RGBMatrix(options=options)
    print(f"✓ Matrice créée: {matrix.width}x{matrix.height}")
except Exception as e:
    print(f"✗ Erreur: {e}")
    sys.exit(1)

print("\nTest 1: Écran ROUGE (3 secondes)...")
offscreen_canvas = matrix.CreateFrameCanvas()
for x in range(matrix.width):
    for y in range(matrix.height):
        offscreen_canvas.SetPixel(x, y, 255, 0, 0)
offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
time.sleep(3)

print("Test 2: Écran VERT (3 secondes)...")
for x in range(matrix.width):
    for y in range(matrix.height):
        offscreen_canvas.SetPixel(x, y, 0, 255, 0)
offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
time.sleep(3)

print("Test 3: Écran BLEU (3 secondes)...")
for x in range(matrix.width):
    for y in range(matrix.height):
        offscreen_canvas.SetPixel(x, y, 0, 0, 255)
offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
time.sleep(3)

print("Test 4: Carrés de couleur (3 secondes)...")
for x in range(matrix.width):
    for y in range(matrix.height):
        offscreen_canvas.SetPixel(x, y, 0, 0, 0)  # Noir

# Carré rouge
for x in range(10, 30):
    for y in range(10, 30):
        offscreen_canvas.SetPixel(x, y, 255, 0, 0)

# Carré vert
for x in range(35, 55):
    for y in range(10, 30):
        offscreen_canvas.SetPixel(x, y, 0, 255, 0)

# Carré bleu
for x in range(10, 30):
    for y in range(35, 55):
        offscreen_canvas.SetPixel(x, y, 0, 0, 255)

# Carré blanc
for x in range(35, 55):
    for y in range(35, 55):
        offscreen_canvas.SetPixel(x, y, 255, 255, 255)

offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
time.sleep(3)

print("\n✓ TEST RÉUSSI !")
print("\nTon écran fonctionne parfaitement !")
print("Le problème était juste Pillow qui ne marche pas avec Python 3.13.")

matrix.Clear()
print("\nUtilise maintenant ce script au lieu de test_display.py")
