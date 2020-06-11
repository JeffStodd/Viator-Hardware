import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import sys

from uuid import getnode as get_mac

def main(argv):
        if len(sys.argv) > 1:
                pass
        else:
                pass

#search database if camera already is registered
def findMACAddress(db):
        macAddress = hex(get_mac())[2:]

        print("Searching MAC Address")
        for camera in db.collection(u'cameras').stream():
                fields = camera.to_dict()
                if fields[u'macAddress'] == macAddress:
                        return True
        return False

if __name__ == "__main__":
        main(sys.argv)
