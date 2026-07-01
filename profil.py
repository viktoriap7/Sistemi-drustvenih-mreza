from strukture import *
from algoritmi import *

def ucitaj_podatke(graf,trie,users_f,connections_f,blocked_f):
    ucitani={}

    with open(users_f,'r', encoding='utf-8') as f:
        for linija in f:
            dio=linija.strip().split('|')
            if len(dio)>1:
                id,ime,bio=dio[0],dio[1],dio[2]

                user=User(id,ime,bio)
                trie.dodaj(user)
                graf.dodaj_cvor(user)
                ucitani[id]=graf._user_to_cvor[user]
    with open(blocked_f,'r', encoding='utf-8') as f:
        for linija in f:
            bloker, blokirani=linija.strip().split('|')
            if bloker in ucitani and blokirani in ucitani:
                graf.blokira(ucitani[bloker],ucitani[blokirani])
    with open(connections_f,'r', encoding='utf-8') as f:
        for linija in f:
            prati,praceni=linija.strip().split('|')
            if prati in ucitani and praceni in ucitani:
                graf.dodaj_pracenje(ucitani[prati],ucitani[praceni])


def pretraga(graf,trie):
    while True:
        print('''
PRETRAGA:
1)po korisnickom imenu
2)po biografiji
x)odustani''')
        a=input().strip()
        if a=='1':
            unos=input('Unesite ime: ').strip()
            if unos.endswith('*'):
                prefiks=unos[:-1]
                rez=trie.autocomplete(prefiks,graf)
                if len(rez)==0: 
                    print("Da li ste mislili na: ")
                    if len(prefiks)>1:
                        print("d")
                        rez=trie.did_you_mean(prefiks,graf)
                    else:
                        print("a")
                        rez=trie.autocomplete('',graf)
                i=1
                for user in rez:
                    print(str(i)+')'+str(user))
                    i+=1

        elif a=='2':
            pass
        elif a=='x':
            break
        else:
            print("Geska u unosu")

    
    