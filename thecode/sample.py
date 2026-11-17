import pandas as pd

df = pd.read_csv("data/raw/BasicCompanyDataAsOneFile-2026-11-01/BasicCompanyDataAsOneFile-2026-11-01.csv", dtype=str)
df.columns = df.columns.str.strip()
df = df[df["CompanyStatus"] == "Active"]
df.sample(400, random_state=42).to_csv("data/sample.csv", index=False)