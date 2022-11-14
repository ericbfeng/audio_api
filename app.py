from flask import Flask, send_from_directory, request, make_response
from werkzeug.utils import secure_filename
from tinytag import TinyTag
import base64
import os
import io
import json


app = Flask(__name__)

@app.route("/post",methods = ['POST'])
def upload_wav():
    Binaryfile = request.get_data()
    file = io.BytesIO(Binaryfile)
    if not os.path.exists("upload"):
         os.mkdir("upload")
    upload = os.listdir('upload')
    file_name = "audio" + str(len(upload)) + ".wav" #no methods to delete so can arbitrarily name it as so:
    with open("upload/" + file_name, mode='bx') as file:
        file.write(Binaryfile)
    return "Your audio has been saved as " + file_name, 200


@app.route("/download",methods = ['GET'])
def download():
    if "name" not in request.args:
        return "provide name", 400
    name = request.args["name"]
    if not os.path.exists("upload"):
         os.mkdir("upload")
    uploaded = os.listdir('upload')
    if name in uploaded:
        response = make_response()
        with open('upload/'+ name, 'br') as f:
            contents = f.read()
        response.data = json.dumps({"encoding_type" : "base64", "data": str(base64.b64encode(contents))})
        response.headers['Content-Type'] = 'JSON'
        return response
    else:
        return "filename not found", 404



@app.route("/list",methods = ['GET'])
def list_audios():
    if "maxduration" not in request.args:
        return "please provide max duration", 400
    max_runtime = int(request.args["maxduration"])
    if not os.path.exists("upload"):
        os.mkdir("upload")
    uploaded = os.listdir('upload')
    names = []
    duration = []
    response = make_response()
    for name in uploaded:
        file_name = "upload/" + name 
        tag = TinyTag.get(file_name)
        if tag.duration <= max_runtime:
            names.append(name)
            duration.append(tag.duration)
    response.data  = json.dumps({"names": names, "durations": duration})
    response.headers['Content-Type'] = 'JSON'
    return response 
    

@app.route("/info",methods = ['GET'])
def info():
    if "name" not in request.args:
        return "provide name", 400
    if not os.path.exists("upload"):
        os.mkdir("upload")
    uploaded = os.listdir('upload')
    name = request.args["name"]
    if name in uploaded:
        response = make_response()
        file_name = "upload/" + name
        tag = TinyTag.get(file_name)
        response.data = json.dumps({
            "title": tag.title,
            "artist": tag.artist,
            "duration": tag.duration,
            "filesize": tag.filesize,
        });
        response.headers['Content-Type'] = 'JSON'
        return response
    else:
        return "filename not found", 404

    
if __name__ == '__main__':
    app.run(host="localhost", port = 80, debug=True)
