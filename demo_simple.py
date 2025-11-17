#!/usr/bin/env python3
"""
Demo simple pour écran LED 128x64
Affiche du texte et des traits de couleur

Pour exécuter sur le Raspberry Pi :
sudo python3 demo_simple.py
"""

import sys
import os
import time

# Configuration des chemins pour la bibliothèque
script_dir = os.path.dirname(os.path.abspath(__file__))
rgb_matrix_path = os.path.join(script_dir, 'rpi-rgb-led-matrix', 'bindings', 'python')
sys.path.insert(0, rgb_matrix_path)

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
except ImportError as e:
    print("ERREUR: Module rgbmatrix non trouvé")
    print(f"Détail: {e}")
    print("\nAssurez-vous d'avoir installé la bibliothèque rpi-rgb-led-matrix")
    sys.exit(1)

def create_matrix():
    """Crée et configure la matrice LED"""
    options = RGBMatrixOptions()

    # Configuration pour écran 128x64 avec Adafruit bonnet
    options.rows = 32              # Hauteur d'un panneau
    options.cols = 64              # Largeur d'un panneau
    options.chain_length = 2       # 2 panneaux en chaîne = 128x64 total
    options.parallel = 1           # Nombre de chaînes en parallèle

    # Hardware mapping pour Adafruit RGB Matrix Bonnet
    options.hardware_mapping = 'adafruit-hat'

    # Paramètres d'affichage
    options.brightness = 50        # Luminosité (0-100)
    options.pwm_bits = 11          # Qualité PWM
    options.gpio_slowdown = 2      # Ralentissement pour stabilité

    # Paramètres pour certains types d'écrans
    options.multiplexing = 0       # Mode de multiplexage
    options.row_address_type = 0   # Type d'adressage
    options.led_rgb_sequence = "RGB"  # Ordre des couleurs

    return RGBMatrix(options=options)

def draw_color_bars(matrix):
    """Dessine des bandes de couleur horizontales"""
    width = matrix.width
    height = matrix.height

    print("Affichage de bandes de couleur...")

    # Définir les couleurs (R, G, B)
    colors = [
        (255, 0, 0),    # Rouge
        (0, 255, 0),    # Vert
        (0, 0, 255),    # Bleu
        (255, 255, 0),  # Jaune
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 255, 255),# Blanc
        (128, 128, 128) # Gris
    ]

    # Hauteur de chaque bande
    bar_height = height // len(colors)

    # Dessiner les bandes
    for i, (r, g, b) in enumerate(colors):
        y_start = i * bar_height
        y_end = min((i + 1) * bar_height, height)

        for y in range(y_start, y_end):
            for x in range(width):
                matrix.SetPixel(x, y, r, g, b)

