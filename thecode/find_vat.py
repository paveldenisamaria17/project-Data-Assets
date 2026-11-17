import re
from urllib.parse import urlparse
import pandas as pd
from playwright.sync_api import sync_playwright

CSV = r"C:\Users\pavel\Desktop\project-Data-Assets\data\companies_websites.csv"
PAGES = ["", "/contact", "/contact-us", "/terms", "/terms-and-conditions", "/privacy-policy", "/about"]
VAT = re.compile(r"\bVAT\b", re.I)

with sync_playwright() as p:
    b = p.chromium.launch(headless=False)  # False = trece mai ușor de Cloudflare
    page = b.new_page()
    for _, r in pd.read_csv(CSV).iterrows():
        u = urlparse(r["Website"])
        base = f"{u.scheme}://{u.netloc}"
        for path in PAGES:
            try:
                resp = page.goto(base + path, timeout=20000, wait_until="domcontentloaded")
                if not resp or resp.status >= 400:
                    continue
                page.wait_for_timeout(1500)
                page.mouse.wheel(0, 20000)  # scroll jos, pentru footer încărcat lazy
                page.wait_for_timeout(500)
                if VAT.search(page.inner_text("body")):
                    print("VAT ✔", r["CompanyName"], "->", base + path)
                    break
            except Exception:
                pass
    b.close()