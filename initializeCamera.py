import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import databaseUtil
import checkRegistry
import registerCamera
import upnp
import subprocess
from subprocess import Popen, PIPE
import os
import sys
import time
import json
from wireless import Wireless
import time as time
import signal
import socket
import zmq
import editConfig

def main():
        #kill motioneye
        cmd = "sudo -s service motion stop"
        subprocess.run([cmd], shell=True)
        #p = Popen(cmd)

        print("Checking if camera is registered")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/pi/Viator/viator.json'
        print("Getting Creds")
        cred = credentials.ApplicationDefault()
        print("Init App")
        firebase_admin.initialize_app(cred, {
                'projectId':'viator-b2e7e',
                })

        print("Getting Client")
        db = firestore.client()

        wifiAuthenticated = isAuthenticated()
        checkForUpdates()
        macAddressExists = initializeComponents(wifiAuthenticated, db)
        if macAddressExists:
                print("Found Camera...\nStarting Detection")
                run(db)
        else:
                #throw error
                print("Camera doesn't exist in database")

def checkForUpdates():
        pass

def initializeComponents(wifiAuthenticated, db):
        if wifiAuthenticated:
                print("Wifi is authenticated...\nChecking registry")
                macAddressExists = checkRegistry.findMACAddress(db)
                if macAddressExists:
                        portNum = editConfig.getPort()
                        upnp.openPort(portNum)

                        #start motioneye
                        cmd = "sudo -s service motion start"
                        subprocess.run([cmd], shell=True)
                        #p3 = Popen(cmd)

                        return True
                else:
                        print("Camera not registered...\nStarting setup sequence")

        print("Starting QR Stream")
        cmd = 'python readQRStream.py'
        p2 = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
        content = p2.stdout.read().decode("utf-8").replace('\n', '')
        print(content)
        #os._exit(os.EX_OK)

        dictionary = json.loads(content)
        print("Authenticating Wifi")
        authenticateWifi(dictionary["ESSID"], dictionary["Password"])

        authenticated = isAuthenticated()
        print("Authenticated:", authenticated)
        if(authenticated == False):
                print("Failed Authentication")
                return False

        print("Getting Open Port")
        port = upnp.get_open_port(lowest_port = 8081, highest_port = 8999)
        print("Opening Port", port)
        upnp.openPort(port)
        upnp.changeConfig(port)

        print("Registering Camera")
        registerCamera.findAndUpdate(dictionary["Address"], port)

        #start motioneye
        cmd = "sudo -s service motion start"
        subprocess.run([cmd], shell=True)
        #p3 = Popen(cmd)

        return True

def run(db):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5555")

        cmd = 'python run.py'
        p = subprocess.Popen(cmd, shell=True)
        while p.poll() is None:
                print("Waiting for request from detector")
                flag = socket.recv().decode("utf8")
                if int(flag) == 1:
                        print("Got request from detector")
                        currReservation = databaseUtil.checkForVehicle(db)
                        print("Current reservation: " + currReservation)
                        #print("Parent is sending")
                        sendReservation(socket, currReservation)

                        #print("Parent is waiting for response")
                        buf = str(socket.recv().decode("utf8"))
                        success = "Received from detector: " + buf
                        print(success)
                        socket.send(success.encode("utf8"))
                        print("Updating database")
                        databaseUtil.findField(buf, db)

def sendReservation(socket, currReservation):
        payload = currReservation.encode("utf8")
        socket.send(payload)

def isAuthenticated():
        print("Checking wifi connectivity")
        for i in range(5):
                try:
                        # connect to the host -- tells us if the host is actually
                        # reachable
                        socket.create_connection(("www.google.com", 80))
                        return True
                except OSError as e:
                        print(e)
                        time.sleep(1)

#Close session
def handler(signum, frame):
        #print(1)
        raise Exception('Action took too much time')

def authenticateWifi(ssid, password):
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(20) #Set the parameter to the amount of seconds you want to wait

        try:
                #RUN CODE HERE
                wireless = Wireless()
                wireless.connect(ssid, password)

        except:
                pass
                #print(2)

        signal.alarm(20) #Resets the alarm to 30 new seconds
        signal.alarm(0) #Disables the alarm

if __name__ == "__main__":
        main()
