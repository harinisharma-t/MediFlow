import os

from flask import Flask, render_template, request, redirect, url_for

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
    save_flag,
    get_flags,
    get_total_patients,
    get_total_documents,
    get_total_flags,
    get_recent_patients,
    patient_exists,
    get_patient_summary,
    get_patient_documents,
    compare_patient_prescriptions
)

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

create_database()


# =====================================================
# Dashboard
# =====================================================

@app.route("/")
def home():

    return render_template(
        "dashboard.html",
        total_patients=get_total_patients(),
        total_documents=get_total_documents(),
        total_flags=get_total_flags(),
        recent_patients=get_recent_patients()
    )


# =====================================================
# Search Patient
# =====================================================

@app.route("/search", methods=["POST"])
def search_patient():

    patient_id = request.form["patient_id"].strip()

    if patient_exists(patient_id):
        return redirect(url_for("patient_profile", patient_id=patient_id))

    return render_template(
        "dashboard.html",
        total_patients=get_total_patients(),
        total_documents=get_total_documents(),
        total_flags=get_total_flags(),
        recent_patients=get_recent_patients(),
        error="Patient not found."
    )


# =====================================================
# Patient Profile
# =====================================================

@app.route("/patient/<patient_id>")
def patient_profile(patient_id):

    summary = get_patient_summary(patient_id)

    if summary is None:
        return "Patient not found."

    return render_template(
        "patient_profile.html",
        summary=summary
    )

# =====================================================
# Document History
# =====================================================

@app.route("/documents/<patient_id>")
def document_history(patient_id):

    diagnosis = request.args.get("diagnosis", "").strip()

    document_type = request.args.get("type", "").strip()

    medicine = request.args.get("medicine", "").strip()

    sort = request.args.get("sort", "desc")

    documents = get_patient_documents(
        patient_id,
        diagnosis,
        document_type,
        medicine,
        sort
    )

    return render_template(
        "document_history.html",
        patient_id=patient_id,
        documents=documents
    )

# =====================================================
# Compare Prescriptions
# =====================================================

@app.route("/compare/<patient_id>")
def compare_prescriptions(patient_id):

    comparison = compare_patient_prescriptions(patient_id)

    return render_template(
        "compare.html",
        patient_id=patient_id,
        comparison=comparison
    )

# =====================================================
# Upload Page
# =====================================================

@app.route("/upload-page")
def upload_page():
    return render_template("upload.html")




# =====================================================
# Upload Prescription
# =====================================================

@app.route("/upload", methods=["POST"])
def upload_file():

    patient_id = request.form["patient"]

    uploaded_file = request.files["document"]

    if uploaded_file.filename == "":
        return "No file selected."

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    save_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        uploaded_file.filename
    )

    uploaded_file.save(save_path)

    ocr_text = extract_text_from_image(save_path)

    document = extract_medical_information(
        ocr_text,
        patient_id
    )

    document_id = save_document(document)

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

    return redirect(
    url_for(
        "patient_profile",
        patient_id=patient_id
    )
)


# =====================================================
# Timeline
# =====================================================

@app.route("/timeline/<patient_id>")
def patient_timeline(patient_id):

    timeline = get_patient_timeline(patient_id)

    return render_template(
        "timeline.html",
        patient_id=patient_id,
        timeline=timeline
    )


# =====================================================
# Safety Dashboard
# =====================================================

@app.route("/safety/<patient_id>")
def safety_dashboard(patient_id):

    flags = get_flags(patient_id)

    return render_template(
        "safety.html",
        patient_id=patient_id,
        flags=flags
    )


# =====================================================
# Run Application
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)