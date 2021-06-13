from djitellopy import tello
import numpy as np
import cv2, time, os
import cv2.aruco as aruco

def initializeDrone(drone):
    drone.connect()
    drone.streamon()
    print(drone.get_battery())
    drone.takeoff()
    time.sleep(4)
    drone.send_rc_control(0, 0, 20, 0)
    time.sleep(2)
    return drone
def loadarucoparam(markersize=4, totalmarkers=50):
    key = getattr(aruco, f'DICT_{markersize}X{markersize}_{totalmarkers}')
    # key = getattr(aruco, f'DICT_ARUCO_ORIGINAL')
    aruco_dict = aruco.Dictionary_get(key)
    arucoparameters = aruco.DetectorParameters_create()
    return arucoparameters, aruco_dict
def loadarucoimages(path):
    objectlist = os.listdir(path)
    objdicts = {}
    for imgpath in objectlist:
        key = int(os.path.splitext(imgpath)[0])
        frameembed = cv2.imread(f'{path}/{imgpath}')
        objdicts[key] = frameembed
    return objdicts
def findarucofeatures(frame, arucoparameters, aruco_dict, draw=True):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedimgpoints = aruco.detectMarkers(gray, aruco_dict, parameters = arucoparameters)
    if draw:
        display = aruco.drawDetectedMarkers(frame, corners, ids)
    return [corners, ids]
def findaruco(cs, id, frame, frameembed, AListC, AListA):
    cx, cy = (cs[0][1][0] + cs[0][3][0]) // 2, (cs[0][1][1] + cs[0][3][1]) // 2
    area = round(pow(cv2.contourArea(cs), 0.5))
    # cv2.circle(frame, (int(cx), int(cy)), 5, (0, 255, 0), cv2.FILLED)
    AListC.append((cx, cy)), AListA.append(area)
    if len(AListA) != 0:
        i = AListA.index(max(AListA))
        return frame, AListC[i], AListA[i]
    else:
        return frame, [0,0], 0
def FindFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade.xml ")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.2,8)
    myFaceListC = []
    myFaceListArea = []
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y +h), (0, 0, 255), 2)
        cx = x + w//2
        cy = y + h//2
        area = w * h
        cv2.circle(img, (int(cx), int(cy)), 5, (0, 255,0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]
def FaceTrack(drone, info, w,h, pid, perror, fbRange):
    area = info[1]
    x,y = info[0]
    fb = 0
    error = [x - w//2, h//2-y, fbRange[0]-area]
    speed = [pid[0]*error[0] +pid[1]*(error[0]-perror[0]), pid[3]*error[1] +pid[4]*(error[1]-perror[1]), pid[6]*error[2] +pid[7]*(error[2]-perror[2])]
    speed[0] = int(np.clip(speed[0], -100, 100))
    speed[1] = int(np.clip(speed[1],-100,100))
    speed[2] = int(np.clip(speed[2], -20, 20))
    if area == 0:
        speed[2] = 0
        error[2] = 0
    if x == 0:
        speed[0] = 0
        error[0] = 0
    if y == 0:
        speed[1] = 0
        error[1] = 0
    drone.send_rc_control(0, speed[2], speed[1], speed[0])
    return error


def main(trackface=False, trackaruco=False):
    drone = tello.Tello()
    initializeDrone(drone)
    arucoparameters, aruco_dict=loadarucoparam()
    objdicts = loadarucoimages("Objects")
    w, h = 360, 240
    fbRange = [6200, 6800]
    abRange = [60, 65]
    pid = [0.5, 0.9, 0, 0.7, 0.8, 0, 0.8, 0.8, 0]
    pError = [0, 0, 0]
    while True:
        # -- using face set trackface to True in main()
        frame = drone.get_frame_read().frame
        frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
        if trackface:
            frame, info = FindFace(frame)
            pError = FaceTrack(drone, info, w,h, pid, pError, fbRange)
        # -- using aruco tags set trackaruco to True in main()
        if trackaruco:
            AListA, AListC, info = [], [], [[0, 0], 0]
            arucofound = findarucofeatures(frame, arucoparameters, aruco_dict)
            if len(arucofound[0]) != 0:
                for corners, id in zip(arucofound[0], arucofound[1]):
                    if int(id) in objdicts.keys():
                        frame, info[0], info[1] = findaruco(corners, id, frame, objdicts[int(id)], AListC, AListA)
            pError = FaceTrack(drone, info, w,h, pid, pError, abRange)
        cv2.imshow('Display', frame)
        print("Center", info[0], "Area", info[1])
        if cv2.waitKey(1) & 0xff == 27:
            drone.land()
            break

if __name__ == "__main__":
    main(trackface=False, trackaruco=True)