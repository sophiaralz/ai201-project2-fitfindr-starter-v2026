# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr helps someone shopping secondhand find a thrifted item and figure out how to wear it. The user types a request like "vintage graphic tee under $30, size M" and the agent searches 40 thrift listings from Depop, ThredUp, and Poshmark for the best match within their price and size. It then suggests one or two outfits that pair the find with clothes already in the user's wardrobe, and writes a short, social-media-style caption (a "fit card") naming the item, its price and where it's listed. If nothing matches, it stops early and tells the user what to change, like raising their price limit or dropping the size. 


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**
Searches the thrift listings data for items matching a keyword description, with optional filtering by size and a maximum price ceiling
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
description (str), size(str | None), max_price(float | None)
- **Returns:**
A list of matching listing dictionaries sorted by keyword relevance score from highest to lowest. Each dictionary contains id, title, description, category, style_tags (list), size, condition, price (float), colors (list), brand (str or None), and platform
- **When it has nothing:**
Returns an empty list [] (not None and not an exception), which signals the planning loop branch to halt execution safely

### `suggest_outfit`

- **What it does:**
Given a thrifted item and the user's wardrobe, it suggests one or two outfits (calls the model).
- **Inputs:**
new_item (dict), wardrobe (dict)
- **Returns:**
A non-empty string with outfit suggestions. 
- **When it has nothing:**
When there is an empty wardrobe, it will return general styling advice (str)

### `create_fit_card`

- **What it does:** 
Writes a short caption someone would actually post about the find (calls the model).

- **Inputs:**
outfit (str), new_item (dict)

- **Returns:**
A string, which is a two-to-four sentence caption.

- **When it has nothing:**
If the outfit is empty or a whitespace, it returns a descriptive message (str) rather than raising. 


---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** 
If search_listings returns an empty list, put a message in the session and stop. Otherwise take the first result and go to suggest_outfit. 

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

Regex

**What moves through the session:** <!-- which fields, in what order -->

'parsed' -> 'search_results' -> 'selected_item' -> 'outfit_suggestion' -> 'fit_card'

Each tool reads its input from the session and writes its result back. error is set only when the search comes back empty.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->


**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

Outfit:   **Outfit 1: Effortless Y2K Street**
Pair the Y2K Baby Tee with your **Baggy straight-leg jeans, dark wash** and layer the **Black cropped zip hoodie** over top. Finish with **Chunky white sneakers** and your **Black crossbody bag**. 

**Outfit 2: Casual Contrast**
Combine the Y2K Baby Tee with your **Wide-leg khaki trousers** and slip on the **Vintage black denim jacket**. Accessorize with the **Brown leather belt** and **Chunky white sneakers**.

  Fit card: Obsessed with this little butterfly tee I just scored for only $18! I'm listing it on depop today, but honestly, I'm tempted to keep it for myself to style with baggy denim or wide-leg khakis. It’s giving total early 2000s off-duty model energy.

```
 

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

**Outfit 1: Casual Streetwear**
*   Vintage Levi's 501 Jeans — Medium Wash
*   White ribbed tank top
*   Oversized grey crewneck sweatshirt
*   Chunky white sneakers

**Outfit 2: Edge & Contrast**
*   Vintage Levi's 501 Jeans — Medium Wash
*   Black cropped zip hoodie
*   Black combat boots
*   Brown leather belt

```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

I finally scored the ultimate pair of vintage Levi's 501 jeans for just $38 and I am never taking them off. They are giving major effortless streetwear energy paired with my beat-up white sneakers for that classic off-duty look. Snagged these beauties on depop and my wardrobe has officially peaked.

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked Claude to walk me through the TODO steps for search_listings: filtering by price and size, scoring by keyword overlap, and returning at most SEARCH_RESULT_LIMIT results.
- *What came back:* It explained each step with a short code example. It also found a bug in the starter helpers: re was used but never imported.
- *What I changed:* I added the filtering and scoring code to search_listings. My first test crashed with NameError: name 're' is not defined, which confirmed the import bug, so I fixed it and reran it. 

**Moment 2**

- *What I asked for:* I asked Claude how to build the prompt for suggest_outfit, and what item_text and piece meant in the example code, because I didn't understand them. 
- *What came back:* It explained that item_text uses f-strings and ','.join() to turn the listing dict into one sentence, and that piece is the loop variable for each wardrobe item. 
- *What I changed:* I wrote suggest_outfit with 2 prompts, one for an empty wardrobe and one for a full one. My first version built the prompt but still ended with return "", so it never called the model. I fixed it and then tested it with the example wardrobe and the empty one. 

**Moment 3**

- *What I asked for:* I asked Claude where to put 'trace.step()' calls in 'run_agent', one per step, so I could see the each tool's inputs and outputs

- *What came back:* It gave me a trace line for each step. For `create_fit_card` it suggested`inputs=session["selected_item"]`, which records only the item.

- *What I changed:* I noticed `create_fit_card` takes two inputs, the outfit *and* the item, so the trace would hide half of what went in. I asked about it, and changed the input to a string with both: `f"item: {title} | outfit: {outfit}"`. A dict wouldn't work, because `trace.py` shortens a dict to "dict with keys: …" and hides the values. When I added the trace, my `parse_query` step also crashed with `UnboundLocalError` because it used `parsed` before that variable existed, so I changed it to read `session["parsed"]` instead.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all 3 tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item reaches suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card includes the item's dollar price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Price ceiling respected | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```
Criterion 1, Try 1, from results/run_2026-10-13_2258_before.md, written by run_eval.py::main, which runs agent.py::run_agent (search through mcp_server.py, outfit and fit card from tools.py).

Query: vintage graphic tee under $30   Wardrobe: example

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Fit card:
Found this absolute dream of a butterfly baby tee thrifting and I'm obsessed. I just listed her on Depop for $18, but honestly, I'm tempted to keep it for myself to style with baggy denim and chunky sneakers for the ultimate Y2K streetwear vibe. Go grab it before I change my mind!

Trace:
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    called via MCP (mcp_server.py)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    took the first result
[4] suggest_outfit
      in:  item: Y2K Baby Tee — Butterfly Print | wardrobe: 10 pieces
      out: **Outfit 1: Y2K Streetwear** *   Y2K Baby Tee — Butterfly Print *   Baggy straight-leg jeans, dark wash *   Ch…
[5] create_fit_card
      in:  item: Y2K Baby Tee — Butterfly Print | outfit: **Outfit 1: Y2K Streetwear** *   Y2K Baby Tee — Butterfly Print…
      out: Found this absolute dream of a butterfly baby tee thrifting and I'm obsessed. I just listed her on Depop for $…


```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all 3 tools | 4 of 5 | MET (5/5) | All 5 tries show stopped early: no and a fit card, and the trace reaches [5] create_fit_card every time |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET (5/5) | All 5 show search_results: 0 and selected_item: (none), and the trace ends at [3] branch with no suggest_outfit. The message names three changes: price, size, and wording. |
| 3 | Selected item's id matches the id passed to suggest_outfit | 5 of 5 | MET (5/5) | In all 5, the item in [3] select_item is the item in [4] suggest_outfit's input. The trace prints titles, not ids. All 40 titles in the data are unique, so matching titles means matching ids.|
| 4 | Fit card includes the selected listing's dollar amount | 5 of 5 | MET (5/5) | The selected item was $45.0 in all 5 tries, and every caption contains "$45" |
| 5 | Listings passed to suggest_outfit are within the price limit | 5 of 5 | MET (5/5) | max_price parsed as 40.0 every time, and the selected item was $12. The $75 Leather Bomber, which matches "leather jacket", never came back. |

