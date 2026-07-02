import re
import math
import time
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
                user._rijeci=izdvoj_rijeci(bio)
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
            poc_vrijeme=time.time()
            rez = []
            if unos.endswith('*'):
                prefiks=unos[:-1]
                rez=trie.autocomplete(prefiks,graf)
                if len(rez)==0: 
                    print("Da li ste mislili na: ")
                    if len(prefiks)>0:
                        print("d")
                        rez=trie.did_you_mean(prefiks,graf)
                    if len(rez)==0:
                        print("a")
                        rez=trie.autocomplete('',graf)
                kraj_vrijeme=time.time()
                print(f'vrijeme: {kraj_vrijeme-poc_vrijeme:.4f}s')
                user=izbor_ponudjenih(rez)
                return user
            else:
                user=trie.vrati_usera(unos)
                if user is not None:
                    return user
                print("Da li ste mislili na: ")
                if len(unos)>0:
                    print("d")
                    rez=trie.did_you_mean(unos,graf)
                if len(rez)==0:
                    print("a")
                    rez=trie.autocomplete('',graf)
                kraj_vrijeme=time.time()
                print(f'vrijeme: {kraj_vrijeme-poc_vrijeme:.4f}s')
                user=izbor_ponudjenih(rez)
                return user
        elif a=='2':
            unos=input("Unesite tekst: ").strip()
            poc_vrijeme=time.time()
            useri=ponadji_kandidate_sa_bio(graf,unos)
            rijeci_unosa=izdvoj_rijeci(unos)
            rez=[]
            for user in useri:
                cvor=graf._user_to_cvor[user]
                pr=graf.dobij_pagerank_za_cvor(cvor)
                slicnost=cosine_slicnost(user._rijeci,rijeci_unosa)

                ocjena=0.7*slicnost+0.3*pr
                rez.append((user,ocjena))
            top10=heapq.nlargest(10,rez,key=lambda x:x[1])
            samo_useri = [element[0] for element in top10]
            kraj_vrijeme=time.time()
            print(f'vrijeme: {kraj_vrijeme-poc_vrijeme:.4f}s')
            user=izbor_ponudjenih(samo_useri)
            if user is None:
                return None
            return graf._user_to_cvor[user]
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
def ponadji_kandidate_sa_bio(graf,unos):
    rijeci=re.findall(r'\w+',unos.lower())
    kandidati=set()
    for rijec in rijeci:
        
        if rijec in graf._inverted_indeks:
            kandidati.update(graf._inverted_indeks[rijec])
    return list(kandidati)
def cosine_slicnost(skup1,skup2):
    zbir=0
    if len(skup1)>len(skup2):
        (skup1,skup2)=(skup2,skup1)
    for r,br in skup1.items():
        if r in skup2:
            zbir+=br*skup2[r]
    zskup1=0
    for br in skup1.values():
        zskup1+=br**2
    zskup2=0
    for br in skup2.values():
        zskup2+=br**2
    imenilac= math.sqrt(zskup1*zskup2)
    if imenilac==0:
        return 0.0
    return zbir/imenilac
def dobij_preporuke(graf,poc_cvor,alfa=0.7):
    ppr_ocjene=graf.izracunaj_ppr(poc_cvor)
    user=poc_cvor._element
    kandidati=[]
    for cvor in graf._izlazni:
        if cvor==poc_cvor:continue
        if cvor in graf._izlazni[poc_cvor]:continue
        if graf.provjeri_blok(poc_cvor,cvor):continue

        ppr=ppr_ocjene.get(cvor,0)
        slicnost=cosine_slicnost(user._rijeci,cvor._element._rijeci)
        ocjena=alfa*ppr+(1-alfa)*slicnost
        kandidati.append((cvor,ocjena))
    return heapq.nlargest(10,kandidati,key=lambda x:x[1])  
def profil_meni(graf,trie,user):
    
    while True:
        print("\n\n")
        print(user)
        print(".....................")
        print(user._element._bio)
        print('''==========================
1)obilazak grafa po pracenju
2)prikaz predlozenih
x)exit''')
        a=input().strip()
        if a=='1':
            unos=input("Unesite dubinu: ").strip()
            if unos.isdigit():
                dubina=(int)(unos)    
                #poc_cvor=graf._user_to_cvor[user]
                rez=graf.obilazak_grafa(user,dubina)
                for i in range(1,dubina+1):
                    print("Nivo "+str(i)+":")
                    for cvor,d in rez:
                        if d==i:
                            print(cvor)
            else:
                print("Greska u unosu")
        elif a=='2':
            try:
                unos=input("Unesite alfa [0-1]: ")
                alfa=float(unos) if unos else 0.7
            except:
                alfa=0.7
            predlozeni=dobij_preporuke(graf,user,alfa)
            samo_useri = [element[0] for element in predlozeni]
            izabran=izbor_ponudjenih(samo_useri)
            if izabran is not None:
                graf.dodaj_pracenje(user,izabran)
                print("\n Zapratili ste: ",end='')
                print(izabran)
        elif a=='x':
            break
        else:
            print("Greska u unosu")