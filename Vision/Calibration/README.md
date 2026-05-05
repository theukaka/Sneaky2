# 📸 capture.py — Camera Calibration Image Capture

## 🧩 Description

`capture.py` is a Python script using OpenCV to capture a series of images from a camera for **camera calibration** purposes (e.g., using a checkerboard pattern).

The script displays a live video feed and allows the user to manually save images by pressing a key.

---

## ⚙️ Requirements

* Python 3.x
* Required library:

  ```bash
  pip install opencv-python
  ```

---

## ▶️ Usage

Run the script:

```bash
python capture.py
```

---

## 🎮 Keyboard Controls

* **SPACE** → Capture an image
* **Q** → Quit the program

---

## 📁 How It Works

* The script opens the camera (default index: `1`).
* A folder named `camera_cal` is automatically created to store captured images.
* The number of images to capture is defined by:

```python
NB_IMAGES = 10
```

* Each captured image is saved with filenames like:

```
calib_01.jpg  
calib_02.jpg  
...
```

* A live counter is displayed on the video feed.

---

## 🖥️ Interface

A window displays:

* The live camera feed
* The number of captured images
* Instructions for controls

---

## 🧠 Technical Details

* Camera capture via `cv2.VideoCapture(1)`
* Text overlay using `cv2.putText`
* Image saving with `cv2.imwrite`
* Keyboard input handling via `cv2.waitKey`

---

## ⚠️ Possible Issues

### ❌ Cannot open camera

* Check the camera index (`0`, `1`, etc.)
* Make sure no other application is using the camera

### ❌ Failed to capture image

* Ensure the camera is working properly
* Try a different camera index

---

## ✏️ Customization

### Change number of images:

```python
NB_IMAGES = 20
```

### Change output folder:

```python
DOSSIER = "my_folder"
```

### Change camera index:

```python
cap = cv2.VideoCapture(0)
```

---

## ✅ Example Workflow (Calibration)

1. Run the script
2. Place a checkerboard in front of the camera
3. Capture multiple images from different angles
4. Use these images in a camera calibration script

---


# 📷 calibration.py — Camera Calibration with OpenCV

## 🧩 Description

`calibration.py` is a Python script that performs **camera calibration** using a set of checkerboard images.

It detects the internal corners of a checkerboard pattern across multiple images and computes the camera’s intrinsic parameters and lens distortion.

---

## ⚙️ Requirements

* Python 3.x
* Required libraries:

  ```bash
  pip install opencv-python numpy
  ```

---

## ▶️ Usage

Make sure you already captured calibration images (e.g., using `capture.py`) in the `camera_cal/` folder, then run:

```bash id="r7k2d1"
python calibration.py
```

---

## 📁 Input Data

* The script automatically loads all images from:

  ```
  camera_cal/*.jpg
  ```

* These images must contain a visible checkerboard pattern.

---

## 🔢 Configuration

### Checkerboard dimensions

```python id="7z2nqk"
DAMIER = (9, 6)
```

* Number of **inner corners** (columns, rows)

### Square size

```python id="p4f8mx"
TAILLE_CASE_MM = 25
```

* Real size of one square (in millimeters)

---

## ⚙️ How It Works

### 1. Prepare 3D reference points

* A grid of 3D points is generated assuming the checkerboard lies on a flat plane (Z = 0)

### 2. Detect checkerboard corners

* For each image:

  * Convert to grayscale
  * Detect corners using `cv2.findChessboardCorners`
  * Refine corner positions to subpixel accuracy with `cv2.cornerSubPix`

### 3. Collect correspondences

* 3D world points (`objpoints`)
* 2D image points (`imgpoints`)

### 4. Calibrate the camera

* Using:

  ```python id="0k9zvb"
  cv2.calibrateCamera(...)
  ```

* Outputs:

  * Camera matrix **K**
  * Distortion coefficients **dist**
  * Rotation vectors **rvecs**
  * Translation vectors **tvecs**

---

## 🖥️ Visualization

* Detected corners are briefly displayed for each image
* Useful for verifying detection quality

---

## 📊 Output

### Console output

* Number of valid images used
* RMS reprojection error
* Camera matrix
* Distortion coefficients

### Saved file

```id="g2l8cn"
calibration_camera.npz
```

Contains:

* `K` → Camera intrinsic matrix
* `dist` → Distortion coefficients
* `rvecs`, `tvecs` → Extrinsic parameters

---

## 🔄 Reload Calibration

You can reuse the calibration later:

```python id="c9d3pw"
data = np.load('calibration_camera.npz')
K, dist = data['K'], data['dist']
```

---

## ⚠️ Possible Issues

### ❌ No checkerboard detected

* Ensure good lighting
* Avoid motion blur
* Make sure the full checkerboard is visible

### ❌ Poor calibration accuracy

* Capture more images (10–20 recommended)
* Use varied angles and positions
* Avoid all images being too similar

---

## ✏️ Customization

### Change checkerboard size:

```python id="2k1hxn"
DAMIER = (8, 5)
```

### Change square size:

```python id="4x9zlm"
TAILLE_CASE_MM = 30
```

### Change input folder:

```python id="8m2vqr"
images = glob.glob('my_folder/*.jpg')
```

---

## ✅ Typical Workflow

1. Capture images using `capture.py`
2. Run `calibration.py`
3. Save calibration parameters
4. Use them to:

   * Undistort images
   * Perform 3D reconstruction
   * Improve measurement accuracy

---

