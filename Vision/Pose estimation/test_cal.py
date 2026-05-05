import cv2
import numpy as np
import glob

# Dimensions du damier : nombre de coins INTÉRIEURS (colonnes, lignes)
DAMIER = (9, 6)
TAILLE_CASE_MM = 25  # taille réelle d'une case en millimètres
# Coordonnées 3D des coins dans le repère du damier (Z=0 car plan plat)
coins_3d_ref = np.zeros((DAMIER[0] * DAMIER[1], 3), np.float32)
coins_3d_ref[:, :2] = np.mgrid[0:DAMIER[0], 0:DAMIER[1]].T.reshape(-1, 2)
coins_3d_ref *= TAILLE_CASE_MM  # convertir en mm réels

objpoints = []  # points 3D (mêmes pour chaque image)
imgpoints = []  # points 2D détectés dans chaque image

images = glob.glob('camera_cal/*.jpg')  # ton dossier d'images

for chemin in images:
    img = cv2.imread(chemin)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Détecter les coins du damier
    ret, coins = cv2.findChessboardCorners(gray, DAMIER, None)

    if ret:
        # Affiner la précision des coins (sous-pixel)
        criteres = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        coins_affines = cv2.cornerSubPix(gray, coins, (11, 11), (-1, -1), criteres)

        objpoints.append(coins_3d_ref)
        imgpoints.append(coins_affines)

        # Optionnel : visualiser
        cv2.drawChessboardCorners(img, DAMIER, coins_affines, ret)
        cv2.imshow('Coins détectés', img)
        cv2.waitKey(300)

cv2.destroyAllWindows()

print(f"{len(objpoints)} images utilisées pour la calibration")
h, w = gray.shape  # taille de l'image (la dernière lue)

ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, (w, h), None, None
)

print(f"Erreur de reprojection RMS : {ret:.4f} px")
print(f"\nMatrice caméra K :\n{K}")
print(f"\nCoefficients de distorsion :\n{dist}")
np.savez('calibration_camera.npz',
         K=K,
         dist=dist,
         rvecs=rvecs,
         tvecs=tvecs)

# Recharger plus tard :
# data = np.load('calibration_camera.npz')
# K, dist = data['K'], data['dist']