import requests
import re
import csv

# URL studentskih del
url = 'https://www.studentski-servis.com/studenti/prosta-dela/'

# URL spremenimo v niz
def url_v_str(url):
    html = requests.get(url)
    return html.text
vsebina_strani = url_v_str(url)

# Funkcija shrani HTML vsebino v 'dela.html'
with open('dela.html', 'w', encoding='utf-8') as file:
    file.write(vsebina_strani)
##########################################################################################

def poisci_vse_oglase(vsebina_strani):
    return re.findall(r'<article class="job-item" data-jobid=.*?>', vsebina_strani, re.DOTALL)
oglasi = poisci_vse_oglase(vsebina_strani)

def podatki_iz_oglasov(oglas):
    primer_dela = r'<h5 class="mb-0">(.*?)</h5>'
    primer_kraj = r'<use.*?></use> (.*?) </p>'
    primer_cena = r'<strong>(.*?) €/h neto</strong>'
    primer_opisa = r'<p class="description text-break">(.*?)</p>'
    delo = re.search(primer_dela, oglas)
    kraj = re.search(primer_kraj, oglas)
    cena = re.search(primer_cena, oglas)
    opis = re.search(primer_opisa, oglas)
    if delo == None or kraj == None or cena == None or opis == None:
        return None
    if 'PO DOGOVORU' in cena.group(1):
        cena = 'PO DOGOVORU'
    else:
        cena = cena.group(1)
    return {'delo': delo.group(1), 'kraj':kraj.group(1), 'cena': cena, 'opis':opis.group(1)}
##########################################################################################

data = []
for oglas in oglasi:
    oglas_podatki = podatki_iz_oglasov(oglas)
    if oglas_podatki is not None:
        data.append(oglas_podatki)

# Določi ime CSV datoteke
csv_file = 'studentska_dela.csv'

# Zapiši podatke v CSV datoteko
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Zapiši glave stolpcev
    writer.writerow(['delo', 'kraj', 'plača', 'opis'])
    # Zapiši podatke
    for oglas_podatki in data:
        writer.writerow([oglas_podatki['delo'], oglas_podatki['kraj'], oglas_podatki['cena'], oglas_podatki['opis']])

print(f"Podatki so shranjeni v '{csv_file}'.")
