import re
import requests

def url_v_str(url):
    html = requests.get(url)
    html.raise_for_status()
    return html.text

def poisci_vse_oglase(stran):
    oglasi = re.findall(r'<article class="job-item" data-jobid=.*?>(.*?)</article>', stran, re.DOTALL)
    # print(f"Najde {len(oglasi)} oglasov")
    return oglasi

def poisci_delo(oglas):
    primer_dela = r'<h5 class="mb-0">(.*?)</h5>'
    delo = re.search(primer_dela, oglas)
    if delo:
        return delo.group(1)
    else:
        return None

def poisci_placo(oglas):
    primer_place = r'<strong>(.*?)</strong>'
    placa = re.search(primer_place, oglas)
    if placa:
        return placa.group(1)
    else:
        return None

def poisci_kraj(oglas):
    primer_kraja = r'<svg class="ticon text-primary">.*?</svg>\s*([^<]+)'
    rezultat = re.search(primer_kraja, oglas)
    if rezultat:
        kraj_olepsan = re.sub(r'\s+', ' ', rezultat.group(1)).strip()
        return kraj_olepsan
    else:
        return None

def poisci_delovnik(oglas):
    primer_delovnika = r'<li>Delovnik: <strong><!--sse-->(.*?)<!--/sse--></strong></li>'
    delovnik = re.search(primer_delovnika, oglas)
    if delovnik:
        return delovnik.group(1)
    else:
        return None

def poisici_trajanje(oglas):
    primer_trajanja = r'<li>Trajanje: <strong><!--sse-->(.*?)<!--/sse--></strong></li>'
    trajanje = re.search(primer_trajanja, oglas)
    if trajanje:
        return trajanje.group(1)
    else:
        return None
