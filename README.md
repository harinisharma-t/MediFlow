# MediFlow

MediFlow is an AI-powered clinical decision support system that analyzes medical prescriptions using Optical Character Recognition (OCR) and a Large Language Model (LLM). The application extracts structured medical information, maintains a patient's medical history, and identifies potential medication safety issues through an intuitive web interface.

---

## Project Overview

Healthcare professionals often manage multiple prescriptions for the same patient, making it difficult to quickly review previous medications and identify duplicate prescriptions.

MediFlow addresses this problem by:

- Extracting structured information from prescription images
- Maintaining a chronological patient timeline
- Detecting duplicate medications
- Displaying medication safety alerts
- Providing an easy-to-use web interface for medical record review

---

## Features

- Prescription image upload
- OCR-based text extraction using Tesseract OCR
- AI-powered medical information extraction using NVIDIA Llama API
- Structured patient record storage using SQLite
- Patient timeline visualization
- Duplicate medication detection
- Medication safety dashboard
- Responsive Bootstrap-based user interface

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| Backend | Python, Flask |
| AI Model | NVIDIA Llama 3.1 API |
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
├── README.md
├── .gitignore
│
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
└── static/
```

---

## Application Workflow

1. Upload a prescription image.
2. Extract text using Tesseract OCR.
3. Process the extracted text using the NVIDIA Llama model.
4. Store structured medical information in SQLite.
5. Generate a patient timeline.
6. Detect duplicate medications.
7. Display medication safety alerts.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/MediFlow.git
```

Navigate to the project folder:

```bash
cd MediFlow
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add:

```env
NVIDIA_API_KEY=your_api_key
```

Run the application:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

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

Harini T

Artificial Intelligence and Machine Learning Engineering Student