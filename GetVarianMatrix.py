import numpy as np

data = np.load("upscaled_matrices.npz")
print(data.files)  # Menampilkan semua nama matrix yang tersimpan

# Akses matrix 256x256
mat256 = data["matrix_16x16"]
print(mat256)