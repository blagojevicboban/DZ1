import sys

def ucitaj_podatke():
    red = sys.stdin.readline()
    if not red:
        return None, None
        
    red = red.strip()
    if not red:
        return None, None
        
    if '-' not in red:
        return None, None
        
    delovi = red.split('-')
    if len(delovi) != 2:
        return None, None
        
    tim1_str = delovi[0]
    tim2_str = delovi[1]
    
    tim1_lista = []
    if tim1_str:
        for min_str in tim1_str.split(','):
            try:
                tim1_lista.append(int(min_str))
            except ValueError:
                return None, None
                
    tim2_lista = []
    if tim2_str:
        for min_str in tim2_str.split(','):
            try:
                tim2_lista.append(int(min_str))
            except ValueError:
                return None, None
                
    return tim1_lista, tim2_lista

def proveri_opseg(tim1, tim2):
    for gol in tim1:
        if gol < 1 or gol > 90:
            return False
    for gol in tim2:
        if gol < 1 or gol > 90:
            return False
    return True

def odredi_rezultat(tim1, tim2):
    tim1_ht = sum(1 for gol in tim1 if gol <= 45)
    tim2_ht = sum(1 for gol in tim2 if gol <= 45)
    
    tim1_ft = len(tim1)
    tim2_ft = len(tim2)
    
    print(f"{tim1_ft}:{tim2_ft} ({tim1_ht}:{tim2_ht})")

def odredi_vremenski_opseg(tim1, tim2):
    svi_golovi = tim1 + tim2
    if svi_golovi:
        najraniji = min(svi_golovi)
        najkasniji = max(svi_golovi)
        print(f"{najraniji}-{najkasniji}")

def main():
    tim1, tim2 = ucitaj_podatke()
    if tim1 is None and tim2 is None:
        return
        
    if not proveri_opseg(tim1, tim2):
        return
        
    print(tim1)
    print(tim2)
    
    odredi_rezultat(tim1, tim2)
    odredi_vremenski_opseg(tim1, tim2)

if __name__ == '__main__':
    main()
