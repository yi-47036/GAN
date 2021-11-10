import os, sys
import random
# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")



#生成rou.xml文件，定义路由
def generateRoutes():

    with open("lane.rou.xml","w") as rouFile:
        rouFile.write("""
<routes>
    <vType id ="myType" vClass ="taxi" accel ="0.8" decel ="4.5" sigma = "0.5" length = "5"
    maxSpeed = "10" callFollowModel = "IDM" actionStepLength = "1" laneChangeModel = "LC2013" />)
    <route id = "r1" edges = "E1 E2"  />
    <vehicle id = "veh1" type = "myType" maxSpeed = "10" departSpeed = "5" arrivalSpeed = "5" depart = "0"  route = "r1" departLane = "0" departPos = "0" 
        arrivalLane = "0" arrivalPos ="max" color = "1,0,0"  />
    <vehicle id = "veh4" type = "myType" departSpeed = "20"  depart = "3"  route = "r1" departLane = "0" departPos = "0" 
        arrivalLane = "0" arrivalPos ="max" color = "0,1,0"  />
    <vehicle id = "veh3" type = "myType" departSpeed = "10"  depart = "5"  route = "r1" departLane = "0" departPos = "0" 
        arrivalLane = "0" arrivalPos ="max" color = "0,0,1"  />
</routes>
        """)

generateRoutes()

def ChangeLane(vehicle1, vehicle2):
    #vehicle1为前车,2为后车
    v1 = traci.vehicle.getSpeed(vehicle1)
    y1 = traci.vehicle.getPosition(vehicle1)[0]
    v2 = traci.vehicle.getSpeed(vehicle2)
    y2 = traci.vehicle.getPosition(vehicle2)[0]
    #if y1 > y2 and v1 < v2 and (y1 - y2)/(v2 - v1) < delta_time:
        


    # print(v1, v2)
    # print(p1,p2)
    # print("")


import traci
from sumolib import checkBinary
sumoBinary = checkBinary("sumo")
traci.start([sumoBinary,"-c","lane.sumocfg"])

time = 0
delta_time = 10
vehicleValueDict = {}
while traci.simulation.getMinExpectedNumber() > 0:
    time += 1
    #print(time)
    traci.simulationStep()

    #输出边上现有车辆的id与速度
    vehicleIDs = traci.edge.getLastStepVehicleIDs("E1")
    for i in range(len(vehicleIDs)-1,-1,-1):
        id = vehicleIDs[i]
        print("%s_speed = "%(id), traci.vehicle.getSpeed(id))
    #print(traci.edge.getLastStepVehicleNumber("E1"))


    # vehicleID = traci.inductionloop.getLastStepVehicleIDs("1")
    # if vehicleID:

    #     r = random.randint(0,10)
    #     vehicleValueDict.update({vehicleID[0]: r})
    #     #测试字典是否添加
    #     print(vehicleValueDict)
    #     print(vehicleValueDict['veh1'])
    # vehicleIDlist = traci.edge.getLastStepVehicleIDs("E1")

    #print(vehicleIDlist)
    # for i in range(len(vehicleIDlist)-1):
    #     ChangeLane(vehicleIDlist[i+1],vehicleIDlist[i])
    #输出边上现有车辆的id与速度
    # vehicleIDs = traci.edge.getLastStepVehicleIDs("E1")
    # for i in range(len(vehicleIDs)-1,-1,-1):
    #     id = vehicleIDs[i]
    #     print("%s_speed = "%(id), traci.vehicle.getSpeed(id))
    
traci.close()

