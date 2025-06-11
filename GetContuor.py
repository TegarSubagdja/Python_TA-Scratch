from Utils import *

# Load gambar grayscale
image = cv2.imread('../Image/2.jpg', cv2.IMREAD_GRAYSCALE)

def Contours(image):
    # Threshold dan erosi
    _, thresh = cv2.threshold(image, 80, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=30)

    # Temukan kontur
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Canvas kosong
    output = np.zeros_like(image)

    for contour in contours:
        if cv2.contourArea(contour) > 10000:
            rect = cv2.minAreaRect(contour)
            (cx, cy), (w, h), angle = rect
            w_enlarged = w + 260
            h_enlarged = h + 260
            enlarged_rect = ((cx, cy), (w_enlarged, h_enlarged), angle)
            box = cv2.boxPoints(enlarged_rect)
            box = np.array(box, dtype=np.int32)
            cv2.drawContours(output, [box], 0, 255, -1)  # Warna putih

    # Ubah gambar ke BGR untuk overlay warna
    image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Buat output berwarna: kontur putih → misalnya warna biru
    output_colored = np.zeros_like(image_bgr)
    output_colored[np.where(output == 255)] = (0, 0, 255)  # Merah

    # Overlay dengan transparansi 20%
    blended = cv2.addWeighted(image_bgr, 1.0, output_colored, 0.2, 0)

    # Simpan hasil akhir
    cv2.imwrite('./Output/Overlay.jpg', blended)

    return output
