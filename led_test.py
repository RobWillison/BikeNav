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
            return [report.lat, report.lon]

class Navigatior:

    def __init__(self):
        gpx_file = open('test.gpx', 'r')
        self.gpx = gpxpy.parse(gpx_file)
        self.points = self.populate_points()

    def populate_points(self):
        points = []
        for track in self.gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append(point)

        return points

    def next_point(self):
        return [self.points[0].latitude, self.points[0].longitude]

class BikeNav:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)
        self.pixels = neopixel.NeoPixel(board.D18, 12)
        self.pixels.brightness = 0.3
        self.gps = GPS()
        self.nav = Navigatior()

        self.angles = []

    def current_direction(self):
        mag_x, mag_y, mag_z = self.sensor.magnetic
        heading = math.degrees(math.atan2(mag_x,mag_y));
        heading += 180;
        return heading

    def setLight(self, angle):
        pixel = round(angle / 33.0)
        self.pixels.fill((0,0,0))
        self.pixels[pixel] = (0,125,0)

    def setPixel(self, i, r, g, b, brightness):
        i = i % 12
        brightness = 255 * brightness
        self.pixels[i] = (int(r*brightness), int(g*brightness), int(b*brightness))

    def update_display(self):
        # current_point = self.gps.position()
        # if current_point == None:
        #     self.pixels.fill((0,0,255))
        #     return
        # print(current_point)
        # target_point = self.nav.next_point()
        # print(target_point)
        # angle = sphere.final_bearing(current_point, target_point)
        # print(angle)
        angle = self.current_direction()
        print(angle)
        self.setLight(angle)

nav = BikeNav()
while True:
    nav.update_display()
    sleep(0.5)
