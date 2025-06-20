import numpy as np
import cv2 
import glob
import os
import matplotlib.pyplot as plt

def calibrate(showPics=True):
    root = os.getcwd()
    calibrationDir = os.path.join(root, 'calibration')
    imagePathList = glob.glob(os.path.join(calibrationDir, '*.jpg'))

    # Ukuran pola papan catur (jumlah sudut dalam baris dan kolom)
    nRows = 9  # jumlah titik di baris
    nCols =  6  # jumlah titik di kolom
    termCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Titik dunia 3D
    worldPtsCur = np.zeros((nRows * nCols, 3), np.float32)
    worldPtsCur[:, :2] = np.mgrid[0:nCols, 0:nRows].T.reshape(-1, 2)

    worldPtsList = []  # Titik dunia 3D
    imgPtsList = []    # Titik citra 2D
    imgSize = None

    for curImagePath in imagePathList:
        imgBGR = cv2.imread(curImagePath)
        if imgBGR is None:
            print(f"Failed to load image: {curImagePath}")
            continue

        imgGray = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2GRAY)
        cornerFound, cornerOrg = cv2.findChessboardCorners(imgGray, (nCols, nRows), None)

        if cornerFound:
            if imgSize is None:
                imgSize = imgGray.shape[::-1]  # Simpan ukuran pertama
            worldPtsList.append(worldPtsCur)
            cornerRefined = cv2.cornerSubPix(imgGray, cornerOrg, (11,11), (-1,-1), termCriteria)
            imgPtsList.append(cornerRefined)
            if showPics:
                cv2.drawChessboardCorners(imgBGR, (nCols, nRows), cornerRefined, cornerFound)
                cv2.imshow('Chessboard', imgBGR)
                cv2.waitKey(500)
        else:
            print(f"Chessboard not found in: {curImagePath}")

    cv2.destroyAllWindows()

    if len(worldPtsList) == 0:
        raise ValueError("Tidak ada sudut papan catur yang ditemukan dalam gambar manapun.")

    # Kalibrasi kamera
    repError, camMatrix, distCoeff, rvecs, tvecs = cv2.calibrateCamera(
        worldPtsList, imgPtsList, imgSize, None, None
    )

    print('Camera Matrix:\n', camMatrix)
    print('Reprojection Error (pixel): {:.4f}'.format(repError))

    # Simpan parameter kalibrasi
    curFolder = os.path.dirname(os.path.abspath(__file__))
    paramPath = os.path.join(curFolder, 'calibration.npz')
    np.savez(paramPath,
             repError=repError,
             camMatrix=camMatrix,
             distCoeff=distCoeff,
             rvecs=rvecs,
             tvecs=tvecs)
    
    return camMatrix, distCoeff


def removeDistortion(camMatrix, distCoeff):
    root = os.getcwd()
    imgPath = os.path.join(root, 'demo2.jpg')
    img = cv2.imread(imgPath)
    if img is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {imgPath}")

    height, width = img.shape[:2]
    camMatrixNew, roi = cv2.getOptimalNewCameraMatrix(camMatrix, distCoeff, (width, height), 1, (width, height))
    imgUndist = cv2.undistort(img, camMatrix, distCoeff, None, camMatrixNew)

    # Gambar garis untuk menunjukkan distorsi
    cv2.line(img, (176, 103), (180, 400), (255, 255, 255), 2)
    cv2.line(imgUndist, (176, 103), (180, 400), (255, 255, 255), 2)

    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.title("Original")
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.subplot(122)
    plt.title("Undistorted")
    plt.imshow(cv2.cvtColor(imgUndist, cv2.COLOR_BGR2RGB))
    plt.tight_layout()
    plt.show()


def runCalibration():
    calibrate(showPics=True)

def runRemoveDistortion():
    camMatrix, distCoeff = calibrate(showPics=True)
    removeDistortion(camMatrix, distCoeff)

if __name__ == '__main__':
    # runCalibration()
    # Jika ingin langsung menghapus distorsi:
    runRemoveDistortion()