**Diagnoses**

No criterion missed. Criteria 2, 3, and 5 test plain code (the regex parser, the price filter, and handling the item through the session), so 5/5 was expected. Criteria 1 and 4 depend on the model, and the free-tier rate limit didn't cause any failures this run. However, the run showed 2 problems my criteria doesn't measure.

1. Captions get the story backwards. In 6 of the 10 fit cards from criteria 1 and 4, the model says the user is selling the item: "I just listed her on Depop for $18", "Just listed this exact piece on Poshmark for $45". The cause is my create_fit_card prompt, which says "Platform: depop" without saying that's where the item was bought. Criterion 4 still passed because the price was there

2. The search engine treats all matching words equally. When a price filter excludes actual jackets, it falls back on less relevant items like belts simply because they share the word "leather". This shows that the search algorithm lacks keyword weighting. It doesn't understand that product categories (like "jacket") should carry more weight than attributes (like "leather")
---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    called via MCP (mcp_server.py)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    took the first result
[4] suggest_outfit
      in:  item: Y2K Baby Tee — Butterfly Print | wardrobe: 10 pieces
      out: **Outfit 1: Effortless Y2K Street** Pair the Y2K Baby Tee with your **Baggy straight-leg jeans, dark wash** an…
[5] create_fit_card
      in:  item: Y2K Baby Tee — Butterfly Print | outfit: **Outfit 1: Effortless Y2K Street** Pair the Y2K Baby Tee with …
      out: Obsessed with this little butterfly tee I just scored for only $18! I'm listing it on depop today, but honestl…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Effortless Y2K Street**
Pair the Y2K Baby Tee with your **Baggy straight-leg jeans, dark wash** and layer the **Black cropped zip hoodie** over top. Finish with **Chunky white sneakers** and your **Black crossbody bag**. 

**Outfit 2: Casual Contrast**
Combine the Y2K Baby Tee with your **Wide-leg khaki trousers** and slip on the **Vintage black denim jacket**. Accessorize with the **Brown leather belt** and **Chunky white sneakers**.

  Fit card: Obsessed with this little butterfly tee I just scored for only $18! I'm listing it on depop today, but honestly, I'm tempted to keep it for myself to style with baggy denim or wide-leg khakis. It’s giving total early 2000s off-duty model energy.

0 model calls this session, 2 served from cache

```

**Empty search**

```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    called via MCP (mcp_server.py)
[3] branch
      out: No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broad…
      →    search empty -> stopping before suggest_outfit

  No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broader words, like 'jacket' instead of a specific style.

0 model calls this session


```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

In `agent.py::run_agent`, I replaced the direct `search_listings(...)` call with `call_tool("search_listings", {...})`, and registered the tool in `mcp_server.py`. The results didn't change: the same 10 listings for "vintage graphic tee" under $30, and `[]` for the impossible query, so my branch still works. The differences were that each search is a bit slower (it starts the server every time), and I had to fix my tool description, which wrongly said it matched on category, brand and colors.


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

I changed 'create_fit_card' in 'tools.py'. The prompt used to label the facts 'Price:' and 'Platform:'. I relabeled them 'Price I paid:' and 'Where I bought it:', and added to the system prompt that the user BOUGHT the item and is keeping it, and must never be described as selling or listing it. Nothing else changed. 

**Which failure it was meant to fix:**

In the before run, 6 of the 10 fit cards for criteria 1 and 4 said the user was *selling* the item ("I just listed her on Depop for $18", "Just listed this exact piece on Poshmark for $45"). The prompt only said 'Platform: depop', so the model guessed what the platform meant to the user, and often guessed "where I'm selling it."

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all 3 tools  | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 3. Selected item's id reaches suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card includes the item's dollar price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 5. Price ceiling respected | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |



## Criterion 1 Output


- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
**Outfit 1: Y2K Streetwear**
*   Y2K Baby Tee — Butterfly Print
*   Baggy straight-leg jeans, dark wash
*   Chunky white sneakers
*   Black crossbody bag

**Outfit 2: Casual Contrast**
*   Y2K Baby Tee — Butterfly Print
*   Wide-leg khaki trousers
*   Black cropped zip hoodie
*   Black combat boots
```

Fit card:

```
Found this absolute dream of a butterfly baby tee thrifting and I'm obsessed. I just listed her on Depop for $18, but honestly, I'm tempted to keep it for myself to style with baggy denim and chunky sneakers for the ultimate Y2K streetwear vibe. Go grab it before I change my mind!
```

Trace:

```
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    called via MCP (mcp_server.py)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    took the first result
[4] suggest_outfit
      in:  item: Y2K Baby Tee — Butterfly Print | wardrobe: 10 pieces
      out: **Outfit 1: Y2K Streetwear** *   Y2K Baby Tee — Butterfly Print *   Baggy straight-leg jeans, dark wash *   Ch…
[5] create_fit_card
      in:  item: Y2K Baby Tee — Butterfly Print | outfit: **Outfit 1: Y2K Streetwear** *   Y2K Baby Tee — Butterfly Print…
      out: Found this absolute dream of a butterfly baby tee thrifting and I'm obsessed. I just listed her on Depop for $…
```


## Criterion 2 Output


- Query: `designer ballgown size XXS under $5`
- Wardrobe: example

**Try 1**

- stopped early: yes — No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broader words, like 'jacket' instead of a specific style.
- selected_item: (none)
- search_results: 0

Trace:

```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    called via MCP (mcp_server.py)
[3] branch
      out: No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broad…
      →    search empty -> stopping before suggest_outfit
```

## Criterion 3 Output


- Query: `platform sneakers`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Platform Sneakers — White Chunky Sole ($48.0, poshmark)
- search_results: 3

Outfit suggestion:

```
**Outfit 1: Casual Streetwear**
Pair your new Platform Sneakers with the White ribbed tank top, Baggy straight-leg jeans, and Black cropped zip hoodie. Add the Black crossbody bag for an effortless, off-duty look.

**Outfit 2: Y2K Contrast**
Style your Platform Sneakers with the Wide-leg khaki trousers and Oversized grey crewneck sweatshirt. Layer the Vintage black denim jacket on top and finish with the Brown leather belt.
```

Fit card:

```
Scored these chunky white platform sneakers on Poshmark for just $48 and I am obsessed. I've been styling them with baggy jeans and a cropped zip hoodie for that ultimate off-duty look, but they also look so good with wide-leg trousers for a total Y2K moment. Honestly my new favorite daily shoe.
```

