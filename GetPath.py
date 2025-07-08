from Utils import *

def getPath(image, scale=20, idStart=1, idGoal=7, detector=False):

    pos, corners = Position(image, idStart, idGoal, detector)

    if not pos:
        return 0, 0

    map, pos = Preprocessing(image, pos, scale, corners)

    (path, time)= jps.method(map, pos['start'], pos['goal'], 2)

    if not path:
        return 0, 0

    # Mengubah setiap koordinat ke ukuran semula
    path = [(y * scale, x * scale) for y, x in path]
    path[0] = pos['start'][::-1]
    path[-1] = pos['goal'][::-1]

    return path