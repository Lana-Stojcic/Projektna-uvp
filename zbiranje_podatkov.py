from funkcije import *
import csv

# URL studentskih del
url = 'https://www.studentski-servis.com/studenti/prosta-dela/'
vsebina_strani = url_v_str(url)

# Funkcija shrani HTML vsebino v 'dela.html'
with open('dela.html', 'w', encoding='utf-8') as file:
    file.write(vsebina_strani)

oglasi = poisci_vse_oglase(vsebina_strani)

def podatki_o_delu(oglas):
    delo = poisci_delo(oglas)
    placa_neto = poisci_placo(oglas)
    kraj = poisci_kraj(oglas)
    delovnik = poisci_delovnik(oglas)
    trajanje = poisici_trajanje(oglas)

    return {
        'delo': delo,
        'plača neto': placa_neto,
        'kraj': kraj,
        'delovnik': delovnik,
        'trajanje': trajanje
    }

def izpisi_podatke(url, max_oglasi=2000):
    stran = 1
    vsa_data = []
    while len(vsa_data) < max_oglasi:
        trenutna_stran = f"{url}?page={stran}"
        vsebina_strani = url_v_str(trenutna_stran)
        oglasi = poisci_vse_oglase(vsebina_strani)
        if not oglasi:
            break
        for oglas in oglasi:
            podrobnosti = podatki_o_delu(oglas)
            if podrobnosti != None:
                vsa_data.append(podrobnosti)
                if len(vsa_data) >= max_oglasi:
                    break
        stran += 1
    return vsa_data

data = izpisi_podatke(url)
csv_file = 'studentska_dela.csv'

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['delo', 'plača neto', 'kraj', 'delovnik', 'trajanje'])
    writer.writeheader()
    writer.writerows(data)

print(f"Podatki so shranjeni v '{csv_file}'.")
