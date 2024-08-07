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
    primer_plače = r'<strong>(.*?)</strong>'
    primer_kraj = r'<svg class="ticon text-primary">.*?</svg>\s*([^<]+)'
    primer_delovnik = r'<li>Delovnik: <strong><!--sse-->(.*?)<!--/sse--></strong></li>'
    primer_trajanje = r'<li>Trajanje: <strong><!--sse-->(.*?)<!--/sse--></strong></li>'
    
    delo = re.search(primer_dela, oglas)
    plača_neto = re.search(primer_plače, oglas)
    kraj = re.search(primer_kraj, oglas)
    kraj_olepšan_zapis = re.sub(r'\s+', ' ', kraj.group(1)).strip()
    delovnik = re.search(primer_delovnik, oglas)
    trajanje = re.search(primer_trajanje, oglas)

    if not delo or not plača_neto or not trajanje or not kraj or not delovnik:
        return None

    return {'delo': delo.group(1), 
            'plača neto': plača_neto.group(1), 
            'kraj': kraj_olepšan_zapis, 
            'delovnik':delovnik.group(1), 
            'trajanje': trajanje.group(1)
            }

def izpisi_podatke(oglasi):
    data = []
    for oglas in oglasi:
        podrobnosti = podatki_o_delu(oglas)
        if podrobnosti:  # Only add if details is not None
            data.append(podrobnosti)
            print(f"Extracted details for {len(data)} job ads")
    return data
data = izpisi_podatke(oglasi)
##########################################################################################

# Določi ime CSV datoteke
csv_file = 'studentska_dela.csv'

# Zapiši podatke v CSV datoteko
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['delo', 'plača neto', 'kraj', 'delovnik', 'trajanje'])
    writer.writeheader()
    writer.writerows(data)

print(f"Podatki so shranjeni v '{csv_file}'.")
