#!/usr/bin/env python3
"""
Test MCP Server with Client
"""
import asyncio
import subprocess
import json
import sys
import time

async def test_mcp_server():
    print("🧪 Testing MCP Server Connection...")
    print("=" * 50)
    
    # Start MCP server as subprocess
    print("🚀 Starting MCP server...")
    server_proc = subprocess.Popen(
        [sys.executable, "run_mcp.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Wait for server to initialize
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    try:
        # Send initialization request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print(f"📤 Sending: {json.dumps(init_request)}")
        server_proc.stdin.write(json.dumps(init_request) + "\n")
        server_proc.stdin.flush()
        
        # Read response
        print("📥 Waiting for response...")
        response = server_proc.stdout.readline()
        
        if response:
            print(f"✅ Response received: {response[:100]}...")
            
            # Parse response
            try:
                data = json.loads(response.strip())
                print(f"📊 Response ID: {data.get('id')}")
                print(f"📊 Result: {data.get('result', {}).get('protocolVersion', 'N/A')}")
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                print(f"Raw response: {response}")
        
        else:
            print("❌ No response received")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        server_proc.terminate()
        server_proc.wait()
        
        stdout, stderr = server_proc.communicate()
        if stderr:
            print(f"⚠️ Server stderr: {stderr[:200]}")
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())