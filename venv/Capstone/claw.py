import serial
import time
from time import sleep
#port = 'COM7' #ALAN'S ARDUINO MEGA
claw = serial.Serial()
claw.baudrate = 9600
claw.port = 'COM15'
claw.open()
val = ['0'.encode(),'1'.encode()]

claw.write(val[0])
sleep(5)
claw.write(val[1])
