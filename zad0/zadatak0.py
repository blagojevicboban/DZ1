def is_valid_time(time_str):
    parts = time_str.split(':')
    if len(parts) != 2:
        return False
    hh, mm = parts
    if not hh.isdigit() or not mm.isdigit():
        return False
    h, m = int(hh), int(mm)
    return 0 <= h <= 23 and 0 <= m <= 59

def time_to_mins(time_str):
    parts = time_str.split(':')
    return int(parts[0]) * 60 + int(parts[1])

def ucitaj_podatke():
    try:
        linije_str = input()
        if not linije_str:
            return None
        trazene_linije = linije_str.split(',')
        
        vreme_polaska_str = input()
        if not is_valid_time(vreme_polaska_str):
            return None
            
        polasci = []
        while True:
            try:
                linija_unosa = input()
            except EOFError:
                break
            if linija_unosa == "":
                break
                
            delovi = linija_unosa.split(',')
            if len(delovi) != 3:
                return None
            
            linija, oznaka, vreme_pol = delovi
            if not is_valid_time(vreme_pol):
                return None
                
            polasci.append({
                'linija': linija,
                'oznaka': oznaka,
                'vreme': vreme_pol,
                'vreme_min': time_to_mins(vreme_pol)
            })
            
        return trazene_linije, vreme_polaska_str, polasci
    except EOFError:
        return None
    except Exception:
        return None

def filtriraj_polaske(trazene_linije, vreme_polaska_str, polasci):
    vreme_polaska_min = time_to_mins(vreme_polaska_str)
    filtrirani = []
    
    for polazak in polasci:
        if polazak['linija'] in trazene_linije and polazak['vreme_min'] >= vreme_polaska_min:
            filtrirani.append(polazak)
            
    return filtrirani

def odredi_najraniji_polazak(filtrirani_polasci):
    if not filtrirani_polasci:
        return None
        
    najraniji = filtrirani_polasci[0]
    for polazak in filtrirani_polasci[1:]:
        if polazak['vreme_min'] < najraniji['vreme_min']:
            najraniji = polazak
            
    return najraniji

def ispisi_podatke(broj_preostalih, najraniji_polazak):
    print(broj_preostalih)
    if najraniji_polazak is None:
        print("Nema autobusa.")
    else:
        print(f"{najraniji_polazak['linija']}-{najraniji_polazak['oznaka']} ({najraniji_polazak['vreme']})")

def main():
    podaci = ucitaj_podatke()
    if podaci is None:
        return
        
    trazene_linije, vreme_polaska_str, polasci = podaci
    
    filtrirani = filtriraj_polaske(trazene_linije, vreme_polaska_str, polasci)
    
    najraniji = odredi_najraniji_polazak(filtrirani)
    
    ispisi_podatke(len(filtrirani), najraniji)

if __name__ == "__main__":
    main()
