import board
import neopixel
from time import sleep
pixels = neopixel.NeoPixel(board.D18, 12)
pixels.brightness = 0.3

def setPixel(i, r, g, b, brightness):
    i = i % 12
    brightness = 255 * brightness
    pixels[i] = (int(r*brightness), int(g*brightness), int(b*brightness))

i = 0
while True:
    setPixel(i-3, 1.0, 0.0, 0.0, 0.25)
    setPixel(i-2, 1.0, 0.0, 0.0, 0.5)
    setPixel(i-1, 1.0, 0.0, 0.0, 0.75)
    setPixel(i, 1.0, 0.0, 0.0, 1.0)
    i += 1
    sleep(0.1)
    pixels.fill((0,0,0))
