import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("ANTHROPIC_API_KEY is missing from .env")
    exit()

client = Anthropic(api_key=api_key)

prompt = """
You are an executive email assistant.

Analyze the following email information and return ONLY valid JSON.

Required JSON format:

{
  "summary": "",
  "required_action": "",
  "draft_reply": ""
}

Rules:
- summary: short summary of the sender's message.
- required_action: what action Vijay should take.
- draft_reply: professional reply that Vijay can send.
- Do not include markdown.
- Do not include ```json.
- Keep the draft reply natural and concise.

Sender Name:
Ahmed Din

Sender Email:
saifur.rahman@pearlorganisation.com

Email Context:
Vijay Jethwani replies to a shared article about burnout and business performance,
thanking the sender and noting he will read the full article on LinkedIn.
"""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("CLAUDE RESPONSE:")
print(response.content[0].text)