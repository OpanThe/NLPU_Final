from google import genai
import os

api_key = os.getenv("GEMINI_API_KEY")
assert api_key is not None, "API KEY TIDAK KEBACA"

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents="Say OK only"
)

print(response.text)
