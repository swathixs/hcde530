# Week 5 — C5 competency claim: Data analysis with pandas

## What I am claiming

I can use **pandas** to load a real dataset, choose appropriate operations for a specific question, aggregate and filter data, and **interpret** what the outputs imply—not only run code and paste tables.

## Evidence (artifact)

- **Notebook:** `A5_pandas_books.ipynb` (this folder, `hcde530_week5/`)
- **Data:** In class I practiced on **CSV** files in a Jupyter kernel with pandas installed. For the Week 5 / A5 work I moved to **live data from the [Hardcover](https://hardcover.app/) GraphQL API** (book metadata, genre tag slugs, star-rating histograms, and related fields)—the same ecosystem as my Mini Project 1.

## Analytical questions I answered (summary)

Beyond exploratory checks (`head`, `info`, `value_counts` on exploded genres, and a **filter** for dystopian books with **average rating ≥ 4.0**), I framed **three research questions** and used pandas (plus matplotlib for one plot) to address them.

---

### Research question 1 — Which genre is associated with the most **1★ and 2★** ratings?

**What I did in pandas:** Genre labels arrive as a **single string** with multiple slugs separated by `|`. I **split** those strings and **exploded** them so each row–genre pair could be counted fairly. I then used **`groupby`** on the exploded genre column and **aggregated** with **`sum`** on low-star counts (and related summaries such as **mean** low-star fraction by genre) so I could rank genres by how much “dissatisfied” rating mass they carry in this sample.

**What the result means:** After attribution across exploded genres, **fiction** had the largest summed 1★+2★ counts, followed by **fantasy** and **young-adult**. That does **not** mean those genres are “worse” in an absolute sense—they are also likely among the **largest** genre buckets, so volume partly drives the pattern. The useful takeaway for my MP is: **any cross-genre comparison of raw low-star totals needs normalization** (e.g., per book, per rating volume, or confidence bounds), not raw sums alone.

---

### Research question 2 — Which books look **polarizing** (heavy 1★ and 5★) versus more **spread out** across star levels?

**What I did in pandas:** I used derived columns that summarize each book’s **empirical rating distribution** (e.g., spread / entropy style measures over half-star buckets). My first idea—books with *only* 1★ and 5★—was too strict for this dataset (effectively empty), so I **reframed** the question: flag books where **at least ~65%** of ratings sit in the **whole 1★** and **whole 5★** buckets combined (`polarized_1_or_5_ge_65pct`), and contrast that with books whose distributions are **wider** (more weight in 2★–4★). Sorting and filtering on those columns let me surface “love it or hate it” titles versus more middled disagreement.

**What the result means:** The operational definition matters: “polarizing” here is **concentration** in extreme buckets, not negativity alone. For the MP, I’m carrying forward that **distribution shape** is a better lens than a single average rating when the story is about mixed opinions.

---

### Research question 3 — Is there a relationship between **how many genre tags** a book has and its **average rating**?

**What I did in pandas:** I computed (or used) a measure of **tag richness** (how many distinct genre slugs apply), then examined its relationship to **`avg_rating`**, including a **matplotlib** scatter for visual pattern-checking.

**What the result means:** The scatter is an **associational** check: it shows whether “more labeled genres” co-occurs with higher or lower averages in this slice. Any slope or cluster is **hypothesis-generating** for the MP (e.g., tagging practices, catalog completeness, or genre overlap)—not causal without controlling for popularity, recency, and review count.

---

## Pandas operations I relied on 

| Operation / pattern | Why it matched the question |
|---------------------|-----------------------------|
| `df.head()` / `df.info()` | Preview rows and confirm **dtypes**, non-null counts, and which columns exist before building filters or merges downstream. |
| Split → `explode` → `value_counts()` | Turn **multi-valued** genre strings into **one row per genre** so “most common genre” is meaningful. |
| Boolean indexing (`df[condition]`) | Restrict to **dystopian** books with **strong average ratings** (≥ 4.0) as a sanity subset. |
| `groupby` + `sum` / `mean` | Aggregate low-star mass and typical low-star **fraction** **by genre** after explode (RQ1). |

## Environment note (how the work was runnable)

I configured a Jupyter **kernel** with **pandas** (and related deps) so the in-class CSV notebooks and the later API-backed notebook share the same foundation.

## Future steps

Seeing **fiction**, then **fantasy**, then **young-adult** at the top of the low-star totals made sense once I remembered those genres probably also have the **most books** in the dataset. In the future, I want to go back and compare genres more fairly (for example **per book** or **per total ratings**), and to keep my wording clear so **“polarizing”** (lots of 1★ and 5★) is not mixed up with **“low average rating.”**
