import socket
import math

def getIMU(soc):
    message, address = soc.recvfrom(4096)
    dataPacket = str(message, 'utf-8')
    pack = dataPacket.split(',')
    azimuth = float(pack[0])
    lat = float(pack[3])
    lon = float(pack[4])
    return azimuth, lat, lon

def main():
    host = '' # edit
    port = 8081 #edit
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((host, port))
    while 1:
        az, lat, lon = getIMU(s)
        print (az, lat, lon)


if __name__ == '__main__':
    main()
