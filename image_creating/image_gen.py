from PIL import Image
from io import BytesIO
import requests
from openai import OpenAI

client = OpenAI()
class ImageGen:
    '''
    This class is used to generate images using OpenAI's DALL-E model.
    prompt: str
        The prompt to generate the image from the model must be creative and dinstinctive.
        This means the ai from api_calls/openai_api.py can be used to generate a prompt.
        We can use the response from the ai to generate the prompt.
        they can create logos, backgrounds, and other images required for them to do their jobs better. This is a great way to generate images for the website for instance.
        

    
    
    '''
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
