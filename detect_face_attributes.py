import cv2
import mediapipe as mp
from PIL import Image
from google.cloud import vision
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
        return None, None, None
    
    # Open the image using PIL to crop and display
    img_pil = Image.open(image_path)

    # Get the landmarks for the first detected face
    landmarks = results.multi_face_landmarks[0].landmark
    
    # Define indices for the specified lip landmarks
    upper_lip_top_left_index = 185
    upper_lip_top_right_index = 409
    lower_lip_bottom_left_index = 375
    lower_lip_bottom_right_index = 146
    top_lip_index = 0
    bottom_lip_index = 17

    # Get the landmarks for the specified lip points
    upper_lip_top_left = landmarks[upper_lip_top_left_index]
    upper_lip_top_right = landmarks[upper_lip_top_right_index]
    lower_lip_bottom_left = landmarks[lower_lip_bottom_left_index]
    lower_lip_bottom_right = landmarks[lower_lip_bottom_right_index]
    top_lip = landmarks[top_lip_index]
    bottom_lip = landmarks[bottom_lip_index]

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

    # Google Cloud Vision API for eyes
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations

    if not faces:
        print("No faces detected with Vision API.")
        return cropped_lips, None, None

    # Use the first detected face
    face = faces[0]

    # Get coordinates for eye facial landmarks
    left_eye = face.landmarks[0].position  # LEFT_EYE
    right_eye = face.landmarks[1].position  # RIGHT_EYE

    # Crop left eye, right eye
    eye_radius = 7  # Define a radius to crop around the eye

    def crop_region_eye(center, width, height, left_offset=0):
        left = int(center.x) - width // 2 - left_offset
        upper = int(center.y) - height // 2
        right = int(center.x) + width // 2
        lower = int(center.y) + height // 2
        return (left, upper, right, lower)

    # Crop regions for eyes
    left_eye_box = crop_region_eye(left_eye, eye_radius * 2, eye_radius * 2)
    right_eye_box = crop_region_eye(right_eye, eye_radius * 2, eye_radius * 2)

    # Crop the eyes
    cropped_left_eye = img_pil.crop(left_eye_box)
    cropped_right_eye = img_pil.crop(right_eye_box)

    # Return the three cropped images: lips, left eye, and right eye
    return cropped_lips, cropped_left_eye, cropped_right_eye



#testing
'''cropped_lips, cropped_left_eye, cropped_right_eye = detect_attributes("/Users/yashagarwal/Downloads/taiyu_headshot.jpg")

# Optionally, you can save the cropped images
if cropped_lips:
    cropped_lips.save("cropped_lips.jpg")
if cropped_left_eye:
    cropped_left_eye.save("cropped_left_eye.jpg")
if cropped_right_eye:
    cropped_right_eye.save("cropped_right_eye.jpg")'''

