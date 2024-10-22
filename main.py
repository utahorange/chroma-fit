import gradio as gr #type: ignore
import detect_face_attributes
import detect_primary_color
import os
from PIL import Image
from pillow_heif import register_heif_opener #type: ignore

def upload_image(image): # WIP
    # image uploaded
    if(not image.endswith("jpeg")):
        if(image.endswith("heic")): 
            register_heif_opener()
            image.save(filepath, format='jpeg')
        else:
            print("file type is not jpeg")
    # call detect_face_attributes, pictures of just face w white bg, just eyes, etc created
    vertices = detect_face_attributes.detect_attributes(image)
    # need to save image to filepath

    # gcloud api dominant color determined for face, eyes, etc
    primary_color = detect_primary_color.detect_properties(image, vertices)
    # color analysis done w api's
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
