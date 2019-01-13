import RPi.GPIO as GPIO


#
# This class is used to pilot a standard RBD led
#
class LedRGB:
    GPIO_PINS = {'RED_GPIO': 11, 'GREEN_GPIO': 12, 'BLUE_GPIO': 13}  # pins is a dict

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
        for i in LedRGB.GPIO_PINS:
            GPIO.setup(LedRGB.GPIO_PINS[i], GPIO.OUT)  # Set all pins to output mode
            GPIO.output(LedRGB.GPIO_PINS[i], GPIO.HIGH)  # Set all pins to high(+3.3V) to off led

        self.red = GPIO.PWM(LedRGB.GPIO_PINS['RED_GPIO'], 2000)  # set frequency to 2KHz
        self.green = GPIO.PWM(LedRGB.GPIO_PINS['GREEN_GPIO'], 2000)
        self.blue = GPIO.PWM(LedRGB.GPIO_PINS['BLUE_GPIO'], 2000)

        self.red.start(0)
        self.green.start(0)
        self.blue.start(0)

    #
    # Value are inverted. So e.g in order to light the LED completely red
    # you should call the function like this set_color(0, 100, 100)
    #
    def set_color(self, red_value, green_value, blue_value):
        self.red.ChangeDutyCycle(red_value)
        self.green.ChangeDutyCycle(green_value)
        self.blue.ChangeDutyCycle(blue_value)

    def reset_gpio(self):
        self.red.stop()
        self.green.stop()
        self.blue.stop()
        GPIO.cleanup()
