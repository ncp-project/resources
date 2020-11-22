from flask import Flask,request
from PIL import Image
import OCR
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['POST'])
def welcome():
    
    uid = uuid.uuid4()
    f =request.files['file']
    file_name = uid.hex+f.filename
    f.save(secure_filename(file_name))
    img = cv2.imread(file_name,0)
    os.remove(file_name)
    return OCR.detect(img)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)