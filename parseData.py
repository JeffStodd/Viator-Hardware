from openalpr import Alpr
from os import path
import detectImage
import sys

def main(argv):
    if len(argv) > 2:
        print("Incorrect Usage")
        return

    fileName = argv[1] #image directory and name

    if not path.exists(fileName):
        print("File not found")
        return

    results = parse(fileName)
    print(results)

def parse(image):
    result = detectImage.detect(image)

    detectedStrings = []

    if(result is not None and len(result) >= 1):
        for candidate in result:
            detectedStrings.append(str(candidate['plate']))
    else:
        pass
        #null do block for firebase

    return detectedStrings

if __name__ == "__main__":
    main(sys.argv)

