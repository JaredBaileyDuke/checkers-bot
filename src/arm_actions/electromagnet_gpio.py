import RPi.GPIO as GPIO
from time import sleep

def electromagnet(relay="on", pin_number=18):
    """
    Activate/deactivate electromagnet
    Requires 5v to relay

    Args:
        relay, str: user sets relay "on" (LOW) or "off" (HIGH)
        pin_number, int: Raspberry Pi pin number used
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_number, GPIO.OUT)

    if relay == "on":
        print("Activate Relay")
        GPIO.output(pin_number, GPIO.LOW)
    else:
        print("Deactivate Relay")
        GPIO.output(pin_number, GPIO.HIGH)

if __name__ == "__main__":
    try:
        while True:
            electromagnet(relay="on")
            sleep(10)
            electromagnet(relay="off")
            sleep(10)

    except KeyboardInterrupt:
        print("Program stopped by user")

    finally:
        GPIO.cleanup()


