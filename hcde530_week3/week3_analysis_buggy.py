import csv

INPUT_FILE = "week3_survey_messy.csv"
OUTPUT_FILE = "week3_survey_cleaned.csv"


def load_rows(filename):
    rows = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def clean_rows(rows):
    cleaned = []
    for row in rows:
        role = (row.get("role") or "").strip()
        participant_name = (row.get("participant_name") or "").strip()

        # Remove rows missing key fields needed for analysis.
        if not role or not participant_name:
            continue

        cleaned_row = row.copy()
        cleaned_row["participant_name"] = participant_name
        cleaned_row["role"] = role.title().replace("Ux", "UX")
        cleaned.append(cleaned_row)
    return cleaned


def write_cleaned_rows(rows, output_filename):
    if not rows:
        return

    fieldnames = list(rows[0].keys())
    with open(output_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


rows = load_rows(INPUT_FILE)
cleaned_rows = clean_rows(rows)
write_cleaned_rows(cleaned_rows, OUTPUT_FILE)

# Count responses by role
# Normalize role names so "ux researcher" and "UX Researcher" are counted together
role_counts = {}

for row in cleaned_rows:
    role = row["role"]
    if role in role_counts:
        role_counts[role] += 1
    else:
        role_counts[role] = 1

print("Responses by role:")
for role, count in sorted(role_counts.items()):
    print(f"  {role}: {count}")

# Calculate the average years of experience
total_experience = 0
valid_experience_count = 0
# This code was buggy because there was a non-numeric value "fifteen" that it was trying to convert to an integer
for row in cleaned_rows:
    try:
        total_experience += int(row["experience_years"])
        valid_experience_count += 1
    except ValueError:
        # Skip non-numeric values like "fifteen"
        continue

avg_experience = (
    total_experience / valid_experience_count
    if valid_experience_count > 0
    else 0
)
print(f"\nAverage years of experience: {avg_experience:.1f}")

# Find the top 5 highest satisfaction scores
scored_rows = []
for row in cleaned_rows:
    if row["satisfaction_score"].strip():
        try:
            scored_rows.append((row["participant_name"], int(row["satisfaction_score"])))
        except ValueError:
            continue
# This code was buggy because it was trying to sort by highest scores but it was in ascending order, thus pulling the lowest scores
scored_rows.sort(key=lambda x: x[1], reverse=True)
top5 = scored_rows[:5]

print("\nTop 5 satisfaction scores:")
for name, score in top5:
    print(f"  {name}: {score}")

print(f"\nCleaned rows written to {OUTPUT_FILE}")
