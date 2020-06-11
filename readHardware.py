import RPi.GPIO as GPIO
import time

def main():
    print("Starting Measurement")
    print(read())

def read():
    value = -1
    while True:
        value = poll()
        if value >= 0:
            return value
        else:
            print("Failed to get distance")

def poll():
    dist = 0

    GPIO.setmode(GPIO.BOARD)

    TRIG = 22 #GPIO output
    ECHO = 40 #GPIO input

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.output(TRIG,0)

    GPIO.setup(ECHO, GPIO.IN)

    time.sleep(0.1)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    start_time = time.time()
    elapsed_time = 0
    while GPIO.input(ECHO) == 0:
        time.sleep(0.000001)
        elapsed_time = time.time() - start_time
        if elapsed_time > 5:
            return -1
    start = time.time()

    start_time = time.time()
    elapsed_time = 0
    while GPIO.input(ECHO) == 1:
        time.sleep(0.000001)
        elapsed_time = time.time() - start_time
        if elapsed_time > 5:
            return -1

    stop = time.time()

    GPIO.cleanup()

    dist = (stop-start) * 17150 #Speed of sound in cm/s divided by 2 (Twice disctance)

    return dist

if __name__ == "__main__":
    main()
