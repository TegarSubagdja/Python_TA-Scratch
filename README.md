#Tuning Image Preprocessing 
https://github.com/TegarSubagdja/Python_Cleaning-Image-Threshold-Morphology.git

#Gambar Ke Plot
# --- Plot semua tahap menggunakan matplotlib ---
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle("Tahapan Pengolahan Citra & Jalur", fontsize=16)

# Helper untuk menampilkan citra BGR → RGB
def show(ax, img, title):
    if len(img.shape) == 2:
        ax.imshow(img, cmap='gray')
    else:
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax.set_title(title)
    ax.axis('off')

show(axes[0, 0], output_image, "Input Image + Posisi")
show(axes[0, 1], gray, "Grayscale")
show(axes[0, 2], map, "Threshold (Map)")
show(axes[1, 0], closing, "Morph Closing")
show(axes[1, 1], opening, "Morph Opening")
show(axes[1, 2], result, "Jalur Hasil Akhir")

plt.tight_layout()
plt.subplots_adjust(top=0.90)
plt.show()