"""Call a NIM hosted endpoint with raw requests."""

import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

INVOKE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "moonshotai/kimi-k3"

# (connect, read). The read timeout has to clear time-to-first-token, measured
# at 33-47s here; with stream=True it applies to the gap between chunks.
TIMEOUT_SECONDS = (10, 180)

api_key = os.environ.get("NVIDIA_API_KEY")
if not api_key:
    sys.exit("NVIDIA_API_KEY is not set. Copy .env.example to .env and add your key.")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "text/event-stream",
}

payload = {
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://assets.ngc.nvidia.com/products/api-catalog/phi-3-5-vision/example1b.jpg"
                    },
                },
            ],
        }
    ],
    "model": MODEL,
    "max_tokens": 16384,
    "seed": 0,
    "stream": True,
    "temperature": 1,
    "reasoning_effort": "max",
}

try:
    response = requests.post(
        INVOKE_URL,
        headers=headers,
        json=payload,
        stream=True,
        timeout=TIMEOUT_SECONDS,
    )

    if response.status_code == 403:
        sys.exit(f"Rejected (403). Bad key, or this key has no access to {MODEL}. ")
    if response.status_code == 401:
        sys.exit("Auth failed (401). Check NVIDIA_API_KEY.")

    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After", "unknown")
        sys.exit(f"Rate limited (429). Retry-After: {retry_after}. Wait and run again.")

    response.raise_for_status()

    for line in response.iter_lines():
        if line:
            print(line.decode("utf-8"))

except requests.exceptions.Timeout:
    sys.exit(f"No response within {TIMEOUT_SECONDS[1]}s. Run again, or raise TIMEOUT_SECONDS.")
except requests.exceptions.ConnectionError as error:
    sys.exit(f"Could not reach the endpoint: {error}. Check your network and run again.")
except requests.exceptions.HTTPError as error:
    sys.exit(f"Request failed: {error}")
