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
        mag_x, mag_y, mag_z = self.sensor.read_mag_raw()
        mag_x += 15144.9363636
        mag_y -= 1202.48282828
        mag_z -= 10295.5449495
        if -10000 > mag_x < 10000:
            return
        if -10000 > mag_y < 10000:
            return
        if -10000 > mag_z < 10000:
            return

        heading = math.degrees(math.atan2(mag_x,mag_y));
        heading += 180;

        return heading

    def compass_heading(self):
        data = []
        for i in range(10):
            sleep(0.01)
            new_data = self.current_direction()
            if new_data:
                data.append(new_data)

        return sum(data) / len(data)

    def setLight(self, angle, target_angle):
        # error from 0 to 180
        error = abs(target_angle - angle)
        # Now from 1 to 10
        error = int(error / 18.0)
        print(error)
        red = 10 * error
        green = 100 - red

        pixel = math.floor(angle / 30.0)
        self.pixels.fill((0,0,0))
        self.pixels[pixel] = (red,green,0)

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
        angle = self.compass_heading()
        print(angle)
        target_angle = 0
        self.setLight(angle, target_angle)

nav = BikeNav()
while True:
    nav.update_display()
    sleep(0.1)
