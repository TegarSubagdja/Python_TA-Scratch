import cv2
from GetPosition import position
from GetPreprocessing import preprocessing

# Callback saat mouse diklik
def click_event(event, x, y, flags, param):
    global img_display, clicked_points

    if event == cv2.EVENT_LBUTTONDOWN:
        # Simpan titik yang diklik
        clicked_points.append((x, y))

        # Ambil nilai piksel pada koordinat (x, y) dengan akses [y, x]
        if len(img_display.shape) == 2:  # Grayscale / biner
            nilai = img_display[y, x]
        else:  # RGB
            nilai = img_display[y, x]  # Tuple (B, G, R)

        # Tampilkan titik dan koordinat pada gambar
        text = f"({x}, {y}) val: {nilai}"
        cv2.putText(img_display, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.circle(img_display, (x, y), 3, (255, 255, 255), -1)
        cv2.imshow("Gambar", img_display)

# Baca gambar dan resize agar tampak besar
img = cv2.imread('Image/IMG20250531140928.jpg')
img = cv2.resize(img, (1280, 720))

# Proses preprocessing dari file eksternal
# img = position(img)
cv2.circle(img, (661, 48), 35, (255,255,255), -1)
cv2.circle(img, (605, 610), 35, (255,255,255), -1)
cv2.imshow('', img)
cv2.waitKey(0)
img = preprocessing(img)

# Salinan gambar asli untuk reset
img_original = img.copy()
img_display = img.copy()
clicked_points = []

# Tampilkan window
cv2.imshow("Gambar", img_display)
cv2.setMouseCallback("Gambar", click_event)

# Loop event keyboard
while True:
    key = cv2.waitKey(0) & 0xFF

    # Tekan 'r' untuk reset gambar
    if key == ord('r'):
        img_display = img_original.copy()
        clicked_points = []
        cv2.imshow("Gambar", img_display)
        print("Reset gambar.")

    # Tekan 'q' untuk keluar
    elif key == ord('q'):
        break

cv2.destroyAllWindows()