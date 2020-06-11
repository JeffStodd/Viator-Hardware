import sys
import time
import snapshot
import parseData
import readHardware
import subprocess
import zmq

secondInterval = 0 #temp
maxFailed = 5

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def main():
    #print("Starting Execution")

    curr = time.time()

    movement = False
    vehicleNear = False

    update() #initialize to prevent glitchy values
    prevDist = update() #initialize to ultrasonic sensor value
    currDist = update()
    while True:

        currDist = update()
        print "Waiting for movement... Distance: " + str(currDist) + " cm"
        movement = detectMovement(prevDist, currDist)

	#if the delta > noise threshold < glitch value ~(100-60)
        if movement == True and abs(currDist - prevDist) < 30:
            print "Detected movement"
            vehicleNear = True
            time.sleep(3)
            #movement = waitUntilStatic(prevDist, currDist)
            movement = False
            failedDetections = 0
            while movement == False and failedDetections <= maxFailed: #run until vehicle leaves
                curr = time.time()
                time.sleep(1)

                currDist = update()
                print "Running detector"
                license = detect(curr)
                if license == "NA":
                    failedDetections = failedDetections + 1

                movement = detectMovement(prevDist, currDist)
                prevDist = currDist
            print "Vehicle is leaving, waiting until it has left"
            time.sleep(3)
            currDist = prevDist = update()
            #movement = waitUntilStatic(prevDist, currDist) #wait until vehicle leaves driveway
            vehicleNear = False
        else:
            time.sleep(1) #prevent overload cpu

def update():
    #update variables
    result = readHardware.read()
    for i in range(4): #number of readings to average
        result = result * 0.75 + readHardware.read() * 0.25
    return result

def detectMovement(prevDist, currDist):
    if abs(prevDist - currDist) > 5: #if delta < noise threshold, movement
        return True
    else:
        return False

def waitUntilStatic(prevDist, currDist):
    while True:
        currDist = update()
        detectMovement(prevDist, currDist)
        prevDist = currDist

        if(abs(currDist - prevDist) < 6):
            return False
        else:
            time.sleep(1) #prevent overload cpu

def detect(curr):
    if True:
        #time.time() - curr > secondInterval:
        snapshot.snapshot()
        results = parseData.parse("snapshot.jpg")
        reservationLicense = ""
        #print "Requesting plate from parent"
        socket.send("1".encode("utf8"))
        #print "Waiting for response"
        reservationLicense = socket.recv().decode("utf8")
        #print "Received response from parent: " + reservationLicense
        if len(results) > 0:
            print "Detected vehicle, seeing if it matches a reservation"
            for result in results:
                print "Comparing " + result + " with " + reservationLicense
                if result == reservationLicense:
                    print "Found match"
                    socket.send(result.encode("utf8"))
                    try:
                        response = socket.recv().decode("utf8")
                    except:
                        sys.exit()
                    #sys.stdout.flush()
                    return result
            print "No match found"
            socket.send("NA".encode("utf8"))
            try:
                response = socket.recv().decode("utf8")
            except:
                sys.exit()

            #sys.stdout.flush()
        else:
            print "No detections"
            #print("No vehicle detected")
            socket.send("NA".encode("utf8"))
            try:
                response = socket.recv().decode("utf8")
            except:
                sys.exit()
            #sys.stdout.flush()
    return "NA"
    #else:
    #time.sleep(1) #-revent overload cpu

if __name__ == "__main__":
    main()
