import logging

from PIL import Image,ImageDraw,ImageFont
from test import get_image

class fake_epd:
    BLACK = 0x000000
    WHITE = 0xffffff
    YELLOW = 0x00ffff
    RED = 0x0000ff
    BLUE  = 0xff0000
    GREEN = 0x008000
    width = 800
    height = 480

try:
    from libs import epd7in3f

    logging.info("Loading epd7in3f")
    epd = epd7in3f.EPD()

    logging.info("init and Clear")
    epd.init()
    #epd.Clear()
except:
    epd = fake_epd()

image = get_image(epd)

try:
    epd.display(epd.getbuffer(image))
except:
    image.save("image.jpg")
