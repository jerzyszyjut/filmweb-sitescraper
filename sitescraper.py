import requests
from datetime import datetime
from typing import TypedDict
from bs4 import BeautifulSoup
import faker
import random
from hashlib import sha256

fake = faker.Faker('pl_PL')

base_url = 'https://www.filmweb.pl'
url = base_url+'/films/search?orderBy=popularity&descending=true&page={}'
strony_filmow = 5
uzytkownicy_platformy = 30
age_options = [7, 12, 15, 18]

class Movie(TypedDict):
  tytul: str
  oryginalny_tytul: str
  premiera: str
  czas_trwania: str
  okladka: str
  zwiastun: str
  ocena: float
  ocena_krytykow: float
  rezyserowie: list[list[str]]
  scenarzysci: list[list[str]]
  kraje: list[str]
  aktorzy: list[list[str]]
  gatunki: list[str]

def get_movie_links() -> list[str]:
    links = []
    for page in range(1, strony_filmow + 1):
      response = requests.get(url.format(page))
      soup = BeautifulSoup(response.text, 'html.parser')
      for film in soup.find_all('div', class_='preview__card'):
        link = film.find('a', class_='preview__link')
        links.append(base_url + link['href'])
    return links

def get_movie_data(url: str) -> Movie:
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  czas_trwania = soup.find('div', class_='filmCoverSection__duration').text
  czas_trwania_2 = czas_trwania.replace(' godz.', ';').replace(' min.', '').split(';')
  czas_trwania_3 = int(czas_trwania_2[0] if len(czas_trwania_2[0].strip()) >= 1 else 0 )  * 3600 + int(czas_trwania_2[1] if len(czas_trwania_2[1].strip()) >= 1 else 0) * 60
  tytul = soup.find('h1', class_='filmCoverSection__title').text.replace('\'','')
  data_premiery = soup.find_all('span', attrs={'itemprop': 'datePublished'})[0]['content'] if soup.find_all('span', attrs={'itemprop': 'datePublished'})[0].get('content') is not None else soup.find_all('span', attrs={'itemprop': 'datePublished'})[1]['content']
  try:
    data_premiery = datetime.strptime(data_premiery, '%d.%m.%Y').strftime('%Y-%m-%d')
  except:
    data_premiery = fake.date_of_birth().strftime('%Y-%m-%d')
  
  kraje = list(map(lambda x: x.text, soup.select('a[href^="/ranking/film/country/"]')))
  
  aktorzy = []
  for aktor in soup.find('section', class_='FilmCastSection').find_all('div', class_="crs__item"):
    imie_nazwisko = aktor.find('a', class_='simplePoster__title').text.replace('\'','')
    url = aktor.find('a', class_='simplePoster__title')['href']
    aktorzy.append([imie_nazwisko, base_url + url])
  
  scenarzysci = []
  for scenarzysta in soup.find('div', class_='filmInfo__info',  attrs={"data-type": "screenwriting-info"}).find_all('a'):
    imie_nazwisko = scenarzysta.text
    url = scenarzysta['href']
    scenarzysci.append([imie_nazwisko, base_url + url])
    
  rezyserowie = []
  for rezyser in soup.find('div', class_='filmInfo__info', attrs={"data-type": "directing-info"}).find_all('a'):
    imie_nazwisko = rezyser.text
    url = rezyser['href']
    rezyserowie.append([imie_nazwisko, base_url + url])
    
  gatunki = list(map(lambda x: x.text, soup.select('a[href^="/ranking/film/genre/"]')))
  
  film: Movie = {
    'tytul': tytul,
    'oryginalny_tytul': soup.find('div', class_='filmCoverSection__originalTitle').text.replace('\'','') if soup.find('div', class_='filmCoverSection__originalTitle') is not None else tytul,
    'premiera': data_premiery,
    'czas_trwania': czas_trwania_3,
    'okladka': soup.find('img', id='filmPoster')['src'],
    'ocena': float((soup.find('div', class_='filmRating').find('span', class_='filmRating__rateValue').text).replace(',', '.')),
    'ocena_krytykow': float((soup.find('div', class_='filmRating--filmCritic').find('span', class_='filmRating__rateValue').text).replace(',', '.')),
    'rezyserowie': rezyserowie,
    'scenarzysci': scenarzysci,
    'zwiastun': f"'{base_url + soup.find('div', class_='videoItem').find('a', class_='thumbnail__link')['href'].strip()}'" if not (soup.find('div', class_='videoItem') is None or soup.find('div', class_='videoItem').find('a', class_='thumbnail__link') is None) else None,
    'kraje': kraje,
    'aktorzy': aktorzy,
    'gatunki': gatunki,
  }
  return film
  
