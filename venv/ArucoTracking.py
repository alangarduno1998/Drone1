from djitellopy import tello
import numpy as np
import cv2, os, time
import cv2.aruco as aruco
def initializeDrone(drone):
    drone.connect()
    drone.streamon()
    print(drone.get_battery())
    drone.takeoff()
    time.sleep(4)
    drone.send_rc_control(0,0,20,0)
    time.sleep(2)
def loadarucoparam(markersize = 4, totalmarkers =50):
    key = getattr(aruco, f'DICT_{markersize}X{markersize}_{totalmarkers}')
    #key = getattr(aruco, f'DICT_ARUCO_ORIGINAL')
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
    area = round(cv2.contourArea(cs) ** 0.5)
    AListC.append((cx, cy)), AListA.append(area)
    if len(AListA) != 0:
        i = AListA.index(max(AListA))
        return frame, AListC[i], AListA[i]
    else:
        return frame, [0,0], 0
def arucotrack(drone, info, w,h, pd, perror, abRange):
    area = info[1]
    x,y = info[0]
    error = (x - w//2, h//2-y, abRange[0]-area)
    i=[perror + 0.4*error[0]]
    speed = (pd[0]*error[0] +pd[1]*(error[0]-perror[0]), pd[2]*error[1] +pd[3]*(error[1]-perror[1]), pd[4]*error[2] +pd[5]*(error[2]-perror[2]))
    yaw = int(np.clip(speed[0], -100, 100)) if x != 0 else 0
    attitude = int(np.clip(speed[1],-100,100)) if y !=0 else 0
    pitch = int(np.clip(speed[2], -100, 100)) if area !=0 else 0
    drone.send_rc_control(0, pitch, attitude, yaw)
    return error

def main():
    drone = tello.Tello()
    initializeDrone(drone)
    arucoparameters, aruco_dict=loadarucoparam()
    objdicts = loadarucoimages("Objects")
    w, h = 540, 360
    abRange = [75, 80]
    pd_yap = [0.4, 0.9, 0.45, 0.9, 0.7, 0.8]
    pError = [0, 0, 0]
    # pTime, cTime = 0, 0
    while True:
        frame = drone.get_frame_read().frame
        frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
        AListA, AListC, info = [], [], [[0, 0], 0]
        arucofound = findarucofeatures(frame, arucoparameters, aruco_dict)
        if len(arucofound[0]) != 0:
            for corners, id in zip(arucofound[0], arucofound[1]):
                if int(id) in objdicts.keys():
                    frame, info[0], info[1] = findaruco(corners, id, frame, objdicts[int(id)], AListC, AListA)
        pError = arucotrack(drone, info, w,h, pd_yap, pError, abRange)
        # cTime = time.time()
        # fps = 1 / (cTime - pTime)
        # pTime = cTime
        # cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow('Display', frame)
        if cv2.waitKey(1) & 0xff== 27:
            drone.land()
            break
if __name__ == "__main__":
    main()