from funkcije import *

url = 'https://www.studentski-servis.com/studenti/prosta-dela/'
vsebina_strani = url_v_str(url)

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

def obdelaj_oglase(oglasi, število_oglasov):
    obdelani_oglasi = []
    for oglas in oglasi:
        podrobnosti = podatki_o_delu(oglas)
        if podrobnosti is not None:
            obdelani_oglasi.append(podrobnosti)
            if len(obdelani_oglasi) >= število_oglasov:
                break
    return obdelani_oglasi

def pridobi_podatke_iz_strani(url, število_oglasov=2000):
    stran = 1
    vsa_data = []
    while len(vsa_data) < število_oglasov:
        trenutna_stran = f"{url}?page={stran}"
        vsebina_strani = url_v_str(trenutna_stran)
        oglasi = poisci_vse_oglase(vsebina_strani)
        if not oglasi:
            break
        obdelani_oglasi = obdelaj_oglase(oglasi, število_oglasov - len(vsa_data))
        vsa_data.extend(obdelani_oglasi)
        stran += 1
    return vsa_data


