from zbiranje_podatkov import *
import csv

url = 'https://www.studentski-servis.com/studenti/prosta-dela/'

data = pridobi_podatke_iz_strani(url)
csv_file = 'studentska_dela.csv'

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['delo', 'plača neto', 'kraj', 'delovnik', 'trajanje'])
    writer.writeheader()
    writer.writerows(data)

print(f"Podatki so shranjeni v '{csv_file}'.")
