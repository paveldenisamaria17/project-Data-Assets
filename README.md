# VAT Identifier Discovery

Pasul 1
Am colectat resursele necare si anume fisierele de la Companies House si le am pus in data/raw si am adaugat .gitignore pentru ca fisirele mari sa nu ajunga pe Github.
Am facut cont HMRC pentru a creea aplicatia VAT-test-find si am adaugat ca API "Check a UK VAT number 2.0" si am generat un client secret 

Step 2
I made the script sample.py which reads the Companies House file, keeps only the companies with status Active, and picks 400
of them at random into data/sample.csv.

Pasul 3 
Gasesc site-ul fiecarei firme
Mai intai am incercat pe 20 de firme inainte sa incerc pe 400 cu script-ul find_site.py
care afiseaza daca pentru primele 20 de firme din esantion exista site si il afiseaza daca exista. Le cauta pe DuckDuckGo numele + orasul.

