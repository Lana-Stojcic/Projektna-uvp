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
    oglasi = re.findall(r'<article class="job-item" data-jobid=.*?>(.*?)</article>>', stran, re.DOTALL)
    print(f"Found {len(oglasi)} job ads")
    return oglasi
oglasi = poisci_vse_oglase(vsebina_strani)

def podatki_o_delu(oglas):
    primer_dela = r'<h5 class="mb-0">(.*?)</h5>'
    primer_kraj = r'<svg class="ticon text-primary"><use xlink:href=.*?></use></svg> (.*?)</p>'
    primer_cena = r'<strong>(.*?) €/h neto</strong>'

    delo = re.search(primer_dela, oglas)
    kraj = re.search(primer_kraj, oglas)
    cena = re.search(primer_cena, oglas)

    print(f"Processing job ad: {oglasi[:100]}...")  # Print first 100 characters of the ad for context
    print(f"delo: {delo.group(1) if delo else 'None'}")
    print(f"kraj: {kraj.group(1) if kraj else 'None'}")
    print(f"cena: {cena.group(1) if cena else 'None'}")

    if not delo or not kraj or not cena:
        return None
    if 'PO DOGOVORU' in cena.group(1):
        cena_value = 'PO DOGOVORU'
    else:
        cena_value = cena.group(1)
    return {
        'delo': delo.group(1),
        'kraj': kraj.group(1),
        'cena': cena_value,
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
    writer = csv.writer(file)
    # Zapiši glave stolpcev
    writer.writerow(['delo', 'kraj', 'plača'])
    # Zapiši podatke
    writer.writerow(data)

print(f"Podatki so shranjeni v '{csv_file}'.")
