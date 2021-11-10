import os, sys
# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import random
import numpy as np
import traci
from sumolib import checkBinary



class Env():
    def __init__(self, ):
        self.generateRoutes()
        self.n = 8  #n为场景中智能体数量，在智能体数量固定的情况下n是不变的
        
    def lane(self, edgeID):
        laneIDList = []
        for i in range(self.lane_Num):
            laneIDList.append(edgeID + '_' + '%i'%i)
        return laneIDList

    def reset(self, sumo):
        
        #启动ｓｕｍｏ，并返回一个全为０的状态矩阵，矩阵的维数根据状态设置　来确定
        sumoBinary = checkBinary(sumo)
        #traci.start([sumoBinary,"-c","junction.sumocfg"])
        sumoCmd = [sumoBinary, "-c", "junction.sumocfg", "--step-length", "0.1" ,"--time-to-teleport", str(-1), \
    "--collision.check-junctions", str(True),"--collision.mingap-factor", "1", "--collision.action", "teleport"]
        traci.start(sumoCmd)
        # return np.zeros((self.lane_Num,self.cell_Num))
        return self.getState()
    
    def step(self,action_n):
        vehicleIDList = traci.vehicle.getIDList()
        for vehicleID in vehicleIDList: 
            # print("step action = ", action_n[i])
            traci.vehicle.setSpeedMode(vehicleID, 0) #设置速度模式
            curSpeed = traci.vehicle.getSpeed(vehicleID)
            tarSpeed = curSpeed + 0.5 * action_n[int(vehicleID)]
            traci.vehicle.setSpeed(vehicleID, tarSpeed)
            #traci.vehicle.slowDown(vehicleID, tarSpeed, 1)
        
        n_s = self.getState()
        r = self.getReward(action_n) #放在simulation前面，否则会延迟一步
        done = self.getDone()

        traci.simulationStep()
        return n_s, r, done
               
    def getState(self):
        #获取场景中所有车辆的状态信息并返回 
        vehicleIDList = traci.vehicle.getIDList()
        #totalState = []
        totalState = np.zeros([self.n , 3])
        #print("vehicleIDList = ", vehicleIDList)
        for vehicleID in vehicleIDList:
            x, y = traci.vehicle.getPosition(vehicleID)  #ｘ代表车前保险杠中心点位置
            speed = traci.vehicle.getSpeed(vehicleID) 
            vehiclState = np.array([round(x, 3), round(y, 3), round(speed, 3)])
            #totalState.append(vehiclState)
            #print("int(vehicleID) = ", int(vehicleID))
            totalState[int(vehicleID)] = vehiclState
        return totalState

    def getReward(self, action_n):  #重新设计
        vehicleIDList = traci.vehicle.getIDList()
        l = traci.simulation.getStartingTeleportIDList()
        #print("l =", l)
        r = np.ones(self.n)
        # for vehicleID in vehicleIDList:
            # if vehicleID in l:
            #     r[int(vehicleID)] = -100
            # else :
            #     r[int(vehicleID)] = action_n[int(vehicleID)]
        r = r * (sum(action_n) - len(l) * 1000)

        r = [round(i, 3) for i in r]
        return r
    
    
    def getDone(self):
        temp = traci.simulation.getMinExpectedNumber()
        if temp > 0:
            done = False
        else:
            done = True
        
        return done


    #生成.rou.xml文件
    def generateRoutes(self):
        step_number = 1

        random.seed(42)
        #四条路径每个step生成一辆车的概率
        p1 = 1. 
        p2 = 1.
        p3 = 1. 
        p4 = 1. 
        #callFollowModel = "IDM"

        with open("junction.rou.xml","w") as route:
            route.write("""
    <routes>
        <vType id ="myType" vClass ="passenger" accel ="0.8" decel ="4.5" sigma = "0.5" length = "5"
        maxSpeed = "50"  laneChangeModel = "SL2015"/>)


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
        <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "0" departLane = "0" departSpeed = "10" route = "route1" depart = "%i"  />"""
                        %(vehicle_number, i))
                    vehicle_number +=1
                    route.write("""
        <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "1" departLane = "1" departSpeed = "10" route = "route5" depart = "%i"  />"""
                        %(vehicle_number, i))
                    vehicle_number +=1


                if random.uniform(0,1) < p2:
                    route.write("""
        <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "0" departLane = "0" departSpeed = "10" route = "route2" depart = "%i"  />"""
                        %(vehicle_number, i))
                    vehicle_number +=1
                    route.write("""
        <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "1" departLane = "1" departSpeed = "10" route = "route6" depart = "%i"  />"""
                        %(vehicle_number, i))
                    vehicle_number +=1


                if random.uniform(0,1) < p3:
                    route.write("""
        <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "0" departLane = "0" departSpeed = "10" route = "route3" depart = "%i"  />"""
                        %(vehicle_number, i))
                    vehicle_number +=1
                    route.write("""
        <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "1" departLane = "1" departSpeed = "10" route = "route7" depart = "%i"  />"""
                        %(vehicle_number, i))
                    vehicle_number +=1


                if random.uniform(0,1) < p4:
                    route.write("""
        <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "0" departLane = "0" departSpeed = "10" route = "route4" depart = "%i"  />"""
                        %(vehicle_number, i))
                    vehicle_number +=1
                if random.uniform(0,1) < p4:
                    route.write("""
        <vehicle id = "%i" type = "myType" guiShape = "passenger" arrivalLane = "1" departLane = "1" departSpeed = "10" route = "route8" depart = "%i"  />"""
                        %(vehicle_number, i))
                    vehicle_number +=1

            route.write("""
    </routes>""")