# VAT Identifier Discovery

Step 1
I collected the necessary resources, specifically the files from Companies House,
placed them in data/raw, and added a .gitignore file to prevent large files from being pushed to GitHub.
I created an HMRC account to set up the VAT-test-find application, 
added the "Check a UK VAT number 2.0" API, and generated a client secret.

Step 2
I made the sample.py script, which reads the Companies House file, 
keeps only the companies with an Active status, and randomly picks 400 of them into data/sample.csv.

Step 3
Finding Each Company's Website
First, I tested on 20 companies before running it on all 400 using the find_site.py script. 
This script checks whether a website exists for the first 20 companies in the sample and displays it if found. 
It searches DuckDuckGo using the company name and city.

Website Test Results (First 20 companies via DuckDuckGo, Name + City):
2 likely correct websites
9 Companies House pages
1 directory page (D&B)
8 nothing found

Manual Verification:
7 have their own website, 14 do not.

The script successfully found the website for 2 out of 7.
It missed 5 (1 returned a D&B directory, 4 returned nothing).
For the 13 companies without a website, it did not return any incorrect websites.

VAT found on website: 1 out of 20 (Giacom, not yet verified with HMRC).

I rewrote the script as find_sites2.py to filter out Companies House links and directories.
I changed find_sites2.py to save the sites with valid links into a CSV file. However, if some directory sites still appear, it is because I cannot block all of them completely.

Step 4
I installed a real browser using Playwright.
Using the script to search for VAT numbers on those 7 sites, I found:
The only company out of all of them that has a VAT number is:

VAT ✔ GIACOM (DEVELOPMENT) LIMITED -> https://giacom.com

Step 5
I will update the scripts to run for the full sample of 400.
A much faster approach is to guess the domain name directly from the company name and check it using 30 threads in parallel with 3 domain choices per company.

108 websites found out of 400

The VAT script for the 400-company sample showed:
none: 83
blocked: 23
found: 2

I ran all 108 websites directly using Playwright with 5 tabs in parallel.
(blocked here means the website returns a 403 error even in a real browser.)
The result of finding only 2 VAT numbers for a list of 400 companies is very low.
