from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "What is agentic AI in one sentence?"}]
)

print(response.choices[0].message.content)