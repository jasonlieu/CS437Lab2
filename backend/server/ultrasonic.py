import RPi.GPIO as GPIO
import time

TRIG = 11
ECHO = 8

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ECHO, GPIO.IN)
    # Trigger pulse
    GPIO.output(TRIG, False)
    time.sleep(2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    # Measure the pulse duration
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    # Calculate distance (in cm)
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def gpio_clean_up():
    GPIO.cleanup()
