from Utils import *

def method(map, start, goal, hchoice=2, JPS=False, BDS=False, GLF=False, BRC=False , TPF=False, PPO=False, show=False, speed=300):

    if JPS:
        if BDS:
            return JPS_Optimize.methodBds(matrix=map, start=start, goal=goal, hchoice=hchoice, TPF=TPF, BRC=BRC , GLF=GLF, PPO=PPO, show=show, speed=speed)
        else:
            return JPS_Optimize.method(matrix=map, start=start, goal=goal, hchoice=hchoice, TPF=TPF, BRC=BRC , GLF=GLF, PPO=PPO, show=show, speed=speed)
    else:
        if BDS:
            return Astar_Optimize.methodBds(map=map, start=start, goal=goal, hchoice=hchoice, TPF=TPF, BRC=BRC , GLF=GLF, PPO=PPO, show=show, speed=speed)
        else:
            return Astar_Optimize.method(map=map, start=start, goal=goal, hchoice=hchoice, TPF=TPF, BRC=BRC , GLF=GLF, PPO=PPO, show=show, speed=speed)