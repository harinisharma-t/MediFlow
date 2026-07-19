import os

from flask import Flask, render_template, request, jsonify

from services.ai_service import (
    extract_text_from_image,
    extract_medical_information
)

from services.timeline_service import (
    get_patient_timeline
)

from services.safety_service import (
    check_duplicate_medications
)

from database.db import (
    create_database,
    save_document,
    save_flag
)

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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

    # Save document
    document_id = save_document(document)

    # Duplicate Medication Check
    duplicate_drugs = check_duplicate_medications(
        patient_id,
        document
    )

    for drug in duplicate_drugs:

        save_flag(
            patient_id,
            document_id,
            "Duplicate Medication",
            f"{drug} already exists in previous prescriptions."
        )

    return render_template(
        "result.html",
        document=document
    )


@app.route("/timeline/<patient_id>")
def patient_timeline(patient_id):

    timeline = get_patient_timeline(patient_id)

    return render_template(
        "timeline.html",
        patient_id=patient_id,
        timeline=timeline
    )


@app.route("/timeline-json/<patient_id>")
def patient_timeline_json(patient_id):

    timeline = get_patient_timeline(patient_id)

    return jsonify(timeline)


if __name__ == "__main__":
    app.run(debug=True)