Trace:

```
[1] parse_query
      in:  platform sneakers
      out: {'description': 'platform sneakers', 'size': None, 'max_price': None}
[2] search_listings
      in:  {'description': 'platform sneakers', 'size': None, 'max_price': None}
      out: 3 items: Platform Sneakers — White Chunky Sole, Platform Mary Janes — Black Patent, Low-Top Canvas Sneakers — Off-White
      →    called via MCP (mcp_server.py)
[3] select_item
      out: Platform Sneakers — White Chunky Sole ($48.0, poshmark)
      →    took the first result
[4] suggest_outfit
      in:  item: Platform Sneakers — White Chunky Sole | wardrobe: 10 pieces
      out: **Outfit 1: Casual Streetwear** Pair your new Platform Sneakers with the White ribbed tank top, Baggy straight…
[5] create_fit_card
      in:  item: Platform Sneakers — White Chunky Sole | outfit: **Outfit 1: Casual Streetwear** Pair your new Platform S…
      out: Scored these chunky white platform sneakers on Poshmark for just $48 and I am obsessed. I've been styling them…
```

## Criterion 4 Output


- Query: `90's track jacket`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
- search_results: 4

Outfit suggestion:

```
**Outfit 1: Sporty Streetwear**
Layer the 90s Track Jacket over the white ribbed tank top and pair with baggy straight-leg jeans, dark wash. Finish with chunky white sneakers and the black crossbody bag for an effortless throwback look. 

**Outfit 2: High-Low Contrast**
Wear the 90s Track Jacket zipped over the white ribbed tank top, paired with wide-leg khaki trousers and a brown leather belt. Ground the outfit with black combat boots for an edgy finish.
```

Fit card:

```
Found this crispy 90s track jacket on Poshmark for just $45 and I'm obsessed. I've been living in it thrown over baggy denim for sporty streetwear vibes, but it looks just as good dressed up with wide-leg khakis and combat boots. It’s the ultimate effortless throwback piece!
```

Trace:

```
[1] parse_query
      in:  90's track jacket
      out: {'description': "90's track jacket", 'size': None, 'max_price': None}
[2] search_listings
      in:  {'description': "90's track jacket", 'size': None, 'max_price': None}
      out: 4 items: 90s Track Jacket — Navy/White Stripe, Denim Jacket — Light Wash, Cropped, 90s Leather Bomber — Black … +1 more
      →    called via MCP (mcp_server.py)
[3] select_item
      out: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
      →    took the first result
[4] suggest_outfit
      in:  item: 90s Track Jacket — Navy/White Stripe | wardrobe: 10 pieces
      out: **Outfit 1: Sporty Streetwear** Layer the 90s Track Jacket over the white ribbed tank top and pair with baggy …
[5] create_fit_card
      in:  item: 90s Track Jacket — Navy/White Stripe | outfit: **Outfit 1: Sporty Streetwear** Layer the 90s Track Jacke…
      out: Found this crispy 90s track jacket on Poshmark for just $45 and I'm obsessed. I've been living in it thrown ov…
```

## Criterion 5 Output


- Query: `leather jacket under $40`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Leather Belt — Brown, Braided ($12.0, thredUp)
- search_results: 3

Outfit suggestion:

```
**Outfit 1: Casual Heritage**
*   Wide-leg khaki trousers
*   White ribbed tank top
*   Leather Belt — Brown, Braided
*   Chunky white sneakers
*   Vintage black denim jacket

**Outfit 2: Earthy Prep**
*   Baggy straight-leg jeans, dark wash
*   Oversized grey crewneck sweatshirt
*   Leather Belt — Brown, Braided
*   Black combat boots
```

Fit card:

```
Found this braided leather beauty on thredUp for just $12 and I'm obsessed. I've been styling it with slouchy khakis and a white tank for that effortless casual heritage look, but it also looks so good over an oversized grey crewneck with combat boots. It’s giving the ultimate vintage western energy without even trying.
```

Trace:

```
[1] parse_query
      in:  leather jacket under $40
      out: {'description': 'leather jacket', 'size': None, 'max_price': 40.0}
[2] search_listings
      in:  {'description': 'leather jacket', 'size': None, 'max_price': 40.0}
      out: 3 items: Leather Belt — Brown, Braided, Shacket — Olive Canvas, Mini Shoulder Bag — Tan Leather
      →    called via MCP (mcp_server.py)
[3] select_item
      out: Leather Belt — Brown, Braided ($12.0, thredUp)
      →    took the first result
[4] suggest_outfit
      in:  item: Leather Belt — Brown, Braided | wardrobe: 10 pieces
      out: **Outfit 1: Casual Heritage** *   Wide-leg khaki trousers *   White ribbed tank top *   Leather Belt — Brown, …
[5] create_fit_card
      in:  item: Leather Belt — Brown, Braided | outfit: **Outfit 1: Casual Heritage** *   Wide-leg khaki trousers *   Wh…
      out: Found this braided leather beauty on thredUp for just $12 and I'm obsessed. I've been styling it with slouchy …
```

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->

Yes. Counting fit cards that contain "list", "listed", "listing" or "sell"in the criteria 1 and 4 scenarios, it went from 6 of 10 to 0 of 10. 

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

No criterion is missed. All five were 5/5 before and after. 

However, the parser only understands "$" prices and exact sizes. "under 30 dollars" sets no price limit, and "size 8" never matches shoes sized "US 8". I'd add those patterns to the regex in 'run_agent'. I stopped because none of my scenarios test these phrasings, so I couldn't measure the fix. 




<!-- ═══════════════════════ CAPSTONE ═══════════════════════ -->

## The Shape

**System:** FitFindr. **Shape:** A — Deploy and instrument, on Path B (local with logs).

Right now FitFindr only runs as a single command (`python app.py ask ...`). It answers one question and then quits. For the capstone, I'm making it stay running as a small web server using `serve.py`. You send a question to `/ask` and it runs the same `run_agent()` function the command line uses. There's also a `/health` route to check that the server is up. I'm also adding logging: every request to `/ask` saves one line to `logs/runs.jsonl` with the time, the query, whether it worked (`ok`, `no_match`, or `crashed`), the answer or error message, and how many seconds it took. In addition, each log line will also record how many model calls that request made, how many answers came from the cache instead of the model, and how many tokens it used. That way I can tell what one request actually costs, and I can tell a real run apart from a fast cached one when I look at the timing. I'm not changing how the agent works. I'm just adding a way to run it and a record of what happened each time.

**Out of scope:**
- **Hosting it online (Path A).** I'm running it on my own computer and saving the log in my repo instead. I chose this because both options are graded the same, I don't have to sign up for a hosting site, and my log won't get deleted when a free server shuts off after sitting unused.
- **Changing the agent or the tools.** I'm not fixing the price/size parser gaps listed in What's Still Broken, and I'm not moving more tools onto MCP. If a request fails, I log it. I don't fix the agent in this unit.

