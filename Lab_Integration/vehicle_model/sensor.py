import lcm
import select
from exlcm import heartbeat_message
from exlcm import sensor_message

lc = lcm.LCM()
sensor_message = sensor_message()

global last_timestamp
global curr_timestamp
global isMoving

last_timestamp = curr_timestamp = 0
isMoving = False

def update_sensor_message(shouldBrake):
    print("Publish on SENSOR channel")
    sensor_message.timestamp =  last_timestamp
    sensor_message.detected_obstacle = shouldBrake
    lc.publish("SENSOR", sensor_message.encode())

    

def heartbeat_handler(channel, data):
    message = heartbeat_message.decode(data)
    global curr_timestamp
    global isMoving
    curr_timestamp = message.timestamp
    isMoving = message.isMoving


lc = lcm.LCM()
subscription = lc.subscribe("HEARTBEAT", heartbeat_handler)

try:
    while True:
        timeout = .001
        rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
        if rfds:
            lc.handle()        
        if(curr_timestamp > last_timestamp):
            print("Updating timestamp")
            print("current %d " %curr_timestamp)
            print("last %d " %last_timestamp)
            print("ismoving \ %s \ " %str(isMoving) )
            last_timestamp = curr_timestamp
            # The following part should be replaced by the opencv module which detects the obstacle 
            #to send the sensor_message to brake.
            if(last_timestamp > 7000 and isMoving == True):
                print("Providing braking signal")
                update_sensor_message(True) 
 
except KeyboardInterrupt:
    pass