import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import urllib.request
import sys

import datetime
from dateutil import parser

def main(argv):
        if len(sys.argv) > 1:
                pass
        else:
                detections = ["test"]
        findField(sys.argv[1:])

#search for parking spot with matching ip address
def findField(detection, db):
        external_ip = urllib.request.urlopen('https://v4.ident.me/').read().decode('utf8')

        print("Searching IP")
        for parkingSpot in db.collection(u'parkingSpots').stream():
                parkingDict = parkingSpot.to_dict()
                cameraID = parkingDict[u'cameraId']
                if not cameraID == "NA":
                        for camera in db.collection(u'cameras').stream():
                                cameraDict = camera.to_dict()
                                if cameraDict[u'ip'] == external_ip:
                                        #print("Found parking spot")
                                        update(camera.reference, detection)
                                        return
        print("Failed to find IP")

#checks for current reservation's expected license
def checkForVehicle(db):
        external_ip = urllib.request.urlopen('https://v4.ident.me/').read().decode('utf8')
        for parkingSpot in db.collection(u'parkingSpots').stream():
                parkingDict = parkingSpot.to_dict()
                cameraID = parkingDict[u'cameraId']
                if not cameraID == "NA":
                        for camera in db.collection(u'cameras').stream():
                                cameraDict = camera.to_dict()
                                if cameraDict[u'ip'] == external_ip:
                                        print("Found parking spot")
                                        for reservation in parkingSpot.reference.collection(u'currentReservation').stream():
                                                reservationDict = reservation.to_dict()
                                                startTime = parser.parse(reservationDict[u'startTime']).time()
                                                endTime = parser.parse(reservationDict[u'endTime']).time()
                                                day = parser.parse(reservationDict[u'reservationDay'])
                                                currentTime = datetime.datetime.utcnow()-datetime.timedelta(hours=7) #hardcoded PST because I can
                                                #print(startTime)
                                                #print(currentTime >= startTime)
                                                #print(endTime)
                                                #print(currentTime <= endTime)
                                                #print(day.date())
                                                #print(currentTime.date())
                                                if day.date() == currentTime.date() and currentTime.time() <= endTime and currentTime.time() >= startTime:
                                                        license = reservationDict[u'vehicleLicense']
                                                        return license
                                                else:
                                                        print("Wrong time window")
                                                        return "NA"

#update field with detection
def update(document, detection):

        #print("Updating Fields")
        currentTime = datetime.datetime.utcnow()-datetime.timedelta(hours=7) #hardcoded PST because I can
        field_updates = {u'lastDetection' : detection, u'lastDetectionTime': currentTime}
        document.update(field_updates)

        print("Update successful")

if __name__ == "__main__":
        main(sys.argv)
