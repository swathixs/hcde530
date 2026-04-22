# Week 3 — Competency 3: Data cleaning and file handling

Personal notes on how this competency shows up in my Week 3 work.

## What Competency 3 means to me

**Data cleaning and file handling** means loading messy real-world CSVs with Python, spotting what breaks the script or skews results, fixing it so runs are repeatable, and treating error messages as clues—not noise. Outputs should be **consistent**: same inputs → same cleaned files and summaries.

---

## C3 — Strong competency claim

I load **real CSV files from disk** (not hardcoded rows in the script). In **`clean_responses.py`**, I read **`responses.csv`** and write **`responses_cleaned.csv`**. That pipeline **drops every row where `name` is missing** (after stripping whitespace), **uppercases** the `role` column for consistent labels, and leaves **`participant_id`** and **`response`** unchanged—so the cleaned file is smaller and easier to scan than the raw export.

For the survey exercise, **`week3_analysis_buggy.py`** reads **`week3_survey_messy.csv`** and writes **`week3_survey_cleaned.csv`**. That cleaning step **removes rows that are missing `participant_name` or `role`**, and **normalizes role text** (e.g. title case with **`UX`** spelled correctly instead of **`Ux`**). Re-saving with Python’s **`csv`** module also keeps **long text fields** (like open-ended responses) in a **single column** by quoting fields correctly, so **commas inside a cell** do not turn into broken “extra” columns when you open or re-read the file.

The script **crashed** once with **`ValueError: invalid literal for int() with base 10: 'fifteen'`** because one row had the word **`fifteen`** in **`experience_years`** instead of digits. The traceback pointed at converting that field with **`int(...)`**. I fixed it by wrapping the conversion in **`try` / `except ValueError`** so **non-numeric experience values are skipped** when computing the average, instead of stopping the whole run.

Separately, I hit a **logic bug**: the “top 5 satisfaction scores” list was sorted **ascending**, so it would have shown the **lowest** scores first. I changed the sort to **`reverse=True`** so the slice **`[:5]`** is actually the **five highest** scores.

My **commit history** shows finding those issues, fixing them, and pushing updates—so the story is documented, not just “I cleaned the data.”

---

## How to reproduce

From the `hcde530_week3` folder:

- `python3 clean_responses.py` → writes **`responses_cleaned.csv`**
- `python3 week3_analysis_buggy.py` → writes **`week3_survey_cleaned.csv`** and prints role counts, average experience, and top 5 satisfaction scores
