# Check if all required environment variables are set
import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Checking environment configuration...")
print()

# Required variables
required = {
    "GEMINI_API_KEY": "Gemini API access"
}

# Optional but recommended
optional = {
    "PYTHON_BACKEND_URL": "Python backend URL (default: http://localhost:8000)",
    "PORT": "Node.js port (default: 5000)"
}

missing = []
warnings = []

# Check required
for var, description in required.items():
    value = os.getenv(var)
    if not value:
        missing.append(f"❌ {var} - {description}")
    else:
        print(f"✅ {var} - Set")

# Check optional
for var, description in optional.items():
    value = os.getenv(var)
    if not value:
        warnings.append(f"⚠️  {var} - {description} (using default)")
    else:
        print(f"✅ {var} - Set")

print()

if missing:
    print("❌ CRITICAL: Missing required environment variables:")
    for msg in missing:
        print(f"  {msg}")
    print()
    print("Please create a .env file with:")
    print("GEMINI_API_KEY=your_api_key_here")
    exit(1)

if warnings:
    print("⚠️  Optional variables not set:")
    for msg in warnings:
        print(f"  {msg}")
    print()

print("✅ Environment configuration OK!")
