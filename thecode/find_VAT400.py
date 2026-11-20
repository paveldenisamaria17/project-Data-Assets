import os, re, asyncio
from urllib.parse import urlparse
import pandas as pd
from playwright.async_api import async_playwright

D = r"C:\Users\pavel\OneDrive\Imagini\Capturi de ecran\Documente\GitHub\project-Data-Assets\data"
IN = os.path.join(D, "companies_websites400.csv")
OUT = os.path.join(D, "vat_results_playwright.csv")
PAGES = ["", "/contact", "/contact-us", "/terms", "/terms-and-conditions", "/privacy-policy", "/about"]
VAT = re.compile(r"\bVAT\b[^0-9]{0,40}(?:GB)?\s?(\d[\d\s\-]{7,14}\d)(?!\d)", re.I)

def valid(n):
    if len(n) not in (9, 12):
        return False
    n = n[:9]
    s = sum(int(d) * w for d, w in zip(n[:7], range(8, 1, -1)))
    last = int(n[7:])
    return (s + last) % 97 == 0 or (s + last + 55) % 97 == 0

async def scan(ctx, r):
    u = urlparse(r["Website"])
    base = f"{u.scheme}://{u.netloc}"
    row = [r["CompanyNumber"], r["CompanyName"], base, "", "none"]
    page = await ctx.new_page()
    page.set_default_timeout(12000)
    await page.route("**/*.{png,jpg,jpeg,gif,webp,svg,woff,woff2,mp4,css}", lambda route: route.abort())
    try:
        for path in PAGES:
            try:
                resp = await page.goto(base + path, wait_until="domcontentloaded")
            except Exception:
                if path == "":
                    row[4] = "unreachable"
                    break
                continue
            if not resp:
                continue
            if resp.status == 403:
                row[4] = "blocked"
                continue
            if resp.status >= 400:
                continue
            try:
                await page.wait_for_timeout(800)
                await page.mouse.wheel(0, 20000)
                await page.wait_for_timeout(300)
                text = await page.inner_text("body")
            except Exception:
                continue
            hit = next((re.sub(r"\D", "", m.group(1)) for m in VAT.finditer(text)
                        if valid(re.sub(r"\D", "", m.group(1)))), "")
            if hit:
                row = [r["CompanyNumber"], r["CompanyName"], base + path, hit, "found"]
                break
    finally:
        await page.close()
    return row

async def work(ctx, sem, r, counter, total):
    async with sem:
        try:
            row = await asyncio.wait_for(scan(ctx, r), 60)
        except Exception:
            row = [r["CompanyNumber"], r["CompanyName"], r["Website"], "", "timeout"]
        counter[0] += 1
        print(f"[{counter[0]}/{total}]", r["CompanyName"], "->", row[4], row[3])
        return row

async def main():
    df = pd.read_csv(IN, dtype=str).fillna("")
    df = df[df["Website"].str.startswith("http")]
    sem = asyncio.Semaphore(10)
    counter = [0]
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36")
        rows = await asyncio.gather(*[work(ctx, sem, r, counter, len(df)) for _, r in df.iterrows()])
        await b.close()
    out = pd.DataFrame(rows, columns=["CompanyNumber", "CompanyName", "Page", "VAT", "Status"])
    out.to_csv(OUT, index=False, encoding="utf-8-sig")
    for s, n in out["Status"].value_counts().items():
        print(s, n)

asyncio.run(main())