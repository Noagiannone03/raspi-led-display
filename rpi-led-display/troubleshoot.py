#!/usr/bin/env python3
"""
Script de diagnostic pour écran LED 64x64
Vérifie l'installation et donne des recommandations
"""

import os
import sys
import subprocess

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_command(command):
    """Vérifie si une commande existe"""
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return True
    except:
        return False

def check_module(module_name):
    """Vérifie si un module Python est installé"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def check_file(filepath):
    """Vérifie si un fichier existe"""
    return os.path.exists(filepath)

def run_command(command):
    """Exécute une commande et retourne la sortie"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return None

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║        DIAGNOSTIC LED MATRIX 64x64                         ║
║                                                            ║
║  Ce script vérifie votre installation et identifie        ║
║  les problèmes potentiels.                                ║
╚════════════════════════════════════════════════════════════╝
    """)

    problems = []
    warnings = []
    checks_ok = []

    # Check 1: Python version
    print_header("1. Version Python")
    python_version = sys.version.split()[0]
    print(f"Version Python: {python_version}")
    major, minor = map(int, python_version.split('.')[:2])
    if major >= 3 and minor >= 7:
        print("✓ Version Python OK")
        checks_ok.append("Python version")
    else:
        print("✗ Python 3.7+ requis")
        problems.append("Version Python trop ancienne")

    # Check 2: Permissions root
    print_header("2. Permissions")
    if os.geteuid() == 0:
        print("✓ Script exécuté en root (sudo)")
        checks_ok.append("Permissions root")
    else:
        print("⚠️  Script non exécuté en root")
        warnings.append("Exécutez avec: sudo python3 troubleshoot.py")

    # Check 3: Git
    print_header("3. Git installé")
    if check_command("git --version"):
        git_version = run_command("git --version")
        print(f"✓ Git installé: {git_version}")
        checks_ok.append("Git")
    else:
        print("✗ Git non installé")
        problems.append("Installez git: sudo apt-get install git")

    # Check 4: Bibliothèque rpi-rgb-led-matrix
    print_header("4. Bibliothèque rpi-rgb-led-matrix")
    if check_file("rpi-rgb-led-matrix"):
        print("✓ Dossier rpi-rgb-led-matrix trouvé")
        checks_ok.append("Bibliothèque téléchargée")

        # Vérification de la compilation
        if check_file("rpi-rgb-led-matrix/bindings/python/rgbmatrix"):
            print("✓ Module Python compilé")
            checks_ok.append("Module compilé")
        else:
            print("✗ Module Python non compilé")
            problems.append("Compilez avec: cd rpi-rgb-led-matrix && make build-python")
    else:
        print("✗ Bibliothèque non téléchargée")
        problems.append("Exécutez: sudo bash install.sh")

    # Check 5: Pillow
    print_header("5. Pillow (PIL)")
    if check_module("PIL"):
        print("✓ Pillow installé")
        checks_ok.append("Pillow")
    else:
        print("✗ Pillow non installé")
        problems.append("Installez avec: pip3 install Pillow")

    # Check 6: Module son désactivé
    print_header("6. Module son (doit être désactivé)")
    blacklist_file = "/etc/modprobe.d/alsa-blacklist.conf"
    if check_file(blacklist_file):
        content = run_command(f"cat {blacklist_file}")
        if "snd_bcm2835" in content:
            print("✓ Module son désactivé")
            checks_ok.append("Module son désactivé")
        else:
            print("⚠️  Fichier trouvé mais configuration incorrecte")
            warnings.append("Vérifiez /etc/modprobe.d/alsa-blacklist.conf")
    else:
        print("✗ Module son non désactivé")
        problems.append("Le son peut interférer avec l'affichage")

    # Check 7: Modèle Raspberry Pi
    print_header("7. Modèle Raspberry Pi")
    model_file = "/proc/device-tree/model"
    if check_file(model_file):
        model = run_command(f"cat {model_file}")
        if model:
            print(f"Modèle: {model}")
            if any(x in model for x in ["Pi 3", "Pi 4", "Pi Zero"]):
                print("✓ Modèle compatible")
                checks_ok.append("Raspberry Pi compatible")
            else:
                print("⚠️  Modèle non testé, pourrait fonctionner")
                warnings.append("Pi 3, 4 ou Zero recommandés")
    else:
        print("⚠️  Impossible de détecter le modèle (pas sur un Raspberry Pi ?)")
        warnings.append("Ce script doit être exécuté sur un Raspberry Pi")

    # Check 8: GPIO disponibles
    print_header("8. GPIO disponibles")
    gpio_path = "/sys/class/gpio"
    if check_file(gpio_path):
        print("✓ Interface GPIO disponible")
        checks_ok.append("GPIO disponibles")
    else:
        print("✗ Interface GPIO non trouvée")
        problems.append("Vérifiez que vous êtes sur un Raspberry Pi")

    # Check 9: Scripts présents
    print_header("9. Scripts du projet")
    scripts = [
        "display_text.py",
        "test_display.py",
        "install.sh",
        "quick_start.sh",
        "examples.sh"
    ]
    missing_scripts = []
    for script in scripts:
        if check_file(script):
            print(f"✓ {script}")
        else:
            print(f"✗ {script} manquant")
            missing_scripts.append(script)

    if not missing_scripts:
        checks_ok.append("Tous les scripts présents")
    else:
        problems.append(f"Scripts manquants: {', '.join(missing_scripts)}")

    # Résumé
    print_header("RÉSUMÉ DU DIAGNOSTIC")

    print(f"✓ Vérifications réussies: {len(checks_ok)}")
    print(f"⚠️  Avertissements: {len(warnings)}")
    print(f"✗ Problèmes: {len(problems)}")

    if problems:
        print("\n" + "="*60)
        print("PROBLÈMES À RÉSOUDRE:")
        print("="*60)
        for i, problem in enumerate(problems, 1):
            print(f"{i}. {problem}")

    if warnings:
        print("\n" + "="*60)
        print("AVERTISSEMENTS:")
        print("="*60)
        for i, warning in enumerate(warnings, 1):
            print(f"{i}. {warning}")

    # Recommandations
    print("\n" + "="*60)
    print("RECOMMANDATIONS:")
    print("="*60)

    if not check_file("rpi-rgb-led-matrix"):
        print("\n1. Commencez par installer la bibliothèque:")
        print("   sudo bash install.sh")
        print("   sudo reboot")
    elif problems:
        print("\n1. Résolvez les problèmes listés ci-dessus")
        print("2. Relancez ce diagnostic: sudo python3 troubleshoot.py")
    elif warnings:
        print("\n1. Vérifiez les avertissements")
        print("2. Testez l'écran: sudo python3 test_display.py")
    else:
        print("\n✓ Tout semble OK !")
        print("\n1. Vérifiez le câblage (consultez wiring_guide.txt)")
        print("2. Testez l'écran: sudo python3 test_display.py")
        print("3. Si ça fonctionne, utilisez: sudo python3 display_text.py \"TEST\"")

    # Guide rapide de dépannage
    print("\n" + "="*60)
    print("GUIDE RAPIDE DE DÉPANNAGE:")
    print("="*60)
    print("""
Si l'écran ne s'affiche pas après avoir résolu les problèmes:

1. VÉRIFIEZ L'ALIMENTATION
   • Utilisez une alim 5V/4A minimum (PAS le Raspberry Pi !)
   • Connectez UNIQUEMENT les GND ensemble

2. TESTEZ DIFFÉRENTES CONFIGURATIONS
   • Lancez: sudo python3 test_display.py
   • Notez quelle configuration fonctionne

3. VÉRIFIEZ LE CÂBLAGE
   • Consultez: wiring_guide.txt
   • Assurez-vous que le pin E est connecté (important pour 64x64 !)

4. PROBLÈMES COURANTS
   • Image coupée → Essayez --row-addr-type 1
   • Seul le rouge → Alimentation insuffisante
   • Rien ne s'affiche → Vérifiez les connexions GPIO
    """)

    print("="*60)
    print("Pour plus d'aide, consultez le README.md")
    print("="*60)

if __name__ == "__main__":
    main()
