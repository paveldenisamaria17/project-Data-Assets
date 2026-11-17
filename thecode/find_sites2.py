import os, re, time
from urllib.parse import urlparse
import pandas as pd
from ddgs import DDGS

OUT = r"C:\Users\pavel\Desktop\project-Data-Assets\data\companies_websites.csv"
GENERIC = {"ltd", "limited", "llp", "plc", "the", "and", "services", "service", "group", "holdings",
           "management", "consulting", "trading", "traders", "development", "company", "uk"}

def ok(name, url):
    d = re.sub(r"[^a-z0-9]", "", urlparse(url).netloc.lower())
    words = [w for w in re.findall(r"[a-z0-9]+", name.lower()) if len(w) >= 3 and w not in GENERIC]
    return "aclick" not in url and any(w in d for w in words)

def find(name, town):
    for _ in range(2):
        try:
            for x in DDGS(timeout=10).text(f"{name} {town}", max_results=10):
                if ok(name, x["href"]):
                    return x["href"]
            return None
        except Exception:
            time.sleep(5)
    return None

df = pd.read_csv("data/sample.csv", dtype=str).head(20)
rows = []
for _, r in df.iterrows():
    s = find(r["CompanyName"], r["RegAddress.PostTown"])
    print(r["CompanyName"], "->", s or "nimic")
    if s:
        rows.append({"CompanyName": r["CompanyName"], "Website": s})
    time.sleep(2)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
pd.DataFrame(rows).to_csv(OUT, index=False, encoding="utf-8-sig")
print(f"\nSalvat {len(rows)} firme în {OUT}")