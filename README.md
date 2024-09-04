# Projektna-uvp
Avtorica: Lana Stojčić

# Uvod
Za projektno nalogo sem analizirala podatke s spletne strani študentskega servisa o prostih delih (https://www.studentski-servis.com/studenti/prosta-dela/). Osredotočila sem se le na 2000 prostih del, zanimali pa so me predvsem podatki o neto plači, kraju, delovniku, trajanju in vrsti deli.

# Navodila
Za delovanje programa naj ima uporabnik naložene knjižnice re, requests, csv, pandas in matplotlib.pyplot.

# Kratek opis
V 'funkcije.py' se nahajajo funkcije, ki iz oglasov poiščejo podatke o vrsti dela, neto plači, kraju, delovniku in trajanju.\
V 'zbiranje_podatkov.py' imamo 3 funkcije:\
    1. Funkcija 'podatki o delu' vrne slovar, ki izpiše podatke o delu,\
    2. Funkcija 'obdelaj_oglase' pregleda seznam oglasov in iz posameznega oglasa pridobi podrobnosti o delu, ter jih shrani v nov seznam. Postopek se ponavlja, dokler ne obdelamo določenega števila oglasov,\
    3. Funkcija 'pridobi_podatke_iz_strani' pridobiva podatke o oglasih z več strani določenega URL-ja.\
V 'zapisi_csv.py' funkcija zapiše csv s podatki o študentskih delih.\
Analiza podatkov, pa se nahaja v 'analiza.ipynb'.

# Opomba
Analiza del prikazuje podatke o oglasih, ki so bili objavljeni na študentskem servisu dne 25. 08. 2024.
Ker je skoraj vsak dan dodan nov oglas, ali pa je kateri odstranjen, so podatki uporabljeni v analizi zastareli.
Če jih želimo posodobiti, moramo najprej pognati 'zapisi_csv.py' in nato še 'analiza.ipynb'.
