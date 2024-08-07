import requests
import re
import csv

# URL studentskih del
url = 'https://www.studentski-servis.com/studenti/prosta-dela/'

# URL spremenimo v niz
def url_v_str(url):
    html = requests.get(url)
    html.raise_for_status()
    return html.text
vsebina_strani = url_v_str(url)

# Funkcija shrani HTML vsebino v 'dela.html'
with open('dela.html', 'w', encoding='utf-8') as file:
    file.write(vsebina_strani)
##########################################################################################

def poisci_vse_oglase(stran):
    oglasi = re.findall(r'<article class="job-item" data-jobid=.*?>(.*?)</article>', stran, re.DOTALL)
    print(f"Found {len(oglasi)} job ads")
    return oglasi
oglasi = poisci_vse_oglase(vsebina_strani)

def podatki_o_delu(oglas):
    primer_dela = r'<h5 class="mb-0">(.*?)</h5>'
    primer_plače = r'<strong>(.*?)</strong> (.*?)</a>'
    delo = re.search(primer_dela, oglas)
    plača_neto = re.search(primer_plače, oglas)
    if not delo:
        return None
    if not plača_neto:
        return None
    return {
        'delo': delo.group(1),
        'plača': plača_neto.group(1)
    }

def izpisi_podatke(oglasi):
    data = []
    for oglas in oglasi:
        details = podatki_o_delu(oglas)
        if details:  # Only add if details is not None
            data.append(details)
            print(f"Extracted details for {len(data)} job ads")
    return data
data = izpisi_podatke(oglasi)
##########################################################################################

# Določi ime CSV datoteke
csv_file = 'studentska_dela.csv'

# Zapiši podatke v CSV datoteko
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['delo', 'plača'])
    writer.writeheader()
    writer.writerows(data)

print(f"Podatki so shranjeni v '{csv_file}'.")
