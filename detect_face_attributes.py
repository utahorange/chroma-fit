from google.cloud import vision
from PIL import Image
import os

def detect_attributes(image_path):
    # downloads_folder = os.path.join(os.path.expanduser("~"), "Desktop") # this part will change based on how we implement our image upload later
    # image_path = os.path.join(downloads_folder, "myface")
    # print(image_path)

    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    face = response.face_annotations
    face_landmarks = face[0].landmarks

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
 
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )

    face_vertices = [
        (vertex.x,vertex.y) for vertex in face[0].bounding_poly.vertices
    ]

    print(face_vertices)
    original_img = Image.open(image_path)

    face_img = original_img.crop((face_vertices[0][0],face_vertices[1][1],face_vertices[1][0],face_vertices[2][1])) # (left, upper, right, lower)

    # ---- to work on here ---

    # right_eye_img = original_img.crop()
    # left_eye_img = original_img.crop()

    # print(face_landmarks)
    
    return(vertices)
