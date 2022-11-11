from PIL import Image
import pytesseract
import requests
from io import BytesIO


class Ocr:
    def __init__(self, ctx):
        self.config = r"--oem 3 --psm 6"

    def get_image(self, link):
        try:
            response = requests.get(link)
        except Exception as e:
            print(e)
            return None
        else:
            if response.status_code == 200:
                content = BytesIO(response.content)
                return content
            else:
                print(f"Got status code {response.status_code}")
                return None

    def get_content(self, link):
        # override for now
        link = "https://miiifystore.s3.eu-west-2.amazonaws.com/images/test.png"
        image = self.get_image(link)
        content = pytesseract.image_to_alto_xml(Image.open(image), config=self.config)
        return content
