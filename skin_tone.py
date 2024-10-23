from google.cloud import vision
from PIL import Image
import os
import stone
def get_skin_tone(image_path):
    if(image_path==""):
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads") # this part will change based on how we implement our image upload later
        image_path = os.path.join(downloads_folder, "headshot.jpeg")
    # print(image_path)

    result = stone.process(image_path, image_type="color", return_report_image=True)

    print(result['faces'][0])
    skin_tone = result['faces'][0]['skin_tone']

    hex_color = skin_tone.lstrip('#')
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    return(rgb_color)