import requests
from bs4 import BeautifulSoup
import openpyxl
import os
import time

class Category:
    def __init__(self, name, url):
        self.name = name
        self.url = url

class Sludinajums:
    def __init__(self, url, dati, statuss):
        self.url = url
        self.dati = dati  #saraksts ar visiem laukiem
        self.statuss = statuss

def dabut_cenu(slud_objekts, idx):
    try:
        cena = slud_objekts.dati[idx]
        skaitli = ''.join(c for c in cena if c.isdigit())
        return int(skaitli) if skaitli else 0
    except:
        return 0

def main():
    kategorijas = [
        Category("Auto (Alfa Romeo)", "https://www.ss.lv/lv/transport/cars/alfa-romeo/"),
        Category("Darbs (Administrators)", "https://www.ss.lv/lv/work/internet-services/administration/"),
        Category("Suņi (viss)", "https://www.ss.lv/lv/animals/dogs/"),
        Category("Cita (rokām ievadīt)", None)
    ]

    for i, x in enumerate(kategorijas):
        print(i+1, "-", x.name)
    izvele = int(input("Kategorijas Nr.: ")) - 1
    if kategorijas[izvele].url is not None:
        url = kategorijas[izvele].url
    else:
        url = input("Ievadi saiti: ").strip()
    filename = input("Faila nosaukums: ").strip()
    if not filename.endswith(".xlsx"):
        filename += ".xlsx"

    vecie_url = []
    vecie_slud = []

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
                vecie_slud.append(Sludinajums(rinda[0], list(rinda[1:-1]), rinda[-1]))
        wb.close()

    lapas = int(input("Cik lapas pārbaudīt? "))
    header = []
    visi_slud = []

    for lapa in range(1, lapas+1):
        if lapa == 1:
            lapas_url = url
        else:
            lapas_url = url.rstrip("/") + "/page" + str(lapa) + ".html"
        atb = requests.get(lapas_url, headers={'User-Agent':'Mozilla/5.0'})
        html = BeautifulSoup(atb.text, 'html.parser')
        tab = None
        for t in html.find_all('table'):
            if t.find_all('tr', id=lambda x: x and x.startswith('tr_')):
                tab = t
                break
        if not tab: break
        if not header:
            galv = tab.find('tr', id='head_line')
            if galv:
                for td in galv.find_all(['td','th']):
                    txt = td.get_text(" ",strip=True)
                    if txt and "Sludinājumi" not in txt:
                        header.append(txt)
        for tr in tab.find_all('tr', id=lambda x: x and x.startswith('tr_')):
            tds = tr.find_all('td')
            slud_url = ""
            for td in tds:
                a = td.find('a')
                if a and '/msg/' in str(a.get('href')):
                    slud_url = "https://www.ss.lv" + a['href']
            if not slud_url:
                continue
            offset = len(tds) - len(header)
            dat = []
            for j in range(len(header)):
                idx = j+offset
                dat.append(tds[idx].get_text(" ",strip=True) if (0<=idx<len(tds)) else "")
            statuss = "Jauns" if slud_url not in vecie_url else "None"
            visi_slud.append(Sludinajums(slud_url, dat, statuss))
        time.sleep(1)

    #vecie kas vairs nav
    atrastie_url = [x.url for x in visi_slud]
    for x in vecie_slud:
        if x.url not in atrastie_url:
            x.statuss = "Izņemts"
            visi_slud.append(x)

    #cenas kartosana
    price_idx = None
    for idx, nos in enumerate(header):
        if "cena" in nos.lower() or "цена" in nos.lower():
            price_idx = idx
            break
    if price_idx is not None:
        kart = input("Kārtot pēc cenas? (1-augoši, 2-dilstoši, Enter-ne): ").strip()
        if kart in ["1","2"]:
            visi_slud.sort(key=lambda x: dabut_cenu(x, price_idx), reverse=(kart=="2"))

    #saglabasana
    wb = openpyxl.Workbook()
    ws = wb.active
    ws["A1"] = "SAITE:" + url
    ws.append(["url"]+header+["Status"])
    for s in visi_slud:
        ws.append([s.url] + s.dati + [s.statuss])
    wb.save(filename)
    print("Gatavs, dati ierakstīti:", filename)

if __name__ == '__main__':
    main()
