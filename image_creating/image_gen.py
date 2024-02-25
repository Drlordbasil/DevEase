from PIL import Image
from io import BytesIO
import requests
from openai import OpenAI

client = OpenAI()
class ImageGen:
    def __init__(self):
        pass
    def generate_image(self, prompt):
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    def save_image_from_url(self, url, filename):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.save(filename)
    
#image_gen = ImageGen()
#url = image_gen.generate_image("a painting of a cat")
#image_gen.save_image_from_url(url, "cat.png")
