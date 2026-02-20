import sys

def ucitaj_piva():
    """
    Učitava ukupan broj piva i zatim podatke o svakom pivu pojedinačno.
    Očekuje ulaz oblika: Ime|ProcenatAlkohola|KoličinaMl|Cena
    Vraća rečnik u kom su ključevi imena piva, a vrednosti su njihove karakteristike.
    """
    try:
        # Čita prvi red iz sistemskog ulaza (ukupan broj piva)
        broj_piva_str = sys.stdin.readline().strip()
        
        # Ako je ulaz prazan (kraj fajla/unosa), prekini rad funkcije
        if not broj_piva_str:
            return None
        
        # Pretvaranje uočenog stringa broja u pravi celobrojni (integer) parametar
        broj_piva = int(broj_piva_str)
        
        # Prema uslovu zadatka, negativan broj izaziva trenutni prekid rada bez izlaza
        if broj_piva < 0:
            return None
            
        piva = {} # Rečnik (dictionary) u kojem ćemo čuvati podatke o svim pivima na stanju
        
        # Pokreće petlju onoliko puta koliko je definisano brojem piva na ulazu
        for _ in range(broj_piva):
            red = sys.stdin.readline().strip()
            
            # Razbijanje linije prema zadanom separatoru teksta '|'
            delovi = red.split('|')
            
            # Očekujemo tačno 4 podatka, ukoliko je format drugačiji - prekidamo program
            if len(delovi) != 4:
                return None
            
            # Izdvajanje vrednosti u promenljive (sa pretvaranjem tipova)
            ime = delovi[0]
            alkohol = float(delovi[1])     # float predstavlja decimalni broj
            kolicina_ml = float(delovi[2])
            cena = float(delovi[3])
            
            # Skladištenje informacija u rečniku koristeći ime piva kao ključ
            piva[ime] = {
                'alkohol': alkohol,
                'kolicina_ml': kolicina_ml,
                'cena': cena
            }
            
        return piva
    except Exception:
        # Svaka greška u parsiranju (npr. greška pri konverziji stringa u broj) nasilno prekida funkciju
        return None

def ucitaj_popijena():
    """
    Učitava jedan red teksta iz koga odvaja piva koja je mušterija popila (odvojena zarezom i razmakom).
    Vraća očišćenu listu popijenih piva.
    """
    red = sys.stdin.readline().strip()
    
    # Ako nema unosa za popijena piva, vraća praznu listu
    if not red:
        return []
        
    # Tekst razdvaja separatorom ", "
    popijena = red.split(', ')
    
    # Lista u kojoj smestamo cista parsirana piva (bez praznih karaktera)
    popijena_ociscena = []
    for p in popijena:
        p = p.strip()
        # Edge-case provere: ukoliko na kraju reda ipak postoji zarez koji remeti formatiranje
        if p.endswith(','):
            p = p[:-1].strip() # Brise poslednji karakter
            
        if p: # Ako pivo zapravo nije prazan string i postoji, pamti se u novu listu
            popijena_ociscena.append(p)
            
    return popijena_ociscena

def izracunaj_i_ispisi(piva, popijena):
    """
    Računa ukupnu količinu tečnosti u Litrama (L) kao i procentualni rastvor alkohola u celom unosu mušterije.
    """
    ukupno_ml = 0.0
    ukupno_alkohola_ml = 0.0
    
    # Iteracija (šetnja) kroz sva pića koja je gost okusio
    for pivo in popijena:
        # Pivo se analizira jedino ukoliko je pronađeno na skladištu (u rečniku)
        if pivo in piva:
            # Dohvatanje tačnih specifikacija iz rečnika zalihe
            kolicina_ml = piva[pivo]['kolicina_ml']
            procenat_alkohola = piva[pivo]['alkohol']
            
            ukupno_ml += kolicina_ml # Sabiranje mililitara
            
            # Sabiranje isključivo mililitara CISTOG alkohola na osnovu procenta zapremine!
            ukupno_alkohola_ml += kolicina_ml * (procenat_alkohola / 100.0) 
            
    # Pretvaranje u litre deleći sa 1000
    ukupno_l = ukupno_ml / 1000.0
    
    procenat = 0.0
    if ukupno_ml > 0:
        # Povratno pravljenje procenta izvučenog čistog alkohola na ukupnu unesenu tečnost
        procenat = (ukupno_alkohola_ml / ukupno_ml) * 100.0
        
    # Ispis na ekran. {.2f} garantuje postavljanje na tačno dve normale decimale!
    print(f"Kolicina: {ukupno_l:.2f}L")
    print(f"Alkohola: {procenat:.2f}%")

def ispisi_neprobana_piva(piva, popijena):
    """
    Pritiska presek spiska. Štampa liniju po liniju sva ona piva iz inventara (rečnika)
    koja se nisu našla na spisku popijenih kod mušterije.
    """
    # Pravljenje strukture skupa ('set') za mnogo brže pretraživanje
    probana_set = set(popijena)
    
    # Zbog prirode rečnika redosled se garantuje čime se zadovoljava zahtev ispisivanja ovim redom
    for pivo in piva.keys():
        if pivo not in probana_set:
            print(pivo)

def main():
    """
    Spaja i pokreće ostale funkcionalnosti koda!
    """
    piva = ucitaj_piva()
    
    if piva is None:
        # Presretnuta greška. Zatvaranje operacija skripte bez štampanja (zahtev iz teksta)
        return
        
    # Priprema listu konzumacije gosta
    popijena = ucitaj_popijena()
    
    # Logika proračunavanja
    izracunaj_i_ispisi(piva, popijena)
    
    # Prikaz nepopijenih zaliha mušteriji
    ispisi_neprobana_piva(piva, popijena)

if __name__ == '__main__':
    main()
