import os
import stone
def get_skin_tone(image_path):
    if(image_path==""):
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads") # this part will change based on how we implement our image upload later
        image_path = os.path.join(downloads_folder, "headshot.jpeg")

    result = stone.process(image_path, image_type="color", return_report_image=True)
    skin_tone = result['faces'][0]['skin_tone']

    rgb_color = tuple(int((skin_tone.lstrip('#'))[i:i+2], 16) for i in (0, 2, 4))

    return(rgb_color)
get_skin_tone("")