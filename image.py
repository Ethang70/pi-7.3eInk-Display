import logging
import os

from PIL import Image,ImageDraw,ImageFont
from libs import color_epd_converter
from libs import google_weather as gw
from dotenv import load_dotenv
load_dotenv()

PADDING = 25
ICON_SIZE = 150
ICON_OFFSET = PADDING + 150

fontType = os.getenv('font')

try:
    font = ImageFont.truetype(('fonts/' + str(fontType)), 84)
    font2 = ImageFont.truetype(('fonts/' + str(fontType)), 24)
    font3 = ImageFont.truetype(('fonts/' + str(fontType)), 16)
except:
    font = ImageFont.load_default(84)
    font2 = ImageFont.load_default(24)
    font3 = ImageFont.load_default(16)



def get_image(epd):
    try:        
        weather = gw.get_current_weather_display_info()
        
        
        
        #logging.info("1.Drawing on the image...")
        Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
        condition = Image.open(weather["condition_icon"])
        condition = condition.resize((ICON_SIZE, ICON_SIZE), Image.NEAREST)
        Himage.paste(condition, (PADDING, PADDING), condition)
        draw = ImageDraw.Draw(Himage)

        draw.text((ICON_OFFSET, PADDING), str(weather["temperature"]), font = font, fill = epd.BLACK, anchor="lt")
        temperature_offset = font.getlength(str(weather["temperature"]))
        temperature_box = font.getbbox(str(weather["temperature"]))

        draw.text((ICON_OFFSET + temperature_offset, PADDING), "°C", font = font2, fill = epd.BLACK, anchor="lt")
        
        draw.text((ICON_OFFSET, temperature_box[3]), str(weather["condition"]), font = font2, fill = epd.BLACK, anchor="lt")
        condition_box = font2.getbbox(str(weather["condition"]))

        draw.text((ICON_OFFSET, temperature_box[3] + condition_box[3]), f'Feels Like: {weather["feels_like"]}°C', font = font3, fill = epd.BLACK, anchor="lt")
        
        
        # Himage = color_epd_converter.convert(Himage,
        #                               orientation="landscape",
        #                               width=480,
        #                               height=800,
        #                               crop_image=False,
        #                               crop_x1=0,
        #                               crop_y1=0,
        #                               crop_x2=480,
        #                               crop_y2=800)
        draw = ImageDraw.Draw(Himage)
        

        return Himage
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        try:
            from libs import epd7in3f
            epd7in3f.epdconfig.module_exit(cleanup=True)
        except:
            logging.info("no connection to epd")
        exit()