"""Call a NIM hosted endpoint through the OpenAI-compatible client."""

import os
import sys
import time

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    PermissionDeniedError,
    RateLimitError,
)

load_dotenv()

MODEL = "moonshotai/kimi-k3"
PROMPT = "What is the meaning of life?"

# Measured on this endpoint: 33-47s to first token, ~2.5 min to finish at max
# reasoning_effort. The SDK default is 600s,
TIMEOUT_SECONDS = 180.0

api_key = os.environ.get("NVIDIA_API_KEY")
if not api_key:
    sys.exit("NVIDIA_API_KEY is not set. Copy .env.example to .env and add your key.")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
    timeout=TIMEOUT_SECONDS,
)

start_time = time.perf_counter()

try:
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT}],
        max_tokens=16384,
        seed=0,
        stream=True,
        temperature=1,
        extra_body={"reasoning_effort": "low"},
    )

    time_to_first_token = None
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        # reasoning_content is a NIM extension, not part of the OpenAI schema:
        # it streams first, then the delta switches to content for the answer.
        text = getattr(delta, "content", None) or getattr(delta, "reasoning_content", None)
        if not text:
            continue
        if time_to_first_token is None:
            time_to_first_token = time.perf_counter() - start_time
        print(text, end="", flush=True)

    print()
    if time_to_first_token is not None:
        print(f"Time to first token: {time_to_first_token:.2f}s")

except PermissionDeniedError:
    sys.exit(f"Rejected (403). Bad key, or this key has no access to {MODEL}. Retrying will not help.")
except AuthenticationError:
    sys.exit("Auth failed (401). Check NVIDIA_API_KEY. Retrying will not help.")

except RateLimitError:
    sys.exit("Rate limited (429). Wait and run again.")
except APITimeoutError:
    sys.exit(f"No response within {TIMEOUT_SECONDS:.0f}s. Run again, or raise TIMEOUT_SECONDS.")
except APIConnectionError as error:
    sys.exit(f"Could not reach the endpoint: {error}. Check your network and run again.")
