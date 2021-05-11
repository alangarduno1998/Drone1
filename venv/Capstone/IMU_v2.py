import serial
import time
from time import sleep

#port = 'COM7' #ALAN'S ARDUINO MEGA
imu = serial.Serial()
imu.baudrate = 115200
imu.port = 'COM9'
imu.open()
imu_bytes[3];
# there are three values from imu, az, lon, lat
while True:
    try:
        imu_bytes = imu.readline()
        imu_decoded = str(imu_bytes, 'utf-8')
        imu_decoded = imu_decoded.strip()
        pack = imu_decoded.split(',')
        #pack = imu_decoded.replace("'","")
        print(pack)
        x = pack[0]
        y = pack[1]
        z = pack[2]
        print(x,y, z)
    except:
        print("Keyboard Interrupt")
        break
