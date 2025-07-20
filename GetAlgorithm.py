from Utils import *

def method(map, start, goal, hchoice=2, JPS=False, BDS=False, GLF=False, BRC=False , TPF=False, PPO=False, EL=False, show=False, speed=300):

    aktif_flags = []
    if JPS: aktif_flags.append("JPS")
    if BDS: aktif_flags.append("BDS")
    if GLF: aktif_flags.append("GL")
    if BRC: aktif_flags.append("BRC")
    if TPF: aktif_flags.append("TPF")
    if PPO: aktif_flags.append("PPO")
    if EL and BDS: aktif_flags.append("EL")
    method_name = "-".join(aktif_flags) if aktif_flags else "A*"
    print(method_name)

    if JPS:
        if BDS:
            print(f"JPS Bidirectional")
            return JPS_Optimize.methodBds(matrix=map, start=start, goal=goal, hchoice=hchoice, TPF=TPF, BRC=BRC , GLF=GLF, PPO=PPO, EL=EL, show=show, speed=speed)
        else:
            # print(f"jps")
            return JPS_Optimize.method(matrix=map, start=start, goal=goal, hchoice=hchoice, TPF=TPF, BRC=BRC , GLF=GLF, PPO=PPO, show=show, speed=speed)
    else:
        if BDS:
            print(f"Astar Bidirectionnal")
            return Astar_Optimize.methodBds(map=map, start=start, goal=goal, hchoice=hchoice, TPF=TPF, BRC=BRC , GLF=GLF, PPO=PPO, EL=EL, show=show, speed=speed)
        else:
            # print(f"Astar")
            return Astar_Optimize.method(map=map, start=start, goal=goal, hchoice=hchoice, TPF=TPF, BRC=BRC , GLF=GLF, PPO=PPO, show=show, speed=speed)