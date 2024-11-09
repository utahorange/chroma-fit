import cv2
import mediapipe as mp
from PIL import Image, ImageDraw
from google.cloud import vision
import numpy as np
import os

import matplotlib.pyplot as plt

# Convert landmark points to pixel coordinates
def landmark_to_pixel(landmark, img_width, img_height):
    return int(landmark.x * img_width), int(landmark.y * img_height)
    
def detect_attributes(image_path):
    return(50,50,50)
    # Initialize MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

    # # Read the image using OpenCV
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_height, img_width = img.shape[:2]

    # Process the image and detect face landmarks
    results = face_mesh.process(img_rgb)
    
    if not results.multi_face_landmarks:
        print("No faces detected.")
        return None, None, None
    
    # # Open the image using PIL to crop and display
    img_pil = Image.open(image_path)

    # # Get the landmarks for the first detected face
    landmarks = results.multi_face_landmarks[0].landmark
    
    # # Indices for upper and lower lip landmarks (user-specified)
    upper_lip_points = [
    landmarks[76], landmarks[61], landmarks[185], landmarks[40], landmarks[39],
    landmarks[37], landmarks[0], landmarks[267], landmarks[269], landmarks[270], 
    landmarks[409], landmarks[291], landmarks[307], landmarks[408], landmarks[304],
    landmarks[303], landmarks[302], landmarks[11], landmarks[72], landmarks[73],
    landmarks[74], landmarks[184]
    ]

    lower_lip_points = [
        landmarks[76], landmarks[61], landmarks[146], landmarks[91], landmarks[181], 
        landmarks[84], landmarks[17], landmarks[314], landmarks[405], landmarks[321], 
        landmarks[375], landmarks[291], landmarks[306], landmarks[307], landmarks[320], 
        landmarks[404], landmarks[315], landmarks[16], landmarks[85], landmarks[180], 
        landmarks[90], landmarks[77]
    ]
   
    # # Combine upper and lower lip points
    lip_points = upper_lip_points + lower_lip_points

    # Convert lip points to pixel coordinates
    lip_pixel_coords = [landmark_to_pixel(point, img_width, img_height) for point in lip_points]

    # # Create a mask for the lips
    mask = np.zeros((img_height, img_width), dtype=np.uint8)
    lip_contour = np.array(lip_pixel_coords, dtype=np.int32)
    cv2.fillPoly(mask, [lip_contour], 255)

    # Apply the mask to the image to isolate the lips
    lips_only = cv2.bitwise_and(img, img, mask=mask)

    # Crop the lips based on the bounding box of the lip points
    x, y, w, h = cv2.boundingRect(lip_contour)
    cropped_lips = lips_only[y:y+h, x:x+w]
    cropped_mask = mask[y:y+h, x:x+w]

    # Convert cropped image to RGBA (4 channels: R, G, B, A)
    cropped_lips_rgba = cv2.cvtColor(cropped_lips, cv2.COLOR_BGR2RGBA)

    # Set the alpha channel (A) to be the cropped mask
    cropped_lips_rgba[:, :, 3] = cropped_mask

    # Convert the result to a PIL image for easier display and saving
    cropped_lips = Image.fromarray(cropped_lips_rgba)
    
    #transparent_image.show()
    
    # # Google Cloud Vision API for eyes
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations

    if not faces:
        print("No faces detected with Vision API.")
        return cropped_lips, None, None

    # # Use the first detected face
    face = faces[0]

    # # Get coordinates for eye facial landmarks
    left_eye = face.landmarks[0].position  # LEFT_EYE
    right_eye = face.landmarks[1].position  # RIGHT_EYE

    # # Crop left eye, right eye
    eye_radius = 7  # Define a radius to crop around the eye

    def crop_region_eye(center, width, height, left_offset=0):
        left = int(center.x) - width // 2 - left_offset
        upper = int(center.y) - height // 2
        right = int(center.x) + width // 2
        lower = int(center.y) + height // 2
        return (left, upper, right, lower)

    # # Crop regions for eyes
    left_eye_box = crop_region_eye(left_eye, eye_radius * 2, eye_radius * 2)
    right_eye_box = crop_region_eye(right_eye, eye_radius * 2, eye_radius * 2)

    # # Crop the eyes
    cropped_left_eye = img_pil.crop(left_eye_box)
    cropped_right_eye = img_pil.crop(right_eye_box)

    # Return the three cropped images: lips, left eye, and right eye

    # cropped_left_eye = 1
    # cropped_right_eye = 1
    # cropped_lips = 1
    return cropped_left_eye, cropped_right_eye, cropped_lips



#testing
# cropped_lips, cropped_left_eye, cropped_right_eye = detect_attributes("/Users/yashagarwal/Downloads/taiyu_headshot.jpg")

