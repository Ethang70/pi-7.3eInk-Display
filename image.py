import logging

from PIL import Image,ImageDraw,ImageFont
from libs import color_epd_converter
from libs import google_weather as gw


def get_image(epd):
    logging.basicConfig(level=logging.DEBUG)

    try:
        font24 = ImageFont.load_default(24)
        
        weather = gw.get_current_weather_display_info()
        
        
        
        #logging.info("1.Drawing on the image...")
        Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
        Himage = Image.open(weather["condition_icon"])
        Himage = Image.composite(Himage, Image.new('RGB', (epd.width, epd.height), epd.WHITE), Himage)
        draw = ImageDraw.Draw(Himage)
        # Himage = color_epd_converter.convert(Himage,
        #                               orientation="landscape",
        #                               width=480,
        #                               height=800,
        #                               crop_image=False,
        #                               crop_x1=0,
        #                               crop_y1=0,
        #                               crop_x2=480,
        #                               crop_y2=800)
        draw.text((30, 20), str(weather["temperature"]) + "°C", font = font24, fill = epd.BLACK)
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
    
    except Exception as e:
        logging.info(e)