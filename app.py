import os

from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_file():

    patient_id = request.form["patient"]

    uploaded_file = request.files["document"]

    if uploaded_file.filename == "":
        return "No file selected."

    save_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        uploaded_file.filename
    )

    uploaded_file.save(save_path)

    return f"""
    <h2>Upload Successful ✅</h2>

    <p><strong>Patient:</strong> {patient_id}</p>

    <p><strong>File:</strong> {uploaded_file.filename}</p>

    <a href="/">Upload Another Document</a>
    """


if __name__ == "__main__":
    app.run(debug=True)