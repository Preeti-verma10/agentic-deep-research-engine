import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Create client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Generate response
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain Artificial Intelligence in 3 simple sentences."
)

print(response.text)