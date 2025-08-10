from Utils import *
from Pengujian.GetData import runPengujianAvgLength, path_length
from Pengujian.GetAverageMap import generate_keseluruhan_excel
from Pengujian.GetAverageAll import rekap_avg_semua_sheet

# Contoh pemanggilan:
if __name__ == "__main__":

    # runPengujianAvgLength()
    # generate_keseluruhan_excel()
    # rekap_avg_semua_sheet()
    # sys.exit()

    timesArr = []

    # for i in range(1):

    mapChoice = 14

    if mapChoice < 1:
        nameMap = "Map"
    else:
        nameMap = f"Map_{mapChoice}"
    map = Z_GetMap.load_grid(path=f"Map/JSON/{nameMap}.json", s=True)

    # map = cv2.imread('Map/Foto/WIN_20250806_03_22_35_Pro.jpg')
    # map = cv2.cvtColor(map, cv2.COLOR_BGR2GRAY)
    # start = ((70*20, 20*20), 0)
    # goal = ((30*20, 20*20), 0)
    # map = Prep(map, start, goal, 10, scale=20)
    # start, goal = PrepCoord(start, goal)

    matrix = map.copy()
    # map = Z_GetMap.upscale(map, 64)
    start = (0, 0)
    goal = (map.shape[1]-1, map.shape[0]-1)

    map = map.astype(np.uint8)

    np.place(matrix, matrix == 1, 255)
    np.place(map, map == 2, 0)
    np.place(map, map == 3, 0)
    tempTimes = []
    tempPaths = []
    tempOpens = []
    tempCloses = []
    tempTurns = []
    tempLengths = []
    for i in range(1):
        (path, times), openlist, closelist = Algoritm(
            matrix, start, goal, 2,
            # JPS=True,
            # BRC=True,
            PPO=True,
            # GLF=True,
            # TPF=True,
            # BDS=True,
            show=True,
        speed=100,
        )

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

    # except Exception as e:
    #     print(f"[!] Error di iterasi : {e}")

    print(f"Rate : {np.mean(tempTimes)}")

    # Munculkan dan simpan map
    if path:
        np.place(map, map == 255, 1)
        Z_GetMap.show(map, window_size=720, name=nameMap, path=path, openlist=openlist, closelist=closelist)
    else:
        np.place(map, map == 255, 1)
        Z_GetMap.show(map, window_size=720, name=nameMap)