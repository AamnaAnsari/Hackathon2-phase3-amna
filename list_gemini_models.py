#!/usr/bin/env python3
"""
List available Gemini models - Fixed version
"""
import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not found")
    exit(1)

print("📋 Listing available Gemini models...")
print("=" * 50)

try:
    client = genai.Client(api_key=api_key)
    
    # List models
    models = list(client.models.list())
    
    print(f"✅ Found {len(models)} models:")
    print("-" * 50)
    
    # Filter for generateContent models only
    generate_models = []
    
    for model in models:
        model_name = model.name
        
        # Check if it's a generation model (not embedding)
        if "embedding" not in model_name.lower():
            generate_models.append(model)
    
    print(f"📊 Generation models (for chat): {len(generate_models)}")
    print("-" * 50)
    
    for i, model in enumerate(generate_models[:10]):  # Show first 10
        print(f"{i+1}. {model.name}")
        print(f"   Display: {getattr(model, 'display_name', 'N/A')}")
        print(f"   Description: {getattr(model, 'description', 'N/A')[:80]}...")
        print("-" * 50)
    
    # Show recommendations
    print("\n🎯 RECOMMENDED MODELS for your project:")
    print("1. gemini-1.5-flash-latest (Fast, free tier)")
    print("2. gemini-1.0-pro-latest (Good balance)")
    print("3. gemini-pro (Basic, reliable)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()