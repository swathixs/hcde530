# Week 6 — C6 competency claim (Data visualization)

## What I've learned to accomplish

I can pick a chart type that fits the question and the data, build it in Python via Cursor, and write a short note so someone else can follow why I chose it and what to look at in the chart.

## Evidence

**Notebook:** `week6_mp1_starter.ipynb` in `hcde530_week6/` — code, printed outputs, and markdown (including Section 4) so someone can rerun the steps and see the same plots. Charts are **matplotlib** (`plt`), not hand-wavy descriptions.

## Chart justifications

### Chart 1 — low-star totals by genre (Question 1)

**What the data is:** Genres live in `genre_slugs` as a pipe-separated list, so one book can count toward more than one genre. In the notebook I split those strings and **exploded** them so each book–genre pair gets its own row, then I **summed** `low_star_ratings` (1★ + 2★ counts) **by genre**.

**Why horizontal bars:** Genres are **categories**, not a number line, so a **bar chart** is the natural way to compare totals across genres. I used **horizontal** bars because there are **many genre labels** and some names are long; sideways labels stay readable. A vertical bar chart would have crowded the x-axis.

**What I want a reader to notice:** The chart title calls out that **raw** 1★+2★ counts are often highest in **big** genres (fiction, fantasy, young-adult showed up high in my tables too). So the chart supports the question “who has the most low stars in absolute terms,” but it also warns you: **rank alone is misleading** if you do not think about how large that genre bucket is. A fairer next step would be normalizing by total ratings or number of books per genre.

### Chart 2 — rating spread vs average rating (Question 2)

**What the data is:** One **dot per book**. On one axis I put **`avg_rating`** (how good the average looks). On the other I put **`dist_spread_stdev`** (how “spread out” the star ratings are — a stand-in for disagreement in the distribution).

**Why a scatter plot:** Both fields are **numbers measured per book**, and I care about how they **move together** (or don’t). A scatter plot shows the whole cloud at once: clusters, gaps, and outliers. A bar chart would not fit here because I am not comparing a small set of fixed categories on both sides.

**What I want a reader to notice:** The Section 4 note says something I think is easy to forget: **high spread does not mean “everyone hates it.”** You can have a wide distribution at **many** different average ratings. So the chart separates **polarization / disagreement** from **mean score** instead of mixing them into one headline number.

### Chart 3 — distinct tags vs average rating (Question 3)

**What the data is:** Again one **dot per book**: **`num_distinct_tags`** on one axis and **`avg_rating`** on the other.

**Why a scatter plot:** I am testing a **simple numeric association** — “do books with more tag slugs tend to rate higher or lower?” Scatter is the right first pass for two continuous measures; it shows whether there is a visible tilt, a blob with no pattern, or weird pockets.

**What I want a reader to notice:** The notebook tells you to look for **vertical scatter** at a given tag count (many different average ratings at the same x). Section 3 already said the correlation in this sample was **small and positive**, and the chart title repeats the honest limit: **association is not causation** — more tags might track popularity, catalog coverage, or community habits, not “quality” by itself.

### How the three charts fit together

Question 1 is **categorical totals** → **bars**. Questions 2 and 3 are **number vs number per row** → **scatters**. Together they line up with the same three questions I answered in tables earlier in the notebook.

## Claim

I used a **horizontal bar chart** for genre vs summed 1★+2★ counts because genres are categories, the data had to be **exploded** from multi-genre strings, and long labels read better on the side than squashed under vertical bars. I used **scatter plots** for spread vs average rating and for tag count vs average rating because each question is **two numeric columns per book**, and I wanted the reader to see **clouds and outliers**, not collapse everything into one ranking. The full code, plot outputs, and the shorter markdown blurbs above each chart are in **`week6_mp1_starter.ipynb`** on GitHub in the (`hcde530_week6/` folder).

## What I would improve next time

If I had more time I would tighten titles so every chart states one clear “so what” in one line, and maybe add one small note under each figure with the exact number of rows in the slice I plotted so a reader can sanity-check the sample size.
