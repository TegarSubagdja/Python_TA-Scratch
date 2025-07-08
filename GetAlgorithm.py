from Utils import *

def method(map, start, goal, hchoice=2, JPS=False, BDS=False, GLF=False, BRC=False , TPF=False, PPO=False, show=False, speed=10):
    if JPS:
        if BDS:
            # print(f"jps dengan bidirectional")
            return jbds.methodBds(map, start, goal, hchoice, GLF, BRC , TPF, PPO, show, speed)
        else:
            # print(f"jps")
            return jps_full.method(map, start, goal, hchoice, GLF, BRC , TPF, PPO, show, speed)
    else:
        if BDS:
            # print(f"Astar Bidirectionnal")
            return bds.method(map, start, goal, hchoice, GLF, BRC , TPF, PPO, show, speed)
        else:
            # print(f"Astar")
            return astar_full.method(map, start, goal, hchoice, GLF, BRC , TPF, PPO, show, speed)