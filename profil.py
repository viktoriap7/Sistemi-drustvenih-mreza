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
                    if len(rez)==0:
                        print("a")
                        rez=trie.autocomplete('',graf)
                user=izbor_ponudjenih(rez)
                return user
            else:
                user=trie.vrati_usera(unos)
                if user is not None:
                    return user
                print("Da li ste mislili na: ")
                if len(unos)>1:
                    print("d")
                    rez=trie.did_you_mean(unos,graf)
                if len(rez)==0:
                    print("a")
                    rez=trie.autocomplete('',graf)
                user=izbor_ponudjenih(rez)
                return user
        elif a=='2':
            pass
        elif a=='x':
            break
        else:
            print("Geska u unosu")

def izbor_ponudjenih(rez):
    i=1
    for user in rez:
        print(str(i)+')'+str(user))
        i+=1
    izbor=input("\nUnesite redni broj zeljenog profila (x za odustajanje)").strip()
    if izbor.isdigit():
        indeks=int(izbor)-1
        if 0<=indeks<len(rez):
            return rez[indeks]
        else:
            print("Greska u unosu")    
    print("Odustjanje")
    return None
def profil_meni(graf,trie,user):
    
    while True:
        print("\n\n")
        print(user)
        print('''==========================
1)lalalal
x)exit''')
        a=input().strip()
        if a=='1':
            pass
        elif a=='x':
            break
        else:
            print("Greska u unosu")