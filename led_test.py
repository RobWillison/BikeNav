import board
import neopixel
from time import sleep
import board
import busio
import adafruit_lsm9ds0
import math

class BikeNav:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)
        self.pixels = neopixel.NeoPixel(board.D18, 12)
        pixels.brightness = 0.3

        self.angles = []

    def direction(self):
        mag_x, mag_y, mag_z = self.sensor.magnetic
        heading = 180 * math.atan2(mag_y,mag_x)/math.pi;
        heading += 180;

        self.angles.append(heading)
        self.angles = angles[-5:]

    def setLight(self):
        angle = sum(angles) / len(angles)
        pixel = round(angle / 33.0)
        self.pixels.fill((0,0,0))
        self.pixels[pixel] = (255,0,0)

    def setPixel(self, i, r, g, b, brightness):
        i = i % 12
        brightness = 255 * brightness
        self.pixels[i] = (int(r*brightness), int(g*brightness), int(b*brightness))


nav = BikeNav()
while True:
    nav.direction()
    nav.setLight()
    sleep(0.1)
