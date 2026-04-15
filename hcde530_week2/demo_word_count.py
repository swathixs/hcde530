# file format
import csv

FILENAME = "demo_responses.csv"

# function that counts words in a string of text
def count_words(text):
    return len(text.split())

# list for storing reviews
reviews = []
with open(FILENAME, newline="", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        reviews.append(row["response"])

# builds a list of word counts for each review
word_counts = [count_words(review) for review in reviews]

# prints the results of the previous functions
print(f"{'Review #':<10}{'Words':<8}Preview")
print("-" * 70)
for index, review in enumerate(reviews, start=1):
    words = count_words(review)
    preview = review[:60] + ("..." if len(review) > 60 else "")
    print(f"{index:<10}{words:<8}{preview}")

# prints the summary of the word counts
print("\nSummary")

# prints 70 dashes as a simple divider under heading
print("-" * 70)

# prints how many reviews were counted
print(f"Total responses: {len(word_counts)}")

# prints smallest word count in the list
print(f"Shortest: {min(word_counts)} words")
# prints largest word count in the list
print(f"Longest: {max(word_counts)} words")
# prints average word count by adding all counts with sum and dividing by total, and eventually formats to one decimal 
print(f"Average: {sum(word_counts) / len(word_counts):.1f} words")
