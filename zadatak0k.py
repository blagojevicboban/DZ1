import sys

def is_valid_time(time_str):
    """
    Funkcija koja pronalazi da li je dati string validnog 'HH:MM' formata.
    Ovaj deo koda garantuje da će se izbeći greška npr. '35:27' ili sličnih nepostojećih vremena.
    Odnosno da korisnik neće prekinuti program sa izuzetkom pre ulaska u logiku programa.
    """
    # Deli npr. "08:45" na ["08", "45"]
    parts = time_str.split(':')
    
    # Mora biti tačno dva dela okružena dvotačkom
    if len(parts) != 2:
        return False
        
    hh, mm = parts
    
    # Obavezno proverava da li to i jesu zaista brojevi pre nego sto ista pretvara
    if not hh.isdigit() or not mm.isdigit():
        return False
        
    # Pretvara delove u celobrojne vrednosti
    h, m = int(hh), int(mm)
    
    # Logika važečeg sata (0-23) i važećeg minuta (0-59)
    return 0 <= h <= 23 and 0 <= m <= 59

def time_to_mins(time_str):
    """
    Korisna funkcija za lakše upoređivanje: 
    Pretvara vreme iz standardnog tekstualnog 'HH:MM' stringa (npr. '08:45') 
    u ukupan broj minuta koji je protekao od ponoći (int). 
    """
    parts = time_str.split(':')
    # Sat se množi sa 60 a onda dodaju minuti
    return int(parts[0]) * 60 + int(parts[1])

def ucitaj_podatke():
    """
    Funkcija koja učitava sve potrebne podatke sa standardnog ulaza onako kako je definisano u zadatku.
    """
    try:
        # Čita prvi red sa liste koja sadrži odgovarajuće autobuske linije (npr. '16,65,77')
        linije_str = input()
        
        # Ako je korisnik udario samo enter bez teksta (prazan unos), prekida se izvršavanje
        if not linije_str:
            return None
            
        # Linije autobusa na ulazu odvaja zarez kako bi činio listu trazenih linija
        trazene_linije = linije_str.split(',')
        
        # Očekujemo zatim korisnikovo najranije vreme (željeno) u kom bi on krenuo
        vreme_polaska_str = input()
        
        # Proverava se da li je ono validno na osnovu naše napisane metode (is_valid_time)
        if not is_valid_time(vreme_polaska_str):
            return None
            
        polasci = [] # Inicijalizujemo praznu listu gde ćemo dodavati podatke reda vožnje
        
        # Čita se po redu vožnje sve do pojave praznog "Enter-a"
        while True:
            try:
                # Očitava se linija koja predstavlja jednu iz niza polazaka na stanici
                linija_unosa = input()
            except EOFError:
                # Ukoliko naiđe na stvarni kraj fajla komande prekida formiranje iteracije unosa
                break
                
            # Po uslovu prazan red prekida unos reda vožnje za izlazak
            if linija_unosa == "":
                break
                
            # Čita format 'linija,oznaka,vreme_polaska' na primer '16,A25,08:00'
            delovi = linija_unosa.split(',')
            
            # Bez 3 komponente ovakvog zapisa u jednom redu prekidamo bezbedno izvrsavanje onako kako se i test podudara
            if len(delovi) != 3:
                return None
            
            linija, oznaka, vreme_pol = delovi
            
            # Još jedna validacija polaznog formata iz linije reda
            if not is_valid_time(vreme_pol):
                return None
                
            # Svaki nađeni validan polazak čuvamo u listi kao rečnik (dictionary) zbog lakše organizacije parametara
            polasci.append({
                'linija': linija,
                'oznaka': oznaka,
                'vreme': vreme_pol,
                'vreme_min': time_to_mins(vreme_pol)  # Usput ga odma pripremamo u minutima
            })
            
        # Uspešan rad funkcije ucitaj_podatke() vraća 3 glavna segmenta (tupla/n-torke)
        return trazene_linije, vreme_polaska_str, polasci
        
    # Bezbedno napuštanje na bilo kakve neočekivane krahove programa (Exception)
    except EOFError:
        return None
    except Exception:
        return None

