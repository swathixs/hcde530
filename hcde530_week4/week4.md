# C4 — APIs and Data Acquisition (Competency Claim)

## What I did (summary)

I used **Google’s Web Fonts Developer API** (public documentation: [Web Fonts API](https://developers.google.com/fonts/docs/developer_api)) to pull the full catalog of hosted fonts, then **filtered** that response down to **serif** families only and saved a structured export for work in another class and for any future UX/visual-design decisions I make.

**Evidence in this folder**

| Artifact | Role |
|----------|------|
| `fetch_serif_fonts.py` | Makes an HTTPS GET, parses JSON, filters and writes output |
| `serif_fonts.csv` | Readable export (spreadsheet-friendly) of the filtered results |
| `.env` | Stores my API key locally (**not** committed to Git) |
| `requirements.txt` | Documents `python-dotenv` so the script can load `.env` |
| Root `.gitignore` | Includes `.env` so secrets stay off GitHub |

This API is **not** the same as the course demo API (the Render reviews endpoint used in `fetch_reviews.py`). For this competency I am claiming **`fetch_serif_fonts.py`** as my self-directed API integration.

---

## Why I chose this API and dataset

I found the **Google Fonts API** while looking for a **structured, real-world catalog** of typography options. It returns machine-readable metadata for every font Google hosts. It also feels more reliable than filtering through a website and aligned with how real products load font lists.

I chose to focus on **serif** fonts because:

- In another class I am working through **brand typography** and learning how **serif, sans-serif, and slab serif** families read differently in UI and print.
- In practice I **reach for serifs often** for readability and tone in certain layouts; I wanted a **filterable list** of actual hosted families instead of ad hoc searching.
- Pulling **only** `category == "serif"` turns a very large catalog into a **small, decision-ready list** I can scan or sort in a spreadsheet before choosing weights and pairing typefaces for a project.

So the “data acquisition” story is not just “I called an API”—it is **I acquired catalog metadata I need for typography decisions**, then **reduced it** to the subset that matches my current design focus.

---

## How the API works (endpoint, parameters, response)

**Endpoint (what the URL is doing)**  
`GET https://www.googleapis.com/webfonts/v1/webfonts`

This endpoint returns **metadata about all Google Fonts** available through the Web Fonts service—not font binary files themselves, but the information developers need to reference fonts (names, categories, available styles, etc.).

**Parameters**  
Google requires an **API key** for this API. The script passes it as a query parameter:

- `key=<your Google Cloud API key>` (created in Google Cloud Console; **Web Fonts Developer API** enabled for the project.)

So the full request looks conceptually like:

`https://www.googleapis.com/webfonts/v1/webfonts?key=...`

**What the API returns**  
The response is **JSON**. At the top level it includes metadata such as `kind`, and the important field for this script is **`items`**: an **array of font objects**.

Each object in `items` includes many fields; for this assignment I relied on three:

| Field | Meaning |
|-------|--------|
| `family` | The font’s display / family name (e.g. “Playfair Display”). |
| `category` | High-level classification—e.g. `serif`, `sans-serif`, `display`, `handwriting`, `monospace`. |
| `variants` | A list of strings describing which weights and styles exist (e.g. `regular`, `700`, `italic`, `700italic`)—useful when specifying CSS or when narrowing choices. |

The script **filters** where `category == "serif"`, then **prints** each match and **writes** `family`, `category`, and a comma-separated `variants` column to **`serif_fonts.csv`**.

---

## Keeping the API key out of version control (elaborated)

**Problem:** Assignment and professional practice both require **never embedding API keys in source code** or pushing them to a **public** GitHub repo. Keys in code get copied, screenshotted, and committed by mistake.

**What I implemented**

1. **`.env` file next to the script**  
   The secret lives in `hcde530_week4/.env` as something like `GOOGLE_API_KEY=<secret>`. This file is for **my machine only** (and optional sharing through a private, non-Git channel if ever needed).

2. **`python-dotenv` + `load_dotenv()`**  
   At runtime, `load_dotenv()` reads `.env` and loads variables into the process **environment**—the same place operating systems put configuration. That lets Python read the key with **`os.environ.get("GOOGLE_API_KEY")`** without the literal key appearing in `fetch_serif_fonts.py`.

3. **`.gitignore` at the repo root**  
   The project `.gitignore` lists **`.env`**, so Git **does not track** that file. Even if I run `git add .`, `.env` stays local unless someone forces an add (which I avoid).

4. **No key in the repository**  
   Reviewers only see a variable **name** in code (`GOOGLE_API_KEY`), not the value. The actual string exists only in `.env` on machines that should have it.

**Operational note:** Anyone cloning the repo must **create their own** `.env` (and enable the API in Google Cloud) to run the script—this is intentional and mirrors real projects.

---

## Strong competency statement (one paragraph)

I called **Google’s Web Fonts Developer API** at `https://www.googleapis.com/webfonts/v1/webfonts`, passing my **API key** as the `key` query parameter after loading it from **`.env`** with **`python-dotenv`** and **`os.environ.get("GOOGLE_API_KEY")`**. The JSON response includes an **`items`** array; each font has metadata such as **`family`**, **`category`**, and **`variants`**. I **filtered** to **`category == "serif"`** because I am studying brand typography and use serifs often, and I wanted a compact list instead of the full catalog. I **printed** each match for quick inspection and **saved** **`family`**, **`category`**, and **`variants`** to **`serif_fonts.csv`** for spreadsheet use. My **`.gitignore`** excludes **`.env`**, so the key is **not** committed to GitHub.

---

## Files referenced

- **Script:** `fetch_serif_fonts.py`
- **Output:** `serif_fonts.csv`
- **Dependencies:** `requirements.txt` (`python-dotenv`)
- **Secrets:** `.env` (local only; gitignored)
