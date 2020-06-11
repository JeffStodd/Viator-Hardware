import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import urllib.request
import sys

from uuid import getnode as get_mac

def main(argv):
        if len(sys.argv) > 1:
                pass
        else:
                pass

#search for matching address and update stream fields
def findAndUpdate(content, port):
        print("Getting Client")
        db = firestore.client()

        print("Searching Address:", content)
        for camera in db.collection(u'cameras').stream():
                fields = camera.to_dict()
                print(fields[u'linkedParkingSpot'])
                if fields[u'linkedParkingSpot'] == content:
                        update(camera.reference, port)
                        return
        print("Could not find match")

def update(document, port):
        external_ip = urllib.request.urlopen('https://v4.ident.me/').read().decode('utf8')
        macAddress = hex(get_mac())[2:]
        print("Updating Camera")

        field_updates = {u'ip' : external_ip, u'port': port, u'macAddress': macAddress}
        document.update(field_updates)

        print("Update Successful")

if __name__ == "__main__":
        main(sys.argv)
