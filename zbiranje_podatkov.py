import requests
import re
import csv

# URL strani
url = 'https://www.studentski-servis.com/studenti/prosta-dela/'

# Pošlji GET zahtevo na stran
html = requests.get(url)
vsebina_strani = html.text

# Regularni izrazi za iskanje potrebnih informacij
primeri_službe = re.compile(r'<article class="job-item" data-jobid=.*?>(.*?)</div>', re.DOTALL)
primer_dela = re.compile(r'<h3>(.*?)</h3>', re.DOTALL)
primer_kraj = re.compile(r'</use></svg> (.*?) </p>', re.DOTALL)
primer_cena = re.compile(r'<strong>.*? €/h neto</strong> (.*? €/h bruto)</a>', re.DOTALL)
primer_opisa = re.compile(r'<p class="description text-break">(.*?) </p>', re.DOTALL)

# Najdi vse oglase
službe = primeri_službe.findall(vsebina_strani)
# Pripravi seznam za shranjevanje podatkov
data = []
# Za vsak oglas pridobi potrebne informacije
for služba in službe:
    delo = primer_dela.search(služba)
    kraj = primer_kraj.search(služba)
    plača = primer_cena.search(služba)
    opis = primer_opisa.search(služba)

    # Preveri, ali so vsi podatki najdeni
    if delo and kraj and plača and opis:
        data.append([delo.group(1).strip(), kraj.group(1).strip(), plača.group(1).strip(), opis.group(1).strip()])

# Določi ime CSV datoteke
csv_file = 'studentska_dela.csv'
# Zapiši podatke v CSV datoteko
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Zapiši glave stolpcev
    writer.writerow(['delo', 'kraj', 'plača', 'opis'])
    # Zapiši podatke
    writer.writerows(data)

print(f"Podatki so shranjeni v '{csv_file}'.")
