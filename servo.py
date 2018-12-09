import RPi.GPIO as GPIO
import time

###############
#!#  Servo  #!#
###############

class Servo():
    __busy = False          # Attribute bounded to class
    __pushed = False        # Attribute bounded to class

    # Initialise servo motor
    def __init__(self):
        print "[i] Servo motor initialisation.."
        self.pin = 17                               # Set GPIO pin to 17
        self.freq = 50                              # Set frequency of 50hz
        self.dc = 10.5                              # Set initial duty cycle to 10.5

        GPIO.setmode(GPIO.BCM)                      # Set GPIO mode
        GPIO.setup(self.pin, GPIO.OUT)              # Setup the used GPIO PIN

        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.pwm.start(self.dc)
        time.sleep(1)                               # Wait to make sure motor goes into initial position
        self.sleep()                                # Set servo motor in sleep mode

    # Method bounded to class that change __busy value
    @classmethod
    def setbusy(cls, bool):
        Servo.__busy = bool

    # Method bounded to class that return __busy value
    @classmethod
    def isbusy(cls):
        return Servo.__busy

    # Method bounded to class that change __pushed value
    @classmethod
    def setpushed(cls, bool):
        Servo.__pushed = bool

    # Method bounded to class that return __pushed value
    @classmethod
    def ispushed(cls):
        return Servo.__pushed

    # Method that close the servo motor properly
    def close(self):
        self.pwm.stop()                 # Stop servo motor
        GPIO.cleanup()                  # Cleanup GPIO pin
        print "[i] Servo motor stopped and GPIO pins cleaned."

    def sleep(self):
        self.pwm.ChangeDutyCycle(0)   # Set duty cycle to 0

    # Method that place motor in pushed position
    def push(self):
        if not Servo.isbusy():                  # Check if servo motor is already being use by another object instance
            if not Servo.ispushed():            # Check if servo motor is not already in pushed position
                Servo.setbusy(True)             # Set Servo Class to busy while working
                self.pwm.ChangeDutyCycle(5.5)   # Change duty cycle to pushed position
                Servo.setpushed(True)           # Set Servo Class attribute __pushed to true
                Servo.setbusy(False)            # Set Servo Class to not busy
            else:
                print "[w] Servo motor already in pushed position."
        else:
            print "[w]  Servo motor is busy."

    # Method that place motor in pushed position
    def idle(self):
        if not Servo.isbusy():                  # Check if servo motor is already being use by another object instance
            if Servo.ispushed():                # Check if servo motor is not already in pushed position
                Servo.setbusy(True)             # Set Servo Class to busy while working
                self.pwm.ChangeDutyCycle(10.5)  # Change duty cycle to idle position
                Servo.setpushed(False)          # Set Servo Class attribute __pushed to False
                Servo.setbusy(False)            # Set Servo Class to not bus
            else:
                print("[w] Servo motor already in released position.")
        else:
            print("[w] Servo motor is busy.")

    # Small test program to test servo motor
    def test(self):
        print "[i] Starting test program.."
        try:
            while True:
                self.push()
                time.sleep(1)
                self.idle()
                time.sleep(1)
        except KeyboardInterrupt:
            self.pwm.stop()
            GPIO.cleanup()



########################
#!# Run Test Program #!#
########################

if __name__ == "__main__":
    servo = Servo()
    servo.test()
