from strukture import *

def ucitaj_podatke(graf,users_f,connections_f,blocked_f):
    ucitani={}

    with open(users_f,'r') as f:
        for linija in f:
            dio=linija.strip().split('|')
            if len(dio)>1:
                id,ime,bio=dio[0],dio[1],dio[2]

                user=User(id,ime,bio)
                cvor=graf.dodaj_cvor(user)
                ucitani[id]=cvor
    with open(blocked_f,'r') as f:
        for linija in f:
            bloker, blokirani=linija.strip().split('|')
            if bloker in ucitani and blokirani in ucitani:
                graf.blokira(ucitani[bloker],ucitani[blokirani])
    with open(connections_f,'r') as f:
        for linija in f:
            prati,praceni=linija.strip().split('|')
            if prati in ucitani and praceni in ucitani:
                graf.dodaj_granu(ucitani[prati],ucitani[praceni])