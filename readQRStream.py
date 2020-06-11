import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
#import socket
import time

def getContent():
        #port = 8081
        #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #s.connect(("8.8.8.8", 80))
        #ip = s.getsockname()[0]
        #s.close()
        #cap = cv2.VideoCapture("http://" + str(ip) + ":" + str(port) + "/")
	cap = cv2.VideoCapture(0)
        decodedObjects = []

        while True:
                valid, frame = cap.read()

                if(valid == True):
                        decodedObjects = pyzbar.decode(frame)

                if len(decodedObjects) > 0:
                        break
        time.sleep(0.1)
        return decodedObjects[0]

def main():
        r = getContent()
        print(r.data)

if __name__ == "__main__":
        main()
