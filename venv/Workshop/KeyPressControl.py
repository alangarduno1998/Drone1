from djitellopy import tello
import KeypressModule as kp
import time
import cv2
kp.init()
drone = tello.Tello()
drone.connect()
drone.streamon()
time.sleep(2)
print(drone.get_battery())

def getKeyPressInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): ud= speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"): yv = speed
    elif kp.getKey("d"): yv = -speed

    if kp.getKey("q"): drone.land()
    elif kp.getKey("e"): drone.takeoff()

    return [lr, fb, ud, yv]

while True:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    vals = getKeyPressInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    cv2.waitKey(1)
