import os
import time
import pandas as pd
from ddgs import DDGS

OUTPUT_DIR = r"C:\Users\pavel\Desktop\project-Data-Assets\data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "companies_websites.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv("data/sample.csv", dtype=str).head(20)

results = []

for i, r in df.iterrows():
    company = r["CompanyName"]
    q = company + " " + r["RegAddress.PostTown"]
    try:
        for x in DDGS().text(q, max_results=5):
            if "gov.uk" not in x["href"] and "dnb.com" not in x["href"]:
                print(company, "->", x["href"])
                results.append({"CompanyName": company, "Website": x["href"]})
                break
        else:
            print(company, "-> nimic")
    except Exception as e:
        print(company, "-> eroare:", e)
    time.sleep(3)

out_df = pd.DataFrame(results, columns=["CompanyName", "Website"])
out_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
print(f"\nSalvat {len(out_df)} firme în {OUTPUT_FILE}")