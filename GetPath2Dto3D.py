from Utils import *

def to3D(path_2d, rvec, tvec, camera_matrix, dist_coeffs, z_world=0.0):
    R, _ = cv2.Rodrigues(rvec)
    R_inv = np.linalg.inv(R)
    cam_inv = np.linalg.inv(camera_matrix)
    tvec = tvec.reshape(3, 1)

    result = []
    for (x, y) in path_2d:
        pixel_vec = np.array([x, y, 1.0]).reshape(3, 1)
        ray = cam_inv @ pixel_vec

        # Hitung skala agar titik berada di z_world dalam koordinat dunia (bidang datar marker)
        scale = (z_world + (R[2] @ tvec)[0]) / (R[2] @ ray)[0]
        cam_point = ray * scale

        # Ubah ke frame marker
        marker_point = R_inv @ (cam_point - tvec)
        result.append(marker_point.flatten())

    return np.array(result)