import lcm
from threading import Thread
from exlcm import heartbeat_message

lc = lcm.LCM()

class heartbeat_init(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.last_timestamp = 0
        self.msg = heartbeat_message()
        self.msg.timestamp = self.last_timestamp
        self.msg.status = 0
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
            
            self.msg.timestamp = self.last_timestamp + 1
            lc.publish("HEARTBEAT", self.msg.encode())
            self.last_timestamp = self.msg.timestamp