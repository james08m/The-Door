import RPi.GPIO as GPIO
import time

###############
#!#  Servo  #!#
###############

class Servo():
    __busy = False
    __pushed = False
    
    def __init__(self):

        # Initialise attributs
        print("Servo motor initialisation..")
        self.pin = 17   # GPIO pin #17
        self.freq = 50  # Frequency of 50hz
        self.dc = 10.5   # Initial duty cycle

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.pwm.start(self.dc)
    
    @classmethod
    def setbusy(cls, bool):
        Servo.__busy = bool
   
    @classmethod
    def isbusy(cls):
        return Servo.__busy
    
    @classmethod
    def setpushed(cls, bool):
        Servo.__pushed = bool
        
    @classmethod
    def ispushed(cls):
        return Servo.__pushed
        
    def push(self):
        if not Servo.isbusy():
            if not Servo.ispushed():
                Servo.setbusy(True) # Set to busy while working
                self.pwm.ChangeDutyCycle(5.5) # Pushing button duty cycle
                Servo.setpushed(True)
                Servo.setbusy(False) # Set to not busy after worked
            else:
                print("Servo motor already in pushed position.")
        else:
            print("Servo motor is busy.")
        
    def idle(self):
        if not Servo.isbusy():
            
            if Servo.ispushed(): 
                Servo.setbusy(True) # Set to busy while working
                self.pwm.ChangeDutyCycle(10.5) # Idle duty cycle
                Servo.setpushed(False)
                Servo.setbusy(False) # Set to not busy after worked
            else:
                print("Servo motor already in released position.")
        else:
            print("Servo motor is busy.")
        
    def test(self):
        print("Starting test program..")
        try:
            while True:
                self.push()
                time.sleep(1)
                self.idle()
                time.sleep(1)
        except KeyboardInterrupt:
            self.pwm.stop()
            GPIO.cleanup()



####################
#!# Main Program #!#
####################

if __name__ == "__main__":
    servo = Servo()
    servo.test()