def filtriraj_polaske(trazene_linije, vreme_polaska_str, polasci):
    """
    Funkcija koja se bavi izbacivanjem irelevantnih autobusa,
    odnosno onih koji se ne nalaze na trasi, ili kreću prerano u odnosu na željeno vreme putnika.
    """
    # Pretvara željeno vreme putnika u minute radi lakšeg i tačnijeg matematičkog upoređivanja
    vreme_polaska_min = time_to_mins(vreme_polaska_str)
    
    # Privremena prazna lista za sve one autobuse koji su nam prošli zadate uslove
    filtrirani = []
    
    # Prolazi se kroz kompletan pročitani red vožnje za dan (petljom FOR)
    for polazak in polasci:
        # Poredi da li se npr. linija autobusa "16" stvarno nalazi u listi ["16", "65", "77"] korisnika
        # i dodatno poredi da li je njeno početno stanično vreme >= (posle) putnikovog najranijeg vremena.
        if polazak['linija'] in trazene_linije and polazak['vreme_min'] >= vreme_polaska_min:
            
            # Ukoliko ispunjava apsolutno sve zahteve dodaje se u filtriranu listu
            filtrirani.append(polazak)
            
    # Na izlasku funkcije ostajemo samo sa kvalitetnim opcijama putnika   
    return filtrirani

def odredi_najraniji_polazak(filtrirani_polasci):
    """
    Pronalazi prvi sledeći autobus koji kreće počevši od putnikovog vremena kako bi se smanjilo čekanje.
    Odnosno tražimo 'najraniji' (prema minutama) u predočenoj filtriranoj listi.
    """
    # Prekid potrage ako je preostalo tačno 0 polazaka nakon filtriranja
    if not filtrirani_polasci:
        return None
        
    # Polazna pretpostavka (inicijalni minimum) za poređenje je prvi element pod indeksom 0 u listi
    najraniji = filtrirani_polasci[0]
    
    # Idemo od drugog elementa u isfiltriranom redu pa sve do poslednjeg na spisku
    for polazak in filtrirani_polasci[1:]:
        
        # Ako neki naredni polazak prema redosledu ima "manji" (tj. pre će doći) broj minuta od našeg,
        # obori pretpostavku, i upiši da je novi iz petlje FOR ipak taj ultimativni "najraniji".
        if polazak['vreme_min'] < najraniji['vreme_min']:
            najraniji = polazak
            
    return najraniji

def ispisi_podatke(broj_preostalih, najraniji_polazak):
    """
    Funkcija koja se isključivo brine oko striktnog pravila formata štampe
    """
    # Na samom vrhu se uvek obavezno ispisuje tačan ukupan broj preostalih (izfiltriranih) mogućnosti
    print(broj_preostalih)
    
    # Odnosno ispisuje poruku ukoliko je naš 'najraniji_polazak' vratio 'None' (tj nije ga bilo ranije pronađenog)
    if najraniji_polazak is None:
        print("Nema autobusa.")
        
    # U suprotnom, spajanje informacija onako kako je traženo sa zadatka u primeru: linija-oznaka (vreme_polaska)
    else:
        print(f"{najraniji_polazak['linija']}-{najraniji_polazak['oznaka']} ({najraniji_polazak['vreme']})")

def main():
    """
    Glavni program (potprogram) koji drži kontrolu čitavog protoka aplikacije unutar zadatka tako
    da obavezno komunicira putanjama, i iskljucivo putem svojih argumenata i povratne vrednosti (ne globalnim).
    """
    # 1. Poziva funkciju za učitavanje sa STDIN
    podaci = ucitaj_podatke()
    
    # Sigurnosni prekid u slučaju neispravno formiranih ulaznih formata iz Moodle platforme (pad bez izbacivanja štampane greške)
    if podaci is None:
        return
        
    # Tuple izvučen i spakovan preko naziva tri potrebne promenljive za izvođenje obrade podataka
    trazene_linije, vreme_polaska_str, polasci = podaci
    
    # 2. Poziva funkciju koja filtrira listu polazaka na propisani opisani način gde dobijamo preostatak unutar promenljive "filtrirani"
    filtrirani = filtriraj_polaske(trazene_linije, vreme_polaska_str, polasci)
    
    # 3. Poziv na funkciju koja određuje minimalnog čekanja na stanici kroz već obrađenu listu pod nazivom promenljive "najraniji"
    najraniji = odredi_najraniji_polazak(filtrirani)
    
    # 4. Finalno pozivanje f-je koja prosto ispisuje podatke na standardni izlaz prema zahtevima
    ispisi_podatke(len(filtrirani), najraniji)

# Startovanje izvođenja glavne logike zadatka
if __name__ == "__main__":
    main()
