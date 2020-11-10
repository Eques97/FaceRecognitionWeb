
from flask import Flask, render_template, request, redirect, url_for
import face_recognition
import numpy as np
import base64
import cv2
import os

def Base64ToImage(base64Image):
    decodedImage = base64.b64decode(base64Image)
    imageArray = np.frombuffer(decodedImage, dtype=np.uint8)
    return cv2.imdecode(imageArray, flags=cv2.IMREAD_COLOR)

def IsKnown(userName):
    knownNames = [os.path.splitext(name)[0] for name in os.listdir("users")]
    return True if userName in knownNames else False

def IsMatch(userName, userImage):
    knownImage = face_recognition.load_image_file("users/" + userName + ".png")
    knownEncodings = face_recognition.face_encodings(knownImage)
    unknownImage = Base64ToImage(userImage)
    unknownEncodings = face_recognition.face_encodings(unknownImage)
    return face_recognition.compare_faces(knownEncodings, unknownEncodings[0], tolerance=0.5)[0] if len(unknownEncodings) > 0 else False

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("signIn"))

@app.route("/signin")
def signIn():
    return render_template("SignIn.html")

@app.route("/signup")
def signUp():
    return render_template("SignUp.html")

@app.route("/user/<name>")
def welcomeUser(name):
   return render_template("User.html", name = name)

@app.route("/signincheck", methods = ["POST", "GET"])
def validateUser():
    if request.method == "POST":
        userName = request.form["name"]
        userImage = request.form["image"]
        if IsKnown(userName):
            if IsMatch(userName, userImage):
                print("match")
                return redirect(url_for("welcomeUser", name = userName))
            else:
                print("face doesn't match")
                return redirect(url_for("signIn"))
        else:
            print("username doesn't exist")
            return redirect(url_for("signIn"))

@app.route("/signupcheck", methods = ["POST", "GET"])
def approveUser():
    if request.method == "POST":
        userName = request.form["name"]
        userImage = request.form["image"]
        if IsKnown(userName):
            return redirect(url_for("signUp"))
        else:
            cv2.imwrite("users/" + userName + ".png", Base64ToImage(userImage))
            return redirect(url_for("welcomeUser", name = userName))

if __name__ == "__main__":
   app.run(debug = True)