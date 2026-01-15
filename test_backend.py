#!/usr/bin/env python3
"""
Test Backend with Gemini Integration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🧪 Testing Backend with Gemini...")
print("=" * 50)

# Test 1: Check imports
print("\n1️⃣ Testing imports...")
try:
    from gemini_handler import get_gemini_assistant
    from mcp_tools import todo_tools
    from main import app
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test 2: Check Gemini API key
print("\n2️⃣ Checking Gemini API key...")
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    print(f"✅ Gemini API key found: {GEMINI_API_KEY[:10]}...")
else:
    print("❌ Gemini API key not found in .env")
    print("💡 Add: GEMINI_API_KEY=your-key-here")

# Test 3: Test Gemini initialization
print("\n3️⃣ Testing Gemini initialization...")
try:
    gemini = get_gemini_assistant()
    print("✅ Gemini initialized successfully")
except Exception as e:
    print(f"❌ Gemini initialization failed: {e}")

# Test 4: Test MCP tools
print("\n4️⃣ Testing MCP tools...")
import asyncio

async def test_tools():
    try:
        # Test add task
        result = await todo_tools.add_task_tool(
            user_id="test_user_backend",
            title="Test from backend test",
            description="Testing backend integration"
        )
        print(f"✅ Task added: {result.get('title')}")
        
        # Test list tasks
        result = await todo_tools.list_tasks_tool("test_user_backend")
        print(f"✅ Found {result.get('count', 0)} tasks")
        
        return True
    except Exception as e:
        print(f"❌ Tools test failed: {e}")
        return False

# Run async test
try:
    success = asyncio.run(test_tools())
except RuntimeError:
    # Handle if event loop already running
    import nest_asyncio
    nest_asyncio.apply()
    success = asyncio.run(test_tools())

# Test 5: Check FastAPI app
print("\n5️⃣ Checking FastAPI app...")
try:
    endpoints = [route.path for route in app.routes if hasattr(route, 'path')]
    print(f"✅ FastAPI app has {len(endpoints)} endpoints")
    print("📌 Main endpoints:")
    for endpoint in ['/health', '/api/chat', '/docs']:
        if any(endpoint in e for e in endpoints):
            print(f"  - {endpoint}")
except Exception as e:
    print(f"❌ FastAPI check failed: {e}")

print("\n" + "=" * 50)
if success:
    print("🎉 Backend tests passed! Ready to run server.")
    print("\n🚀 Run: python backend/main.py")
else:
    print("⚠️ Some tests failed. Check above for errors.")