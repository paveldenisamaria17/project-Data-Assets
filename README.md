# VAT Identifier Discovery

Step 1
Am colectat resursele necare si anume fisierele de la Companies House si le am pus in data/raw si am adaugat .gitignore pentru ca fisirele mari sa nu ajunga pe Github.
Am facut cont HMRC pentru a creea aplicatia VAT-test-find si am adaugat ca API "Check a UK VAT number 2.0" si am generat un client secret 

Step 2
I made the script sample.py which reads the Companies House file, keeps only the companies with status Active, and picks 400
of them at random into data/sample.csv.

Step 3 
Gasesc site-ul fiecarei firme
Mai intai am incercat pe 20 de firme inainte sa incerc pe 400 cu script-ul find_site.py
care afiseaza daca pentru primele 20 de firme din esantion exista site si il afiseaza daca exista. Le cauta pe DuckDuckGo numele + orasul.

Test site-uri, primele 20 firme (DuckDuckGo, nume + oras): 
2 site-uri probabil corecte, 
9 pagini Companies House, 
1 director (dnb), 
8 nimic

Verificat manual:
7 au site propriu, 14 nu au. 
Scriptul a gasit site-ul la 2 din 7,
a ratat 5 (1 a dat director dnb, 4 au dat nimic).
La cele 13 fara site nu a dat niciun site gresit.
VAT pe site: 1 din 20 (Giacom, neverificat inca la HMRC).

Am refacut script-ul incat sa fie find_sites2.py si ar trebui sa nu afiseze companies house sites si directoare dar
find_sites2.py rulat de 3 ori pe aceleasi 20 firme da rezultate diferite de fiecare data (Wild Box gasit/pierdut/gasit). Rularea 3 a gasit 4 din 7 site-uri cunoscute (Wild Box, Sonatune, Kilncare, Koel). Au trecut de filtru 5 directoare noi 
+ o reclama Bing. 
