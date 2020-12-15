# Class definitions for the sparkie robot class
# Christo George
# christogeorge@live.in
# Dec 2020

#This is solely for the purpose 
#so any action that alters the values are required to update on a single object.
class sparkieRobot: 
    
    # wrapper class to define and set robot status and properties 
    # all updates regarding the robot status and position should be updated on the sparkieRobot object.
    # init with the x and y positions of the robot. 
    def __init__(self, x,y, z=0, platoonID=0, robotID=0, robot_type=0, laneID=0, pos_in_platoon=0, theta=0, speed=0):
        self.platoonID = platoonID
        self.robotID = robotID
        self.robot_type = robot_type
        self.laneID = laneID
        self.pos_in_platoon = pos_in_platoon        
        self.position = (x,y,z,theta)
        self.speed = speed

    # setter functions
    def setPlatoon(self, platoonID):
        self.platoonID = platoonID

    def setID(self, robotID):
        self.robotID = robotID
    
    def setType(self, robot_type):
        self.robot_type = robot_type
    
    def setLane(self, laneID):
        self.laneID = laneID
    
    def setRole(self, pos_in_platoon):
        self.pos_in_platoon = pos_in_platoon
    
    #postion should be a tuple with four values x, y, z, theta
    def setPosition(self, position, z=0, theta=0):
        self.position = (x,y,z, theta)

    def setSpeed(self, sspeed):
        self.speed = speed




