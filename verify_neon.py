#!/usr/bin/env python3
"""
Verify NEON Connection Step-by-Step
"""
import os
import sys
from dotenv import load_dotenv

print("🔍 NEON Connection Verification")
print("=" * 50)

# Step 1: Load .env
load_dotenv()
db_url = os.getenv("DATABASE_URL")

if not db_url:
    print("❌ Step 1 FAILED: DATABASE_URL not found in .env")
    print("💡 Add this to .env file:")
    print("DATABASE_URL=postgresql://username:password@ep-xxx.neon.tech/dbname")
    sys.exit(1)

print("✅ Step 1: .env loaded")
print(f"   URL: {db_url.split('@')[0]}@[hidden]")

# Step 2: Check if it's NEON URL
if "neon.tech" not in db_url:
    print("⚠️ Warning: URL doesn't contain 'neon.tech'")
    print("   Are you sure this is NEON connection?")
else:
    print("✅ Step 2: NEON URL detected")

# Step 3: Try to connect
print("\n🔄 Step 3: Testing connection...")
try:
    import psycopg2
    
    # Hide password in print
    safe_url = db_url
    if "@" in db_url:
        parts = db_url.split("@")
        safe_url = f"{parts[0].split(':')[0]}:***@{parts[1]}"
    
    print(f"   Connecting to: {safe_url}")
    
    conn = psycopg2.connect(db_url)
    
    # Test query
    cursor = conn.cursor()
    cursor.execute("SELECT 1 as test, current_timestamp as time")
    result = cursor.fetchone()
    
    print(f"✅ Step 3: Connected successfully!")
    print(f"   Test query result: {result}")
    
    # Step 4: Check existing tables
    print("\n📋 Step 4: Checking existing tables...")
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    
    tables = cursor.fetchall()
    
    if tables:
        print(f"   Found {len(tables)} existing tables:")
        for table in tables:
            print(f"   - {table[0]}")
    else:
        print("   No tables found. Will create them.")
    
    conn.close()
    
except ImportError:
    print("❌ psycopg2 not installed")
    print("💡 Run: pip install psycopg2-binary")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Connection failed: {str(e)[:100]}")
    print("\n💡 Common NEON issues:")
    print("1. Check connection string is correct")
    print("2. Go to NEON dashboard → Settings → IP Allowlist")
    print("3. Add your IP address (or allow all IPs temporarily)")
    print("4. Ensure database is not paused")
    sys.exit(1)

print("\n" + "=" * 50)
print("✅ NEON verification complete!")
print("\n📝 Next: Create tables with:")
print("python create_neon_tables.py")