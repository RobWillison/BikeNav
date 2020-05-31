import board
import neopixel
from time import sleep
import board
import busio
import adafruit_lsm9ds0
import math
import gpxpy
from geo import sphere
import gps

class GPS:
    def __init__(self):
        self.session = gps.gps('localhost', '2947')
        self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    def position(self):
        report = self.session.next()
        if hasattr(report, 'lat') and hasattr(report, 'lon'):
            return [report['lat'], report['lon']]


class BikeNav:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)
        self.pixels = neopixel.NeoPixel(board.D18, 12)
        self.pixels.brightness = 0.3

        self.angles = []

    def direction(self):
        mag_x, mag_y, mag_z = self.sensor.magnetic
        heading = 180 * math.atan2(mag_y,mag_x)/math.pi;
        heading += 180;

        self.angles.append(heading)
        self.angles = self.angles[-5:]

    def setLight(self):
        angle = sum(self.angles) / len(self.angles)
        print(angle)
        pixel = round(angle / 33.0)
        self.pixels.fill((0,0,0))
        self.pixels[pixel] = (255,0,0)

    def setPixel(self, i, r, g, b, brightness):
        i = i % 12
        brightness = 255 * brightness
        self.pixels[i] = (int(r*brightness), int(g*brightness), int(b*brightness))

class Navigatior:

    def __init__(self):
        gpx_file = open('test.gpx', 'r')
        self.gpx = gpxpy.parse(gpx_file)
        self.points = self.populate_points()

    def populate_points(self):
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append(point)

        return points

    def first_point(self):
        return self.points[0]

nav = GPS()
while True:
    print(nav.position())
    sleep(1)
