from google.cloud import vision
from PIL import Image
import os
import stone
from json import dumps # Optional


downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads") # this part will change based on how we implement our image upload later
image_path = os.path.join(downloads_folder, "headshot.jpeg")
print(image_path)

client = vision.ImageAnnotatorClient()
'''
with open(image_path, "rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)
'''
result = stone.process(image_path, image_type="color", return_report_image=True)
print(result['faces'][0])

#result_json = dumps(result)
#print(result_json)