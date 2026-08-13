# MediFlow

MediFlow is an AI-powered healthcare navigation application designed to organize, understand, and monitor patient medical information in one place.

## Features

- Medical document upload
- OCR-based text extraction
- AI-powered medical information extraction
- Patient profile management
- Medical document history
- Patient medical timeline
- Prescription comparison
- Duplicate medication detection
- Drug interaction alerts
- AI patient summary
- Follow-up reminders
- Patient history PDF export
- Dashboard analytics
- Responsive web interface

## Tech Stack

### Backend
- Python
- Flask
- SQLite

### AI & Medical Processing
- OCR
- Pytesseract
- AI-based medical information extraction

### Frontend
- HTML
- CSS
- Bootstrap
- Jinja2

### PDF Generation
- ReportLab

## Project Structure

```text
MediFlow/
│
├── app.py
├── database/
│   └── db.py
│
├── services/
│   ├── ai_service.py
│   ├── safety_service.py
│   └── timeline_service.py
│
├── templates/
│   ├── dashboard.html
│   ├── patient_profile.html
│   ├── document_history.html
│   ├── timeline.html
│   ├── safety.html
│   ├── compare.html
│   ├── summary.html
│   └── followups.html
│
├── static/
│   └── style.css
│
├── uploads/
├── database/
└── README.md

## Development Progress

MediFlow is being developed incrementally with regular testing and feature improvements.

Current modules include:

- Patient management
- Medical document processing
- Medical timeline
- Prescription comparison
- Medication safety checks
- AI patient summaries
- Follow-up reminders
- PDF report generation
- Dashboard analytics