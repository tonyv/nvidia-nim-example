# Getting access

This is the path from a cold start (no account, no key) to a working API key,
as it actually happened. Total elapsed time: about 3 minutes.

## What worked well

- **Getting started was easy** Just sign up for an account, pick a model, copy a
  code snippet from the model page, and run it
- **No other accounts needed** The whole flow stayed on `build.nvidia.com`.
- **The code samples come with the API key already filled in** once you have one.
  That made the first call easy. No separate step to wire the key into the example.

## The path

1. Start at `build.nvidia.com`.
2. Click a model in the catalog — in this case the first one listed, Kimi-K3
   (`moonshotai/kimi-k3`).
3. Click **Generate API Key**. This prompts a sign-in.
4. **The sign-in screen is also the signup route** — it just doesn't say so.
   Signing in is obvious; signing up isn't a separate, labeled option. The fastest
   way through is a social login (Google, in this case): choosing it creates the
   account implicitly, with no separate signup step. Knowing that going in saves the
   minute or so otherwise spent looking for a "create account" link.
5. Verify by phone (SMS code) when prompted.
6. Back on the model page, select the **Shell** tab and click **Generate API Key**
   again to get a key tied to your account.
