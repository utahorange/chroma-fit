import gradio as gr #type: ignore
import detect_face_attributes
import detect_primary_color
import skin_tone
import os
from PIL import Image
from pillow_heif import register_heif_opener #type: ignore

def upload_image(face_image): 
    # image uploaded
    # if(not face_image.endswith("jpeg")):
    #     if(face_image.endswith("heic")): 
    #         register_heif_opener()
    #         face_image.save(filepath, format='jpeg')
    #     else:
    #         print("file type is not jpeg")
    
    # call detect_face_attributes, pictures of just face w white bg, just eyes, etc created
    # left_eye_image, right_eye_image, lip_image = detect_face_attributes(face_image)
    
    # gcloud api dominant color determined for face, eyes, etc
    # skin_primary_color = skin_tone.get_skin_tone(face_image)
    # left_eye_primary_color = detect_primary_color.detect_properties(left_eye_image)
    # right_eye_primary_color = detect_primary_color.detect_properties(right_eye_image)
    # lip_primary_color = detect_primary_color.detect_properties(lip_image)

    # color analysis done w api's


    return(face_image) # returns a tuple of rgb color

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
