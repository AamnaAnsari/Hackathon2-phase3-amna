#!/usr/bin/env python3
"""
Fix all dict() to model_dump() warnings
"""
import os

def replace_in_file(filepath, old_text, new_text):
    """Replace text in a file"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_text not in content:
        print(f"⚠️ Text not found in {filepath}: {old_text}")
        return False
    
    new_content = content.replace(old_text, new_text)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated: {filepath}")
    return True

def main():
    print("🔧 Fixing dict() to model_dump() warnings...")
    
    # Files to fix
    files_to_fix = [
        ("test_tools.py", "result.dict()", "result.model_dump()"),
        ("mcp_server/server.py", "json.dumps(result.dict()", "json.dumps(result.model_dump()"),
        ("mcp_server/server.py", "json.dumps(result.dict(),", "json.dumps(result.model_dump(),"),
    ]
    
    success_count = 0
    for filepath, old_text, new_text in files_to_fix:
        if replace_in_file(filepath, old_text, new_text):
            success_count += 1
    
    print(f"\n📊 Fixed {success_count}/{len(files_to_fix)} files")
    
    # Also check schemas.py
    schemas_path = "mcp_server/schemas.py"
    if os.path.exists(schemas_path):
        with open(schemas_path, 'r') as f:
            content = f.read()
        
        if "class Config:" in content and "json_encoders" in content:
            print("✅ schemas.py already has Config class")
        else:
            print("⚠️ schemas.py might need Config class update")

if __name__ == "__main__":
    main()