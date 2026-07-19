# MediFlow

MediFlow is an AI-powered medical document analysis system that extracts structured information from medical prescriptions using OCR and a Large Language Model. The application stores patient records, generates a chronological medical timeline, and identifies duplicate medications to assist in safer clinical decision-making.

---

## Overview

The system enables users to upload prescription images, automatically extracts medical information, and organizes patient history into a structured database. It also includes a medication safety module that detects duplicate prescriptions and displays alerts through a dedicated dashboard.

---

## Features

- Upload prescription images
- OCR-based text extraction using Tesseract
- AI-powered medical information extraction using NVIDIA Llama API
- Structured storage of patient records using SQLite
- Patient timeline with chronological medical history
- Duplicate medication detection
- Safety dashboard for medication alerts
- Responsive web interface built with Bootstrap

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| Backend | Python, Flask |
| AI | NVIDIA Llama 3.1 API |
| OCR | Tesseract OCR |
| Database | SQLite |
| Frontend | HTML, Bootstrap 5 |
| Version Control | Git, GitHub |

---

## Project Structure

```text
MediFlow/
│
├── app.py
├── requirements.txt
├── .gitignore
├── database/
│   ├── db.py
│   └── mediflow.db
│
├── services/
│   ├── ai_service.py
│   ├── safety_service.py
│   └── timeline_service.py
│
├── templates/
│   ├── upload.html
│   ├── result.html
│   ├── timeline.html
│   └── safety.html
│
├── uploads/
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/MediFlow.git
```

Navigate to the project directory:

```bash
cd MediFlow
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your NVIDIA API key:

```env
NVIDIA_API_KEY=your_api_key
```

Run the application:

```bash
python app.py
```

Open the application in your browser:

```
http://127.0.0.1:5000
```

---

## Application Workflow

1. Upload a prescription image.
2. Extract text using Tesseract OCR.
3. Process the extracted text using the NVIDIA Llama model.
4. Store structured medical information in SQLite.
5. Display the extracted report.
6. Generate the patient's medical timeline.
7. Detect duplicate medications.
8. Display medication safety alerts.

---

## Current Modules

- Medical Document Upload
- OCR Pipeline
- AI Information Extraction
- Patient Timeline
- Duplicate Medication Detection
- Safety Dashboard

---

## Future Enhancements

- Drug-drug interaction detection
- Duplicate diagnostic test detection
- PDF report generation
- Patient authentication
- Doctor dashboard
- Cloud deployment
- Electronic Health Record (EHR) integration

---

## License

This project was developed for educational and hackathon purposes.

---

## Author

**Harini T**

Artificial Intelligence and Machine Learning Engineering Student