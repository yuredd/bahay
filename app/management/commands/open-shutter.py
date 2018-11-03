import RPi.GPIO as GPIO
import time, sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(sys.argv[1],GPIO.OUT)
while True:
    print "Relay 6 On"
    GPIO.output(sys.argv[1],GPIO.HIGH)
    time.sleep(30)

