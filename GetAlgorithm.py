from Utils import *

def method(map, start, goal, hchoice=2, jps=False, bd=False, glm=False, brm=False , tpm=False, ppom=False, show=False, speed=10):
    if jps:
        if bd:
            # print(f"jps dengan bidirectional")
            return jps_full.methodBds(map, start, goal, hchoice, glm, brm , tpm, ppom, show, speed)
        else:
            # print(f"jps")
            return jps_full.method(map, start, goal, hchoice, glm, brm , tpm, ppom, show, speed)
    else:
        if bd:
            # print(f"Astar Bidirectionnal")
            return bds.method(map, start, goal, hchoice, glm, brm , tpm, ppom, show, speed)
        else:
            # print(f"Astar")
            return astar_full.method(map, start, goal, hchoice, glm, brm , tpm, ppom, show, speed)