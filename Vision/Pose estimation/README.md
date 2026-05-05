# 📷 test_pose.py — Pose Estimation with a Chessboard (OpenCV)

This script estimates the **pose of a camera** relative to a chessboard pattern using a previously computed camera calibration. It works with both **static images** and **real-time webcam input**.

---

## 🚀 Features

* Automatic detection of a chessboard (9x6 inner corners)
* Pose estimation using `solvePnP`
* Projection and display of a 3D coordinate frame (X, Y, Z axes)
* Outputs pose parameters:

  * translation vector (`tvec`)
  * rotation matrix
* Real-time webcam mode
* Frame capture support

---

## 📦 Requirements

* Python 3.x
* OpenCV (`cv2`)
* NumPy

Install dependencies:

```bash
pip install opencv-python numpy
```

---

## 📁 Required Calibration File

The script expects a file:

```
calibration_camera.npz
```

This file must contain:

* `K` : camera intrinsic matrix
* `dist` : distortion coefficients

---

## ⚙️ Parameters

```python
DAMIER = (9, 6)        # Number of inner corners (columns, rows)
TAILLE_CASE_MM = 25    # Size of one square in mm
```

---

## 🧠 How It Works

1. Detect chessboard corners in the image
2. Refine corner positions (`cornerSubPix`)
3. Match them with known 3D points
4. Estimate pose using `solvePnP`
5. Project a 3D coordinate frame onto the image

Axes color convention:

* **X** → red
* **Y** → green
* **Z** → blue (pointing toward the camera)

---

## 🖼️ Static Image Mode

Uncomment this line in `main`:

```python
traiter_image("test.jpg")
```

And comment out the webcam mode.

### Output:

* Image with projected 3D axes
* Console output:

  * translation (mm)
  * rotation matrix

---

## 🎥 Webcam Mode (Real-Time)

Default:

```python
traiter_webcam(1)
```

> ⚠️ Camera index may vary (`0`, `1`, etc.)

### Keyboard Controls:

| Key | Action             |
| --- | ------------------ |
| `q` | Quit               |
| `s` | Save current frame |

### Display:

* Real-time 3D axes overlay
* Z distance (depth) displayed

---

## 💾 Saving Images

Captured frames are saved as:

```
capture_000.jpg
capture_001.jpg
...
```

---

