import time
from strukture import *
from algoritmi import *
from profil import *

def main():
    poc_vrijeme=time.time()
    small='small'
    medium='medium'
    full='full'
    izabrani='dataset/'+small+'/'
    trie=Trie()
    graf=Graf()
    ucitaj_podatke(graf,trie,izabrani+'users.txt',
                   izabrani+'connections.txt',izabrani+'blocked.txt')
    graf.pocetni_pagerank()
    graf.izracunaj_pagerank()
    kraj_vrijeme=time.time()
    print(f'vrijeme ucitavanja: {kraj_vrijeme-poc_vrijeme:.4f}s')
    while True:
        print("""
              

========================
Meni:
========================
1)pretraga
2)prikaz najuticajnijih
3)dodaj pracenje
4)prikaz istorije
x)exit


""")
        a=input().strip()
        if a=='1':
            pretraga(graf,trie)
        elif a=='2':
            poc_vrijeme=time.time()
            lista=list(graf._pagerank.keys())
            top10=heapq.nlargest(10,lista,key=graf.dobij_pagerank_za_cvor)
            for user in top10:
                print(user)
            kraj_vrijeme=time.time()
            print(f'vrijeme: {kraj_vrijeme-poc_vrijeme:.4f}s')
        elif a=='3':
            pass
        elif a=='4':
            pass
        elif a=='x':
            break
        else:
            print("greska u unosu")
main()