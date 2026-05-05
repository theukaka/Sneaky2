import cv2
import numpy as np

# ─── Paramètres ───────────────────────────────────────────────────────────────
DAMIER = (9, 6)
TAILLE_CASE_MM = 25

# ─── Chargement de la calibration ─────────────────────────────────────────────
data = np.load('calibration_camera.npz')
K    = data['K']
dist = data['dist']

# ─── Points 3D de référence du damier ─────────────────────────────────────────
coins_3d_ref = np.zeros((DAMIER[0] * DAMIER[1], 3), np.float32)
coins_3d_ref[:, :2] = np.mgrid[0:DAMIER[0], 0:DAMIER[1]].T.reshape(-1, 2)
coins_3d_ref *= TAILLE_CASE_MM

# ─── Axes du repère à tracer (longueur = 3 cases) ─────────────────────────────
LONGUEUR_AXE = 3 * TAILLE_CASE_MM  # 75 mm

axes_3d = np.float32([
    [0, 0, 0],                  # origine
    [LONGUEUR_AXE, 0, 0],       # axe X  → rouge
    [0, LONGUEUR_AXE, 0],       # axe Y  → vert
    [0, 0, -LONGUEUR_AXE],      # axe Z  → bleu  (négatif = vers la caméra)
])

def dessiner_repere(img, coins_image, K, dist, coins_3d_ref):
    """
    Estime la pose du damier et trace les axes XYZ sur l'image.
    Retourne l'image annotée + (rvec, tvec) ou None si échec.
    """
    ret, rvec, tvec = cv2.solvePnP(coins_3d_ref, coins_image, K, dist)
    if not ret:
        return img, None, None

    # Projeter les axes 3D → pixels 2D
    pts_image, _ = cv2.projectPoints(axes_3d, rvec, tvec, K, dist)
    pts_image = pts_image.reshape(-1, 2).astype(int)

    origine = tuple(pts_image[0])
    pt_x    = tuple(pts_image[1])
    pt_y    = tuple(pts_image[2])
    pt_z    = tuple(pts_image[3])

    epaisseur = 3
    cv2.arrowedLine(img, origine, pt_x, (0, 0, 255), epaisseur, tipLength=0.2)  # X rouge
    cv2.arrowedLine(img, origine, pt_y, (0, 255, 0), epaisseur, tipLength=0.2)  # Y vert
    cv2.arrowedLine(img, origine, pt_z, (255, 0, 0), epaisseur, tipLength=0.2)  # Z bleu

    # Étiquettes
    decalage = 10
    cv2.putText(img, "X", (pt_x[0]+decalage, pt_x[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(img, "Y", (pt_y[0]+decalage, pt_y[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(img, "Z", (pt_z[0]+decalage, pt_z[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    return img, rvec, tvec


# ─── Mode image fixe ──────────────────────────────────────────────────────────
def traiter_image(chemin):
    img = cv2.imread(chemin)
    if img is None:
        print(f"Impossible de lire : {chemin}")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, coins = cv2.findChessboardCorners(gray, DAMIER, None)

    if not ret:
        print("Damier non détecté.")
        cv2.imshow("Résultat", img)
        cv2.waitKey(0)
        return

    criteres = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    coins = cv2.cornerSubPix(gray, coins, (11, 11), (-1, -1), criteres)

    img, rvec, tvec = dessiner_repere(img, coins, K, dist, coins_3d_ref)

    if rvec is not None:
        # Afficher translation et rotation dans la console
        rot_mat, _ = cv2.Rodrigues(rvec)
        print(f"Translation (mm) : {tvec.ravel()}")
        print(f"Matrice de rotation :\n{rot_mat}")

        # Superposer les valeurs sur l'image
        txt = f"t = [{tvec[0,0]:.1f}, {tvec[1,0]:.1f}, {tvec[2,0]:.1f}] mm"
        cv2.putText(img, txt, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Pose estimation", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ─── Mode webcam temps réel ───────────────────────────────────────────────────
def traiter_webcam(index_camera=0):
    cap = cv2.VideoCapture(index_camera)
    if not cap.isOpened():
        print("Impossible d'ouvrir la caméra.")
        return

    print("Appuie sur 'q' pour quitter, 's' pour sauvegarder une frame.")
    compteur = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Détection rapide (flags = FAST_CHECK évite le calcul complet si pas de damier)
        flags = cv2.CALIB_CB_FAST_CHECK
        trouve, coins = cv2.findChessboardCorners(gray, DAMIER, flags)

        if trouve:
            criteres = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            coins = cv2.cornerSubPix(gray, coins, (11, 11), (-1, -1), criteres)
            frame, rvec, tvec = dessiner_repere(frame, coins, K, dist, coins_3d_ref)

            if tvec is not None:
                txt = f"Z = {tvec[2,0]:.1f} mm"
                cv2.putText(frame, txt, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (255, 255, 0), 2)
        else:
            cv2.putText(frame, "Damier non détecté", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        cv2.imshow("Pose estimation (webcam)", frame)

        touche = cv2.waitKey(1) & 0xFF
        if touche == ord('q'):
            break
        elif touche == ord('s'):
            nom = f"capture_{compteur:03d}.jpg"
            cv2.imwrite(nom, frame)
            print(f"Sauvegardé : {nom}")
            compteur += 1

    cap.release()
    cv2.destroyAllWindows()


# ─── Point d'entrée ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Choix du mode :
    # traiter_image("test.jpg")   ← image fixe
    traiter_webcam(1)             # ← webcam en temps réel