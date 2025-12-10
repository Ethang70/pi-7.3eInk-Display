import logging
import os

from PIL import Image,ImageDraw,ImageFont
from libs import color_epd_converter
from libs import google_weather as gw
from dotenv import load_dotenv
load_dotenv()

# Constants
BORDER_PADDING = 25
INTERNAL_PADDING = 7
ICON_SIZE = 150
ICON_OFFSET = BORDER_PADDING + 150
TEXT_PADDING = 2


# Load fonts or use default if none
fontType = os.getenv('font')
try:
    font = ImageFont.truetype(('fonts/' + str(fontType)), 84)
    font2 = ImageFont.truetype(('fonts/' + str(fontType)), 30)
    font3 = ImageFont.truetype(('fonts/' + str(fontType)), 20)
except:
    font = ImageFont.load_default(84)
    font2 = ImageFont.load_default(30)
    font3 = ImageFont.load_default(20)



def get_image(epd):
    try:        
        weather = gw.get_current_weather_display_info()
        
        #logging.info("1.Drawing on the image...")
        Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
        condition = Image.open(weather["condition_icon"])
        condition = condition.resize((ICON_SIZE, ICON_SIZE), Image.NEAREST)
        Himage.paste(condition, (BORDER_PADDING, BORDER_PADDING), condition)
        draw = ImageDraw.Draw(Himage)

        draw.text((ICON_OFFSET + INTERNAL_PADDING, BORDER_PADDING), weather["temperature"], font = font, fill = epd.BLACK, anchor="lt")
        temperature_offset = font.getlength(weather["temperature"])
        temperature_bbox = draw.textbbox((ICON_OFFSET + INTERNAL_PADDING, BORDER_PADDING), weather["temperature"], font = font, anchor="lt")
        
        draw.text((ICON_OFFSET + temperature_offset + INTERNAL_PADDING, BORDER_PADDING), "°C", font = font2, fill = epd.BLACK, anchor="lt")
        
        draw.text((ICON_OFFSET + INTERNAL_PADDING, temperature_bbox[3] + TEXT_PADDING + INTERNAL_PADDING), weather["condition"], font = font2, fill = epd.BLACK, anchor="lt")
        condition_bbox = draw.textbbox((ICON_OFFSET + INTERNAL_PADDING, temperature_bbox[3] + TEXT_PADDING + INTERNAL_PADDING), weather["condition"], font = font2, anchor="lt")

        draw.text((ICON_OFFSET + INTERNAL_PADDING, condition_bbox[3] + TEXT_PADDING), f'Feels Like: {weather["feels_like"]}°C', font = font3, fill = epd.BLACK, anchor="lt")
        
        
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