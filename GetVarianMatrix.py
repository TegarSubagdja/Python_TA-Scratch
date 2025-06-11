import numpy as np
from GetVisualize import visualize_matrix

data = np.load("upscaled_matrices.npz")
print(data.files)  # Menampilkan semua nama matrix yang tersimpan

"""
Varian Size 
'matrix_16x16', 
'matrix_32x32', 
'matrix_64x64', 
'matrix_128x128', 
'matrix_256x256', 
'matrix_512x512', 
'matrix_1024x1024'
"""

# Akses matrix 256x256
mat256 = data["matrix_256x256"]
visualize_matrix(mat256, cell_size=2)