from djitellopy import tello
#import KeypressModule as kp
import keyboard as kb
import time
import cv2
#kp.init()
drone = tello.Tello()
drone.connect()
drone.streamon()
time.sleep(2)
print(drone.get_battery())

# def getKeyPressInput():
#     lr, fb, ud, yv = 0, 0, 0, 0
#     speed = 50
#
#     if kp.getKey("LEFT"): lr = -speed
#     elif kp.getKey("RIGHT"): lr = speed
#
#     if kp.getKey("UP"): fb = speed
#     elif kp.getKey("DOWN"): fb = -speed
#
#     if kp.getKey("w"): ud= speed
#     elif kp.getKey("s"): ud = -speed
#t
#     if kp.getKey("a"): yv = speed
#     elif kp.getKey("d"): yv = -speed
#
#     if kp.getKey("q"): drone.land()
#     elif kp.getKey("e"): drone.takeoff()
#
#     return [lr, fb, ud, yv]

def getKeyBoardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 100

    if kb.is_pressed("LEFT"):
        lr = -speed
        time.sleep(0.05)
    elif kb.is_pressed("RIGHT"):
        lr = speed
        time.sleep(0.05)
    if kb.is_pressed("UP"):
        fb = speed
        time.sleep(0.05)
    elif kb.is_pressed("DOWN"):
        fb = -speed
        time.sleep(0.05)

    if kb.is_pressed("w"):
        ud= speed
        time.sleep(0.05)
    elif kb.is_pressed("s"):
        ud = -speed
        time.sleep(0.05)

    if kb.is_pressed("d"):
        yv = speed
        time.sleep(0.05)
    elif kb.is_pressed("a"):
        yv = -speed
        time.sleep(0.05)

    if kb.is_pressed("l"): drone.land()
    elif kb.is_pressed("t"): drone.takeoff()

    return [lr, fb, ud, yv]

while True:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    vals = getKeyBoardInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    cv2.waitKey(1)
