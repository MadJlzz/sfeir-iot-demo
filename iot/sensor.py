import Adafruit_DHT


#
# This class aims to read temperature and humidity from a DHT11 sensor.
# It uses the Adafruit_DHT library to reach it's goal.
#
class DHT11:

    def __init__(self):
        self.humidity = 0
        self.temperature = 0

    def __str__(self):
        return 'Temp: {0:0.1f} C Humidity: {1:0.1f} %'.format(self.temperature, self.humidity)

    def read_dht11(self):
        self.humidity, self.temperature = Adafruit_DHT.read_retry(11, 4)
