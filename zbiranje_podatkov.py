import requests
import re
import csv

# URL strani
url = 'https://www.studentski-servis.com/studenti/prosta-dela/'

# Pošlji GET zahtevo na stran
response = requests.get(url)
page_content = response.text

# Regularni izrazi za iskanje potrebnih informacij
job_pattern = re.compile(r'<div class="job-item">(.*?)</div>', re.DOTALL)
title_pattern = re.compile(r'<h3>(.*?)</h3>', re.DOTALL)
location_pattern = re.compile(r'<div class="job-location">(.*?)</div>', re.DOTALL)
date_pattern = re.compile(r'<div class="job-date">(.*?)</div>', re.DOTALL)
description_pattern = re.compile(r'<div class="job-description">(.*?)</div>', re.DOTALL)

# Najdi vse oglase
jobs = job_pattern.findall(page_content)

# Pripravi seznam za shranjevanje podatkov
data = []

# Za vsak oglas pridobi potrebne informacije
for job in jobs:
    title = title_pattern.search(job).group(1).strip()
    location = location_pattern.search(job).group(1).strip()
    date = date_pattern.search(job).group(1).strip()
    description = description_pattern.search(job).group(1).strip()
    
    # Dodaj podatke v seznam
    data.append([title, location, date, description])

# Določi ime CSV datoteke
csv_file = 'student_jobs.csv'

# Zapiši podatke v CSV datoteko
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Zapiši glave stolpcev
    writer.writerow(['Title', 'Location', 'Date', 'Description'])
    # Zapiši podatke
    writer.writerows(data)

print(f"Podatki so shranjeni v '{csv_file}'.")
