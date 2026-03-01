import sys

def ucitaj_podatke():
    """
    Funkcija za učitavanje podataka sa standardnog ulaza prema specifikaciji zadatka.
    Vraća (min_vreme, min_baterija, rekordi) ili (None, None, None) u slučaju greške.
    """
    try:
        # Čita prvi red sa ulaza koji sadrži minimalno vreme i minimalnu bateriju
        prvi_red = sys.stdin.readline()
        # Ako nema unosa (EOF), prekida i vraća None
        if not prvi_red:
            return None
            
        # Uklanjamo prelaz u novi red ('\r' za Windows, '\n' za Linux/Mac)
        prvi_red = prvi_red.strip('\r\n')
        # Ako je red potpuno prazan, prekida učitavanje
        if prvi_red == "":
            return None
            
        # Razdvajamo pročitani red po zarezima (očekujemo dva broja)
        delovi_prvi = prvi_red.split(',')
        # Ako nismo dobili tačno 2 dela, unos je neispravan
        if len(delovi_prvi) != 2:
            return None
            
        # Pretvaramo pročitane niske (stringove) u cele brojeve (int)
        min_vreme = int(delovi_prvi[0])
        min_baterija = int(delovi_prvi[1])
        
        # Prema tekstu, vrednosti ne smeju biti negativne
        if min_vreme < 0 or min_baterija < 0:
            return None
            
        rekordi = []  # Lista u koju ćemo redom dodavati podatke iz svake linije
        
        # Beskonačna petlja za čitanje preostalih linija, koja se prekida na prazan red ili EOF
        while True:
            # Čita jedan po jedan red sa ulaza
            red = sys.stdin.readline()
            
            # EOF (Kraj fajla/unosa) prekida petlju
            if not red:  
                break
                
            # Uklanjamo prelazne karaktere na kraju linije
            red = red.strip('\r\n')
            # Po uslovu zadatka, prazan red označava kraj unosa
            if red == "":
                break
                
            # Razdvajamo podatke iz trenutnog reda
            delovi = red.split(',')
            # Očekujemo 3 dela: ime aplikacije, vreme (minuti) i procenat baterije
            if len(delovi) != 3:
                return None
                
            # Parsiramo dobijene delove u odgovarajuće tipove podataka
            naziv = delovi[0]
            vreme = int(delovi[1])
            baterija = int(delovi[2])
            
            # Ako su vreme ili baterija negativni formati, stani sa radom
            if vreme < 0 or baterija < 0:
                return None
            
            # Uspešno pročitan zapis dodajemo u listu u vidu tuple-a (n-torke)
            rekordi.append((naziv, vreme, baterija))
            
        return min_vreme, min_baterija, rekordi
    except Exception:
        # Ukoliko dođe do bilo kakve greške u parsiranju (npr. tekst umesto broja), prekida ispravno
        return None

def grupisi_rekorde(rekordi):
    """
    Kroz sve rekorde pravi sumu utrošenog vremena i baterije po pojedinačnoj aplikaciji.
    """
    grupe = {}  # Rečnik (dictionary) u kojem ključevi predstavljaju nazive aplikacija
    
    # Prolazimo kroz unete n-torke 
    for naziv, vreme, baterija in rekordi:
        
        # Ako aplikacija do sada nije uneta u rečnik, inicijalizujemo joj sumarnu vrednost na 0
        if naziv not in grupe:
            grupe[naziv] = {'vreme': 0, 'baterija': 0}
            
        # Akumuliramo (sabiramo) vreme i bateriju za trenutu aplikaciju
        grupe[naziv]['vreme'] += vreme
        grupe[naziv]['baterija'] += baterija
        
    return grupe

def filtriraj_rekorde(grupe, min_vreme, min_baterija):
    """
    Izbacuje iz rezultata aplikacije koje nisu sakupile minimalan zahtevani broj minuta ili procenata.
    """
    filtrirane = {}  # Pomoćni rečnik u koji beležimo aplikacije koje su prošle uslov
    
    for naziv, podaci in grupe.items():
        # Aplikacija je relevantna jedino ako ispunjava OBA praga (minimalno vreme i minimalna baterija)
        if podaci['vreme'] >= min_vreme and podaci['baterija'] >= min_baterija:
            filtrirane[naziv] = podaci
            
    return filtrirane

def ispisi_podatke(filtrirane_grupe):
    """
    Prolazi kroz filtrirani spisak aplikacija i ispisuje ih u formatu:
    naziv_aplikacije (HH:MM,ukupni_procenat%)
    """
    for naziv, podaci in filtrirane_grupe.items():
        ukupno_vreme = podaci['vreme']
        
        # Prebacujemo ukupno vreme u satima i minutima (celobrojno deljenje 60)
        sati = ukupno_vreme // 60
        # Ostatak u minutima računamo putem modula (%) od 60
        minuti = ukupno_vreme % 60
        
        # Formatiranje u string tako da sati i minuti popunjavaju vodeće nule ukoliko je cifra 0-9 (npr. 01:05)
        vreme_str = f"{sati:02d}:{minuti:02d}"
        
        # Završni štampani izlaz za trenutni red
        print(f"{naziv} ({vreme_str},{podaci['baterija']}%)")

def main():
    """
    Glavni program (potprogram) koji diriguje i integriše sve operacije kako je zahtevano.
    """
    # 1. Poziva funkciju za učitavanje
    podaci = ucitaj_podatke()
    
    # Sigurnosna provera na greške po uslovu "prekinuti izrvšavanje bez ispisa"
    if podaci is None:
        return
        
    # Razdvaja tuple na tri posebne promenljive da bi prosledio narednim funkcijama 
    min_vreme, min_baterija, rekordi = podaci
    
    # 2. Grupisanje i akumuliranje iz list-a
    grupe = grupisi_rekorde(rekordi)
    
    # 3. Filtriranje iz rečnika preko minimalnih vrednosti
    filtrirane = filtriraj_rekorde(grupe, min_vreme, min_baterija)
    
    # 4. Finalni formatirani ispis na STDOUT u terminal/Moodle
    ispisi_podatke(filtrirane)

# Ovaj uslov znači: Ako pokrećemo ovu skriptu direktno, izvrši 'main()'. 
# (Zato što u Python-u main f-je ne idu po automatizmu kao u Javi/C)
if __name__ == '__main__':
    main()
