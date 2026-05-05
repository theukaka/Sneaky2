# 📷 test_pose.py — Estimation de pose avec un damier (OpenCV)

Ce script permet d’estimer la **pose d’une caméra** par rapport à un damier (chessboard) à partir d’une calibration préalable. Il fonctionne soit sur une **image fixe**, soit en **temps réel avec une webcam**.

---

## 🚀 Fonctionnalités

* Détection automatique d’un damier (9x6 coins internes)
* Estimation de la pose via `solvePnP`
* Projection et affichage d’un repère 3D (axes X, Y, Z)
* Affichage des paramètres de pose :

  * vecteur de translation (`tvec`)
  * matrice de rotation
* Mode temps réel avec webcam
* Capture d’images à la volée

---

## 📦 Prérequis

* Python 3.x
* OpenCV (`cv2`)
* NumPy

Installation des dépendances :

```bash
pip install opencv-python numpy
```

---

## 📁 Fichier de calibration requis

Le script utilise un fichier :

```
calibration_camera.npz
```

Ce fichier doit contenir :

* `K` : matrice intrinsèque de la caméra
* `dist` : coefficients de distorsion

---

## ⚙️ Paramètres

```python
DAMIER = (9, 6)        # Nombre de coins internes (colonnes, lignes)
TAILLE_CASE_MM = 25    # Taille d’une case du damier en mm
```

---

## 🧠 Principe

1. Détection des coins du damier dans l’image
2. Raffinement des positions (`cornerSubPix`)
3. Association avec des points 3D connus
4. Estimation de la pose avec `solvePnP`
5. Projection d’un repère 3D dans l’image

Axes affichés :

* **X** → rouge
* **Y** → vert
* **Z** → bleu (vers la caméra)

---

## 🖼️ Mode image fixe

Décommente cette ligne dans le `main` :

```python
traiter_image("test.jpg")
```

Puis commente le mode webcam.

### Résultat :

* Affichage de l’image avec le repère 3D
* Affichage console :

  * translation (mm)
  * matrice de rotation

---

## 🎥 Mode webcam (temps réel)

Par défaut :

```python
traiter_webcam(1)
```

> ⚠️ L’index de caméra peut varier (`0`, `1`, etc.)

### Contrôles clavier :

| Touche | Action                |
| ------ | --------------------- |
| `q`    | Quitter               |
| `s`    | Sauvegarder une image |

### Affichage :

* Repère 3D en temps réel
* Distance Z (profondeur) affichée

---

## 💾 Sauvegarde

Les captures sont enregistrées sous la forme :

```
capture_000.jpg
capture_001.jpg
...
```

---

