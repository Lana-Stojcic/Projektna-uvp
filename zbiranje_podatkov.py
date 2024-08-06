import csv
import os
import re
import requests
###############################################################################
# Najprej definirajmo nekaj pomožnih orodij za pridobivanje podatkov s spleta.
###############################################################################

# definirajte URL glavne strani bolhe za oglase z mačkami
url = 'https://www.studentski-servis.com/studenti/prosta-dela/'
# mapa, v katero bomo shranili podatke
dela_directory = 'podatki'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'dela.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'dela.csv'


def download_url_to_string(url):
    """Funkcija kot argument sprejme niz in poskusi vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try:
        # del kode, ki morda sproži napako
        headers = {'User-agent': 'Chrome/124.0.6367.201'}
        page_content = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print('Spletna stran ni dosegljiva.')
        return None
    # nadaljujemo s kodo če ni prišlo do napake
    return page_content.text


def save_string_to_file(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


# Definirajte funkcijo, ki prenese glavno stran in jo shrani v datoteko.


def save_frontpage(page, directory, filename):
    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
    "directory"/"filename"."""
    text = download_url_to_string(page)
    if text:
        save_string_to_file(text, directory, filename)
    return text

save_frontpage(url, dela_directory, frontpage_filename)
###############################################################################
# Po pridobitvi podatkov jih želimo obdelati.
###############################################################################


def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz."""
    path = os.path.join(directory, filename)
    with open(path, "r", encoding='UTF-8') as file_in:
        text = file_in.read()
    return text


# Definirajte funkcijo, ki sprejme niz, ki predstavlja vsebino spletne strani,
# in ga razdeli na dele, kjer vsak del predstavlja en oglas. To storite s
# pomočjo regularnih izrazov, ki označujejo začetek in konec posameznega
# oglasa. Funkcija naj vrne seznam nizov.


def page_to_ads(page_content):
    """Funkcija poišče posamezne oglase, ki se nahajajo v spletni strani in
    vrne seznam oglasov."""
    return re.findall(r'<article class="job-item" data-jobid=(.*?)>(.*?)</article>', page_content, flags=re.DOTALL)


# Definirajte funkcijo, ki sprejme niz, ki predstavlja oglas, in izlušči
# podatke o imenu, lokaciji, datumu objave in ceni v oglasu.


def get_dict_from_ad_block(block):
    """Funkcija iz niza za posamezen oglasni blok izlušči podatke o imenu, ceni
    in opisu ter vrne slovar, ki vsebuje ustrezne podatke."""
    vzorec_delo = r'<h5 class="mb-0">(.*?)</h5>'
    delo = re.search(vzorec_delo, block)
    if delo == None:
        return None
    return{'delo': delo.group(1)}

# Definirajte funkcijo, ki sprejme ime in lokacijo datoteke, ki vsebuje
# besedilo spletne strani, in vrne seznam slovarjev, ki vsebujejo podatke o
# vseh oglasih strani.


def ads_from_file(filename, directory):
    """Funkcija prebere podatke v datoteki "directory"/"filename" in jih
    pretvori (razčleni) v pripadajoč seznam slovarjev za vsak oglas posebej."""
    page_content = read_file_to_string(directory, filename)
    blocks = page_to_ads(page_content)
    ads =[get_dict_from_ad_block(block) for block in blocks]
    return [ad for ad in ads if ad != None]

ads_from_file(frontpage_filename, dela_directory)
###############################################################################
# Obdelane podatke želimo sedaj shraniti.
###############################################################################


def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return


# Definirajte funkcijo, ki sprejme neprazen seznam slovarjev, ki predstavljajo
# podatke iz oglasa mačke, in zapiše vse podatke v csv datoteko. Imena za
# stolpce [fieldnames] pridobite iz slovarjev.


def write_cat_ads_to_csv(ads, directory, filename):
    """Funkcija vse podatke iz parametra "ads" zapiše v csv datoteko podano s
    parametroma "directory"/"filename". Funkcija predpostavi, da so ključi vseh
    slovarjev parametra ads enaki in je seznam ads neprazen."""
    # Stavek assert preveri da zahteva velja
    # Če drži se program normalno izvaja, drugače pa sproži napako
    # Prednost je v tem, da ga lahko pod določenimi pogoji izklopimo v
    # produkcijskem okolju
    assert ads and (all(j.keys() == ads[0].keys() for j in ads))
    fieldnames = list(ads[0].keys())
    write_csv(fieldnames, ads, directory, filename)

# Celoten program poženemo v glavni funkciji

def main(redownload=True, reparse=True):
    """Funkcija izvede celoten del pridobivanja podatkov:
    1. Oglase prenese iz bolhe
    2. Lokalno html datoteko pretvori v lepšo predstavitev podatkov
    3. Podatke shrani v csv datoteko
    """
    # Najprej v lokalno datoteko shranimo glavno stran
    path = os.path.join(dela_directory, frontpage_filename)
    if redownload or not os.path.exists(path):
        save_frontpage(url, dela_directory, frontpage_filename)
    else:
        print('Datoteka html že obstaja.')
    # Iz lokalne (html) datoteke preberemo podatke

    # Podatke preberemo v lepšo obliko (seznam slovarjev)

    # Podatke shranimo v csv datoteko
    path_csv = os.path.join(dela_directory, csv_filename)
    if reparse or not os.path.exists(path_csv):
        ads = ads_from_file(frontpage_filename, dela_directory)
        write_cat_ads_to_csv(ads, dela_directory, csv_filename)
    else:
        print('Datoteka csv že obstaja.')
    # Dodatno: S pomočjo parametrov funkcije main omogoči nadzor, ali se
    # celotna spletna stran ob vsakem zagon prenese (četudi že obstaja)
    # in enako za pretvorbo

if __name__ == '__main__':
    main(False, True)
