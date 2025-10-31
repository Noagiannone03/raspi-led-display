# 🔧 Solution pour le problème "4 lignes verticales bleu/rouge"

## 📋 Votre problème actuel

Vous voyez seulement **4 lignes verticales** de LED en bleu et un peu de rouge qui ne changent presque pas durant le test.

### Ce que cela signifie :

✅ **Les pins RGB fonctionnent** (R1, G1, B1, R2, G2, B2 sont bien branchées)
❌ **Problème de configuration logicielle** - Les paramètres critiques ne sont pas corrects

---

## 🎯 Le paramètre manquant : `row_address_type`

Votre panneau a **seulement A, B, C** (3 bits d'adressage, pas de D ni E).

Le script `test_all_mappings.py` ne testait **PAS** le paramètre `row_address_type` qui est **CRUCIAL** pour ce type de panneau !

### Les valeurs possibles de `row_address_type` :

| Valeur | Description | Pour quel panneau ? |
|--------|-------------|---------------------|
| `0` | Direct (défaut) | Panneaux avec A,B,C,D,E (5 bits) |
| `1` | AB-addressed | Panneaux avec seulement A,B |
| `2` | Direct row select | Certains panneaux P10 |
| **`3`** | **ABC-addressed** | **← PROBABLEMENT VOTRE PANNEAU** |
| `4` | ABC Shift + DE | Panneaux hybrides |

**Pour votre panneau avec A, B, C seulement → Probablement `row_address_type = 3`**

---

## 🚀 SOLUTION : Utilisez le nouveau script de test

J'ai créé un script **exhaustif** qui teste TOUS les paramètres :

```bash
sudo python3 test_exhaustive.py
```

### Ce que ce script teste :

1. ✅ Tous les `hardware_mapping` (regular, adafruit-hat, etc.)
2. ✅ Tous les `row_address_type` (0, 1, 2, **3**, 4)  ← **NOUVEAU !**
3. ✅ Tous les `multiplexing` (0 à 11)
4. ✅ Différentes configurations de panneau

---

## 📝 Comment utiliser le script

### 1. Lancez le script

```bash
sudo python3 test_exhaustive.py
```

### 2. Choisissez le mode

Le script vous propose 2 modes :

**Mode RAPIDE (recommandé)** : Teste uniquement les combinaisons les plus probables
- `row_address_type` = 2 ou 3
- `multiplexing` = 0 ou 1
- `hardware_mapping` = regular ou adafruit-hat
- **Durée : 5-10 minutes**

**Mode COMPLET** : Teste TOUTES les combinaisons possibles
- **Durée : 30+ minutes**
- Utilisez-le seulement si le mode RAPIDE ne trouve rien

### 3. Pour chaque test

Le script affiche :
1. **3 bandes de couleur** (rouge, vert, bleu)
2. **2 lignes blanches** (en haut et en bas)

**Vérifiez :**
- ✅ Les bandes couvrent TOUT l'écran (128 pixels de large) ?
- ✅ Les couleurs sont correctes ?
- ✅ Les lignes blanches sont bien en haut et en bas ?
- ✅ Pas de lignes bizarres ou répétées ?

Si **TOUT est parfait**, tapez `o` puis ENTRÉE.

### 4. Quand la configuration est trouvée

Le script :
- ✅ Affiche les paramètres exacts à utiliser
- ✅ Sauvegarde dans `CONFIGURATION_TROUVEE.txt`

---

## 🔍 Exemple de configuration trouvée

Si ça marche, vous verrez quelque chose comme :

```python
options = RGBMatrixOptions()
options.hardware_mapping = 'regular'
options.row_address_type = 3  # ← C'était ce paramètre qui manquait !
options.multiplexing = 0
options.rows = 32
options.cols = 64
options.chain_length = 2
options.parallel = 1
options.brightness = 70
```

---

## 🛠️ Ensuite : Mettre à jour vos scripts

Une fois la configuration trouvée, mettez à jour vos scripts d'affichage :

### Fichier `display_text_128x64.py`

Trouvez la section "CONFIGURATION" (ligne ~35) et remplacez par les paramètres trouvés.

**IMPORTANT : N'oubliez pas d'ajouter le paramètre `row_address_type` !**

---

## 📊 Différence avec `test_all_mappings.py`

| Script | Ce qu'il teste | Nombre de tests | Durée |
|--------|----------------|-----------------|-------|
| `test_all_mappings.py` | hardware_mapping + multiplexing | ~18 tests | 5-10 min |
| **`test_exhaustive.py`** | **+ row_address_type** | Mode rapide: ~16 tests<br>Complet: ~240 tests | 5-10 min<br>30+ min |

---

## ⚡ Commande rapide

```bash
# 1. Lancez le test exhaustif (mode rapide recommandé)
sudo python3 test_exhaustive.py

# 2. Choisissez le mode 1 (RAPIDE)

# 3. Pour chaque test, vérifiez si tout est correct
#    Si OUI → tapez 'o'
#    Si NON → appuyez juste sur ENTRÉE

# 4. La configuration sera sauvegardée automatiquement dans CONFIGURATION_TROUVEE.txt
```

---

## 🐛 Si le mode RAPIDE ne trouve rien

Essayez le **mode COMPLET** :

```bash
sudo python3 test_exhaustive.py
# Choisissez "2" pour le mode complet
```

⚠️ Cela va prendre **30+ minutes** car il teste ~240 combinaisons différentes.

**Astuce** : Notez quelle configuration donne le **meilleur** résultat (même si pas parfait), on pourra affiner après.

---

## 💡 Explication technique

### Pourquoi seulement 4 lignes verticales ?

Avec les mauvais paramètres `row_address_type` et `multiplexing` :
- La bibliothèque envoie les données dans le mauvais ordre
- Les lignes de scan ne sont pas adressées correctement
- Résultat : seulement quelques pixels s'allument au mauvais endroit

### Le rôle de `row_address_type` :

Ce paramètre indique comment les bits d'adressage (A, B, C) sont interprétés :
- **Type 0** : A,B,C,D,E → adressage binaire direct (0-31)
- **Type 3** : A,B,C uniquement → adressage spécial pour scan 1/8

Votre panneau ayant **seulement A,B,C**, il utilise probablement le type 3.

---

## ✅ Checklist

Avant de lancer le test, vérifiez :

- [ ] Le câblage est correct (selon `CABLAGE_EXACT.md`)
- [ ] L'alimentation 5V externe est branchée
- [ ] Les GND sont connectés ensemble (alim + RPi)
- [ ] Vous lancez avec `sudo`

---

## 🎉 Résumé

1. **Lancez** : `sudo python3 test_exhaustive.py`
2. **Choisissez** : Mode 1 (RAPIDE)
3. **Pour chaque test** : Vérifiez si c'est parfait
4. **Si parfait** : Tapez `o`
5. **Copiez** la configuration trouvée dans vos scripts

---

Bonne chance ! Ce nouveau script devrait trouver la bonne configuration. 🚀
