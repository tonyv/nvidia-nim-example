# First call

Going from a working API key to a real model response.

## Steps

1. From the model's catalog page, select the **Shell** tab.
2. Copy the prefilled command shown there and run it. The key is already filled in.

## Set your expectations on timing

The catalog's prefilled example ships with `reasoning_effort` set to `max`. At that
setting, expect:

- **~30-70 seconds** before the first token appears
- **A couple of minutes** total before the response finishes

The response does stream — it isn't silent for the whole wait — but the gap before
anything shows up is long enough to wonder if the request is stuck. It isn't; that's
the normal range observed here.

## About `reasoning_effort`

This parameter is documented in the API reference and controls how much reasoning the
model does before answering. It's tempting to lower it to speed things up.

Worth knowing before you do the same: across single runs at `low`, `high`, and `max`,
first-token time ranged from about 33s to about 71s, and the two `low` runs alone
differed by nearly 2x. Lowering `reasoning_effort` did not reliably reduce the wait in
these runs. Run-to-run variance looked larger than any difference between settings.
This isn't a controlled benchmark, so treat it as one data point. Bottom line is
don't count on this parameter to reduce the take it takes to get the first token.

See [the example scripts](example.md) for a script that measures time-to-first-token
directly.
