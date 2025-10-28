#!/usr/bin/env python3
"""
Affichage de texte SIMPLE sans Pillow
Utilise directement la méthode DrawText de rgbmatrix
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
    parser = argparse.ArgumentParser(description='Affiche du texte sur l\'écran LED')
    parser.add_argument('text', nargs='?', default='HELLO!', help='Texte à afficher')
    parser.add_argument('--color', default='255,255,255', help='Couleur RGB (ex: 255,0,0)')
    parser.add_argument('--duration', type=int, default=10, help='Durée (secondes)')
    parser.add_argument('--scroll', action='store_true', help='Texte défilant')
    parser.add_argument('--brightness', type=int, default=70, help='Luminosité (0-100)')

    args = parser.parse_args()

    # Parse couleur
    try:
        r, g, b = map(int, args.color.split(','))
    except:
        print("Erreur: Format couleur invalide. Utilisez R,G,B (ex: 255,0,0)")
        sys.exit(1)

    # Configuration matrice
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.row_address_type = 0
    options.hardware_mapping = 'regular'
    options.brightness = args.brightness

    matrix = RGBMatrix(options=options)
    offscreen_canvas = matrix.CreateFrameCanvas()

    # Charge une police
    font = graphics.Font()
    font.LoadFont(os.path.join(script_dir, "rpi-rgb-led-matrix/fonts/7x13.bdf"))

    color = graphics.Color(r, g, b)

    if args.scroll:
        # Texte défilant
        print(f"Affichage de '{args.text}' (défilant)...")
        pos = matrix.width

        try:
            while True:
                offscreen_canvas.Clear()
                length = graphics.DrawText(offscreen_canvas, font, pos, 32, color, args.text)
                pos -= 1
                if pos + length < 0:
                    pos = matrix.width

                time.sleep(0.05)
                offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        except KeyboardInterrupt:
            pass
    else:
        # Texte statique
        print(f"Affichage de '{args.text}' ({args.duration}s)...")
        offscreen_canvas.Clear()
        graphics.DrawText(offscreen_canvas, font, 2, 32, color, args.text)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        time.sleep(args.duration)

    matrix.Clear()
    print("✓ Terminé")

if __name__ == "__main__":
    main()
