from PIL import Image,ImageDraw,ImageFont
class fake_epd:
    BLACK = 0
    WHITE = 0
    YELLOW = 0
    RED = 0
    BLUE  = 0
    GREEN = 0x008000

epd = fake_epd()
epd.BLACK  = 0x000000   #   0000  BGR
epd.WHITE  = 0xffffff   #   0001
epd.YELLOW = 0x00ffff   #   0010
epd.RED    = 0x0000ff   #   0011
epd.BLUE   = 0xff0000   #   0101

font24 = ImageFont.load_default(24)#truetype('Font.ttf', 24)
font18 = ImageFont.load_default(18)#truetype('Font.ttf', 18)
font40 = ImageFont.load_default(40)#truetype('Font.ttf', 40)

size = (800, 480)
Himage = Image.open("image2.png")
Himage = Image.composite(Himage, Image.new('RGB', size, epd.WHITE), Himage).show()

# Himage = Image.new('RGB', (800, 480), epd.WHITE)  # 255: clear the frame
# draw = ImageDraw.Draw(Himage)
# draw.text((5, 0), 'hello world', font = font18, fill = epd.RED)
# draw.text((5, 20), '7.3inch e-Paper (e)', font = font24, fill = epd.YELLOW)
# draw.text((5, 45), u'Hello', font = font40, fill = epd.GREEN)
# draw.text((5, 85), u'Hello', font = font40, fill = epd.BLUE)
# draw.text((5, 125), u'Hello', font = font40, fill = epd.BLACK)

# draw.line((5, 170, 80, 245), fill = epd.BLUE)
# draw.line((80, 170, 5, 245), fill = epd.YELLOW)
# draw.rectangle((5, 170, 80, 245), outline = epd.BLACK)
# draw.rectangle((90, 170, 165, 245), fill = epd.GREEN)
# draw.arc((5, 250, 80, 325), 0, 360, fill = epd.RED)
# draw.chord((90, 250, 165, 325), 0, 360, fill = epd.YELLOW)

Himage.save("image.jpg")