#!/usr/bin/env python3
"""
Affichage de texte pour panneau P3 128×64-32S
À AJUSTER avec les paramètres trouvés par test_p3_128x64.py
"""

import sys
import time
import os
import argparse

# Configuration des chemins
script_dir = os.path.dirname(os.path.abspath(__file__))
rgb_matrix_path = os.path.join(script_dir, 'rpi-rgb-led-matrix', 'bindings', 'python')
sys.path.insert(0, rgb_matrix_path)

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
except ImportError as e:
    print("ERREUR: Module rgbmatrix non trouvé")
    print(f"Détail: {e}")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Affiche du texte sur l\'écran LED 128×64')
    parser.add_argument('text', nargs='?', default='MODULEAIR', help='Texte à afficher')
    parser.add_argument('--color', default='255,255,255', help='Couleur RGB (ex: 255,0,0)')
    parser.add_argument('--duration', type=int, default=10, help='Durée (secondes)')
    parser.add_argument('--scroll', action='store_true', help='Texte défilant')
    parser.add_argument('--brightness', type=int, default=60, help='Luminosité (0-100)')

    args = parser.parse_args()

    # Parse couleur
    try:
        r, g, b = map(int, args.color.split(','))
    except:
        print("Erreur: Format couleur invalide. Utilisez R,G,B (ex: 255,0,0)")
        sys.exit(1)

    # ========================================================================
    # CONFIGURATION À AJUSTER SELON LE RÉSULTAT DE test_p3_128x64.py
    # ========================================================================
    # Configuration la plus probable pour P3 128×64-32S:
    options = RGBMatrixOptions()
    options.rows = 32              # ← AJUSTER si nécessaire
    options.cols = 64              # ← AJUSTER si nécessaire
    options.chain_length = 2       # ← AJUSTER si nécessaire
    options.parallel = 1           # ← AJUSTER si nécessaire
    options.multiplexing = 0       # ← AJUSTER si nécessaire
    options.row_address_type = 0   # ← AJUSTER si nécessaire
    options.hardware_mapping = 'regular'  # ← AJUSTER si nécessaire
    options.brightness = args.brightness
    options.disable_hardware_pulsing = False
    # ========================================================================

    print(f"Initialisation de la matrice {options.cols * options.chain_length}×{options.rows * options.parallel}...")

    try:
        matrix = RGBMatrix(options=options)
        print(f"✓ Matrice créée: {matrix.width}×{matrix.height}")
    except Exception as e:
        print(f"✗ Erreur: {e}")
        sys.exit(1)

    offscreen_canvas = matrix.CreateFrameCanvas()

    # Charge une police
    font = graphics.Font()
    font_path = os.path.join(script_dir, "rpi-rgb-led-matrix/fonts/7x13.bdf")

    if not os.path.exists(font_path):
        print(f"⚠ Police {font_path} non trouvée")
        print("Essai avec une autre police...")
        font_path = os.path.join(script_dir, "rpi-rgb-led-matrix/fonts/6x10.bdf")

    font.LoadFont(font_path)
    color = graphics.Color(r, g, b)

    if args.scroll:
        # Texte défilant
        print(f"Affichage de '{args.text}' (défilant)...")
        pos = matrix.width

        try:
            while True:
                offscreen_canvas.Clear()
                length = graphics.DrawText(offscreen_canvas, font, pos, matrix.height // 2 + 4, color, args.text)
                pos -= 1
                if pos + length < 0:
                    pos = matrix.width

                time.sleep(0.05)
                offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        except KeyboardInterrupt:
            pass
    else:
        # Texte statique centré
        print(f"Affichage de '{args.text}' ({args.duration}s)...")
        offscreen_canvas.Clear()

        # Calcul pour centrer le texte
        text_length = len(args.text) * 7  # Approximation
        x_pos = max(2, (matrix.width - text_length) // 2)
        y_pos = matrix.height // 2 + 4

        graphics.DrawText(offscreen_canvas, font, x_pos, y_pos, color, args.text)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        time.sleep(args.duration)

    matrix.Clear()
    print("✓ Terminé")

if __name__ == "__main__":
    main()
