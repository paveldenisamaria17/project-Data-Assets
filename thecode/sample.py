import glob
import pandas as pd

path = glob.glob("data/raw/**/*.csv", recursive=True)[0]
print("Citesc:", path)

cols = ["CompanyName", "CompanyNumber", "CompanyStatus", "CompanyCategory",
        "RegAddress.PostTown", "RegAddress.PostCode",
        "SICCode.SicText_1", "Accounts.AccountCategory", "URI"]

parts = []
for chunk in pd.read_csv(path, chunksize=500000, dtype=str, skipinitialspace=True):
    chunk.columns = chunk.columns.str.strip()
    chunk = chunk[chunk["CompanyStatus"] == "Active"]
    chunk = chunk[chunk["CompanyCategory"] == "Private Limited Company"]
    parts.append(chunk[cols])

df = pd.concat(parts)
print("Firme active (Private Limited):", len(df))

sample = df.sample(n=400, random_state=42)
sample.to_csv("data/sample.csv", index=False)
print("Salvat data/sample.csv cu", len(sample), "firme")