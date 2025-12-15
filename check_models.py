import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

print("🔍 Checking available models with your API key...\n")

# List all available models
for model in genai.list_models():
    print(f"Model: {model.name}")
    print(f"  Display Name: {model.display_name}")
    print(f"  Description: {model.description}")
    print(f"  Supported methods: {model.supported_generation_methods}")
    print()
