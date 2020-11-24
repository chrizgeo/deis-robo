import lcm
from threading import Thread
from exlcm import heartbeat_message
import time

lc = lcm.LCM()

class heartbeat_init(Thread):
    def __init__(self, mode, botUID):
        Thread.__init__(self)
        self.last_timestamp = time.time()
        self.msg = heartbeat_message()
        self.msg.timestamp = self.last_timestamp
        self.msg.mode = mode
        self.msg.botUID = botUID
        self.msg.isMoving = True
        self.msg.apply_brakes = False
        self.obstacle = False

    def run(self):
        while(True):
            if(self.obstacle == True) :
                self.msg.apply_brakes = True
                self.msg.isMoving = False
            else :
                self.msg.apply_brakes = False
                self.msg.isMoving = True
            
            if((time.time()*1000 - self.last_timestamp)  > 1 ):
                self.msg.timestamp = int(time.time()*1000)
                lc.publish("HEARTBEAT", self.msg.encode())
                self.last_timestamp = self.msg.timestamp