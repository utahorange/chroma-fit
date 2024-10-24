import gradio as gr #type: ignore
import detect_face_attributes
import detect_primary_color
import skin_tone
import color
import os
from PIL import Image
from pillow_heif import register_heif_opener #type: ignore

def upload_image(face_image): 
    print("Generating colors...")
    # image uploaded
    # if(not face_image.endswith("jpeg")):
    #     if(face_image.endswith("heic")): 
    #         register_heif_opener()
    #         face_image.save(filepath, format='jpeg')
    #     else:
    #         print("file type is not jpeg")
    
    # call detect_face_attributes, pictures of just face w white bg, just eyes, etc created
    left_eye_image, right_eye_image, lip_image = detect_face_attributes.detect_attributes(face_image)
    
    # gcloud api dominant color determined for face, eyes, etc
    skin_primary_color = skin_tone.get_skin_tone(face_image)
    left_eye_primary_color = detect_primary_color.detect_properties(left_eye_image)
    right_eye_primary_color = detect_primary_color.detect_properties(right_eye_image)
    lip_primary_color = detect_primary_color.detect_properties(lip_image)

    average_eye_rgb = ((left_eye_primary_color.color.red + right_eye_primary_color.color.red)/2, (left_eye_primary_color.color.green + right_eye_primary_color.color.green)/2, (left_eye_primary_color.color.blue + right_eye_primary_color.color.blue)/2)
    lip_rgb = (lip_primary_color.color.red, lip_primary_color.color.green, lip_primary_color.color.blue)
    print(skin_primary_color, average_eye_rgb, lip_rgb)

    # color analysis done w api's
    return(color.gradio_interface(skin_primary_color, average_eye_rgb, lip_rgb))

    # return(face_image)

# Create Gradio interface
interface = gr.Interface(
    fn=upload_image,  # The function to process the uploaded image
    inputs=gr.Image(type='filepath'),  # Input is an image file
    outputs=gr.HTML(label="Generated Color Palettes"),  # Output is also displayed as an image
    title="ChromaFit",
    description="Upload an image to see your color analysis!",
    flagging_mode="never"
)

# Launch the interface
interface.launch(share=True)