import os, re
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import requests

D = r"C:\Users\pavel\OneDrive\Imagini\Capturi de ecran\Documente\GitHub\project-Data-Assets\data"
IN = os.path.join(D, "sample.csv")
OUT = os.path.join(D, "companies_websites400.csv")
GENERIC = {"ltd", "limited", "llp", "plc", "the", "and", "uk"}
H = {"User-Agent": "Mozilla/5.0"}

def candidates(name):
    name = re.sub(r"\(.*?\)", " ", name.lower())
    words = [w for w in re.findall(r"[a-z0-9]+", name) if w not in GENERIC]
    out = []
    if words:
        out.append(("full", words, "".join(words)))
        if len(words) > 2:
            out.append(("partial", words[:2], "".join(words[:2])))
        if len(words) > 1 and len(words[0]) >= 4:
            out.append(("partial", words[:1], words[0]))
    return out

def find(r):
    for kind, words, slug in candidates(r["CompanyName"]):
        for tld in (".co.uk", ".com", ".uk"):
            url = "https://www." + slug + tld
            try:
                x = requests.get(url, timeout=(3, 4), headers=H)
            except Exception:
                continue
            text = re.sub(r"<[^>]+>", " ", x.text).lower()
            if x.status_code == 403 or (x.status_code == 200 and " ".join(words) in text):
                return r["CompanyNumber"], r["CompanyName"], url, kind
    return r["CompanyNumber"], r["CompanyName"], "", ""

df = pd.read_csv(IN, dtype=str)
df.columns = df.columns.str.strip()

rows = []
with ThreadPoolExecutor(30) as ex:
    for i, f in enumerate(as_completed([ex.submit(find, r) for _, r in df.iterrows()]), 1):
        rows.append(f.result())
        print(f"[{i}/{len(df)}]", rows[-1][1], "->", rows[-1][2] or "nimic", rows[-1][3])

out = pd.DataFrame(rows, columns=["CompanyNumber", "CompanyName", "Website", "Match"])
out.to_csv(OUT, index=False, encoding="utf-8-sig")
print(len(out[out.Website != ""]), "cu site din", len(out))