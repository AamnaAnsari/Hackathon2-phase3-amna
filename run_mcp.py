
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

try:
    print("MCP Server starting...")  # Removed emoji
    from mcp_server.server import main
    main()
except ImportError as e:
    print(f"Import error: {e}")
    print("\nChecking installed packages:")
    os.system("pip list | findstr mcp")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)