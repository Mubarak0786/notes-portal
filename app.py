from flask import Flask, render_template, request, redirect, send_file
from models import db, Student, Note
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

UPLOAD_FOLDER = "static/notes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    notes = Note.query.all()
    return render_template("index.html", notes=notes)

@app.route("/enroll", methods=["POST"])
def enroll():
    name = request.form["name"]
    email = request.form["email"]

    student = Student(name=name, email=email)
    db.session.add(student)
    db.session.commit()

    return redirect("/")

@app.route("/upload", methods=["POST"])
def upload_note():
    title = request.form["title"]
    file = request.files["file"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    note = Note(title=title, filename=file.filename)
    db.session.add(note)
    db.session.commit()

    return redirect("/")

@app.route("/download/<id>")
def download(id):
    note = Note.query.get(id)
    filepath = os.path.join(UPLOAD_FOLDER, note.filename)
    return send_file(filepath, as_attachment=True)

@app.route("/delete/<id>")
def delete(id):
    note = Note.query.get(id)
    path = os.path.join(UPLOAD_FOLDER, note.filename)

    if os.path.exists(path):
        os.remove(path)

    db.session.delete(note)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
