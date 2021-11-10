import os,sys
import random
# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


#生成.rou.xml文件
def generate_routefile():
    step_number = 1000


#     with open("junction.rou.xml","w") as route:
#         route.write("""
# <routes>
#     <vType id ="myType" vClass ="taxi" accel ="0.8" decel ="4.5" sigma = "0.5" length = "5"
#     maxSpeed = "50" callFollowModel = "IDM" actionStepLength = "1" laneChangeModel = "SL2015"/>)


#     <route id="route1" edges = "3i 1o"/>
#     <route id="route2" edges = "4i 1o"/>
#     <routeDistribution id = "routedist">
#         <route id = "r1" color = "1,1,0" edges = "1i 2o" probability = "0.5"/>
#         <route id = "r2" color = "1,0,1" edges = "1i 3o" probability = "0.5"/>
#     </routeDistribution>


#     <flow id="carflow1" type="myType" begin="0" end="100" period = "10" route= "route1" color = "0,1,0"/>
#     <flow id="carflow2" type="myType" begin="10" end="20" number="10" route= "route2"/>
#     <flow id="carflow3" type="myType" begin="15" end="40" number="15" route= "routedist"/>
# </routes>""")

    random.seed(42)
    #四条路径每个step生成一辆车的概率
    p1 = 1. / 3
    p2 = 1. / 5
    p3 = 1. / 3
    p4 = 1. / 5

    with open("junction.rou.xml","w") as route:
        route.write("""
<routes>
    <vType id ="myType" vClass ="taxi" accel ="0.8" decel ="4.5" sigma = "0.5" length = "5"
    maxSpeed = "50" callFollowModel = "IDM" actionStepLength = "1" laneChangeModel = "SL2015"/>)


    <route id="route1" edges = "5i 1i 3o 7o"/>
    <route id="route2" edges = "6i 2i 4o 8o"/>
    <route id="route3" edges = "7i 3i 1o 5o"/>
    <route id="route4" edges = "8i 4i 2o 6o"/>
        """)
        vehicle_number = 0
        for i in range(step_number):
            if random.uniform(0,1) < p1:
                route.write("""
    <vehicle id = "1_%i" type = "myType" guiShape = "passenger" route = "route1" depart = "%i"  />"""
                    %(vehicle_number, i))
                vehicle_number +=1

            if random.uniform(0,1) < p2:
                route.write("""
    <vehicle id = "2_%i" type = "myType" guiShape = "passenger" route = "route2" depart = "%i"  />"""
                    %(vehicle_number, i))
                vehicle_number +=1

            if random.uniform(0,1) < p3:
                route.write("""
    <vehicle id = "3_%i" type = "myType" guiShape = "passenger" route = "route3" depart = "%i"  />"""
                    %(vehicle_number, i))
                vehicle_number +=1

            if random.uniform(0,1) < p4:
                route.write("""
    <vehicle id = "4_%i" type = "myType" guiShape = "passenger" route = "route4" depart = "%i"  />"""
                    %(vehicle_number, i))
                vehicle_number +=1
        route.write("""
</routes>""")



#生成ｓｕｍｏｃｆｇ文件
# with open("junction.sumocfg.xml","w") as cfg:
#     cfg.write("""
# <?xml version="1.0" encoding="UTF-8"?>

# <configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">

#     <input>
#         <net-file value="junction.net.xml"/>
#         <route-files value="junction.rou.xml"/>
#     </input>

#     <time>
#         <begin value="0"/>
#         <end value="10000"/>
#     </time>
#     <time-to-teleport value="-1"/>  
#     <!--  禁止自动删除在十字路口前等待时间过长的车辆 -->

# </configuration>

#     """)


import traci
import traci.constants as tc
from sumolib import checkBinary

generate_routefile()


sumoBinary = checkBinary("sumo-gui")
sumoCmd = [sumoBinary, "-c", "junction.sumocfg"]
traci.start(sumoCmd)

#traci.trafficlight.setRedYellowGreenState("J1", "rrrGGgrrrGGg")
flag = "rrrGGgrrrGGg"
a = 0
while traci.simulation.getMinExpectedNumber() > 0:
    print(" ")
    traci.simulationStep()
    traci.trafficlight.setRedYellowGreenState("J1", flag)
    # vehicleIDList = traci.vehicle.getIDList()
    # print(vehicleIDList)

    #上一个仿真步中给定边的停车数量
    edge1_vehicleNumber = traci.edge.getLastStepVehicleNumber("1i")
    edge2_vehicleNumber = traci.edge.getLastStepVehicleNumber("2i")
    edge3_vehicleNumber = traci.edge.getLastStepVehicleNumber("3i")
    edge4_vehicleNumber = traci.edge.getLastStepVehicleNumber("4i")
    

    if traci.trafficlight.getPhaseDuration("J1") < 0:
        print("shijain:",traci.trafficlight.getPhaseDuration("J1"))
        a+=1
        print("traci.trafficlight.getPhaseDuration(J1) < 30",  a)
        if edge1_vehicleNumber + edge3_vehicleNumber == 0:
            flag = "rrrGGgrrrGGg"
            print("case1","rrrGGgrrrGGg")
            continue
        if edge2_vehicleNumber + edge4_vehicleNumber == 0:
            flag = "GGgrrrGGgrrr"
            print("case2","GGgrrrGGgrrr")
            continue
        print("     case3",flag)
        continue
    

    if edge1_vehicleNumber + edge3_vehicleNumber >=10:
        flag = "GGgrrrGGgrrr"
        print("case4","GGgrrrGGgrrr")
        continue
    
    if edge2_vehicleNumber + edge4_vehicleNumber >=10:
        flag = "rrrGGgrrrGGg"
        print("case5","rrrGGgrrrGGg")
        continue

    
    
    
    # print(edge1_vehicleNumber)
    # print(edge2_vehicleNumber)
    # print(edge3_vehicleNumber)
    # print(edge4_vehicleNumber)

    

traci.close()
