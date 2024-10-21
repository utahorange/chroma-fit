import gradio as gr

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

