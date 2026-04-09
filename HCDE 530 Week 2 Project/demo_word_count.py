import csv

FILENAME = "demo_responses.csv"


def count_words(text):
    return len(text.split())


reviews = []
with open(FILENAME, newline="", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        reviews.append(row["response"])

word_counts = [count_words(review) for review in reviews]

print(f"{'Review #':<10}{'Words':<8}Preview")
print("-" * 70)
for index, review in enumerate(reviews, start=1):
    words = count_words(review)
    preview = review[:60] + ("..." if len(review) > 60 else "")
    print(f"{index:<10}{words:<8}{preview}")

print("\nSummary")
print("-" * 70)
print(f"Total responses: {len(word_counts)}")
print(f"Shortest: {min(word_counts)} words")
print(f"Longest: {max(word_counts)} words")
print(f"Average: {sum(word_counts) / len(word_counts):.1f} words")
