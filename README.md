# Projekta uzdevums

Projekta uzdevums ir izstrādāt Python programmu, kas automatizē datu iegūšanu no SS.lv sludinājumu portāla pēc lietotāja pieprasījuma, nodrošinot kategoriju izvēli. Pēc izvēles izdarīšanas programmai jāveic tīmekļa lapu parsēšana, datu filtrēšana un strukturēta saglabāšana .xslx tipa failā. Lietotajam ir jābūt izvēlei saglabāt datus augošā, dilstošā vai nesakārtotā secībā. Rezultātā lietotājam jābūt iespējai ērti analizēt tirgus tendences, salīdzināt cenas un sekot izmaiņām dažādās produktu kategorijās. Turklāt programmai jānovērš dublētu datu pievienošana, ja tiek izvēlēta viena un tā pati kategorija un jāapstrādā neparadzēta lietotāja ievade.

# Galvenās funkcijas
## Kategoriju izvēle

Programma piedāvā vairākas iepriekš definētas kategorijas, piemēram, Auto (Alfa Romeo), Darbs (Administrators) un Suņi (Viss). 
Lietotājam ir arī iespēja ievadīt pielāgotu kategorijas saiti, kas nodrošina elastību dažādu produktu grupu izpētē.

``` python
kategorijas = [
        Category("Auto (Alfa Romeo)", "https://www.ss.lv/lv/transport/cars/alfa-romeo/"),
        Category("Darbs (Administrators)", "https://www.ss.lv/lv/work/internet-services/administration/"),
        Category("Suņi (viss)", "https://www.ss.lv/lv/animals/dogs/"),
        Category("Cita (rokām ievadīt)", None)
    ]
```

## Datu iegūšana
Datu iegūšana tiek veikta, parsējot HTML no SS.lv lapām, izmantojot requests un BeautifulSoup bibliotēkas. Tiek meklēti sludinājumu URL, virsraksti, cenas un citas būtiskas detaļas.
``` python
atb = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
html = BeautifulSoup(atb.text, 'html.parser')
for t in html.find_all('table'):
    if t.find_all('tr', id=lambda x: x and x.startswith('tr_')):
        tab = t
        break
for tr in tab.find_all('tr', id=lambda x: x and x.startswith('tr_')):
    tds = tr.find_all('td')
    slud_url = "https://www.ss.lv" + tds[0].find('a')['href']
    dat = [td.get_text(" ", strip=True) for td in tds[1:]]
    print(slud_url, dat)
```

Failu apstrāde un dublētu datu novēršana
Programma pārbauda, vai izvēlētais Excel fails jau eksistē, un salīdzina tajā esošos sludinājumus ar jaunajiem datiem, lai novērstu dublēšanos. Tiek izmantotas sarakstu un vārdnīcu struktūras, lai nodrošinātu unikālu datu glabāšanu.
``` python
if os.path.exists(filename):
    wb = openpyxl.load_workbook(filename)
    ws = wb.active
    head = ws['A1'].value or ""
    iepr_url = ""
    if head.startswith("SAITE:"):
        iepr_url = head[6:]
    if iepr_url.strip() != url.strip():
        print("Faila citas kategorijas saite!")
        return
    for rinda in ws.iter_rows(min_row=2, values_only=True):
        if rinda and rinda[0]:
            vecie_url.append(rinda[0])
    wb.close()
```

## Datu eksports uz excel
Programma saglabā iegūtos datus Excel failā, izmantojot OpenPyXL bibliotēku. Katrs sludinājums tiek pievienots kā jauna rinda, ietverot virsrakstu, cenu, URL un statusu.
``` python
wb = openpyxl.Workbook()
ws = wb.active
ws["A1"] = "SAITE:" + url
ws.append(["url"] + header + ["Status"])
for s in visi_slud:
    ws.append([s.url] + s.dati + [s.statuss])
wb.save(filename)
```

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
* Vārdnīcas (dict), jo ```requests.get``` izmanto vārdnīcas: ```atb = requests.get(lapas_url, headers={'User-Agent':'Mozilla/5.0'})``` python
* Korteži (tuples)

