from google import genai
import os

# Make sure API key is set
os.environ["GOOGLE_API_KEY"] = "AIzaSyBcGX82-W2kmNzxnoHtvu158DoVKhBXhQ8"

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("Available Models:\n")

for m in client.models.list():
    print(m.name)