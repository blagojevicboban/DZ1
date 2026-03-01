import sys

def ucitaj_piva():
    try:
        broj_piva_str = sys.stdin.readline().strip()
        if not broj_piva_str:
            return None
        
        broj_piva = int(broj_piva_str)
        if broj_piva < 0:
            return None
            
        piva = {}
        for _ in range(broj_piva):
            red = sys.stdin.readline().strip()
            delovi = red.split('|')
            if len(delovi) != 4:
                return None
            
            ime = delovi[0]
            alkohol = float(delovi[1])
            kolicina_ml = float(delovi[2])
            cena = float(delovi[3])
            
            piva[ime] = {
                'alkohol': alkohol,
                'kolicina_ml': kolicina_ml,
                'cena': cena
            }
            
        return piva
    except Exception:
        return None

def ucitaj_popijena():
    red = sys.stdin.readline().strip()
    if not red:
        return []
        
    popijena = red.split(', ')
    # U slučaju da postoji zarez na kraju bez razmaka
    # ili neki sličan edge-case uočljiv iz teksta zadatka
    popijena_ociscena = []
    for p in popijena:
        p = p.strip()
        if p.endswith(','):
            p = p[:-1].strip()
        if p:
            popijena_ociscena.append(p)
            
    return popijena_ociscena

def izracunaj_i_ispisi(piva, popijena):
    ukupno_ml = 0.0
    ukupno_alkohola_ml = 0.0
    
    for pivo in popijena:
        if pivo in piva:
            kolicina_ml = piva[pivo]['kolicina_ml']
            procenat_alkohola = piva[pivo]['alkohol']
            
            ukupno_ml += kolicina_ml
            ukupno_alkohola_ml += kolicina_ml * (procenat_alkohola / 100.0)
            
    ukupno_l = ukupno_ml / 1000.0
    
    procenat = 0.0
    if ukupno_ml > 0:
        procenat = (ukupno_alkohola_ml / ukupno_ml) * 100.0
        
    print(f"Kolicina: {ukupno_l:.2f}L")
    print(f"Alkohola: {procenat:.2f}%")

def ispisi_neprobana_piva(piva, popijena):
    probana_set = set(popijena)
    for pivo in piva.keys():
        if pivo not in probana_set:
            print(pivo)

def main():
    piva = ucitaj_piva()
    if piva is None:
        return
        
    popijena = ucitaj_popijena()
    
    izracunaj_i_ispisi(piva, popijena)
    ispisi_neprobana_piva(piva, popijena)

if __name__ == '__main__':
    main()
