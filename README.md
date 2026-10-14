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
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

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
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



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



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



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
