import sys

def ucitaj_podatke():
    """
    Funkcija za učitavanje i parsiranje minuta postignutih golova sa standardnog ulaza.
    Očekuje format stringa u jednom redu: golovi_tim1-golovi_tim2, gde su minuti odvojeni zarezom.
    Vraća (tim1_lista, tim2_lista) ili (None, None) u slučaju neispravnog formata.
    """
    # Čita ceo prvi i jedini red sa ulaza
    red = sys.stdin.readline()
    
    # Provera da li postoji unos ili je detektovana EOF (kraj unosa)
    if not red:
        return None, None
        
    # Uklanjanje nevidljivih znakova (npr. space ili prelaz u novi red)
    red = red.strip()
    
    # Ako je red potpuno prazan, prekini obradu
    if not red:
        return None, None
        
    # Osnovni format provere: mora postojati znak '-' koji razdvaja timove
    if '-' not in red:
        return None, None
        
    # Razbijanje stringa na dve celine (levi tim i desni tim) koristeći '-'
    delovi = red.split('-')
    
    # Očekujemo tačno dva dela nakon podočke. Ukoliko ih ima manje/više, ulaz je neispravan.
    if len(delovi) != 2:
        return None, None
        
    # Tekstualni zapis golova prvog tima (pre crtice) i drugog tima (posle crtice)
    tim1_str = delovi[0]
    tim2_str = delovi[1]
    
    # Lista za čuvanje izdvojenih minuta
    tim1_lista = []
    
    # Provera da li uopšte prvi tim ima datih golova
    if tim1_str:
        # Delimo spisak zareza da dobijemo pojedinačne string-minute
        for min_str in tim1_str.split(','):
            try:
                # Pokušaj pretvaranja tekstualne vrednosti vremena u pravi ceo broj (integer)
                tim1_lista.append(int(min_str))
            except ValueError:
                # Ukoliko se nađe slovni karakter umesto broja prekini sve
                return None, None
                
    # Isto važi i za tim 2
    tim2_lista = []
    if tim2_str:
        for min_str in tim2_str.split(','):
            try:
                tim2_lista.append(int(min_str))
            except ValueError:
                return None, None
                
    return tim1_lista, tim2_lista

def proveri_opseg(tim1, tim2):
    """
    Proverava da li su svi minuti u dozvoljenom rasponu [1, 90].
    """
    # Proveri golove tima 1
    for gol in tim1:
        if gol < 1 or gol > 90:
            return False
            
    # Proveri golove tima 2
    for gol in tim2:
        if gol < 1 or gol > 90:
            return False
            
    # Ako su svi minuti u rasponu, vrati istinu 
    return True

def odredi_rezultat(tim1, tim2):
    """
    Kalkuliše poluvreme (minuti <= 45) i ukupni rezultat cele uktakmice.
    Ispisuje informaciju u formatu 'TIM1_FT:TIM2_FT (TIM1_HT:TIM2_HT)'
    """
    # Sumiranje jedinica (brojanje komada) za svaki gol koji je bio manji ili jednak 45. minutu
    tim1_ht = sum(1 for gol in tim1 if gol <= 45)
    tim2_ht = sum(1 for gol in tim2 if gol <= 45)
    
    # Puni rezultati (Full Time) - dobijaju se običnom proverom dužine liste golova
    tim1_ft = len(tim1)
    tim2_ft = len(tim2)
    
    # Ispis na sistemski izlaz primenom formatiranih stringova (f"")
    print(f"{tim1_ft}:{tim2_ft} ({tim1_ht}:{tim2_ht})")

def odredi_vremenski_opseg(tim1, tim2):
    """
    Pronalazi najraniji i najkasniji minut u kome se dogodio gol u meču.
    """
    # Konstrukcija nove unificirane liste koja spaja događaje oba tima na jedno mesto
    svi_golovi = tim1 + tim2
    
    # Proverava da li uopšte po stoji obeležen gol na meču (tj. lista nije prazna)
    if svi_golovi:
        # Pomoću sistemskih funkcija pronalazimo apsolutni minimum i maksimum kolekcije
        najraniji = min(svi_golovi)
        najkasniji = max(svi_golovi)
        print(f"{najraniji}-{najkasniji}")

def main():
    """
    Deo koda koji dekomponuje i pokreće strukture ovog zadatka po redosledu.
    """
    # 1. Deklaracija unosa i razvrtavanje u liste
    tim1, tim2 = ucitaj_podatke()
    
    # Ako parsiranje listi nije uspelo (bilo kakva greška formatiranja), izbaci None
    if tim1 is None and tim2 is None:
        return
        
    # 2. Provera logičke regularnosti vremenskog okvira fudbala
    if not proveri_opseg(tim1, tim2):
        return
        
    # Izbacivanje surovih Python listi u terminal formatu (kao što traži zahtev pdf-a pod br. 3)
    print(tim1)
    print(tim2)
    
    # Potprogram za analizu rezultata
    odredi_rezultat(tim1, tim2)
    
    # Potprogram za analizu graničnih vrednosti 
    odredi_vremenski_opseg(tim1, tim2)

# Globalni preduslov koji osigurava da samostalno pokretanje fajla komandom "python zadatak2k.py" automatski pobudi main() proces
if __name__ == '__main__':
    main()
