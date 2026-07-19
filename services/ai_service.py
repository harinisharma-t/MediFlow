import os
import json

import pytesseract
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)


def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def extract_medical_information(ocr_text, patient_id):

    prompt = f"""
You are a medical document extraction assistant.

Return ONLY valid JSON.

Schema:

{{
    "patient_id": "{patient_id}",
    "type": "",
    "drug_name": [],
    "dosage": [],
    "frequency": [],
    "diagnosis": "",
    "doctor_name": "",
    "hospital": "",
    "date": "",
    "follow_up_instructions": "",
    "raw_text": ""
}}

IMPORTANT:
- Use the patient_id exactly as provided in the schema.
- Do NOT extract or change the patient_id from the document.
- Return ONLY valid JSON.

OCR Text:

{ocr_text}
"""

    response = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    ai_text = response.choices[0].message.content.strip()

    document = json.loads(ai_text)

    # Always use the patient selected in the app
    document["patient_id"] = patient_id

    return document


if __name__ == "__main__":

    sample_image = "uploads/sample_prescription.png"

    ocr_text = extract_text_from_image(sample_image)

    result = extract_medical_information(
        ocr_text,
        "patient1"
    )

    print(result)