#!/usr/bin/env python3
"""
Test des signaux GPIO pour vérifier si les pins A, B, C envoient des signaux
"""

import RPi.GPIO as GPIO
import time

print("""
╔════════════════════════════════════════════════════════════╗
║         TEST DES SIGNAUX GPIO (A, B, C)                   ║
║                                                            ║
║  Ce script va tester si les GPIO 15, 16, 20 peuvent       ║
║  envoyer des signaux (test sans le panneau LED)           ║
╚════════════════════════════════════════════════════════════╝
""")

# Configuration des pins selon CABLAGE_EXACT.md
PIN_A = 15   # Pin physique 10
PIN_B = 16   # Pin physique 36
PIN_C = 20   # Pin physique 38

print("⚠️  ATTENTION : Débranchez le panneau LED avant ce test !")
print("              Ce test va juste vérifier si les GPIO fonctionnent.")
input("\nAppuyez sur ENTRÉE une fois le panneau débranché...")

# Configuration GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configuration des pins en sortie
GPIO.setup(PIN_A, GPIO.OUT)
GPIO.setup(PIN_B, GPIO.OUT)
GPIO.setup(PIN_C, GPIO.OUT)

print("\n" + "="*70)
print("TEST 1 : Alternance des signaux A, B, C")
print("="*70)
print("\nSi vous avez un multimètre ou un oscilloscope, mesurez les pins :")
print(f"  - GPIO {PIN_A} (A) - Pin physique 10")
print(f"  - GPIO {PIN_B} (B) - Pin physique 36")
print(f"  - GPIO {PIN_C} (C) - Pin physique 38")
print("\nChaque pin va alterner entre HIGH (3.3V) et LOW (0V) pendant 10 secondes.")
print("")

for test_num in range(3):
    print(f"\nTest {test_num + 1}/3 : Alternance rapide (5 Hz)...")

    for i in range(50):  # 10 secondes à 5Hz
        GPIO.output(PIN_A, GPIO.HIGH if i % 2 == 0 else GPIO.LOW)
        GPIO.output(PIN_B, GPIO.HIGH if i % 4 < 2 else GPIO.LOW)
        GPIO.output(PIN_C, GPIO.HIGH if i % 8 < 4 else GPIO.LOW)
        time.sleep(0.1)

    # Retour à LOW
    GPIO.output(PIN_A, GPIO.LOW)
    GPIO.output(PIN_B, GPIO.LOW)
    GPIO.output(PIN_C, GPIO.LOW)

    if test_num < 2:
        time.sleep(0.5)

print("\n" + "="*70)
print("TEST 2 : Test individuel de chaque pin")
print("="*70)

pins_to_test = [
    (PIN_A, "A", "Pin physique 10"),
    (PIN_B, "B", "Pin physique 36"),
    (PIN_C, "C", "Pin physique 38"),
]

for pin, name, physical in pins_to_test:
    print(f"\n🔍 Test de {name} (GPIO {pin} - {physical})...")
    print("   Devrait alterner entre 3.3V et 0V...")

    for i in range(10):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.25)

    print(f"   ✓ Test de {name} terminé")

# Nettoyage
GPIO.cleanup()

print("\n" + "="*70)
print("📋 RÉSULTATS À VÉRIFIER")
print("="*70)
print("\nSi vous avez mesuré avec un multimètre/oscilloscope :")
print("")
print("✅ NORMAL : Chaque pin alterne entre ~3.3V et 0V")
print("❌ PROBLÈME : Une ou plusieurs pins restent à 0V ou 3.3V constant")
print("")
print("Si une pin ne change pas de valeur :")
print("  → Le GPIO est peut-être endommagé (grillé)")
print("  → Solution : Utiliser d'autres GPIO disponibles")
print("")
print("="*70)
print("\n💡 PROCHAINES ÉTAPES")
print("="*70)
print("\nSi les GPIO fonctionnent mais le panneau ne répond pas :")
print("")
print("1. PROBLÈME DE NIVEAU LOGIQUE (3.3V vs 5V)")
print("   → Votre panneau nécessite probablement un LEVEL SHIFTER")
print("   → Le Raspberry Pi envoie du 3.3V")
print("   → Certains panneaux nécessitent du 5V pour les signaux")
print("")
print("2. SOLUTION : Utiliser un HAT avec level shifter")
print("   → Adafruit RGB Matrix HAT")
print("   → Électrodragon RGB LED Matrix Panel Driver")
print("   → OU construire un level shifter avec 74HCT245")
print("")
print("3. SOLUTION ALTERNATIVE : Tester avec --led-slowdown-gpio")
print("   → Ralentit les signaux GPIO")
print("   → Peut aider certains panneaux à détecter les signaux 3.3V")
print("")
print("="*70)
print("\nVoulez-vous que je vous guide pour tester avec --led-slowdown-gpio ?")
print("="*70)
