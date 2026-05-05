import cv2
import os
import time

DOSSIER = "camera_cal"
NB_IMAGES = 10

os.makedirs(DOSSIER, exist_ok=True)

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Erreur : impossible d'ouvrir la caméra")
    exit()

print("=== Capture d'images pour la calibration ===")
print("Appuie sur [ESPACE] pour capturer une image")
print("Appuie sur [Q] pour quitter\n")

compteur = 0

while compteur < NB_IMAGES:
    ret, frame = cap.read()
    if not ret:
        print("Erreur : impossible de lire l'image")
        break

    # Afficher le compteur sur l'image
    texte = f"Images capturees : {compteur}/{NB_IMAGES}"
    cv2.putText(frame, texte, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Capture calibration - [ESPACE] capturer | [Q] quitter", frame)

    touche = cv2.waitKey(1) & 0xFF

    if touche == ord('q'):
        print("Capture annulée.")
        break

    elif touche == ord(' '):
        chemin = os.path.join(DOSSIER, f"calib_{compteur+1:02d}.jpg")
        cv2.imwrite(chemin, frame)
        compteur += 1
        print(f"[{compteur}/{NB_IMAGES}] Image sauvegardée : {chemin}")

        if compteur == NB_IMAGES:
            print(f"\nCapture terminée ! {NB_IMAGES} images dans '{DOSSIER}/'")

cap.release()
cv2.destroyAllWindows()