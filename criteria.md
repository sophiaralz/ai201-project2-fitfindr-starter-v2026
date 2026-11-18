# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

My search is a plain keyword match, so a different wording like "t-shirt" instead of "tee" can miss. Also, two of my tools call the model on the free tier, so a try can fail on a rate limit even when my code is right. That's why I allow one miss, but not more.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

When 'search_listings' returns an empty list, stopping the flow depends entirely on explicit code logic rather than LLM reasoning. Because halting on empty results is handled by hardcoded execution control, it should succeed in 5 of 5 attempts. 

---

## 3. Something about state
<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

When 'search_listing' returns matching items, the selected item's id stored in session state matches the id passed into 'suggest_outfit' in 5 of 5 tries. 


**Why this target:**

Passing the item id between tools is just regular Python code, not AI guessing. Since it's just Python dictionary lookups, it needs to work 100% of the time or the backend logic is just broken. 

---

## 4. Something about the fit card

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

The caption inside the fit card explicitly includes the dollar amount (e.g., matching $ followed by the price) of the selected listing in 5 of 5 tries. 

**Why this target:**

Since the system prompt can explicitly instruct the model to include the dollar figure from the input context, failing to include it is a prompt-following error, so it should hit 5 of 5 tries.  


---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

When a search query specifies a maximum price (e.g., "under \$30"), 100% of the listings passed to 'suggest_outfit' have a price lower than or equal to that threshold across 5 of 5 tries

**Why this target:**

Recommending an item that exceeds the user's explicit budget breaks core functional requirements, so this must hold across all test attempts. 


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

# Capstone criteria

## 1. One log line per request

Over a session of 15 requests to `/ask` (5 matching queries, 5 impossible
queries, 5 empty requests), `logs/runs.jsonl` gains exactly 15 new lines — none
missing, none duplicated. Every line except `rejected` ones has all of
`timestamp`, `status`, `query`, `seconds`, `model_calls`, `cache_hits`,
`prompt_tokens` and `output_tokens` — 15 of 15.

**Why this target:**

Writing the log line is plain Python with one `log_run()` call on each path, so there's no reason for it to ever miss. I made this target because I've already had a bug where the old `log_run()` line was left in and every request got logged twice, so duplicates are a real risk, not a made-up one. A missing line is worse: a failure that leaves no record is one I would never find, so anything less than 15 of 15 means the log can't be trusted.

---

## 2. The logged status matches what actually happened

In the same 15-request session, each line's `status` matches the response the
caller got: `ok` when the response has a fit card and `error` is null,
`no_match` when the error starts with "No listings matched", `rejected` when the
response is HTTP 400, and `model_unavailable` for any other error — 15 of 15.

**Why this target:**

The status comes from a few simple `if` checks in my code, not from the model, so it should be right every time. If the status is wrong, then any numbers I count from the log are wrong too. For example, if a failed run got logged as `ok`, FitFindr would look like it works better than it really does. I compare the status to the response the user actually got, not to the query, because even a good query can fail when the model is overloaded (too many people sending requests at the same moment and Gemini's servers can't keep up).

---

## 3. The cost fields count the right things

With the cache off, every `ok` line in the 15-request session has
`model_calls: 2`, `cache_hits: 0`, and `prompt_tokens` and `output_tokens`
both above 0. Every `no_match` line has all four fields at 0 — 100% of lines.

**Why this target:**

A successful run always calls the model exactly twice (`suggest_outfit` and `create_fit_card`), and an impossible query stops before the model is ever called, so the right numbers are known ahead of time. The counts are just the difference between `generate.py`'s counters before and after the run, inside the one-request-at-a-time lock, so another request can't leak into them. My "What It Costs" number is averaged from these fields, so if they count wrong, my cost number is wrong.

---

## 4. When the model can't be reached, the failure is logged and the server keeps going

With the server started using a broken API key, 5 matching queries each return
a JSON error (not an HTML 500 page) and each write one `model_unavailable` line
whose `output` contains the error message. After each one, an impossible query
still returns `no_match`, and `/health` still returns `ok` — 5 of 5 tries.

**Why this target:**

This is the bad path. It already happened for real in Milestone 3, when the model failed twice because Gemini was overloaded. Using a broken API key makes the model fail every time, so I can test this on purpose instead of waiting for Gemini to go down again. My code already catches this kind of error, so it should work 5 of 5 times. The impossible query and the `/health` check don't need the model, so if they still work after a failure, I know the server is still running. One failed request is okay, but a failure that crashes the whole server is not.

---

## 5. A real run finishes in under 20 seconds

With the cache off, the median `seconds` across 10 `ok` runs is under 20
seconds, and at least 8 of the 10 finish in under 30 seconds. Runs that fail
with `model_unavailable` don't count toward the 10.

**Why this target:**

In Milestone 3 my median was 19 seconds, but that was one session, and runs ranged from 13 to 42 seconds. I'm setting 20 seconds to test whether 19 was normal or a lucky session, not to give myself room. About 30 seconds is as long as I think someone would wait for a clothing suggestion before assuming it's broken. I allow 2 slow runs out of 10 because most of the time is the model answering, which I don't control. The 42-second run happened right when Gemini was overloaded.
