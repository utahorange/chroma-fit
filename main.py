import gradio as gr #type: ignore
import detect_face_attributes
import detect_primary_color
import skin_tone
import os
from PIL import Image
from pillow_heif import register_heif_opener #type: ignore

def upload_image(face_image): 
    # image uploaded
    if(not image.endswith("jpeg")):
        if(image.endswith("heic")): 
            register_heif_opener()
            image.save(filepath, format='jpeg')
        else:
            print("file type is not jpeg")

    tmp = detect_primary_color.detect_properties(image)
    return([skin_tone.get_skin_tone(image), tmp[0],tmp[1]]) # returns a tuple of rgb color

# Create Gradio interface
interface = gr.Interface(
    fn=upload_image,  # The function to process the uploaded image
    inputs=gr.Image(type='filepath'),  # Input is an image file
    outputs="image",  # Output is also displayed as an image
    title="Simple Image Uploader",
    description="Upload an image file and display it below."
)

# Launch the interface
interface.launch()