#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from libs import epd7in3f
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from libs import color_epd_converter

from libs import google_weather as gw

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in3f Demo")
    font24 = ImageFont.load_default(24)

    epd = epd7in3f.EPD()   
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    weather = gw.get_current_weather()
    temp = weather["temperature"]["degrees"]
    
    
    # Drawing on the image
    logging.info("1.Drawing on the image...")
    Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
    draw = ImageDraw.Draw(Himage)
    # Himage = Image.open("image2.png")
    # Himage = Image.composite(Himage, Image.new('RGB', (epd.width, epd.height), epd.WHITE), Himage)
    # Himage = color_epd_converter.convert(Himage,
    #                               orientation="landscape",
    #                               width=480,
    #                               height=800,
    #                               crop_image=False,
    #                               crop_x1=0,
    #                               crop_y1=0,
    #                               crop_x2=480,
    #                               crop_y2=800)
    draw.text((5, 20), 'The temperature is ' + temp, font = font24, fill = epd.YELLOW)
    draw = ImageDraw.Draw(Himage)
    epd.display(epd.getbuffer(Himage))
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in3f.epdconfig.module_exit(cleanup=True)
    exit()