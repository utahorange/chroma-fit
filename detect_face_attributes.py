import cv2
import mediapipe as mp
from PIL import Image
from google.cloud import vision
from PIL import Image
import os
import matplotlib.pyplot as plt

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

def detect_attributes(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the image and detect face landmarks
    results = face_mesh.process(img_rgb)
    
    if not results.multi_face_landmarks:
        print("No faces detected.")
        return
    
    # Open the image using PIL to crop and display
    img_pil = Image.open(image_path)

    for i, face_landmarks in enumerate(results.multi_face_landmarks):
        print(f'Face {i + 1} detected:')
        
        # Get coordinates for facial landmarks
        landmarks = face_landmarks.landmark
        print(landmarks)
        
        
           
    # Define indices for the specified lip landmarks
    upper_lip_top_left_index = 185
    upper_lip_top_right_index = 409
    lower_lip_bottom_left_index = 375
    lower_lip_bottom_right_index = 146

    # Additional indices for top and bottom lip
    top_lip_index = 0
    bottom_lip_index = 17

    # Get the landmarks for the specified lip points
    upper_lip_top_left = landmarks[upper_lip_top_left_index]
    upper_lip_top_right = landmarks[upper_lip_top_right_index]
    lower_lip_bottom_left = landmarks[lower_lip_bottom_left_index]
    lower_lip_bottom_right = landmarks[lower_lip_bottom_right_index]

    # Get coordinates for the top and bottom lip landmarks
    top_lip = landmarks[top_lip_index]
    bottom_lip = landmarks[bottom_lip_index]

    # Print coordinates for the selected lip landmarks
    print('Lips:')
    print(f'  Upper Lip Top Left: ({upper_lip_top_left.x}, {upper_lip_top_left.y})')
    print(f'  Upper Lip Top Right: ({upper_lip_top_right.x}, {upper_lip_top_right.y})')
    print(f'  Lower Lip Bottom Left: ({lower_lip_bottom_left.x}, {lower_lip_bottom_left.y})')
    print(f'  Lower Lip Bottom Right: ({lower_lip_bottom_right.x}, {lower_lip_bottom_right.y})')
    print(f'  Top Lip: ({top_lip.x}, {top_lip.y})')
    print(f'  Bottom Lip: ({bottom_lip.x}, {bottom_lip.y})')

    # Calculate the bounding box for the lips
    img_height, img_width, _ = img.shape

    def get_crop_box_lips(upper_left, upper_right, lower_left, lower_right, top_lip, bottom_lip, img_width, img_height):
        x_min = int(min(upper_left.x, upper_right.x, lower_left.x, lower_right.x) * img_width)
        x_max = int(max(upper_left.x, upper_right.x, lower_left.x, lower_right.x) * img_width)
        y_min = int(top_lip.y * img_height)  # Use the y-coordinate of the top lip landmark
        y_max = int(bottom_lip.y * img_height)  # Use the y-coordinate of the bottom lip landmark
        
        return (x_min, y_min, x_max, y_max)

    # Get the crop box for the lips
    lip_box = get_crop_box_lips(
        upper_lip_top_left, 
        upper_lip_top_right, 
        lower_lip_bottom_left, 
        lower_lip_bottom_right, 
        top_lip, 
        bottom_lip,
        img_width, 
        img_height
    )

    # Crop lips using the calculated bounding box
    cropped_lips = img_pil.crop(lip_box)

    # Display the cropped images
    cropped_lips.show(title="Cropped Lips")
    
    
    
    
    
    # Assuming 'img' is your original image in BGR format (as used by OpenCV)
    # Create a copy of the original image to overlay points
    overlay_img = img.copy()

    # Define the indices for all lip landmarks
    lip_indices = [185, 408, 375, 146] 

    # Loop through each landmark index to draw a red circle
    for i in lip_indices:
        landmark = landmarks[i]
        x = int(landmark.x * img.shape[1])  # Width of the image
        y = int(landmark.y * img.shape[0])  # Height of the image

        # Draw a red circle on the overlay image
        cv2.circle(overlay_img, (x, y), 5, (0, 0, 255), -1)  # Circle with radius 5

    # Convert the overlay image to RGB format for display (if using matplotlib or PIL)
    overlay_img_rgb = cv2.cvtColor(overlay_img, cv2.COLOR_BGR2RGB)


    plt.imshow(overlay_img_rgb)
    plt.axis('off')  # Hide axes
    plt.title("Lip Points Overlay")
    plt.show()
    
    
    
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()


    #google cloud vision API for eyes
    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations
    if not faces:
        print("No faces detected.")
        return

    # Open the image using PIL to crop and display
    img = Image.open(image_path)

    for i, face in enumerate(faces):
        print(f'Face {i+1} detected:')

        # Get coordinates for eye facial landmarks
        left_eye = face.landmarks[0].position  # LEFT_EYE
        right_eye = face.landmarks[1].position  # RIGHT_EYE

        # Print eye coordinates
        print('Eyes:')
        print(f'  Left Eye: ({left_eye.x}, {left_eye.y})')
        print(f'  Right Eye: ({right_eye.x}, {right_eye.y})')

    
        # Crop left eye, right eye
        eye_radius = 7  # Define a radius to crop around the eye

        def crop_region_eye(center, width, height, left_offset=0):
            # Calculate the crop box (left, upper, right, lower)
            left = int(center.x) - width // 2 - left_offset  # Extend left
            upper = int(center.y) - height // 2
            right = int(center.x) + width // 2
            lower = int(center.y) + height // 2
            return (left, upper, right, lower)

        # Crop regions for eyes
        left_eye_box = crop_region_eye(left_eye, eye_radius * 2, eye_radius * 2)
        right_eye_box = crop_region_eye(right_eye, eye_radius * 2, eye_radius * 2)
       

        # Crop and show the eyes
        cropped_left_eye = img.crop(left_eye_box)
        cropped_right_eye = img.crop(right_eye_box)
        

        # Display the cropped images
        cropped_left_eye.show(title="Cropped Left Eye")
        cropped_right_eye.show(title="Cropped Right Eye")
       

        # Optionally, save the cropped images
        #cropped_left_eye.save(f"cropped_left_eye_face_{i+1}.jpg")
        #cropped_right_eye.save(f"cropped_right_eye_face_{i+1}.jpg")
        

    # Check for errors
    if response.error.message:
        raise Exception(f'{response.error.message}')

if __name__ == '__main__':
    image_path = '/Users/yashagarwal/Downloads/taiyu_headshot.jpg'
    detect_attributes(image_path)