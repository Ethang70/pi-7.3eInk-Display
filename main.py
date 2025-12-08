import logging

from image import get_image

logging.basicConfig(level=logging.DEBUG)

class fake_epd:
    BLACK  = 0x000000   #   0000  BGR
    WHITE  = 0xffffff   #   0001
    GREEN  = 0x00ff00   #   0010
    BLUE   = 0xff0000   #   0011
    RED    = 0x0000ff   #   0100
    YELLOW = 0x00ffff   #   0101
    ORANGE = 0x0080ff   #   0110
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
    #image.show()
    image.save("image.jpg")
