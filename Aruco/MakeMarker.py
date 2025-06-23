import cv2
import cv2.aruco as aruco

# Pilih dictionary ArUco, misalnya DICT_4X4_50
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Tentukan ID marker yang ingin dibuat (ID harus dalam range dictionary, misalnya 0-49 untuk DICT_4X4_50)
marker_id = 0  # Ganti sesuai kebutuhan

# Ukuran marker dalam piksel
marker_size = 720  # Bisa diubah sesuai kebutuhan

# Buat marker
marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)

# Simpan ke file
filename = f"aruco_marker_id_{marker_id}{"DICT_7X7_50"}.png"
cv2.imwrite(filename, marker_image)

print(f"Marker ID {marker_id} berhasil disimpan sebagai {filename}")
