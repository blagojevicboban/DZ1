def ucitaj_podatke():
    try:
        ulaz = open(0, "r")
        prvi_red = ulaz.readline()
        if not prvi_red:
            return None
            
        prvi_red = prvi_red.strip('\r\n')
        if prvi_red == "":
            return None
            
        delovi_prvi = prvi_red.split(',')
        if len(delovi_prvi) != 2:
            return None
            
        min_vreme = int(delovi_prvi[0])
        min_baterija = int(delovi_prvi[1])
        
        if min_vreme < 0 or min_baterija < 0:
            return None
            
        rekordi = []
        while True:
            red = ulaz.readline()
            if not red:  # EOF
                break
            red = red.strip('\r\n')
            if red == "":
                break
                
            delovi = red.split(',')
            if len(delovi) != 3:
                return None
                
            naziv = delovi[0]
            vreme = int(delovi[1])
            baterija = int(delovi[2])
            
            if vreme < 0 or baterija < 0:
                return None
            
            rekordi.append((naziv, vreme, baterija))
            
        return min_vreme, min_baterija, rekordi
    except Exception:
        return None

def grupisi_rekorde(rekordi):
    grupe = {}
    for naziv, vreme, baterija in rekordi:
        if naziv not in grupe:
            grupe[naziv] = {'vreme': 0, 'baterija': 0}
        grupe[naziv]['vreme'] += vreme
        grupe[naziv]['baterija'] += baterija
    return grupe

def filtriraj_rekorde(grupe, min_vreme, min_baterija):
    filtrirane = {}
    for naziv, podaci in grupe.items():
        if podaci['vreme'] >= min_vreme and podaci['baterija'] >= min_baterija:
            filtrirane[naziv] = podaci
    return filtrirane

def ispisi_podatke(filtrirane_grupe):
    for naziv, podaci in filtrirane_grupe.items():
        ukupno_vreme = podaci['vreme']
        sati = ukupno_vreme // 60
        minuti = ukupno_vreme % 60
        vreme_str = f"{sati:02d}:{minuti:02d}"
        print(f"{naziv} ({vreme_str},{podaci['baterija']}%)")

def main():
    podaci = ucitaj_podatke()
    if podaci is None:
        return
    min_vreme, min_baterija, rekordi = podaci
    grupe = grupisi_rekorde(rekordi)
    filtrirane = filtriraj_rekorde(grupe, min_vreme, min_baterija)
    ispisi_podatke(filtrirane)

if __name__ == '__main__':
    main()
