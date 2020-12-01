
from flask import Flask, render_template, request, redirect, url_for, session
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
    assert len(knownEncodings) < 2 and len(knownEncodings) > 0
    unknownImage = Base64ToImage(userImage)
    unknownEncodings = face_recognition.face_encodings(unknownImage)
    return face_recognition.compare_faces(knownEncodings, unknownEncodings[0], tolerance=0.5)[0] if len(unknownEncodings) > 0 else False

app = Flask(__name__)
app.secret_key = "any random string"

@app.route("/")
def home():
    username = None
    if "username" in session:
        username = session["username"]
    return render_template("Home.html", username = username)

@app.route("/signin", methods = ["POST", "GET"])
def signIn():
    error = None
    if request.method == "POST":
        username = request.form["name"]
        userImage = request.form["image"]
        if IsKnown(username):
            if IsMatch(username, userImage):
                session["username"] = username
                return redirect(url_for("home"))
            else:
                error = "Face doesn't match!"
        else:
            error = "Username doesn't exist!"
    return render_template("SignIn.html", error = error)

@app.route("/signup", methods = ["POST", "GET"])
def signUp():
    error = None
    if request.method == "POST":
        username = request.form["name"]
        userImage = request.form["image"]
        if IsKnown(username):
            error = "Username already exists!"
        else:
            cv2.imwrite("users/" + username + ".png", Base64ToImage(userImage))
            session["username"] = username
            return redirect(url_for("home"))
    return render_template("SignUp.html", error = error)

@app.route("/signout")
def signOut():
    session.pop("username", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
   app.run(debug = True)