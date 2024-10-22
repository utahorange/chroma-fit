import gradio as gr
import detect_face_attributes
import os
from PIL import Image
from pillow_heif import register_heif_opener

def upload_image(image): # WIP
    return image

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

# image uploaded

if(not image.endswith("jpeg")):
    if(image.endswith("heic")): 
        register_heif_opener()
        image.save(filepath, format='jpeg')
    else:
        print("file type is not jpeg")

# call detect_face_attributes, pictures of just face w white bg, just eyes, etc created

# need to save image to filepath
detect_face_attributes(filepath)

# gcloud api dominant color determined for face, eyes, etc

# color analysis done w api's