movies = []
for link in get_movie_links():
  print(link)
  movies.append(get_movie_data(link))

users = []
for i in range(1, uzytkownicy_platformy):
  nick = fake.user_name()
  users.append({
    'email': fake.email(),
    'nick': nick if len(nick) <= 20 else nick[:20],
    'imie': fake.first_name(),
    'nazwisko': fake.last_name(),
    'avatar': fake.image_url(),
    'data_urodzenia': fake.date_of_birth().strftime('%Y-%m-%d'),
    'haslo': sha256(fake.password().encode('utf-8')).hexdigest()[:255],
    'zweryfikowano_email': random.randrange(0, 2),
  })
  
critics = []
for user in users[:len(users)//4]:
  critics.append({
    'email': user['email'],
    'start_date': fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
    'end_date': random.choice([fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'), None]),
  })
  
ratings = []
  
for movie in movies:
  used_users = []
  for i in range(random.randrange(1, 5)):
    random_user = random.choice(users)
    while random_user['email'] in used_users:
      random_user = random.choice(users)
    if len(list(filter(lambda x: x['uzytkownicy_platformy_email'] == random_user['email'] and x['filmy_tytul'] == movie['tytul'], ratings))) > 0:
      continue
    ratings.append({
      'filmy_tytul': movie['tytul'],
      'uzytkownicy_platformy_email': random_user['email'],
      'ocena': random.randrange(1, 11),
      'recenzja': f"'{fake.text()}'" if random.randrange(0, 2) == 1 else None,
    })

watched_movies = []
for user in users:
  used_movies = []
  for movie in random.choices(movies, k=random.randrange(1, len(movies)//2)):
    if movie['tytul'] in used_movies:
      continue
    used_movies.append(movie['tytul'])
    watched_movies.append({
      'uzytkownicy_platformy_email': user['email'],
      'filmy_tytul': movie['tytul'],
      'czas': random.randrange(1, movie['czas_trwania']),
    })
    
kraje = list(set([kraj for movie in movies for kraj in movie['kraje']]))
    
age_certificates = []
for kraj in kraje:
  for i in range(1, len(age_options)*2):
    age_certificates.append({
      'nazwa': fake.word(),
      'wiek': random.choice(age_options),
      'kraje_nazwa': kraj,
    })
    
owned_certificates = []
for movie in movies:
  used_certificates = []
  for i in range(random.randrange(1, len(age_certificates)//2)):
    random_certificate = random.choice(age_certificates)
    while random_certificate['nazwa'] in used_certificates:
      random_certificate = random.choice(age_certificates)
    used_certificates.append(random_certificate['nazwa'])
    owned_certificates.append({
      'filmy_tytul': movie['tytul'],
      'certyfikaty_wiek': random_certificate['wiek'],
      'certyfikaty_nazwa': random_certificate['nazwa'],
      'certyfikaty_kraje_nazwa': random_certificate['kraje_nazwa'],
    })

funkcje_w_filmie = []
pracownicy_filmowi = []
for movie in movies:
  for aktor in movie['aktorzy']:
    if(len(list(filter(lambda x: x['imie_nazwisko'] == aktor[0], pracownicy_filmowi))) > 0):
      continue
    print(aktor[1])
    response = requests.get(aktor[1])
    soup = BeautifulSoup(response.text, 'html.parser')
    data_urodzenia = soup.find('span', attrs={"itemprop": "birthDate"})['content'] if soup.find('span', attrs={"itemprop": "birthDate"}) is not None else None
    data_smierci = soup.find('span', attrs={"itemprop": "personDeathAge"})['data-death-date'] if soup.find('span', attrs={"itemprop": "personDeathAge"}) is not None else None
    imie = aktor[0].split(' ')[0]
    nazwisko = aktor[0].split(' ')[-1]
    try:
      data_urodzenia = datetime.strptime(data_urodzenia, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
      data_urodzenia = fake.date_of_birth().strftime('%Y-%m-%d')
    try:
      if data_smierci is not None:
        data_smierci = datetime.strptime(data_smierci, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
      data_smierci = None
    pracownicy_filmowi.append({
      'imie_nazwisko': aktor[0],
      'imie': imie,
      'nazwisko': nazwisko,
      'data_urodzenia': data_urodzenia,
      'data_smierci': data_smierci,
      'plec': random.choice(['M', 'K']),
    })
    funkcje_w_filmie.append({
      'filmy_tytul': movie['tytul'],
      'pracownicy_imie': imie,
      'pracownicy_nazwisko': nazwisko,
      'funkcja': 'aktor',
    })
  
  for rezyser in movie['rezyserowie']:
    if(len(list(filter(lambda x: x['imie_nazwisko'] == rezyser[0], pracownicy_filmowi))) > 0):
      continue
    print(rezyser[1])
    response = requests.get(rezyser[1])
    soup = BeautifulSoup(response.text, 'html.parser')
    data_urodzenia = soup.find('span', attrs={"itemprop": "birthDate"})['content'] if soup.find('span', attrs={"itemprop": "birthDate"}) is not None else None
    data_smierci = soup.find('span', attrs={"itemprop": "personDeathAge"})['data-death-date'] if soup.find('span', attrs={"itemprop": "personDeathAge"}) is not None else None
    imie = rezyser[0].split(' ')[0]
    nazwisko = rezyser[0].split(' ')[-1]
    try:
      data_urodzenia = datetime.strptime(data_urodzenia, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
      data_urodzenia = fake.date_of_birth().strftime('%Y-%m-%d')
    try:
      if data_smierci is not None:
        data_smierci = datetime.strptime(data_smierci, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
      data_smierci = None
    pracownicy_filmowi.append({
      'imie_nazwisko': rezyser[0],
      'imie': imie,
      'nazwisko': nazwisko,
      'data_urodzenia': data_urodzenia,
      'data_smierci': data_smierci,
      'plec': random.choice(['M', 'K']),
    })
    funkcje_w_filmie.append({
      'filmy_tytul': movie['tytul'],
      'pracownicy_imie': imie,
      'pracownicy_nazwisko': nazwisko,
      'funkcja': 'reżyser',
    })
    
  for scenarzysta in movie['scenarzysci']:
    if(len(list(filter(lambda x: x['imie_nazwisko'] == scenarzysta[0], pracownicy_filmowi))) > 0):
      continue
    print(scenarzysta[1])
    response = requests.get(scenarzysta[1])
    soup = BeautifulSoup(response.text, 'html.parser')
    data_urodzenia = soup.find('span', attrs={"itemprop": "birthDate"})['content'] if soup.find('span', attrs={"itemprop": "birthDate"}) is not None else None
    data_smierci = soup.find('span', attrs={"itemprop": "personDeathAge"})['data-death-date'] if soup.find('span', attrs={"itemprop": "personDeathAge"}) is not None else None
    imie = scenarzysta[0].split(' ')[0]
    nazwisko = scenarzysta[0].split(' ')[-1]
    try:
      data_urodzenia = datetime.strptime(data_urodzenia, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
      data_urodzenia = fake.date_of_birth().strftime('%Y-%m-%d')
    try:
      if data_smierci is not None:
        data_smierci = datetime.strptime(data_smierci, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
      data_smierci = None
    pracownicy_filmowi.append({
      'imie_nazwisko': scenarzysta[0],
      'imie': imie,
      'nazwisko': nazwisko,
      'data_urodzenia': data_urodzenia,
      'data_smierci': data_smierci,
      'plec': random.choice(['M', 'K']),
    })
    funkcje_w_filmie.append({
      'filmy_tytul': movie['tytul'],
      'pracownicy_imie': imie,
      'pracownicy_nazwisko': nazwisko,
      'funkcja': 'scenarzysta',
    })
    
narodowosci = []
for pracownik in pracownicy_filmowi:
  narodowosci.append({
    'pracownicy_imie': pracownik['imie'],
    'pracownicy_nazwisko': pracownik['nazwisko'],
    'kraje_nazwa': list(set(random.choices(kraje, k=random.randrange(0, 3)))),
  })
  
gatunki = list(set([gatunek for movie in movies for gatunek in movie['gatunki']]))

nalezy_do_gatunku = []
for movie in movies:
  for gatunek in movie['gatunki']:
    nalezy_do_gatunku.append({
      'filmy_tytul': movie['tytul'],
      'gatunki_nazwa': gatunek,
    })

uzytkownicy_z_kraju = []
kraj_zerowy = kraje[0]

with open("insert_scraper.sql", "w+", encoding="utf-8") as f:
  f.write("USE filmy;\n\n");
  template = """('{}', '{}', '{}', {}, '{}', {})"""
  f.write("INSERT INTO filmy (tytul, oryginalny_tytul, premiera, czas_trwania, okladka, zwiastun) VALUES\n")
  for movie in movies:
    f.write(template.format(movie['tytul'], movie['oryginalny_tytul'].replace('\'','\\\''), movie['premiera'], movie['czas_trwania'], movie['okladka'], movie['zwiastun'] or 'NULL'))
    f.write(",\n")
  f.seek(f.tell() - 3, 0)
  f.truncate()
  f.write(";")
  
  template = """('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"""
  f.write("\n\nINSERT INTO uzytkownicy_platformy (email, nick, imie, nazwisko, awatar, data_urodzenia, haslo, zweryfikowano_email) VALUES\n")
  for user in users:
    f.write(template.format(user['email'], user['nick'], user['imie'], user['nazwisko'], user['avatar'], user['data_urodzenia'], user['haslo'], user['zweryfikowano_email']))
    f.write(",\n")
  f.seek(f.tell() - 3, 0)
  f.truncate()
  f.write(";")
  
  template = """('{}')"""
  f.write("\n\nINSERT INTO kraje (nazwa) VALUES\n")
  for kraj in kraje:
    f.write(template.format(kraj))
    f.write(",\n")
  f.seek(f.tell() - 3, 0)
  f.truncate()
  f.write(";\n\n")
  

  template = """INSERT INTO wyprodukowano_film_w (filmy_id, kraje_nazwa) SELECT id, '{}' FROM filmy WHERE tytul = '{}'"""
  for movie in movies:
    for kraj in movie['kraje']:
      f.write(template.format(kraj, movie['tytul']))
      f.write(";\n")
      
  f.write("\n")
      
  template = """INSERT INTO oceny (filmy_id, uzytkownicy_platformy_email, ocena, recenzja) SELECT id, '{}', {}, {} FROM filmy WHERE tytul = '{}'"""
  for rating in ratings:
    f.write(template.format(rating['uzytkownicy_platformy_email'], rating['ocena'], (rating['recenzja'] or 'NULL').replace("\n", ""), rating['filmy_tytul']))
    f.write(";\n")

  f.write("\n")
  
  template = """INSERT INTO krytycy_filmowi (uzytkownicy_platformy_email, data_przyznania_statusu_krytyka, data_odebrania_statusu_krytyka) VALUES ('{}', '{}', {})"""
  for critic in critics:
    f.write(template.format(critic['email'], critic['start_date'], (f"'{critic['end_date']}'" if critic['end_date'] is not None else 'NULL')))
    f.write(";\n")
  
  f.write("\n")
  
  template = """INSERT INTO obejrzane_tytuly (uzytkownicy_platformy_email, filmy_id, czas) SELECT '{}', id, {} FROM filmy WHERE tytul = '{}'"""
  for watched_movie in watched_movies:
    f.write(template.format(watched_movie['uzytkownicy_platformy_email'], watched_movie['czas'], watched_movie['filmy_tytul']))
    f.write(";\n")
    
  f.write("\n")
  
  template = """INSERT INTO certyfikaty_wiekowe (nazwa, wiek, kraje_nazwa) VALUES ('{}', {}, '{}')"""
  for certificate in age_certificates:
    f.write(template.format(certificate['nazwa'], certificate['wiek'], certificate['kraje_nazwa']))
    f.write(";\n")
    
  f.write("\n")
  
  template = """INSERT INTO posiadane_certyfikaty_wiekowe (filmy_id, certyfikaty_wiekowe_id) VALUES ((SELECT id FROM filmy WHERE tytul = '{}'), (SELECT id FROM certyfikaty_wiekowe WHERE nazwa = '{}' AND kraje_nazwa = '{}' AND wiek = {}))"""
  for owned_certificate in owned_certificates:
    f.write(template.format(owned_certificate['filmy_tytul'], owned_certificate['certyfikaty_nazwa'], owned_certificate['certyfikaty_kraje_nazwa'], owned_certificate['certyfikaty_wiek']))
    f.write(";\n")
    
  f.write("\n")
  
  template = """INSERT INTO pracownicy_filmowi (imie, nazwisko, data_urodzenia, data_smierci, plec) VALUES ('{}', '{}', '{}', {}, '{}')"""
  for pracownik in pracownicy_filmowi:
    f.write(template.format(pracownik['imie'], pracownik['nazwisko'], pracownik['data_urodzenia'], (f"'{pracownik['data_smierci']}'" if pracownik['data_smierci'] is not None else 'NULL'), pracownik['plec']))
    f.write(";\n")
    
  f.write("\n")
  
  template = """INSERT INTO funkcje_w_filmie (filmy_id, pracownicy_filmowi_id, nazwa_funkcji) VALUES ((SELECT id FROM filmy WHERE tytul = '{}'), (SELECT id FROM pracownicy_filmowi WHERE imie = '{}' AND nazwisko = '{}'), '{}')"""
  for funkcja in funkcje_w_filmie:
    f.write(template.format(funkcja['filmy_tytul'], funkcja['pracownicy_imie'], funkcja['pracownicy_nazwisko'], funkcja['funkcja']))
    f.write(";\n")
    
  f.write("\n")
  
  template = """INSERT INTO narodowosc (pracownicy_filmowi_id, kraje_nazwa) VALUES ((SELECT id FROM pracownicy_filmowi WHERE imie = '{}' AND nazwisko = '{}'), '{}')"""
  for narodowosc in narodowosci:
    for kraj in narodowosc['kraje_nazwa']:
      f.write(template.format(narodowosc['pracownicy_imie'], narodowosc['pracownicy_nazwisko'], kraj))
      f.write(";\n")
  f.write("\n")
  
  template = """INSERT INTO gatunki (nazwa) VALUES ('{}')"""
  for gatunek in gatunki:
    f.write(template.format(gatunek))
    f.write(";\n")
    
  f.write("\n")
  
  template = """INSERT INTO nalezace_gatunki (filmy_id, gatunki_nazwa) VALUES ((SELECT id FROM filmy WHERE tytul = '{}'), '{}')"""
  for nalezy_do_gatunku in nalezy_do_gatunku:
    f.write(template.format(nalezy_do_gatunku['filmy_tytul'], nalezy_do_gatunku['gatunki_nazwa']))
    f.write(";\n")

  f.write("\n")
    
  template = """INSERT INTO zalozono_w (uzytkownicy_platformy_email, kraje_nazwa) VALUES ('{}', '{}')"""
  for user in users:
    kraj = random.choice(kraje)
    if len(uzytkownicy_z_kraju) == 0:
      kraj = kraj_zerowy
    if kraj == kraj_zerowy:
      uzytkownicy_z_kraju.append(user)
    f.write(template.format(user['email'], kraj))
    f.write(";\n")
    
  f.write("\n")
  

with open('update_scraper.sql', 'w+') as f:
  f.write("USE filmy;\n\n")
  f.write("SELECT * FROM kraje;\n")
  f.write(f"SELECT * FROM uzytkownicy_platformy INNER JOIN zalozono_w ON uzytkownicy_platformy.email = zalozono_w.uzytkownicy_platformy_email WHERE zalozono_w.kraje_nazwa = '{kraj_zerowy}';\n");
  f.write(f"DELETE FROM kraje WHERE nazwa = '{kraj_zerowy}';\n");
  f.write("SELECT * FROM kraje;\n")
  f.write(f"SELECT * FROM uzytkownicy_platformy INNER JOIN zalozono_w ON uzytkownicy_platformy.email = zalozono_w.uzytkownicy_platformy_email WHERE zalozono_w.kraje_nazwa = '{kraj_zerowy}';\n");
  f.write(f"SELECT * FROM uzytkownicy_platformy WHERE email = '{uzytkownicy_z_kraju[0]['email']}';\n");
  f.write("\n\n");
  f.write(f"SELECT * FROM filmy INNER JOIN obejrzane_tytuly ON filmy.id = obejrzane_tytuly.filmy_id WHERE obejrzane_tytuly.uzytkownicy_platformy_email = '{users[0]['email']}';\n");
  f.write(f"UPDATE uzytkownicy_platformy SET email = '{users[0]['email']}_updated' WHERE email = '{users[0]['email']}';\n");
  f.write(f"SELECT * FROM filmy INNER JOIN obejrzane_tytuly ON filmy.id = obejrzane_tytuly.filmy_id WHERE obejrzane_tytuly.uzytkownicy_platformy_email = '{users[0]['email']}_updated';\n");