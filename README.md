# Projekta uzdevums

Projekta uzdevums ir izstrādāt Python programmu, kas automatizē datu iegūšanu no SS.lv sludinājumu portāla pēc lietotāja pieprasījuma, nodrošinot kategoriju izvēli. Pēc izvēles izdarīšanas programmai jāveic tīmekļa lapu parsēšana, datu filtrēšana un strukturēta saglabāšana .xslx tipa failā. Lietotajam ir jābūt izvēlei saglabāt datus augošā, dilstošā vai nesakārtotā secībā. Rezultātā lietotājam jābūt iespējai ērti analizēt tirgus tendences, salīdzināt cenas un sekot izmaiņām dažādās produktu kategorijās. Turklāt programmai jānovērš dublētu datu pievienošana, ja tiek izvēlēta viena un tā pati kategorija un jāapstrādā neparadzēta lietotāja ievade.

# Galvenās funkcijas
## Kategoriju izvēle

Programma piedāvā vairākas iepriekš definētas kategorijas, piemēram, Auto (Alfa Romeo), Mēbeles (Mājas priekšmeti) un Suņi (Viss).
Lietotājiem ir iespēja norādīt pielāgotu kategorijas saiti, kas ļauj izmantot skriptu arī citām produktu grupām.
Kategorijas tiek glabātas vārdnīcā, nodrošinot vieglu piekļuvi un paplašināšanu:
``` python
kategorijas = [
        Category("Auto (Alfa Romeo)", "https://www.ss.lv/lv/transport/cars/alfa-romeo/"),
        Category("Darbs (Administrators)", "https://www.ss.lv/lv/work/internet-services/administration/"),
        Category("Suņi (viss)", "https://www.ss.lv/lv/animals/dogs/"),
        Category("Cita (rokām ievadīt)", None)
    ]
```

## Datu iegūšana
Skripts izmanto requests bibliotēku, lai lejupielādētu tīmekļa lapu saturu, un BeautifulSoup, lai analizētu HTML kodu.
Tas meklē sludinājumu URL, virsrakstus, cenas, un citas būtiskas detaļas, kas tiek saglabātas strukturētā formā Excel failā.
Piemērs datu iegūšanai no HTML:
``` python
def extract_ads(soup):
    ads = []
    for ad in soup.find_all("a", class_="am"):
        title = ad.text.strip()
        url = ad.get("href")
        ads.append((title, url))
    return ads
```

## Failu apstrāde un dublētu datu novēršana

Ja izvēlētais Excel fails jau eksistē, skripts pārbauda, vai jaunie URL jau nav saglabāti, lai novērstu dublēšanos.
Tas tiek panākts, izmantojot set datu struktūru, kas nodrošina tikai unikālu vērtību glabāšanu.
Piemērs esošo URL pārbaudei:
``` python
if os.path.exists(filename):
    existing_urls = set(pd.read_excel(filename)["URL"].tolist())
else:
    existing_urls = set()
```

## Datu eksports uz excel
Dati tiek saglabāti Excel failā, izmantojot OpenPyXL.
Katrs sludinājums tiek pievienots kā jauna rinda ar atsevišķiem laukiem virsrakstam, cenai un URL.
Piemērs datu saglabāšanai:
``` python
def save_to_excel(data, filename):
    wb = Workbook()
    ws = wb.active
    ws.append(["Virsraksts", "Cena", "URL"])
    for title, price, url in data:
        ws.append([title, price, url])
    wb.save(filename)
```
## Kategoriju izvēle
Lietotājs var ievadīt jebkuru SS.lv kategorijas saiti, ja tā nav iekļauta iepriekš definētajā kategoriju sarakstā.
Tas nodrošina lielāku elastību un iespēju izmantot skriptu dažādiem tirgus segmentiem.

# Izmantotās bibliotēkas

```requests``` - tīmekļa lapu lejupielādei un HTTP pieprasījumu veikšanai. Šī bibliotēka nodrošina stabilu un ātru datu iegūšanu no tiešsaistes avotiem.
```beautifulsoup4``` - HTML dokumentu parsēšanai un elementu meklēšanai. Tā ļauj viegli izvilkt nepieciešamo informāciju no sarežģītiem HTML dokumentiem.
```openpyxl``` - Excel failu veidošanai un manipulēšanai. Šī bibliotēka ļauj strukturēt un saglabāt datus tabulu formātā, padarot tos viegli pieejamus tālākai analīzei.

Šīs bibliotēkas izvēlētas to stabilitātes, plašās dokumentācijas un vienkāršās lietošanas dēļ, kas ļauj ātri un efektīvi apstrādāt lielus datu apjomus.

# Instalācija
1. Klonē repozitoriju
``` bash
git clone https://github.com/lietotajs/ss-scraper.git
cd ss-scraper
```

3. Instalē nepieciešamās bibliotēkas no requirements.txt
``` bash
pip install -r requirements.txt
```
4. Palaid Programmu
``` bash
python sslvChecker.py
```

## Piezīmes
Priekšnosacījums: Python 3.7+ jābūt uzstādītam sistēmā.
Nav nepieciešama virtuālā vide, taču to var izmantot (ieteicams lielākiem projektiem).
Programma pati detektē dublētus sludinājumus un novērš to pievienošanu jau eksistējošam Excel failam.

# Lietošana

Palaidiet skriptu “python sslvChecker.py”.
Izvēlieties kategoriju vai norādiet pielāgotu saiti.
Norādiet Excel faila nosaukumu, kurā saglabāt datus (piem., dati.xlsx).
Sekojiet norādēm, lai izvairītos no datu dublēšanas, ja fails jau eksistē.

## Piemērs:
Ja izvēlēta Auto (Alfa Romeo) kategorija un fails nosaukts par “alfa_dati.xlsx”, programma iegūs visu noteikto sludinājumu datus un saglabās tos norādītajā .xslx failā.

# Izmantotās datu struktūras
* Saraksti (list)
* Simbolu virknes (string)
* Vārdnīcas (dict), jo ```requests.get``` izmanto vārdnīcas: ```atb = requests.get(lapas_url, headers={'User-Agent':'Mozilla/5.0'})```python
* Korteži (tuples)

