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

    for i in range(1):

        mapChoice = 8

        if mapChoice < 1:
            nameMap = "Map"
        else:
            nameMap = f"Map_{mapChoice}"

        # Load dan persiapan peta
        map = Z_GetMap.load_grid(path=f"Map/JSON/{nameMap}.json", s=True)
        # map = Z_GetMap.upscale(map, 32)
        matrix = map.copy()

        start = (0, 0)
        goal = (map.shape[0]-1, map.shape[0]-1)

        start = np.where(map == 2)
        goal = np.where(map == 3)
        start = (int(start[0][0]), int(start[1][0]))
        goal = (int(goal[0][0]), int(goal[1][0]))
        print(goal)

        np.place(matrix, matrix == 1, 255)
        # np.place(map, map == 2, 0)
        # np.place(map, map == 3, 0)

        tempTimes = []
        tempPaths = []
        tempOpens = []
        tempCloses = []
        tempTurns = []
        tempLengths = []

        for i in range(1):

            # try:
            (path, times), openlist, closelist = Astar_Animate.methodBds(
                matrix, start, goal, 2,
                # JPS=True,
                # BDS=True,
                BRC=False,
                PPO=False,
                TPF=False,
                GLF=False,
                show=True,
                speed=100,
            )

            timesArr.append(times)
            tempTimes.append(times)
            tempPaths.append(len(path))
            tempLengths.append(path_length(path))
            tempOpens.append(len(openlist))
            tempCloses.append(len(closelist))
            tempTurns.append(len(Turn(path)))

            belokan = len(Turn(path)) if path else None

        print(f"  Map : {nameMap}")
        # print(f"  Size : {sz}")
        # print(f"  Metod Name : {method_name}")
        # print(f"  Path adalah : {path}")
        # print(f"  Waktu Pencarian : {times}")
        # print(f"  Panjang Jalur : {path_length(path)}")
        # print(f"  Jumlah Open Set : {len(openlist)}")
        # print(f"  Jumlah Close Set : {len(closelist)}")
        # print(f"  Jumlah Open + Close di i {i} : {len(openlist) + len(closelist)}")
        # print(f"  Jumlah Belokan : {belokan}")

        # except Exception as e:
        #     print(f"[!] Error di iterasi : {e}")

        print(f"Rate : {np.mean(tempTimes)}")

    # Munculkan dan simpan map
    Z_GetMap.show(map, window_size=512, name=nameMap, path=path, openlist=openlist, closelist=closelist)
    # Z_GetMap.show(map, window_size=512, name=nameMap)