**Size check:** The server is already built, so I only have a few things left: clean up the log so every line has the same fields, add the per-request cost fields (model calls, cache hits, tokens), write down how to start it in RUNNING.md, and make sure it works from a fresh copy of the repo. That should take way less than 90 minutes, which leaves plenty of time for writing criteria, testing, and the write-up.


### Regression check

After adding logging to serve.py, I re-ran the original command line to make sure nothing broke.

`python app.py ask 'vintage graphic tee under $30'`

```
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    called via MCP (mcp_server.py)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    took the first result
[4] suggest_outfit
      in:  item: Y2K Baby Tee — Butterfly Print | wardrobe: 10 pieces
      out: **Outfit 1: Effortless Y2K Street** Pair the Y2K Baby Tee with your **Baggy straight-leg jeans, dark wash** an…
[5] create_fit_card
      in:  item: Y2K Baby Tee — Butterfly Print | outfit: **Outfit 1: Effortless Y2K Street** Pair the Y2K Baby Tee with …
      out: Scored this butterfly print Y2K baby tee on Depop for just $18 and I am obsessed. It's giving total early 2000…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Effortless Y2K Street**
Pair the Y2K Baby Tee with your **Baggy straight-leg jeans, dark wash** and layer the **Black cropped zip hoodie** over top. Finish with **Chunky white sneakers** and your **Black crossbody bag**. 

**Outfit 2: Casual Contrast**
Combine the Y2K Baby Tee with your **Wide-leg khaki trousers** and slip onthe **Vintage black denim jacket**. Accessorize with the **Brown leather belt** and **Chunky white sneakers**.

  Fit card: Scored this butterfly print Y2K baby tee on Depop for just $18and I am obsessed. It's giving total early 2000s street style paired with my baggy dark wash jeans and a cropped zip hoodie. Can't wait to wear it all spring!

0 model calls this session, 2 served from cache
```

`python app.py ask 'designer ballgown size XXS under $5'`

```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    called via MCP (mcp_server.py)
[3] branch
      out: No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broad…
      →    search empty -> stopping before suggest_outfit

  No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broader words, like 'jacket' instead of a specific style.

0 model calls this session
```

Both behave the same as in unit 4: the matching query finds an item, suggests outfits and writes a fit card, and the impossible query stops at the empty-search branch with tips.

## Instrumentation

Every request to `/ask` writes one JSON line to `logs/runs.jsonl`. Each line has the time, the query (input), the fit card or error message (output), how many seconds the agent took, and a `status` saying how the run ended. It also has the cost fields I added: how many model calls the request made, how many answers came from the cache, and how many tokens it used. Requests with no query are logged as `rejected` before the agent runs, so those lines are shorter.

This is the full log from one session, run with the cache off (`AI201_CACHE=0 python serve.py`). I sent matching queries until 10 came back `ok`, then one impossible query and one empty request on purpose. Two of the matching queries failed on their own: the model returned `503 UNAVAILABLE` ("experiencing high demand"), and the agent stopped and logged them as `model_unavailable` instead of crashing.

```
{"timestamp": "2026-11-18T06:27:25+00:00", "status": "ok", "query": "vintage graphic tee under $30", "output": "Scored this Y2K butterfly print baby tee on Depop for only $18 and I am obsessed. I’m leaning all the way into the nostalgic streetwear vibe by pairing it with baggy dark-wash jeans, chunky sneakers, and a cropped zip hoodie. Such a good little vintage find for my rotation!", "seconds": 12.91, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 487, "output_tokens": 174}
{"timestamp": "2026-11-18T06:27:44+00:00", "status": "ok", "query": "denim jacket under $50", "output": "Scored this vintage cropped light wash denim jacket on Poshmark for just $42, and I am obsessed. I'm already planning to layer it over a black zip hoodie with khaki trousers for the ultimate effortless streetwear vibe. It's giving high-contrast denim sandwich energy, and I am never taking it off.", "seconds": 19.02, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 519, "output_tokens": 218}
{"timestamp": "2026-11-18T06:28:26+00:00", "status": "ok", "query": "platform sneakers", "output": "Just scored these platform sneakers on Poshmark for only $48 and I am obsessed. They are giving major Y2K street vibes paired with my baggy dark wash jeans and a vintage denim jacket. Can't wait to style them with wide-leg trousers for that perfect off-duty grunge look, too!", "seconds": 42.28, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 493, "output_tokens": 183}
{"timestamp": "2026-11-18T06:28:27+00:00", "status": "model_unavailable", "query": "leather jacket under $40", "output": "Found Leather Belt — Brown, Braided, but couldn't reach the model to style it. Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}} Then run the same query again.", "seconds": 0.94, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T06:28:49+00:00", "status": "ok", "query": "y2k baby tee", "output": "Found this absolute gem of a butterfly print baby tee on Depop for just $18 and I am never taking it off. I’m living for that nostalgic Y2K streetwear energy today paired with baggy dark wash jeans and a cropped zip hoodie. It’s giving total early 2000s heartthrob vibes and fits like a glove!", "seconds": 22.22, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 488, "output_tokens": 184}
{"timestamp": "2026-11-18T06:29:08+00:00", "status": "ok", "query": "cargo pants under $40", "output": "Score these low-rise khaki cargo pants on Poshmark for just $27 and I am so obsessed! They give off the ultimate off-duty streetwear vibe when I style them with a cropped hoodie and chunky sneakers. Can't wait to live in these all season long!", "seconds": 18.97, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 474, "output_tokens": 149}
{"timestamp": "2026-11-18T06:29:27+00:00", "status": "ok", "query": "band tee", "output": "Scored this 2003 tour bootleg graphic tee on Depop for just $24 and I'm obsessed. I'm leaning all the way into the vibe with baggy dark-wash jeans, heavy combat boots, and a black denim jacket. Can't wait to beat this thing up and wear it everywhere.", "seconds": 19.24, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 500, "output_tokens": 187}
{"timestamp": "2026-11-18T06:29:45+00:00", "status": "ok", "query": "mesh top", "output": "Scored this black mesh long-sleeve top on Depop for only $15 and I am so obsessed with it. I'm already planning to layer it for that ultimate Y2K grunge look with baggy jeans and combat boots, or keep it goth casual with wide-leg trousers and a zip hoodie. It's giving major dark academia meets 90s indie sleaze and I'm never taking it off.", "seconds": 17.79, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 484, "output_tokens": 203}
{"timestamp": "2026-11-18T06:29:53+00:00", "status": "model_unavailable", "query": "graphic hoodie", "output": "Found Vintage Graphic Hoodie — Faded Black, but couldn't reach the model to style it. Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}} Then run the same query again.", "seconds": 8.01, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 210, "output_tokens": 112}
{"timestamp": "2026-11-18T06:30:11+00:00", "status": "ok", "query": "vintage jeans under $50", "output": "Scored these vintage Levi's 501 jeans on Depop for just $38 and I am never taking them off. They have that perfect broken-in feel for throwing on with a white tank, oversized crewneck, and chunky sneakers for casual streetwear days. Can't wait to switch up the vibe later with a black cropped hoodie and combat boots for some edgy contrast.", "seconds": 17.81, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 467, "output_tokens": 171}
{"timestamp": "2026-11-18T06:30:34+00:00", "status": "ok", "query": "cardigan", "output": "Scored this dreamy chunky brown knit cardigan on Depop for just $35 and I'm never taking it off. It’s giving major cozy cottagecore energy and looks so good layered over a simple tank. Whether I'm throwing it on with baggy jeans for a casual coffee run or styling it with khaki trousers and combat boots for an earthy autumnal vibe, it's my new everyday uniform.", "seconds": 22.82, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 462, "output_tokens": 169}
{"timestamp": "2026-11-18T06:30:49+00:00", "status": "ok", "query": "black boots", "output": "Scored this oversized flannel shirt on thredUp for just $22 and I am obsessed with the 90s grunge energy. It’s the ultimate layering piece whether I'm throwing it on over baggy denim or tying it around the waist of some wide-leg trousers for a more edgy look. Honestly the easiest streetwear upgrade for fall.", "seconds": 15.53, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 486, "output_tokens": 178}
{"timestamp": "2026-11-18T06:30:50+00:00", "status": "no_match", "query": "designer ballgown size XXS under $5", "output": "No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.45, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T06:30:50+00:00", "status": "rejected", "error": "no query in the request body"}
```

