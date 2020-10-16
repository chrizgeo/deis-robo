import lcm
import select
from exlcm import heartbeat_message
from exlcm import sensor_message
from heart_beat import heartbeat_init

lc = lcm.LCM()
heartbeat_message = heartbeat_message()
heartbeat_thread = heartbeat_init()
heartbeat_thread.deamon = True
heartbeat_thread.start()

def sensor_handler(channel, data):
    sensor_msg = sensor_message.decode(data)
    print("Received message on  \ %s \ " %channel)
    print("Timestamp \ %s \ " %str(sensor_msg.timestamp))
    if (sensor_msg.detected_obstacle == True):
        print("Obstacle detected")
        heartbeat_thread.obstacle = True
    print(" ")

subscription = lc.subscribe("SENSOR", sensor_handler)

try:
    while True:
        timeout = .001
        rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
        if rfds:
            lc.handle()
except KeyboardInterrupt:
    pass