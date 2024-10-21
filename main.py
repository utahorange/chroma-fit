import gradio as gr
import detect_face_attributes

def upload_image(image):
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

# call detect_face_attributes, pictures of just face w white bg, just eyes, etc created

# gcloud api dominant color determined for face, eyes, etc

# color analysis done w api's
