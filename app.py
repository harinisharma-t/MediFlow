import os
import json

from flask import Flask, render_template, request

from services.ai_service import (
    extract_text_from_image,
    extract_medical_information
)

from database.db import (
    create_database,
    save_document
)

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create the database when the app starts
create_database()


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

    # OCR
    ocr_text = extract_text_from_image(save_path)

    # AI Extraction
    document = extract_medical_information(
        ocr_text,
        patient_id
    )

    # Save to database
    save_document(document)

    return render_template(
        "result.html",
        document=document
    )


if __name__ == "__main__":
    app.run(debug=True)