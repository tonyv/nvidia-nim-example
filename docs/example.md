# The example scripts

Two small scripts, both calling the same model (`moonshotai/kimi-k3`) on the same
endpoint, `https://integrate.api.nvidia.com/v1`. I created both scripts to
demonstrate how to get a raw response directly from a NIM endpoint. The second
script uses the OpenAI SDK to see if we can easily swap in different models at
will.

Both read the key from `NVIDIA_API_KEY` via `python-dotenv`. Both were run against
a live key and produced a response.

```
uv run python examples/nim-example-openai.py
uv run python examples/nim-example-nvidia.py
```

## `nim-example-nvidia.py` — raw `requests`

Calls the endpoint directly with `requests`, `stream=True`, and prints each
server-sent event line as-is: `data: {...}` chunks, exactly as they come off the
wire. Nothing is parsed. This is the shape the catalog's own Shell example gives you,
made a little more durable (explicit timeout, real error handling).

It sends a multimodal request — text plus an image URL — to Kimi-K3, and got a real
response when run.

Reach for this version when you want to see the raw protocol, or you're debugging
something a parsed client might be hiding from you.

## `nim-example-openai.py` — OpenAI-compatible client

Points the OpenAI SDK at `base_url="https://integrate.api.nvidia.com/v1"` instead of
OpenAI's own endpoint. This works, but it's not something the catalog UI confirmed
directly: the model page's Python tab only offered a raw `requests` snippet, with no
OpenAI-client option shown.

This script also parses the streamed chunks into `delta` objects and measures
time-to-first-token, printed at the end of the run.

### The `reasoning_content` extension

Captured chunks (`examples/example.json`, `examples/example-nv.json`, both captured
from this endpoint's own streaming output, since the API reference had no response
example) show the ordering: early chunks carry `delta.reasoning_content`, then the
delta switches to `delta.content` once the actual answer starts. For example:

```json
{"delta": {"role": "assistant", "reasoning_content": " user"}, ...}
```

followed later by chunks like:

```json
{"delta": {"content": "ential", ...}, ...}
```

`reasoning_content` is a NIM extension — it isn't part of the OpenAI chat-completions
schema. The script handles this by checking `content` first and falling back to
`reasoning_content`.

The API reference's built-in try-it tool (on `docs.api.nvidia.com`) was the first
thing tried to inspect a response shape, but it failed repeatedly in Chrome with a
bearer token pasted in:

```
Network Error: The request could not be completed. This is typically caused by a
CORS issue, a network error, or an invalid URL.
```

### Why the timeout is explicit

Both scripts set an 180s read timeout rather than relying on the client default
(600s for the OpenAI SDK). Given first-token times observed in the 33-70s range, a
600s default is too long to catch a genuine stall.