**What the log shows:**
- **10 `ok` runs**, each with exactly 2 model calls (`suggest_outfit` and `create_fit_card`) and 0 cache hits, so every one is a real run.
- **2 `model_unavailable` failures** from the model being overloaded (503). The `graphic hoodie` one failed on the second model call, so it still used 322 tokens and produced nothing.
- **1 `no_match`** (the impossible query): 0 model calls, under half a second, because the agent stops before calling the model.
- **1 `rejected`** (the empty request): turned away with HTTP 400 before the agent ran.

## What It Costs

**One successful run costs about 668 tokens and 21 seconds.**

| Per `ok` run (10 runs) | Average | Median | Min | Max |
|---|---|---|---|---|
| Model calls | 2 | 2 | 2 | 2 |
| Prompt tokens | 486 | 486.5 | 462 | 519 |
| Output tokens | 181.6 | 180.5 | 149 | 218 |
| **Total tokens** | **667.6** | | | |
| Seconds | 20.86 | 19.0 | 12.91 | 42.28 |

**How I measured it:** I started the server with the cache off (`AI201_CACHE=0 python serve.py`) so every request really called the model. I sent matching queries with a small script until 10 came back with `status: "ok"`, then averaged the `prompt_tokens`, `output_tokens` and `seconds` fields from those 10 log lines. The token numbers aren't estimates: `serve.py` reads `generate.py`'s counters before and after each run, and those counters add up the token counts the Gemini API reports on each response. `seconds` is measured around `run_agent()` with `time.perf_counter()`.

**What the numbers mean:**
- **Money:** I'm on the Gemini free tier, so the actual spend was $0. The real limits are the free tier's 15 requests per minute and its daily quota. Each successful run uses 2 of those requests.
- **Time:** the seconds cover the whole agent run, including starting the MCP server process for the search, not just the model thinking. The rate limiter never paused during this session (it prints a message when it does, and none appeared), so the time is the model being slow to answer. The 42-second run is an outlier, and it happened right before the first 503, so my guess is the model was already overloaded at that moment.
- **Failures cost something too:** a run that fails on the second model call still spends tokens. Out of 12 runs that reached the model, 2 failed (about 1 in 6), all from the 503.


## Capstone Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. One log line per request | 15 of 15 | 15/15 | 15/15 | 15/15 | MET |
| 2. The logged status matches what actually happened | 15 of 15 | 15/15 | 15/15 | 15/15 | MET |
| 3. The cost fields count the right things | 100% of lines | 10/10 | 9/10 | 10/10 | MISSED |
| 4. When the model can't be reached, the failure is logged and the server keeps going | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. A real run finishes in under 20 seconds | median < 20s, 8 of 10 < 30s | median 2.67s, 9/10 < 30s | median 3.78s, 9/10 < 30s | median 3.75s, 9/10 < 30s | MET |


### Capstone Criterion 1 Output — one log line per request

Produced by `serve.py::log_run`, called from `serve.py::ask`. Run 2, session A: 15 requests, and these are the 15 lines `logs/runs.jsonl` gained (`results/capstone/before/run2/session_a_log.jsonl`):

```
{"timestamp": "2026-11-18T07:32:02+00:00", "status": "ok", "query": "vintage graphic tee under $30", "output": "Scored this gorgeous butterfly print Y2K baby tee on Depop for only $18 and I’m obsessed. I'm leaning all the way into the nostalgic vibes today, pairing it with baggy dark-wash jeans and chunky sneakers. It’s giving effortless 2000s comfort, but I can't wait to toughen it up with combat boots and a distressed denim jacket next time.", "seconds": 61.72, "model_calls": 3, "cache_hits": 0, "prompt_tokens": 492, "output_tokens": 200}
{"timestamp": "2026-11-18T07:32:11+00:00", "status": "ok", "query": "denim jacket under $50", "output": "Scored this cropped light wash denim jacket on Poshmark for just $42, and it’s about to be my entire personality. I'm already planning to live in it with baggy dark-wash jeans for a double denim moment, or layered over a black zip hoodie with khakis for the ultimate casual streetwear fit. It has that perfectly broken-in vintage look that instantly pulls any outfit together.", "seconds": 8.9, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 504, "output_tokens": 220}
{"timestamp": "2026-11-18T07:32:14+00:00", "status": "ok", "query": "platform sneakers", "output": "Scored these chunky white platforms on Poshmark for just $48 and I am obsessed! I'm already planning to live in them with baggy dark denim and a cropped zip hoodie for that ultimate Y2K streetwear vibe. They also look insanely good dressed down with wide-leg trousers and an oversized crewneck for easy, elevated neutrals.", "seconds": 3.27, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 466, "output_tokens": 162}
{"timestamp": "2026-11-18T07:32:18+00:00", "status": "ok", "query": "y2k baby tee", "output": "Scored this Y2K butterfly print baby tee on Depop for just $18 and I am obsessed. It’s giving major nostalgic vibes, so I’m leaning into a casual Y2K street look with baggy dark-wash jeans and chunky sneakers. Can't wait to style it with wide-leg trousers and combat boots for an edgy contrast, too!", "seconds": 3.88, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 458, "output_tokens": 157}
{"timestamp": "2026-11-18T07:32:21+00:00", "status": "ok", "query": "cargo pants under $40", "output": "Scored these khaki low-rise cargo pants on Poshmark for just $27 and I’m so obsessed with the fit. They’re giving major off-duty Y2K streetwear vibes, especially paired with my zip hoodie and chunky sneakers. Can't wait to grunge them up with a big crewneck and combat boots next!", "seconds": 3.0, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 480, "output_tokens": 168}
{"timestamp": "2026-11-18T07:32:21+00:00", "status": "no_match", "query": "designer ballgown size XXS under $5", "output": "No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.38, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:32:21+00:00", "status": "no_match", "query": "wedding dress under $2", "output": "No listings matched 'wedding dress'. Try: raise your price limit above $2; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.33, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:32:22+00:00", "status": "no_match", "query": "ski boots size 15 under $3", "output": "No listings matched 'ski boots'. Try: raise your price limit above $3; try without size 15; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.32, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:32:22+00:00", "status": "no_match", "query": "tuxedo size XXXL under $1", "output": "No listings matched 'tuxedo'. Try: raise your price limit above $1; try without size XXXL; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.4, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:32:23+00:00", "status": "no_match", "query": "ballet slippers size 2 under $4", "output": "No listings matched 'ballet slippers'. Try: raise your price limit above $4; try without size 2; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.32, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:32:23+00:00", "status": "rejected", "error": "no query in the request body"}
{"timestamp": "2026-11-18T07:32:23+00:00", "status": "rejected", "error": "no query in the request body"}
{"timestamp": "2026-11-18T07:32:23+00:00", "status": "rejected", "error": "no query in the request body"}
{"timestamp": "2026-11-18T07:32:23+00:00", "status": "rejected", "error": "no query in the request body"}
{"timestamp": "2026-11-18T07:32:23+00:00", "status": "rejected", "error": "no query in the request body"}
```

