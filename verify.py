import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

#initialise a previous input variable to 0 (Assume no pressure applied)
prev_input = 0
try:
    while True:
        #take a reading
        input = GPIO.input(4)
        #if the last reading was low and this one high, alert us
        if ((not prev_input) and input):
            print("Under Pressure")
        #update previous input
        prev_input = input
        #slight pause
        time.sleep(0.10)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

