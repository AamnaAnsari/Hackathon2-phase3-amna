#!/usr/bin/env python3
"""
Create tables in NEON PostgreSQL automatically
"""
import os
import sys
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

print("🛠️ Creating Tables in NEON PostgreSQL")
print("=" * 50)

# Load environment
load_dotenv()
db_url = os.getenv("DATABASE_URL")

if not db_url:
    print("❌ DATABASE_URL not found")
    sys.exit(1)

print(f"📊 Database: {db_url.split('@')[1] if '@' in db_url else 'Unknown'}")

try:
    # Create engine
    print("🔗 Creating database engine...")
    engine = create_engine(db_url, echo=True)
    
    # Import your models
    print("📦 Importing models...")
    from mcp_server.models import Task, Conversation, Message
    
    # Create tables
    print("🏗️ Creating tables...")
    SQLModel.metadata.create_all(engine)
    
    print("\n✅ SUCCESS! Tables created:")
    print("   - tasks")
    print("   - conversations") 
    print("   - messages")
    
    # Verify
    print("\n🔍 Verifying...")
    with engine.connect() as conn:
        result = conn.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = [row[0] for row in result]
        print(f"📋 Found {len(tables)} tables: {tables}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\n💡 Install: pip install sqlmodel psycopg2-binary")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Alternative: Create tables manually via NEON SQL Editor")

print("\n" + "=" * 50)
print("🎉 Tables ready! Test with:")
print("python test_tools.py")