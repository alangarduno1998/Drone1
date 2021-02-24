from djitellopy import tello
import KeypressModule as kp
import numpy as np
import cv2
from time import sleep
import math
#### Parameters ####
fspeed = 117/10 # Forward speed in cm/s
aspeed = 360/10 # Angular speed Degrees/s
interval = 0.25
dInterval = fspeed*interval #distance
aInterval = aspeed*interval
###########################################
x, y, yaw, a= 500, 500, 0, 0
kp.init()

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

points = []
def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    d =0
    global x, y, yaw, a
    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180

    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("w"): ud= speed

    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"):
        yv = speed
        yaw += aInterval


    elif kp.getKey("d"):
        yv = -speed
        yaw -= aInterval


    if kp.getKey("q"): drone.land(); sleep(3)
    elif kp.getKey("e"): drone.takeoff()

    sleep(interval)
    a += yaw
    x += int(d*math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]

def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)


while True:
    vals = getKeyboardInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)

    img = np.zeros((1000, 1000, 3), np.uint8)
    points.append((vals[4], vals[5]))
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)