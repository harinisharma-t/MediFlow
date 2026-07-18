import os
import json

import pytesseract
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Tell Python where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Create NVIDIA client
client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)


def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def extract_medical_information(ocr_text):

    prompt = f"""
You are a medical document extraction assistant.

Read the following OCR text from a prescription or medical report.

Return ONLY valid JSON.

Use exactly this schema:

{{
    "patient_id": "",
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

    return response.choices[0].message.content


if __name__ == "__main__":

    sample_image = "uploads/sample_prescription.png"

    if not os.path.exists(sample_image):
        print("Sample image not found.")
        exit()

    print("Reading image with OCR...\n")

    ocr_text = extract_text_from_image(sample_image)

    print("OCR COMPLETE\n")

    print("Sending text to NVIDIA AI...\n")

    ai_result = extract_medical_information(ocr_text)

    print("AI RESPONSE\n")

    print(ai_result)