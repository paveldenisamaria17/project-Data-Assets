import os, re
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import requests

D = r"C:\Users\pavel\Desktop\project-Data-Assets\data"
IN = os.path.join(D, "sample.csv")
OUT = os.path.join(D, "companies_websites400.csv")
GENERIC = {"ltd", "limited", "llp", "plc", "the", "and", "uk"}
H = {"User-Agent": "Mozilla/5.0"}

def find(r):
    words = [w for w in re.findall(r"[a-z0-9]+", r["CompanyName"].lower()) if w not in GENERIC]
    site = ""
    if words:
        for tld in (".co.uk", ".com", ".uk"):
            url = "https://www." + "".join(words) + tld
            try:
                x = requests.get(url, timeout=(3, 4), headers=H)
            except Exception:
                continue
            text = re.sub(r"<[^>]+>", " ", x.text).lower()
            if x.status_code == 403 or (x.status_code == 200 and " ".join(words) in text):
                site = url
                break
    return r["CompanyNumber"], r["CompanyName"], site

df = pd.read_csv(IN, dtype=str)
df.columns = df.columns.str.strip()

rows = []
with ThreadPoolExecutor(30) as ex:
    for i, f in enumerate(as_completed([ex.submit(find, r) for _, r in df.iterrows()]), 1):
        rows.append(f.result())
        print(f"[{i}/{len(df)}]", rows[-1][1], "->", rows[-1][2] or "nimic")

out = pd.DataFrame(rows, columns=["CompanyNumber", "CompanyName", "Website"])
out.to_csv(OUT, index=False, encoding="utf-8-sig")
print(len(out[out.Website != ""]), "cu site din", len(out))