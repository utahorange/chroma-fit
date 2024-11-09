from flask import Flask
app = Flask(__name__)
@app.route('/api/ml')

def upload_image():
    # print("hehe")
    return({'skin_primary_color' : 128}) 