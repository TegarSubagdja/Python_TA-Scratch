from Utils import *
from Pengujian.GetData import runPengujianAvgLength, path_length
from Pengujian.GetAverageMap import generate_keseluruhan_excel
from Pengujian.GetAverageAll import rekap_avg_semua_sheet

# Inisialisasi Aruco Marker
detector_params = aruco.DetectorParameters()
detector_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
detector = aruco.ArucoDetector(detector_dict, detector_params)

# Contoh pemanggilan:
if __name__ == "__main__":

    # runPengujianAvgLength()
    # generate_keseluruhan_excel()
    # rekap_avg_semua_sheet()
    # sys.exit()

    timesArr = []

    size = [16, 32, 64, 128]

    for sz in range(1):

        for i in range(5):

            mapChoice = 2

            if mapChoice < 1:
                nameMap = "Map"
            else:
                nameMap = f"Map_{mapChoice}"

            # foto = cv2.imread("C:/Users/kingt/Desktop/Sample Foto/0829.png")
            # start, goal, marksize = Pos(img=foto, detector=detector)
            # start, goal = PrepCoord(start, goal)
            # print(f"Ini start {start}")
            # print(f"Ini goal {goal}")
            # print(f"Ini marksize {marksize}")
            # map = Prep(img=foto, start=None, goal=None, markSize=marksize, scale=20)

            map = Z_GetMap.load_grid(path=f"Map/JSON/{nameMap}.json", s=True)
            map = Z_GetMap.upscale(map, size[sz])
            # map = Z_GetMap.upscale(map, 128)
            matrix = map.copy()
            start = (0, 0)
            goal = (map.shape[1]-1, map.shape[0]-1)
            map = map.astype(np.uint8)
            df = pd.DataFrame(map)
            df.to_excel("Grid.xlsx")

            np.place(map, map == 1, 255)
            np.place(map, map == 2, 0)
            np.place(map, map == 3, 0)
            tempTimes = []
            tempPaths = []
            tempOpens = []
            tempCloses = []
            tempTurns = []
            tempLengths = []

            show = True

            for i in range(1):
                (path, times), openlist, closelist = Algoritm(
                    map, start, goal, 2,
                    JPS=True,
                    BRC=True,
                    PPO=True,
                    GLF=True,
                    # TPF=True,
                    # BDS=True,
                    # show=True,
                    speed=300,
                )

                # (path2, times), openlist, closelist = Algoritm(
                #     matrix, start, goal, 2,
                #     # JPS=True,
                #     # BRC=True,
                #     # PPO=True,
                #     # GLF=True,
                #     # TPF=True,
                #     # BDS=True,
                #     # show=True,
                #     speed=30,
                # )

                if path:
                    timesArr.append(times)
                    tempTimes.append(times)
                    tempPaths.append(len(path))
                    # tempLengths.append(path_length(path))
                    tempOpens.append(len(openlist))
                    tempCloses.append(len(closelist))
                    tempTurns.append(len(Turn(path)))
                    belokan = len(Turn(path)) if path else None

            # print(f"  Map : {nameMap}")
            # print(matrix)
            # print(f"  Size : {sz}")
            # print(f"  Metod Name : {method_name}")
            # print(f"  Path adalah Asli : {path}")

            if path:
                print(f"  Waktu Pencarian : {times}")
                print(f"  Panjang Jalur : {path_length(path)}")
                print(f"  Jumlah Open Set : {len(openlist)}")
                print(f"  Jumlah Close Set : {len(closelist)}")
                print(f"  Jumlah Open + Close di i {i} : {len(openlist) + len(closelist)}")
                print(f"  Jumlah Belokan : {belokan}")
                # print(f"  Duplicate Closelist : {closelist}")

            # except Exception as e:
            #     print(f"[!] Error di iterasi : {e}")

            # print(f"Rate : {np.mean(tempTimes)}")

            # Munculkan dan simpan map
            if show:
                if path:
                    np.place(map, map == 255, 1)
                    Z_GetMap.show(map, window_size=1080, name=nameMap, path=path, closelist=closelist, openlist=openlist, size="opt") 
                else:
                    np.place(map, map == 255, 1)
                    Z_GetMap.show(map, window_size=1080, name=nameMap, size=sz)