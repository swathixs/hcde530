import csv
import json
import os
import ssl
from urllib.request import urlopen


# Course demo API on Render: returns fake app reviews as JSON. BASE_URL is the server;
# REVIEWS_PATH asks for up to 100 review objects (pagination uses offset/limit on the API).
BASE_URL = "https://hcde530-week4-api.onrender.com"
REVIEWS_PATH = "/reviews?limit=100"
OUTPUT_FILE = "reviews_category_helpful.csv"
FILTERED_PREFIX = "reviews_category_helpful_"
FILTERED_SUFFIX = ".csv"

# Include the reviews with more than 30 helpful votes only (filtered file only)
VOTE_THRESHOLD = 30


def _next_filtered_csv_path() -> str:
    """Next path reviews_category_helpful_N.csv; N is highest existing number + 1 (new snapshot each run)."""
    here = os.path.dirname(os.path.abspath(__file__))
    highest = 0
    for name in os.listdir(here):
        if not name.startswith(FILTERED_PREFIX) or not name.endswith(FILTERED_SUFFIX):
            continue
        middle = name[len(FILTERED_PREFIX) : -len(FILTERED_SUFFIX)]
        if middle.isdigit():
            highest = max(highest, int(middle))
    return os.path.join(here, f"{FILTERED_PREFIX}{highest + 1}{FILTERED_SUFFIX}")


def _open_json_from_url(url: str) -> dict:
    """HTTPS GET and parse JSON, using common CA bundles if the default SSL store fails."""
    try:
        import certifi  # type: ignore[import-untyped]

        ca_candidates = [certifi.where()]
    except ImportError:
        ca_candidates = []
    ca_candidates.extend(
        ["/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt"]
    )

    last_err: OSError | None = None
    for cafile in ca_candidates:
        if not cafile or not os.path.isfile(cafile):
            continue
        try:
            ctx = ssl.create_default_context(cafile=cafile)
            with urlopen(url, context=ctx) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except OSError as e:
            last_err = e

    if last_err is not None:
        raise RuntimeError(
            "HTTPS fetch failed after trying CA bundles found on this machine. "
            "On macOS with python.org installers, run Install Certificates.command, "
            "or install certifi (`pip install certifi`)."
        ) from last_err
    raise RuntimeError(f"Could not find a CA bundle to validate HTTPS for {url!r}")


def main() -> None:
    url = f"{BASE_URL}{REVIEWS_PATH}"
    payload = _open_json_from_url(url)

    # The API returns metadata (total count, limit, offset) plus a "reviews" list. Each review
    # has app name, star rating, full text, dates, etc.—we only need category and helpful_votes.
    reviews = payload.get("reviews", [])
    all_rows: list[tuple[str, int]] = []
    filtered_rows: list[tuple[str, int]] = []
    out_dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(out_dir, OUTPUT_FILE)

    for item in reviews:
        # category: type of research tool (e.g. field research). helpful_votes: how many users
        # marked the review as helpful—used to find popular opinions (filter > 30 below).
        category = item.get("category", "")
        helpful = int(item.get("helpful_votes", 0) or 0)
        print(f"{category}: {helpful} helpful votes")
        all_rows.append((category, helpful))
        if helpful > VOTE_THRESHOLD:
            filtered_rows.append((category, helpful))

    # Full export: every fetched review’s category and vote count (matches the original assignment).
    with open(main_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "helpful votes"])
        writer.writerows(all_rows)

    # Numbered file: same two columns but only rows above the vote threshold (iteration snapshot).
    filtered_path = _next_filtered_csv_path()
    with open(filtered_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "helpful votes"])
        writer.writerows(filtered_rows)

    print(f"\nSaved {len(all_rows)} rows to {main_path}")
    print(
        f"Saved {len(filtered_rows)} rows (helpful votes > {VOTE_THRESHOLD}) to {filtered_path}"
    )


if __name__ == "__main__":
    main()
