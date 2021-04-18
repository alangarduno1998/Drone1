from djitellopy import tello
import cv2
import numpy as np
import matplotlib.pyplot as plt
import KeypressModule as kp
kp.init()

frameWidth = 480
frameHeight = 360



#drone = tello.Tello()
#drone.connect()
#print(drone.get_battery())
#drone.streamon()




def empty(a):
    pass

def ColorPicker(img):
    cv2.namedWindow("HSV")
    cv2.resizeWindow("HSV", 640, 240)
    cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
    cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
    cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
    cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
    cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
    cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)
    while True:
        img = cv2.resize(img, (480, 360))
        imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h_min = cv2.getTrackbarPos("HUE Min", "HSV")
        h_max = cv2.getTrackbarPos("HUE Max", "HSV")
        s_min = cv2.getTrackbarPos("SAT Min", "HSV")
        s_max = cv2.getTrackbarPos("SAT Max", "HSV")
        v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
        v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(imgHsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)
        print(f'[{h_min}, {s_min}, {v_min}, {h_max}, {s_max}, {v_max}]')
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        hStack = np.hstack([img, mask, result])
        cv2.imshow('PP STACK', hStack)
        if kp.getKey("q"):
            break
    return hStack


while True:

    #img = drone.get_frame_read().frame

    #_,img = cap.read()
    img = cv2.imread(r"C:\Users\alang\PycharmProjects\Drone1\Resources\Images\*.jpg")
    img = ColorPicker(img)
    cv2.imshow("First Balloon",img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
    cap.release()
    cv2.destroyAllWindows()
