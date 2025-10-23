'''
This program tests the OpenAI to ensure the 
API Key is working properly.
'''

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": "Hello! Respond with 'OpenAI API working!'"}]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print("Error:", e)