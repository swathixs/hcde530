import csv
import json
import os
import ssl
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from dotenv import load_dotenv


# This API is a Google Developer Fonts API that lists all the hosted web fonts Google provides. It includes information
# about what typefaces the fonts belong to (serif, sans-serif, etc), as well as weights and variants. I added this 
# API key to an .env file in the folder for security reasons and so that Google authenticates the request. Then, I used the Python script
# to pull only the serif fonts and save the extracted data to the CSV file mentioned below. I'm choosing to extract this specific type of font because
# it's most commonly used in UX and Visual Design for better readability. I've had moments in my HCD work where I'm working on typography and I can't 
# filter by font family, so this script certainly helps out with that action. This matters for HCD work because it tightens my workflow when figuring out
# the best font to use for a specific project. I don't have to manually search them up.
FONTS_API_BASE = "https://www.googleapis.com/webfonts/v1/webfonts"
OUTPUT_FILE = "serif_fonts.csv"


def _open_json_from_url(url: str) -> dict:
    """HTTPS GET and parse JSON, using common CA bundles if the default SSL store fails."""
    # HTTPS requires trusted certificate locations so the script works on more computers like Mac and Linux
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
    # Put the key only in hcde530_week4/.env so it does not have to be exposed in the code. 
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit(
            f"Missing GOOGLE_API_KEY in {env_path} (or environment). "
            "Add your Google API key to .env."
        )

    # Build the URL by combining the base endpoint with the API key required by Google.
    query = urlencode({"key": api_key})
    url = f"{FONTS_API_BASE}?{query}"
    payload = _open_json_from_url(url)

    # The API returns one JSON object with an "items" array. Each element describes one font:
    # family name, category (serif, sans-serif, ...), variants (weights/styles), and more.
    items = payload.get("items") or []
    # Keep only serif fonts so the CSV matches the assignment filter and returns specifically what I asked for.
    serif_fonts = [item for item in items if item.get("category") == "serif"]

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / OUTPUT_FILE
    rows: list[tuple[str, str, str]] = []

    for item in serif_fonts:
        # family: this will display the name of the font. category: this one shows me that serif fonts have been correctly pulled out.
        # variants: list of strings like "regular", "700", "italic" — which styles exist for CSS. it adds more detail to just the serif fonts, differentiating them by styles like bold, italic, etc.
        family = item.get("family", "")
        category = item.get("category", "")
        variants = item.get("variants") or []
        variants_str = ", ".join(str(v) for v in variants)
        print(f"{family} | {category} | variants: {variants_str}")
        rows.append((family, category, variants_str))

    # Save the three fields so we can open them in a spreadsheet or reuse them in the UI/CSS.
    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["family", "category", "variants"])
        writer.writerows(rows)

    print(f"\nSaved {len(rows)} serif fonts to {out_path}")


if __name__ == "__main__":
    main()