### Capstone Criterion 2 Output — status matches the response

Responses produced by `serve.py::ask` and recorded by `capstone_eval.py::ask` (HTTP code, whether the body was JSON, and the body's `error` and `fit_card`). Run 2, session A, one per kind of request, each followed by the log line it wrote (`results/capstone/before/run2/session_a_responses.json`, `session_a_log.jsonl`):

```json
{
  "query": "vintage graphic tee under $30",
  "http": 200,
  "json": true,
  "error": null,
  "fit_card": "Scored this gorgeous butterfly print Y2K baby tee on Depop for only $18 and I’m obsessed. I'm leaning all the way into the nostalgic vibes today, pairing it with baggy dark-wash jeans and chunky sneakers. It’s giving effortless 2000s comfort, but I can't wait to toughen it up with combat boots and a distressed denim jacket next time."
}
```
```
{"timestamp": "2026-11-18T07:32:02+00:00", "status": "ok", "query": "vintage graphic tee under $30", "output": "Scored this gorgeous butterfly print Y2K baby tee on Depop for only $18 and I’m obsessed. I'm leaning all the way into the nostalgic vibes today, pairing it with baggy dark-wash jeans and chunky sneakers. It’s giving effortless 2000s comfort, but I can't wait to toughen it up with combat boots and a distressed denim jacket next time.", "seconds": 61.72, "model_calls": 3, "cache_hits": 0, "prompt_tokens": 492, "output_tokens": 200}
```

```json
{
  "query": "designer ballgown size XXS under $5",
  "http": 200,
  "json": true,
  "error": "No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broader words, like 'jacket' instead of a specific style.",
  "fit_card": null
}
```
```
{"timestamp": "2026-11-18T07:32:21+00:00", "status": "no_match", "query": "designer ballgown size XXS under $5", "output": "No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.38, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

```json
{
  "query": null,
  "http": 400,
  "json": true,
  "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}",
  "fit_card": null
}
```
```
{"timestamp": "2026-11-18T07:32:23+00:00", "status": "rejected", "error": "no query in the request body"}
```

### Capstone Criterion 3 Output — cost fields

Produced by `serve.py::usage_since`, which reads the counters in `generate.py::call_count` and `generate.py::token_counts`. Run 2, session A: the miss (`model_calls: 3`) followed by a correct `ok` and `no_match` line (`results/capstone/before/run2/session_a_log.jsonl`):

```
{"timestamp": "2026-11-18T07:32:02+00:00", "status": "ok", "query": "vintage graphic tee under $30", "output": "Scored this gorgeous butterfly print Y2K baby tee on Depop for only $18 and I’m obsessed. I'm leaning all the way into the nostalgic vibes today, pairing it with baggy dark-wash jeans and chunky sneakers. It’s giving effortless 2000s comfort, but I can't wait to toughen it up with combat boots and a distressed denim jacket next time.", "seconds": 61.72, "model_calls": 3, "cache_hits": 0, "prompt_tokens": 492, "output_tokens": 200}
{"timestamp": "2026-11-18T07:32:11+00:00", "status": "ok", "query": "denim jacket under $50", "output": "Scored this cropped light wash denim jacket on Poshmark for just $42, and it’s about to be my entire personality. I'm already planning to live in it with baggy dark-wash jeans for a double denim moment, or layered over a black zip hoodie with khakis for the ultimate casual streetwear fit. It has that perfectly broken-in vintage look that instantly pulls any outfit together.", "seconds": 8.9, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 504, "output_tokens": 220}
{"timestamp": "2026-11-18T07:32:21+00:00", "status": "no_match", "query": "designer ballgown size XXS under $5", "output": "No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.38, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

Printed by `generate.py::generate` while that first request ran (`results/capstone/before/run2/server_real_key.out`):

```
[rate limit] service pushed back. Waiting 59s (attempt 1 of 5). This is the limiter doing its job, not a bug.
```

### Capstone Criterion 4 Output — model unreachable

Produced by `serve.py::ask`, on a server started with `GEMINI_API_KEY=not-a-real-key`. Run 2, session C: all 10 log lines from the 5 rounds (`results/capstone/before/run2/session_c_log.jsonl`):

```
{"timestamp": "2026-11-18T07:33:33+00:00", "status": "model_unavailable", "query": "vintage graphic tee under $30", "output": "Found Y2K Baby Tee — Butterfly Print, but couldn't reach the model to style it. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "seconds": 1.07, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:33:33+00:00", "status": "no_match", "query": "designer ballgown size XXS under $5", "output": "No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.37, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:33:34+00:00", "status": "model_unavailable", "query": "denim jacket under $50", "output": "Found Denim Jacket — Light Wash, Cropped, but couldn't reach the model to style it. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "seconds": 0.43, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:33:34+00:00", "status": "no_match", "query": "wedding dress under $2", "output": "No listings matched 'wedding dress'. Try: raise your price limit above $2; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.33, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:33:35+00:00", "status": "model_unavailable", "query": "platform sneakers", "output": "Found Platform Sneakers — White Chunky Sole, but couldn't reach the model to style it. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "seconds": 0.38, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:33:35+00:00", "status": "no_match", "query": "ski boots size 15 under $3", "output": "No listings matched 'ski boots'. Try: raise your price limit above $3; try without size 15; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.32, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:33:35+00:00", "status": "model_unavailable", "query": "y2k baby tee", "output": "Found Y2K Baby Tee — Butterfly Print, but couldn't reach the model to style it. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "seconds": 0.38, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:33:36+00:00", "status": "no_match", "query": "tuxedo size XXXL under $1", "output": "No listings matched 'tuxedo'. Try: raise your price limit above $1; try without size XXXL; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.32, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:33:36+00:00", "status": "model_unavailable", "query": "cargo pants under $40", "output": "Found Low-Rise Cargo Pants — Khaki, but couldn't reach the model to style it. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "seconds": 0.38, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-18T07:33:36+00:00", "status": "no_match", "query": "ballet slippers size 2 under $4", "output": "No listings matched 'ballet slippers'. Try: raise your price limit above $4; try without size 2; use broader words, like 'jacket' instead of a specific style.", "seconds": 0.35, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

The responses from round 1: the matching query, the impossible query, and `/health`, recorded by `capstone_eval.py::session_c` (`results/capstone/before/run2/session_c_rounds.json`):

```json
{
  "matching": {
    "query": "vintage graphic tee under $30",
    "http": 200,
    "json": true,
    "error": "Found Y2K Baby Tee — Butterfly Print, but couldn't reach the model to style it. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.",
    "fit_card": null
  },
  "impossible": {
    "query": "designer ballgown size XXS under $5",
    "http": 200,
    "json": true,
    "error": "No listings matched 'designer ballgown'. Try: raise your price limit above $5; try without size XXS; use broader words, like 'jacket' instead of a specific style.",
    "fit_card": null
  },
  "health": {
    "http": 200,
    "body": {
      "status": "ok"
    }
  }
}
```

### Capstone Criterion 5 Output — speed

Produced by `serve.py::ask` (`seconds` is `time.perf_counter()` around `run_agent()`) and written by `serve.py::log_run`. Run 2, session B: the 10 `ok` lines (`results/capstone/before/run2/session_b_log.jsonl`):

```
{"timestamp": "2026-11-18T07:32:25+00:00", "status": "ok", "query": "vintage graphic tee under $30", "output": "Scored this Y2K baby tee with the cutest butterfly print on Depop for only $18 and I am obsessed. I'm styling it with baggy straight-leg jeans, chunky white sneakers, and a cropped zip hoodie for the ultimate nostalgic streetwear moment. Such a dreamy little vintage find!", "seconds": 2.48, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 494, "output_tokens": 178}
{"timestamp": "2026-11-18T07:32:28+00:00", "status": "ok", "query": "denim jacket under $50", "output": "Scored this vintage light wash cropped denim jacket on Poshmark for only $42, and I'm already obsessed. Throwing it on over a black zip hoodie with wide-leg khaki trousers and combat boots for the ultimate 90s streetwear vibe. It’s definitely going to be my new daily go-to jacket!", "seconds": 2.64, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 472, "output_tokens": 174}
{"timestamp": "2026-11-18T07:32:31+00:00", "status": "ok", "query": "platform sneakers", "output": "Scored these chunky platform sneakers on Poshmark for just $48 and I am obsessed. They are bringing all the Y2K street vibes to my closet today. Can't wait to style them with a cropped hoodie and baggy jeans.", "seconds": 3.58, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 473, "output_tokens": 149}
{"timestamp": "2026-11-18T07:33:04+00:00", "status": "ok", "query": "y2k baby tee", "output": "Scored this absolute dream of a Y2K baby tee with the cutest butterfly print on Depop for just $18! I'm so obsessed with the nostalgic streetwear energy it brings, especially paired with baggy dark wash jeans and chunky sneakers. It’s giving effortless retro vibes, but I can't wait to style it with wide-leg trousers for a cool, casual contrast too.", "seconds": 32.66, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 496, "output_tokens": 199}
{"timestamp": "2026-11-18T07:33:12+00:00", "status": "ok", "query": "cargo pants under $40", "output": "Just scored these khaki low-rise cargo pants on Poshmark for only $27, and I am obsessed. I'm totally leaning into the ultimate 2000s streetwear vibe by pairing them with a white ribbed tank, an unzipped black cropped hoodie, and chunky sneakers. Such a good secondhand win!", "seconds": 7.97, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 498, "output_tokens": 182}
{"timestamp": "2026-11-18T07:33:15+00:00", "status": "ok", "query": "band tee", "output": "Score this 2003 tour bootleg style graphic tee on Depop for just $24 and I'm honestly obsessed. I'm styling it with dark wash baggy jeans and combat boots for that effortless 90s grunge vibe. Total instant favorite in my rotation.", "seconds": 2.98, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 534, "output_tokens": 211}
{"timestamp": "2026-11-18T07:33:20+00:00", "status": "ok", "query": "mesh top", "output": "Scored this black mesh long-sleeve top on Depop for just $15 and I am so obsessed with it. It’s got that ultimate 90s goth-grunge energy and is going to be my new go-to for layering. Can’t wait to style it with baggy dark denim and combat boots for a moody look, or throw a cropped zip hoodie over it with wide-leg trousers for peak Y2K contrast.", "seconds": 4.82, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 464, "output_tokens": 187}
{"timestamp": "2026-11-18T07:33:24+00:00", "status": "ok", "query": "vintage jeans under $50", "output": "Just scored these vintage Levi's 501 jeans on Depop for only $38 and I am never taking them off. They have that perfect broken-in feel for throwing on with a white tank and chunky sneakers for casual streetwear days. Already planning to style them with a cropped hoodie and combat boots too for a little bit of edge.", "seconds": 4.17, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 467, "output_tokens": 163}
{"timestamp": "2026-11-18T07:33:28+00:00", "status": "ok", "query": "cardigan", "output": "Scored this chunky brown knit cardigan on Depop for just $35 and it’s basically a wearable hug. I'm so obsessed with the cozy earth-tone vibe that I've already planned two ways to wear it—either thrown over wide-leg trousers for that rustic neutral look, or buttoned up with dark wash denim and combat boots for some edgy cottagecore energy. Definitely my new favorite fall staple!", "seconds": 3.88, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 490, "output_tokens": 201}
{"timestamp": "2026-11-18T07:33:31+00:00", "status": "ok", "query": "black boots", "output": "Just scored this oversized red and black plaid flannel shirt on thredUp for only $22, and it's already my new favorite layering piece. I’m leaning hard into the 90s grunge vibe today, wearing it open over a white ribbed tank with baggy dark wash jeans and black combat boots. It also looks so good buttoned up with wide-leg khakis and chunky sneakers for that effortless streetwear look.", "seconds": 3.67, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 496, "output_tokens": 204}
```

Every rate-limit line printed by `generate.py::_wait_for_slot` and `generate.py::generate` on that server during sessions A and B (`results/capstone/before/run2/server_real_key.out`):

```
[rate limit] service pushed back. Waiting 59s (attempt 1 of 5). This is the limiter doing its job, not a bug.
[rate limit] 15 requests used this minute. Waiting 29s. This is normal.
[rate limit] 15 requests used this minute. Waiting 2s. This is normal.
[rate limit] 15 requests used this minute. Waiting 4s. This is normal.
[rate limit] 15 requests used this minute. Waiting 2s. This is normal.
```


## Capstone Verdicts and Diagnosis

| Criterion | Verdict |
|---|---|
| 1. One log line per request | **MET** — 15/15 in all three runs |
| 2. The logged status matches what actually happened | **MET** — 15/15 in all three runs |
| 3. The cost fields count the right things | **MISSED** — 10/10, 9/10, 10/10. The target was 100% in every run |
| 4. When the model can't be reached, the failure is logged and the server keeps going | **MET** — 5/5 in all three runs |
| 5. A real run finishes in under 20 seconds | **MET** — medians 2.67s, 3.78s and 3.75s, 9/10 under 30s in every run |

**Diagnosis of criterion 3:**

- **Where:** the call counter in `generate.py::generate`.
- **How:** `generate()` adds 1 to `_session_calls` on every attempt, before it knows whether Gemini will answer. In Run 2, Gemini refused the first call with a rate-limit error (429), `generate()` retried it, and the retry was counted as another call, so the line logged `model_calls: 3` instead of 2.

**The pattern:** this miss and the one slow run in each criterion 5 trial (42.69s, 32.66s, 37.68s) have the same cause: the rate limit in `generate.py`. The slow runs happened because my code paused after 15 calls in one minute. The miss happened because Google refused a call that my code thought was allowed. So it's one problem showing up in two places. Criterion 5 still passed because I allowed 2 slow runs out of 10.

**Were the targets set too low?** Criterion 5 was. I set "median under 20 seconds" from Milestone 3, where the median was 19 seconds, but in these runs the median was 3–4 seconds, so the target never came close to failing. Model speed changes a lot from day to day, so I wouldn't tighten it all the way to 4 seconds. I'd tighten it to **median under 8 seconds**, which is about twice what I measured here, and keep "8 of 10 under 30 seconds".

## Capstone Improvement

**What I changed:** I added a second counter in `generate.py` that only counts calls Gemini actually answers. `serve.py` now logs that as `model_calls`, and logs refused calls in a new `refused_attempts` field. The old counter still counts every attempt, because the session budget needs it.

This targets the diagnosis: the problem was that the counter counted attempts, so now `model_calls` only counts answers. I didn't change the rate limiter itself, since that would be a second fix.


## Capstone Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. One log line per request | 15 of 15 | 15/15 | 15/15 | 15/15 | MET |
| 2. The logged status matches what actually happened | 15 of 15 | 15/15 | 15/15 | 15/15 | MET |
| 3. The cost fields count the right things | 100% of lines | 10/10 | 10/10 | 10/10 | MET |
| 4. When the model can't be reached, the failure is logged and the server keeps going | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. A real run finishes in under 20 seconds | median < 20s, 8 of 10 < 30s | median 3.65s, 9/10 < 30s | median 2.54s, 8/10 < 30s | median 4.09s, 8/10 < 30s | MET |

**Before and after, side by side:**

| Criterion | Before (Run 1 / 2 / 3) | After (Run 1 / 2 / 3) |
|---|---|---|
| 1 | 15/15, 15/15, 15/15 — MET | 15/15, 15/15, 15/15 — MET |
| 2 | 15/15, 15/15, 15/15 — MET | 15/15, 15/15, 15/15 — MET |
| 3 | 10/10, **9/10**, 10/10 — **MISSED** | 10/10, 10/10, 10/10 — **MET** |
| 4 | 5/5, 5/5, 5/5 — MET | 5/5, 5/5, 5/5 — MET |
| 5 | 2.67s / 3.78s / 3.75s, 9, 9, 9 of 10 < 30s — MET | 3.65s / 2.54s / 4.09s, 9, **8, 8** of 10 < 30s — MET |

**The fix helped, it wasn't just lucky.** The miss only happens when Gemini refuses a call and my code retries it, and that's random. If it hadn't happened in the after runs, criterion 3 would have passed even without the fix. But it did happen, 3 times (only once in the before runs), and every time the log was correct: `model_calls: 2` for the 2 calls Gemini answered, and `refused_attempts: 1` for the refused one. Before the fix, these would have been logged as `model_calls: 3`. 

```
{"timestamp": "2026-11-18T07:57:03+00:00", "status": "ok", "query": "vintage graphic tee under $30", "output": "Scored this butterfly print Y2K baby tee on Depop for just $18 and I am obsessed! It’s giving major nostalgic streetwear energy paired with baggy dark wash jeans and chunky sneakers, but I can't wait to toughen it up with wide-leg trousers and combat boots next. My closet has officially peaked.", "seconds": 35.38, "model_calls": 2, "refused_attempts": 1, "cache_hits": 0, "prompt_tokens": 467, "output_tokens": 158}
{"timestamp": "2026-11-18T07:59:02+00:00", "status": "ok", "query": "black boots", "output": "Scored this red and black oversized flannel on thredUp for just $22, and it’s officially my new uniform. I'm obsessed with throwing it over a ribbed tank with baggy denim and combat boots for that effortless 90s grunge look. Seriously never taking this off.", "seconds": 44.98, "model_calls": 2, "refused_attempts": 1, "cache_hits": 0, "prompt_tokens": 474, "output_tokens": 155}
{"timestamp": "2026-11-18T08:00:11+00:00", "status": "ok", "query": "platform sneakers", "output": "Scoreeeed these chunky white platform sneakers on Poshmark for just $48 and I am never taking them off. They are giving major Y2K off-duty model mixed with effortless streetwear. Can't wait to pair them with baggy dark wash denim and my go-to cropped hoodie.", "seconds": 46.07, "model_calls": 2, "refused_attempts": 1, "cache_hits": 0, "prompt_tokens": 466, "output_tokens": 153}
```

Printed by `generate.py::generate` while those requests ran (`results/capstone/after/run2/server_real_key.out`, `run3/server_real_key.out`):

```
[rate limit] service pushed back. Waiting 32s (attempt 1 of 5). This is the limiter doing its job, not a bug.
[rate limit] service pushed back. Waiting 32s (attempt 1 of 5). This is the limiter doing its job, not a bug.
[rate limit] service pushed back. Waiting 36s (attempt 1 of 5). This is the limiter doing its job, not a bug.
```

**Did it help?** Yes, for criterion 3: it went from MISSED to MET, and the three refused calls show it working on the exact case that caused the miss. Criteria 1, 2 and 4 didn't change.

**The trade:** criterion 5 got closer to missing. Runs 2 and 3 had exactly 8 of 10 under 30 seconds, the lowest my target allows. That's not caused by the fix, which only changes what gets counted, not how long anything takes. Those slow runs are the same refusals shown above: each one waited 32–36 seconds before retrying (35.38s, 44.98s, 46.07s). The fix makes those refusals *visible* in the log, but it doesn't make them happen less often. The real cause is the stage I didn't change: each new `serve.py` process starts with an empty rate limiter and doesn't know about calls made just before it started. Fixing that, for example by spacing out requests or remembering calls across restarts, is what I'd do next.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
