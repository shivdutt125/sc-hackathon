from flask import Flask, request
import base64
from io import BytesIO
import drowsiness_detection as ds
import urllib
import random
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/isDrowsy", methods = ['POST'])
@cross_origin()
def isDrowsy():
    data = request.json
    uri = data["dataURI"]
    response = urllib.request.urlopen(uri)
    filePath = "image" + str(random.randint(1,100)) + ".jpg"
    with open(filePath, 'wb') as f:
        f.write(response.file.read())
    val =  ds.isDrowsy(filePath)
    os.remove(filePath)
    return str(val)
    
