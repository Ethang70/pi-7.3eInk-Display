import logging

from PIL import Image,ImageDraw,ImageFont
from libs import color_epd_converter
from libs import google_weather as gw


def get_image(epd):
    try:
        font = ImageFont.load_default(84)
        font2 = ImageFont.load_default(24)
        
        weather = gw.get_current_weather_display_info()
        
        
        
        #logging.info("1.Drawing on the image...")
        Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
        condition = Image.open(weather["condition_icon"])
        condition = condition.resize((200, 200), Image.NEAREST)
        Himage.paste(condition, (25, 25), condition)
        draw = ImageDraw.Draw(Himage)
        draw.text((235, 5), str(weather["temperature"]), font = font, fill = epd.BLACK)
        draw.text((235, 99), str(weather["condition"]), font = font2, fill = epd.BLACK)
        
        
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