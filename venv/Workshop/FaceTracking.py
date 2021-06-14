import cv2
import numpy as np
import time
from djitellopy import tello


def initializedrone():
    drone = tello.Tello()
    drone.connect()
    drone.land()
    time.sleep(2)
    print(drone.get_battery())
    drone.streamon()
    drone.takeoff()
    time.sleep(2)
    drone.send_rc_control(0, 0, 20, 0)
    time.sleep(2.2)
    return drone


def findface(img):
    facecascade = cv2.CascadeClassifier("Resources/haarcascade.xml ")
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = facecascade.detectMultiScale(imggray, 1.2, 8)
    myfacelistc = []
    myfacelistarea = []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (int(cx), int(cy)), 5, (0, 255, 0), cv2.FILLED)
        myfacelistc.append([cx, cy])
        myfacelistarea.append(area)
    if len(myfacelistarea) != 0:
        i = myfacelistarea.index(max(myfacelistarea))  # index of largest value in area list
        return img, [myfacelistc[i], myfacelistarea[i]]
    else:
        return img, [[0, 0], 0]


def facetrack(drone, info, w, h, pid, perror, fbrange):
    area = info[1]
    x, y = info[0]
    error = [x - w // 2, h // 2 - y]
    speed = [pid[0] * error[0] + pid[1] * (error[0] - perror[0]), pid[3] * error[1] + pid[4] * (error[1] - perror[1])]
    speed[0] = int(np.clip(speed[0], -100, 100))
    speed[1] = int(np.clip(speed[1], -100, 100))
    if fbrange[0] < area < fbrange[1]:
        fb = 0
    elif area > fbrange[1]:
        fb = -20
    elif area < fbrange[0] and area != 0:
        fb = 20
    if x == 0:
        speed[0] = 0
        error[0] = 0
    if y == 0:
        speed[1] = 0
        error[1] = 0
    drone.send_rc_control(0, fb, speed[1], speed[0])
    return error


def main():
    drone = initializedrone()
    w, h = 360, 240
    fbrange = [6200, 6800]
    pd = [0.6, 0.7, 0, 0.7, 0.8, 0]
    p_error = [0, 0]
    while True:
        img = drone.get_frame_read().frame
        img = cv2.resize(img, (w, h))
        img, info = findface(img)
        p_error = facetrack(drone, info, w, h, pd, p_error, fbrange)
        cv2.imshow("Output", img)
        print("Center", info[0], "Area", info[1])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break


if __name__ == "__main__":
    main()
