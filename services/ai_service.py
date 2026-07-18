import os

from dotenv import load_dotenv
from openai import OpenAI

# Load variables from the .env file
load_dotenv()

# Create the NVIDIA client
client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

def test_connection():
    response = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: MediFlow setup successful."
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    print(test_connection())