from google.cloud import vision
from Pillow import Image
import os

downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads") # this part will change based on how we implement our image upload later
image_path = os.path.join(downloads_folder, "headshot.jpeg")
# print(image_path)

client = vision.ImageAnnotatorClient()

with open(image_path, "rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.face_detection(image=image)
face = response.face_annotations
face_landmarks = face[0].landmarks

# print(face_landmarks)

# Names of likelihood from google.cloud.vision.enums
likelihood_name = (
    "UNKNOWN",
    "VERY_UNLIKELY",
    "UNLIKELY",
    "POSSIBLE",
    "LIKELY",
    "VERY_LIKELY",
)

vertices = [
    f"({vertex.x},{vertex.y})" for vertex in face[0].bounding_poly.vertices
]

print("face bounds: {}".format(",".join(vertices)))

original_img = Image.open(image_path)
face_img = original_img.crop(vertices[3][0],vertices[3][1],vertices[2][0],vertices[2][1]) # last coord first, 2nd one second
# right_eye_img = original_img.crop()
# left_eye_img = original_img.crop()

print(face_landmarks)

if response.error.message:
    raise Exception(
        "{}\nFor more info on error messages, check: "
        "https://cloud.google.com/apis/design/errors".format(response.error.message)
    )
