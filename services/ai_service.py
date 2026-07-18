import os

import pytesseract
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Tell Python where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# NVIDIA NIM client
client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)


def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


if __name__ == "__main__":

    sample_image = "uploads/sample_prescription.png"

    if os.path.exists(sample_image):

        print("Reading text from image...\n")

        extracted_text = extract_text_from_image(sample_image)

        print(extracted_text)

    else:

        print("sample_prescription.png not found inside uploads folder.")