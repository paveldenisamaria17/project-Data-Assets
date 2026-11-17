import time
import pandas as pd
from ddgs import DDGS

df = pd.read_csv("data/sample.csv", dtype=str).head(20)

for i, r in df.iterrows():
    q = r["CompanyName"] + " " + r["RegAddress.PostTown"]
    try:
        res = DDGS().text(q, max_results=1)
        print(r["CompanyName"], "->", res[0]["href"])
    except:
        print(r["CompanyName"], "-> nimic")
    time.sleep(3)