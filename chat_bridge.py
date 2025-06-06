import os
import requests

# Basic demonstration script to authenticate to Blackbaud's SKY API
# and send user questions to the OpenAI ChatGPT API for natural language interpretation.
# Replace or extend functionality as needed.

BLACKBAUD_AUTH_URL = "https://oauth2.sky.blackbaud.com/token"
BLACKBAUD_API_BASE = "https://api.sky.blackbaud.com"  # Example base URL

# Load credentials from environment variables
CLIENT_ID = os.getenv("BLACKBAUD_CLIENT_ID")
CLIENT_SECRET = os.getenv("BLACKBAUD_CLIENT_SECRET")
SUBSCRIPTION_KEY = os.getenv("BLACKBAUD_SUBSCRIPTION_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not CLIENT_ID or not CLIENT_SECRET or not SUBSCRIPTION_KEY:
    raise RuntimeError("Blackbaud credentials are not set in environment variables")

if not OPENAI_API_KEY:
    raise RuntimeError("OpenAI API key not set in environment variables")


def get_blackbaud_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    resp = requests.post(BLACKBAUD_AUTH_URL, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]


def query_chatgpt(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }
    resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def main():
    user_query = input("Ask a question about your Blackbaud data: ")
    # Send the user query to ChatGPT to determine intent or required endpoint
    gpt_response = query_chatgpt(
        f"Translate the following natural language question into a Blackbaud SKY API endpoint or instruction: '{user_query}'"
    )
    print("ChatGPT suggestion:", gpt_response)

    # Example: Acquire token and perform an API request
    token = get_blackbaud_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Bb-Api-Subscription-Key": SUBSCRIPTION_KEY
    }
    # This is just a placeholder example using the constituent search endpoint
    endpoint = f"{BLACKBAUD_API_BASE}/constituent/v1/constituents"  # modify based on GPT suggestion
    params = {"limit": 5}
    api_resp = requests.get(endpoint, headers=headers, params=params)
    api_resp.raise_for_status()
    print("Sample API response:", api_resp.json())


if __name__ == "__main__":
    main()
