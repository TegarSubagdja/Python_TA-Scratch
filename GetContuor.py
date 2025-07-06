from Utils import *

def Contour(image, corners):
    # Hitung Lebar Marker
    if corners:
        pts = corners[0][0] 
        mark_size = 0.5 * (np.linalg.norm(pts[0] - pts[1]) + np.linalg.norm(pts[2] - pts[3]))
    else:
        return 0, 0

    # Hilangkan Aruco Marker
    for corner in corners:
        pts = corner[0].astype(int)  # Koordinat sudut marker dalam integer
        cv2.fillPoly(image, [pts], (255, 255, 255))  # Putih di BGR

    # Threshold dan erosi
    _, thresh = cv2.threshold(image, 115, 255, cv2.THRESH_BINARY_INV)
    # kernel = np.ones((3,3), np.uint8)
    # thresh = cv2.erode(thresh, kernel, iterations=iterate)

    # Temukan kontur
    cv2.imwrite('Data/Image/Process/5-findContours.jpg', image)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Canvas kosong
    output = np.zeros_like(image)

    for contour in contours:
        if cv2.contourArea(contour) > 1000:
            rect = cv2.minAreaRect(contour)
            (cx, cy), (w, h), angle = rect
            w_enlarged = w + (2 * mark_size)
            h_enlarged = h + (2 * mark_size)
            enlarged_rect = ((cx, cy), (w_enlarged, h_enlarged), angle)
            box = cv2.boxPoints(enlarged_rect)
            box = np.array(box, dtype=np.int32)
            cv2.drawContours(output, [box], 0, 255, -1, lineType=cv2.LINE_8)

    # Ubah gambar ke BGR untuk overlay warna
    image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Buat output berwarna: kontur putih → misalnya warna biru
    output_colored = np.zeros_like(image_bgr)
    output_colored[np.where(output == 255)] = (255, 100, 255)  # Merah

    # Overlay dengan transparansi 20%
    blended = cv2.addWeighted(image_bgr, 1.0, output_colored, 0.2, 0)
    cv2.imwrite('Data/Image/Process/6-overleay.jpg', blended)
    cv2.imwrite('Data/Image/Process/7-OutputContour.jpg', output)

    cv2.imwrite('Output/Overlay.jpg', output)

    return output, mark_size
