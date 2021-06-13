from djitellopy import tello
import keyboard as kb
import time, cv2
drone = tello.Tello()
drone.connect()
drone.streamon()
time.sleep(2)
print(drone.get_battery())

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
    if kb.is_pressed("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg',img)
        time.sleep(0.3)

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