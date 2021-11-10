import os,sys
import random
# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


#生成.rou.xml文件
def generateRoutes():
    step_number = 30

    random.seed(1111)
    #四条路径每个step生成一辆车的概率
    p1 = 0.7
    p2 = 0.7
    p3 = 0.
    p4 = 0.
    p5 = 0.
    p6 = 0.
    p7 = 0.
    p8 = 0.
    #callFollowModel = ""Krauss

    with open("junction.rou.xml","w") as route:
        route.write("""
<routes>
    <vType id ="myType" vClass ="passenger" accel ="0.8" decel ="4.5" sigma = "0.5" length = "5" 
    maxSpeed = "20"  carFollowModel="IDM" laneChangeModel = "SL2015"/>)


    <route id="route1" edges = "1i 3o"/>
    <route id="route2" edges = "2i 4o"/>
    <route id="route3" edges = "3i 1o"/>
    <route id="route4" edges = "4i 2o"/>
    <route id="route5" edges = "1i 2o"/>
    <route id="route6" edges = "2i 3o"/>
    <route id="route7" edges = "3i 4o"/>
    <route id="route8" edges = "4i 1o"/>
        """)
        vehicle_number = 0
        for i in range(step_number):
            if random.uniform(0,1) < p1:
                route.write("""
    <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "0" departLane = "0" departSpeed = "10" route = "route1" depart = "%i" arrivalPos = "5" />"""
                    %(vehicle_number, i))
                vehicle_number +=1
            if random.uniform(0,1) < p2:
                route.write("""
    <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "1" departLane = "1" departSpeed = "10" route = "route5" depart = "%i" arrivalPos = "5" />"""
                    %(vehicle_number, i))
                vehicle_number +=1


            if random.uniform(0,1) < p3:
                route.write("""
    <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "0" departLane = "0" departSpeed = "10" route = "route2" depart = "%i" arrivalPos = "5" />"""
                    %(vehicle_number, i))
                vehicle_number +=1
            if random.uniform(0,1) < p4:
                route.write("""
    <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "1" departLane = "1" departSpeed = "10" route = "route6" depart = "%i" arrivalPos = "5" />"""
                    %(vehicle_number, i))
                vehicle_number +=1


            if random.uniform(0,1) < p5:
                route.write("""
    <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "0" departLane = "0" departSpeed = "10" route = "route3" depart = "%i" arrivalPos = "5" />"""
                    %(vehicle_number, i))
                vehicle_number +=1
            #if random.uniform(0,1) < p6:
            if i == step_number / 2:
                route.write("""
    <vehicle id = "egocar" type = "myType" color = "red" guiShape = "passenger" arrivalLane = "1" departLane = "1" departSpeed = "10" route = "route7" depart = "%i" departPos = "50" arrivalPos = "5" />"""
                    %(i))
                vehicle_number +=1


            if random.uniform(0,1) < p7:
                route.write("""
    <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "0" departLane = "0" departSpeed = "10" route = "route4" depart = "%i" arrivalPos = "5" />"""
                    %(vehicle_number, i))
                vehicle_number +=1
            if random.uniform(0,1) < p8:
                route.write("""
    <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "1" departLane = "1" departSpeed = "10" route = "route8" depart = "%i" arrivalPos = "5" />"""
                    %(vehicle_number, i))
                vehicle_number +=1

        route.write("""
</routes>""")


import traci
import traci.constants as tc
from sumolib import checkBinary

generateRoutes()

#
sumoBinary = checkBinary("sumo-gui")
sumoCmd = [sumoBinary, "-c", "junction.sumocfg", "--step-length", "0.1" , "--time-to-teleport", "-1",\
    "--collision.check-junctions", str(True),"--collision.mingap-factor", "1", "--collision.action", "remove"]
traci.start(sumoCmd)
#traci.vehicletype.setMinGap('myType', 1)

a = 0
while traci.simulation.getMinExpectedNumber() > 0:
    vehicleIDList = traci.vehicle.getIDList()
    for i in range(len(vehicleIDList)): 
    #     # print("step action = ", action_n[i])
        vehicleID = vehicleIDList[i]
    #     # traci.vehicle.setSpeedMode(vehicleID, 0)
        
        # curSpeed = traci.vehicle.getSpeed(vehicleID)
    #     gap = traci.vehicle.getMinGap(vehicleID)
        print('vehicleID = ', vehicleID, '    speed = ',traci.vehicle.getSpeed(vehicleID))
    #     tarSpeed = 20
    #     traci.vehicle.setSpeed(vehicleID, tarSpeed)
    #     #traci.vehicle.slowDown(vehicleID, tarSpeed, 1)

    a +=1
    #n = traci.simulation.getCollidingVehiclesNumber()
    # n = traci.simulation.getStartingTeleportNumber()
    # l = traci.simulation.getStartingTeleportIDList()
    #c = traci.simulation.getCollisions()
    # print("n = ", n)
    # print("l = ", l)
    print("")
    traci.simulationStep()
    
    
    #c = traci.simulation.getCollisions()
    
    # print("c = ", c)

    print("step = ",a)

traci.close()
