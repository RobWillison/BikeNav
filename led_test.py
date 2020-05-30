import board
import neopixel
from time import sleep
import board
import busio
import adafruit_lsm9ds0
import math

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)
pixels = neopixel.NeoPixel(board.D18, 12)
pixels.brightness = 0.3

angles = []

def direction():
    mag_x, mag_y, mag_z = sensor.magnetic
    heading = 180 * math.atan2(mag_y,mag_x)/math.pi;
    heading += 180;

    angles.append(heading)
    angles = angles[-5:]

def setLight():
    angle = sum(angles) / len(angles)
    pixel = round(angle / 33.0)
    pixels.fill((0,0,0))
    pixels[pixel] = (255,0,0)

def setPixel(i, r, g, b, brightness):
    i = i % 12
    brightness = 255 * brightness
    pixels[i] = (int(r*brightness), int(g*brightness), int(b*brightness))


while True:
    direction()
    setLight()
    sleep(0.1)
