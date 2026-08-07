import os
import tempfile

from flask import Flask, render_template, request, send_file, redirect, url_for

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from services.ai_service import (
    extract_text_from_image,
    extract_medical_information
)

from services.timeline_service import (
    get_patient_timeline
)

from services.safety_service import (
    check_duplicate_medications,
    check_drug_interactions
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
    get_recent_documents,
    patient_exists,
    get_patient_summary,
    get_patient_documents,
    compare_patient_prescriptions,
    get_top_diagnosis,
    get_top_medicine,
    get_upcoming_followups
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
        recent_patients=get_recent_patients(),
        recent_documents=get_recent_documents(),
        top_diagnosis=get_top_diagnosis(),
        top_medicine=get_top_medicine()
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

    # Duplicate medicines
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

    # Drug interactions
    interaction_warnings = check_drug_interactions(
        document["drug_name"]
    )

    for interaction in interaction_warnings:

        save_flag(
            patient_id,
            document_id,
            "Drug Interaction",
            f"{interaction['drug1']} + {interaction['drug2']}: {interaction['warning']}"
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
# AI Patient Summary
# =====================================================

@app.route("/summary/<patient_id>")
def patient_summary(patient_id):

    summary = get_patient_summary(patient_id)
    documents = get_patient_documents(patient_id)
    flags = get_flags(patient_id)

    return render_template(
        "summary.html",
        patient_id=patient_id,
        summary=summary,
        documents=documents,
        flags=flags
    )

# =====================================================
# Follow-up Reminders
# =====================================================

@app.route("/followups")
def followups():

    reminders = get_upcoming_followups()

    return render_template(
        "followups.html",
        reminders=reminders
    )

# =====================================================
# Export Patient History as PDF
# =====================================================

@app.route("/export/<patient_id>")
def export_patient_pdf(patient_id):

    summary = get_patient_summary(patient_id)
    documents = get_patient_documents(patient_id)

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    pdf = SimpleDocTemplate(temp_file.name)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>MediFlow Patient Report</b>",
            styles["Heading1"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Patient ID:</b> {patient_id}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Total Documents:</b> {summary['total_documents']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Total Safety Alerts:</b> {summary['total_flags']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph("<br/>", styles["Normal"])
    )

    for document in documents:

        elements.append(
            Paragraph(
                f"<b>Date:</b> {document['date']}",
                styles["Heading3"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Diagnosis:</b> {document['diagnosis']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Doctor:</b> {document['doctor_name']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Hospital:</b> {document['hospital']}",
                styles["Normal"]
            )
        )

        medicines = ", ".join(document["drug_name"])

        elements.append(
            Paragraph(
                f"<b>Medicines:</b> {medicines}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph("<br/>", styles["Normal"])
        )

    pdf.build(elements)

    return send_file(
        temp_file.name,
        as_attachment=True,
        download_name=f"{patient_id}_report.pdf"
    )

# =====================================================
# Run Application
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)