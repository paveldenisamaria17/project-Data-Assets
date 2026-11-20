import os, re
from urllib.parse import urlparse
import pandas as pd
from playwright.sync_api import sync_playwright

D = r"C:\Users\pavel\OneDrive\Imagini\Capturi de ecran\Documente\GitHub\project-Data-Assets\data"
IN = os.path.join(D, "companies_websites.csv")
OUT = os.path.join(D, "vat_results_20.csv")
PAGES = ["", "/contact", "/contact-us", "/terms", "/terms-and-conditions", "/privacy-policy", "/about"]
WORD = re.compile(r"\bVAT\b", re.I)
NUM = re.compile(r"\bVAT\b[^0-9]{0,40}(?:GB)?\s?(\d[\d\s\-]{7,14}\d)(?!\d)", re.I)

def valid(n):
    if len(n) not in (9, 12):
        return False
    n = n[:9]
    s = sum(int(d) * w for d, w in zip(n[:7], range(8, 1, -1)))
    last = int(n[7:])
    return (s + last) % 97 == 0 or (s + last + 55) % 97 == 0

df = pd.read_csv(IN, dtype=str).fillna("")
df = df[df["Website"].str.startswith("http")]
rows = []

with sync_playwright() as p:
    b = p.chromium.launch(headless=False)
    page = b.new_page()
    for i, (_, r) in enumerate(df.iterrows(), 1):
        u = urlparse(r["Website"])
        base = f"{u.scheme}://{u.netloc}"
        row = [r["CompanyNumber"], r["CompanyName"], base, "", "none"]
        for path in PAGES:
            try:
                resp = page.goto(base + path, timeout=20000, wait_until="domcontentloaded")
                if not resp:
                    continue
                if resp.status == 403:
                    if row[4] == "none":
                        row[4] = "blocked"
                    continue
                if resp.status >= 400:
                    continue
                page.wait_for_timeout(1500)
                page.mouse.wheel(0, 20000)
                page.wait_for_timeout(500)
                text = page.inner_text("body")
            except Exception:
                continue
            hit = next((re.sub(r"\D", "", m.group(1)) for m in NUM.finditer(text)
                        if valid(re.sub(r"\D", "", m.group(1)))), "")
            if hit:
                row = [r["CompanyNumber"], r["CompanyName"], base + path, hit, "found"]
                break
            if WORD.search(text) and row[4] != "word_only":
                row = [r["CompanyNumber"], r["CompanyName"], base + path, "", "word_only"]
        rows.append(row)
        print(f"[{i}/{len(df)}]", r["CompanyName"], "->", row[4], row[3])
    b.close()

out = pd.DataFrame(rows, columns=["CompanyNumber", "CompanyName", "Page", "VAT", "Status"])
out.to_csv(OUT, index=False, encoding="utf-8-sig")
for s, n in out["Status"].value_counts().items():
    print(s, n)