import os, re
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests

D = r"C:\Users\pavel\Desktop\project-Data-Assets\data"
IN = os.path.join(D, "sample.csv")
OUT = os.path.join(D, "companies_websites400.csv")
GENERIC = {"ltd", "limited", "llp", "plc", "the", "and", "uk"}
H = {"User-Agent": "Mozilla/5.0"}

def find(r):
    words = [w for w in re.findall(r"[a-z0-9]+", r["CompanyName"].lower()) if w not in GENERIC]
    if not words:
        return r["CompanyNumber"], r["CompanyName"], ""
    slugs = {"".join(words), "-".join(words)}
    for s in slugs:
        for tld in (".co.uk", ".com", ".uk", ".org.uk", ".net"):
            for pre in ("https://www.", "https://"):
                try:
                    x = requests.get(pre + s + tld, timeout=5, headers=H)
                except Exception:
                    continue
                text = re.sub(r"<[^>]+>", " ", x.text).lower()
                if x.status_code == 403 or (x.status_code == 200 and " ".join(words) in text):
                    return r["CompanyNumber"], r["CompanyName"], pre + s + tld
    return r["CompanyNumber"], r["CompanyName"], ""

df = pd.read_csv(IN, dtype=str)
df.columns = df.columns.str.strip()

with ThreadPoolExecutor(40) as ex:
    rows = list(ex.map(find, [r for _, r in df.iterrows()]))

out = pd.DataFrame(rows, columns=["CompanyNumber", "CompanyName", "Website"])
out.to_csv(OUT, index=False, encoding="utf-8-sig")
print(len(out[out.Website != ""]), "with site out of", len(out))