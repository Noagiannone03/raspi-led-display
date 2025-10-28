#!/usr/bin/env python3
"""
Script principal pour afficher du texte sur l'écran LED 64x64
Usage: sudo python3 display_text.py "Votre texte ici"
"""

import sys
import time
import argparse

sys.path.append('rpi-rgb-led-matrix/bindings/python')

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print("ERREUR: Modules non trouvés. Exécutez d'abord: sudo bash install.sh")
    sys.exit(1)

def create_matrix(config=None):
    """Crée et configure la matrice LED"""
    options = RGBMatrixOptions()

    # Configuration par défaut (modifiez selon les résultats de test_display.py)
    options.rows = 64
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.row_address_type = 0  # Changez selon vos tests (0, 1, ou 2)
    options.multiplexing = 0
    options.hardware_mapping = 'regular'  # ou 'adafruit-hat' si vous utilisez un HAT
    options.brightness = 70
    options.pwm_lsb_nanoseconds = 130
    options.disable_hardware_pulsing = False

    # Surcharge avec config personnalisée
    if config:
        for key, value in config.items():
            setattr(options, key, value)

    return RGBMatrix(options=options)

def display_static_text(matrix, text, color=(255, 255, 255), duration=10):
    """Affiche du texte statique"""
    image = Image.new('RGB', (matrix.width, matrix.height))
    draw = ImageDraw.Draw(image)

    # Essaie de charger une police, sinon utilise la police par défaut
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
    except:
        font = ImageFont.load_default()

    # Découpe le texte en lignes si nécessaire
    lines = []
    words = text.split()
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]

        if width <= matrix.width - 4:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    # Affiche les lignes
    y_offset = 2
    line_height = 12

    for line in lines[:5]:  # Max 5 lignes
        draw.text((2, y_offset), line, font=font, fill=color)
        y_offset += line_height

    matrix.SetImage(image)
    time.sleep(duration)

def display_scrolling_text(matrix, text, color=(255, 255, 255), speed=0.05):
    """Affiche du texte qui défile horizontalement"""
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    except:
        font = ImageFont.load_default()

    # Crée une image temporaire pour mesurer le texte
    temp_image = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_image)
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

    # Crée une image plus large pour le texte
    canvas_width = matrix.width + text_width + 10
    image = Image.new('RGB', (canvas_width, matrix.height))
    draw = ImageDraw.Draw(image)

    # Dessine le texte
    y_pos = (matrix.height - (bbox[3] - bbox[1])) // 2
    draw.text((matrix.width, y_pos), text, font=font, fill=color)

    # Animation de défilement
    try:
        for x_offset in range(0, text_width + matrix.width):
            # Crée une vue de la partie visible
            cropped = image.crop((x_offset, 0, x_offset + matrix.width, matrix.height))
            matrix.SetImage(cropped)
            time.sleep(speed)
    except KeyboardInterrupt:
        pass

def main():
    parser = argparse.ArgumentParser(description='Affiche du texte sur l\'écran LED 64x64')
    parser.add_argument('text', nargs='?', default='HELLO LED!', help='Texte à afficher')
    parser.add_argument('--scroll', action='store_true', help='Fait défiler le texte')
    parser.add_argument('--color', default='255,255,255', help='Couleur RGB (ex: 255,0,0 pour rouge)')
    parser.add_argument('--duration', type=int, default=10, help='Durée d\'affichage en secondes (mode statique)')
    parser.add_argument('--speed', type=float, default=0.05, help='Vitesse de défilement (mode scroll)')
    parser.add_argument('--brightness', type=int, default=70, help='Luminosité (0-100)')
    parser.add_argument('--row-addr-type', type=int, default=0, help='Type d\'adressage (0, 1, ou 2)')

    args = parser.parse_args()

    # Parse la couleur
    try:
        color = tuple(map(int, args.color.split(',')))
        if len(color) != 3:
            raise ValueError
    except:
        print("Erreur: Format de couleur invalide. Utilisez R,G,B (ex: 255,0,0)")
        sys.exit(1)

    print(f"""
╔════════════════════════════════════════════════════════════╗
║              AFFICHAGE LED MATRIX 64x64                    ║
╚════════════════════════════════════════════════════════════╝

Texte: {args.text}
Mode: {'Défilement' if args.scroll else 'Statique'}
Couleur: RGB{color}
Luminosité: {args.brightness}%
Row Address Type: {args.row_addr_type}

Démarrage...
""")

    try:
        # Configuration personnalisée
        config = {
            'brightness': args.brightness,
            'row_address_type': args.row_addr_type,
        }

        # Crée la matrice
        matrix = create_matrix(config)

        print("✓ Matrice initialisée")
        print(f"Dimensions: {matrix.width}x{matrix.height}")
        print("\nAffichage en cours... (Ctrl+C pour arrêter)\n")

        # Affiche le texte
        if args.scroll:
            while True:
                display_scrolling_text(matrix, args.text, color, args.speed)
        else:
            display_static_text(matrix, args.text, color, args.duration)
            matrix.Clear()
            print("\n✓ Affichage terminé")

    except KeyboardInterrupt:
        print("\n\nInterruption par l'utilisateur")
        matrix.Clear()
    except Exception as e:
        print(f"\n✗ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
