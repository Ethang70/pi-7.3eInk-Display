import logging
import os

from PIL import Image,ImageDraw,ImageFont
from libs import color_epd_converter
from libs import google_weather as gw
from dotenv import load_dotenv
load_dotenv()

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
        condition = condition.resize((150, 150), Image.NEAREST)
        Himage.paste(condition, (25, 25), condition)
        draw = ImageDraw.Draw(Himage)

        draw.text((175, 25), str(weather["temperature"]), font = font, fill = epd.BLACK, anchor="lt")
        temperature_offset = font.getlength(str(weather["temperature"]))
        temperature_box = font.getbbox(str(weather["temperature"]))

        draw.text((175 + temperature_offset, 25), "°C", font = font2, fill = epd.BLACK, anchor="lt")
        
        draw.text((175, temperature_box[3]), str(weather["condition"]), font = font2, fill = epd.BLACK, anchor="lt")
        condition_box = font2.getbbox(str(weather["condition"]))

        draw.text((175, temperature_box[3] + condition_box[3]), f'Feels Like: {weather["feels_like"]}°C', font = font3, fill = epd.BLACK, anchor="lt")
        
        
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