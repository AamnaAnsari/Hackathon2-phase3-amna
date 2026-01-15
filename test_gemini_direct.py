#!/usr/bin/env python3
"""
Test Gemini API with CORRECT models from your account
"""
import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not found in .env")
    exit(1)

print("🧪 Testing Gemini API with YOUR available models...")
print("=" * 50)

client = genai.Client(api_key=api_key)

# Use models that ARE in your list
models_to_test = [
    "models/gemini-2.0-flash-001",      # Stable version
    "models/gemini-2.0-flash-lite-001", # Lite version
    "models/gemini-2.5-flash",          # Latest 2.5
    "models/gemini-2.5-pro",            # Pro version
    "gemini-2.0-flash-001",             # Without models/ prefix
    "gemini-2.0-flash-lite-001",
]

for model_name in models_to_test:
    print(f"\n🔄 Testing: {model_name}")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Say 'Hello World' in one word."
        )
        print(f"✅ SUCCESS! Response: {response.text}")
        print(f"🎯 USE THIS MODEL: {model_name}")
        
        # Save working model
        with open("working_model.txt", "w") as f:
            f.write(model_name)
        break
        
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            print(f"❌ Model not found")
        elif "permission" in error_msg.lower():
            print(f"❌ Permission issue")
        else:
            print(f"❌ Error: {error_msg[:100]}")

print("\n" + "=" * 50)
if os.path.exists("working_model.txt"):
    with open("working_model.txt", "r") as f:
        working_model = f.read().strip()
    print(f"✅ Working model found: {working_model}")
    print(f"\n💡 Update gemini_handler.py with: self.model_name = '{working_model}'")
else:
    print("❌ No model worked. Trying alternative approach...")