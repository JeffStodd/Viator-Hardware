from openalpr import Alpr
import sys
#import cv2

def main():
    alpr = Alpr("us", "/etc/openalpr/openalp.conf", "/usr/share/openalpr/runtime_data")
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    alpr.set_top_n(20) #top candidates
    alpr.set_default_region("ca") #default region

    fileName = "snapshot.jpg"

    results = alpr.recognize_file(fileName)
    #file = cv2.imread(fileName)
    #cv2.imshow("test", file)
    i = 0
    print(len(results['results']))
    for plate in results['results']:
        i += 1
        coords = plate['coordinates']
        topLeft = coords[0]
        bottomRight = coords[2]

        w = bottomRight['x'] - topLeft['x']
        h = bottomRight['y'] - topLeft['y']

        print("Plate #%d" % i)
        print("Width: %d" % w)
        print("Height: %d" % h)
        print("   %12s %12s" % ("Plate", "Confidence"))
        for candidate in plate['candidates']:
            prefix = "-"
            if candidate['matches_template']:
                prefix = "*"

            print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
    # Call when completely done to release memory
    alpr.unload()

def detect(path):
    alpr = Alpr("us", "/etc/openalpr/openalp.conf", "/usr/share/openalpr/runtime_data")
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    alpr.set_top_n(20) #top candidates
    alpr.set_default_region("ca") #default region

    results = alpr.recognize_file(path)

    largestPlate = None
    largestArea = 0

    for plate in results['results']:
        coords = plate['coordinates']
        topLeft = coords[0]
        bottomRight = coords[2]

        w = bottomRight['x'] - topLeft['x']
        h = bottomRight['y'] - topLeft['y']

        prevArea = largestArea
        largestArea = max(w*h,largestArea)
        if(prevArea != largestArea):
            largestPlate = plate

    # Call when completely done to release memory
    alpr.unload()
    if largestPlate == None:
        return []
    return largestPlate['candidates']


if __name__ == "__main__":
    main()