def draw_vertical_lines(matrix):
    """Dessine des lignes verticales de couleur"""
    width = matrix.width
    height = matrix.height

    print("Affichage de lignes verticales...")

    matrix.Clear()

    colors = [
        (255, 0, 0),    # Rouge
        (0, 255, 0),    # Vert
        (0, 0, 255),    # Bleu
        (255, 255, 0),  # Jaune
    ]

    # Dessiner des lignes tous les 8 pixels
    for x in range(0, width, 8):
        color = colors[(x // 8) % len(colors)]
        for y in range(height):
            matrix.SetPixel(x, y, color[0], color[1], color[2])

def draw_rainbow_gradient(matrix):
    """Dessine un dégradé arc-en-ciel"""
    width = matrix.width
    height = matrix.height

    print("Affichage d'un dégradé arc-en-ciel...")

    matrix.Clear()

    for x in range(width):
        # Calculer la couleur basée sur la position X
        hue = (x * 360) // width

        # Convertir HSV en RGB (simplifié)
        if hue < 60:
            r, g, b = 255, int(hue * 255 / 60), 0
        elif hue < 120:
            r, g, b = int((120 - hue) * 255 / 60), 255, 0
        elif hue < 180:
            r, g, b = 0, 255, int((hue - 120) * 255 / 60)
        elif hue < 240:
            r, g, b = 0, int((240 - hue) * 255 / 60), 255
        elif hue < 300:
            r, g, b = int((hue - 240) * 255 / 60), 0, 255
        else:
            r, g, b = 255, 0, int((360 - hue) * 255 / 60)

        for y in range(height):
            matrix.SetPixel(x, y, r, g, b)

def draw_text(matrix, font, text, color):
    """Affiche du texte sur la matrice"""
    width = matrix.width
    height = matrix.height

    print(f"Affichage du texte: {text}")

    matrix.Clear()

    # Calculer la position pour centrer le texte
    text_width = len(text) * 6  # Approximation de la largeur
    x_pos = max(0, (width - text_width) // 2)
    y_pos = height // 2 + 4  # Centre vertical

    # Dessiner le texte
    graphics.DrawText(matrix, font, x_pos, y_pos, color, text)

def draw_scrolling_text(matrix, font, text, color, speed=0.02):
    """Fait défiler du texte de droite à gauche"""
    width = matrix.width
    height = matrix.height

    print(f"Défilement du texte: {text}")

    text_width = len(text) * 6
    y_pos = height // 2 + 4

    # Défilement de droite à gauche
    for x_offset in range(width, -text_width, -1):
        matrix.Clear()
        graphics.DrawText(matrix, font, x_offset, y_pos, color, text)
        time.sleep(speed)

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║         DEMO SIMPLE - ÉCRAN LED 128x64                       ║
║                                                              ║
║  Écran: DV08-210519 128x64-32S V1.0                          ║
║  Interface: Adafruit RGB Matrix Bonnet                       ║
╚══════════════════════════════════════════════════════════════╝
""")

    # Vérifier les permissions root
    if os.geteuid() != 0:
        print("⚠️  ATTENTION: Ce script doit être exécuté avec sudo")
        print("   Utilisez: sudo python3 demo_simple.py")
        sys.exit(1)

    try:
        # Initialiser la matrice
        print("Initialisation de la matrice LED...")
        matrix = create_matrix()
        print(f"✓ Matrice initialisée: {matrix.width}x{matrix.height} pixels\n")

        # Charger la police
        try:
            font = graphics.Font()
            font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")
        except:
            print("⚠️  Police par défaut non trouvée, texte limité")
            font = None

        # Couleur pour le texte (blanc)
        text_color = graphics.Color(255, 255, 255)

        # --- DÉMONSTRATION ---

        # 1. Bandes de couleur
        print("\n1️⃣  BANDES DE COULEUR")
        draw_color_bars(matrix)
        time.sleep(3)

        # 2. Lignes verticales
        print("\n2️⃣  LIGNES VERTICALES")
        draw_vertical_lines(matrix)
        time.sleep(3)

        # 3. Dégradé arc-en-ciel
        print("\n3️⃣  DÉGRADÉ ARC-EN-CIEL")
        draw_rainbow_gradient(matrix)
        time.sleep(3)

        # 4. Texte statique (si police disponible)
        if font:
            print("\n4️⃣  TEXTE STATIQUE")
            draw_text(matrix, font, "HELLO!", text_color)
            time.sleep(3)

            draw_text(matrix, font, "LED MATRIX", text_color)
            time.sleep(3)

            # 5. Texte défilant
            print("\n5️⃣  TEXTE DÉFILANT")
            draw_scrolling_text(matrix, font, "MODULEAIR - TEST LED 128x64", text_color, speed=0.03)

        # 6. Animation finale - flashs de couleur
        print("\n6️⃣  ANIMATION FINALE")
        flash_colors = [
            (255, 0, 0),    # Rouge
            (0, 255, 0),    # Vert
            (0, 0, 255),    # Bleu
            (255, 255, 0),  # Jaune
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
        ]

        for _ in range(2):
            for r, g, b in flash_colors:
                for y in range(matrix.height):
                    for x in range(matrix.width):
                        matrix.SetPixel(x, y, r, g, b)
                time.sleep(0.2)

        # Effacer l'écran
        matrix.Clear()

        print("\n✓ Démonstration terminée !")
        print("\nPour personnaliser:")
        print("  - Modifiez les couleurs dans le code")
        print("  - Changez le texte à afficher")
        print("  - Ajustez la luminosité (brightness)")

    except KeyboardInterrupt:
        print("\n\nArrêt demandé par l'utilisateur (Ctrl+C)")
        matrix.Clear()
    except Exception as e:
        print(f"\n✗ ERREUR: {str(e)}")
        print("\nSi l'écran ne s'affiche pas:")
        print("  1. Vérifiez l'alimentation (5V minimum 3A recommandé)")
        print("  2. Vérifiez le câblage avec le bonnet Adafruit")
        print("  3. Essayez différents 'hardware_mapping' (regular, adafruit-hat-pwm)")
        print("  4. Lancez: sudo python3 test_DV08_128x64_32S.py pour tester d'autres configs")
        sys.exit(1)

if __name__ == "__main__":
    main()
