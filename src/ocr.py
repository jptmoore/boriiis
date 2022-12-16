from PIL import Image
import pytesseract
import requests
from io import BytesIO
import sys

def pp_exit(msg):
    print(f"\n\U0001F4A5 {msg}", file=sys.stderr)
    sys.exit(1)

class Ocr:
    def __init__(self, ctx):
        self.config = f"--oem {ctx.oem} --psm {ctx.psm} -l {ctx.lang}"
        self.log = ctx.log
    def get_image(self, link):
        try:
            response = requests.get(link)
        except Exception as e:
            pp_exit("failed to get image for ocr")
        if response.status_code != 200:
            pp_exit(f"Got {response.status_code} code trying to access image")
        else:
            content = BytesIO(response.content)
            return content

    def get_alto(self, link):
        image = self.get_image(link)
        try:
            content = pytesseract.image_to_alto_xml(Image.open(image), config=self.config)
        except Exception as e:
            self.log.warning("failed to convert image to alto")
            return None
        else:        
            return content
