import lcm
import select
from exlcm import heartbeat_message
from exlcm import sensor_message
from heart_beat import heartbeat_init
import time
import sys

f1=open("SensorLogFile.csv", 'w')
f1.write("Logfile of sensor data \n")
f1.write("Received time,Local time \n")


lc = lcm.LCM()

print(sys.argv)
global  mode
global botUID
mode = int(sys.argv[1])
botUID = int(sys.argv[2])
heartbeat_message = heartbeat_message()
heartbeat_thread = heartbeat_init(mode, botUID)
heartbeat_thread.deamon = True
heartbeat_thread.start()

#timestamp logging of data from the head
#this is used to find the jitter in time for different number of active bots
#this logging is only done by one bot which has UID=2
if(mode == 2 and botUID == 2):
    f2 = open("HeartbeatLogFile.csv", 'w')
    f2.write("Logfile of heartbeat data \n")
    f2.write("Received time,Local time \n")

def sensor_handler(channel, data):
    global mode
    global botUID
    if(mode == 1 or mode == 0):
        sensor_msg = sensor_message.decode(data)
        print("Received message on  \ %s \ " %channel)
        print("Timestamp \ %s \ " %str(sensor_msg.timestamp))
        writeString = str(sensor_msg.timestamp) + ',' + str(int(time.time()*1000)) + '\n'
        f1.write(writeString)
        if(sensor_msg.detected_obstacle == True):
            print("Obstacle \n")
            heartbeat_thread.obstacle = True
        else :
            print("No obstacle \n")
            heartbeat_thread.obstacle = False
        
        #print(" ")

def heartbeat_handler(channel, data):
    global mode
    global botUID
    heartbeat_message_rcvd = heartbeat_message.decode(data)
    #print("Mode \ %s\ " %str(mode))
    #print("BotUID \ %s\ " %str(botUID))
    #print("Received mode \%s \ " %str(heartbeat_message_rcvd.mode))
    #print("Received obstacle \%s\ " %str(heartbeat_message_rcvd.apply_brakes))
    if(mode == 2):
        if(heartbeat_message_rcvd.mode == 1 and botUID == 2):
            print("Received heartbeat data from head \n")
            writeString = str(heartbeat_message_rcvd.timestamp) + ',' + str(int(time.time()*1000)) + '\n'
            f2.write(writeString)
        if(heartbeat_message_rcvd.apply_brakes ==  True):
            heartbeat_thread.obstacle = True
        else:
            heartbeat_thread.obsatcle = False
            

subscription = lc.subscribe("SENSOR", sensor_handler)
subscription = lc.subscribe("HEARTBEAT", heartbeat_handler)

try:
    while True:
        lc.handle()
except KeyboardInterrupt:
    f1.close()
    if(mode == 2 and botUID == 2):
        f2.close()
    pass