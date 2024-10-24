import gradio as gr #type: ignore
from google.cloud import vision
from PIL import Image
import io

def detect_properties(image_input):
    """Detects image properties in the file."""    

    client = vision.ImageAnnotatorClient()

    #convert cropped image to bytes so it can be utilized by google cloud vision
    b = io.BytesIO()
    image_input.save(b, 'jpeg')
    im_bytes = b.getvalue()

    #convert this to image processable by google cloud vision
    image = vision.Image(content=im_bytes)

    #find the most dominant color
    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    # print("Properties:")

    #sort it by percentage of pixels
    props.dominant_colors.colors.sort(key=lambda x: x.pixel_fraction, reverse=True)

    #output all the pixels
    # for color in props.dominant_colors.colors:
    #     print(f"fraction: {color.pixel_fraction}")
    #     print(f"\tr: {color.color.red}")
    #     print(f"\tg: {color.color.green}")
    #     print(f"\tb: {color.color.blue}")
    #     print(f"\ta: {color.color.alpha}")

    #if errors
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    #NEED TO CHANGE THIS (because of background)
    return(props.dominant_colors.colors[0])