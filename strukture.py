import re
class User:
    def __init__(self,id,ime,bio):
        self._id=id
        self._ime=ime
        self._bio=bio
        self._pagerank=0
        self._rijeci={}
    def __str__(self):
        return str(self._id)+" | "+str(self._ime)
class Cvor:
    
    def __init__(self,x):
        """ element je user """
        self._element=x;    
    def element(self):
        return self._element
    def __hash__(self):
        return hash(id(self))
    def __str__(self):
        return str(self._element)
class Grana:
    def __init__(self,u,v):
        self._pocetak=u
        self._kraj=v
    def cvorovi(self):
        return(self._pocetak,self._kraj)
    def obrnut_cvor(self,v):
        if not isinstance(v,Cvor):
            return None
        return self._kraj if v is self._pocetak else self._pocetak
    def __hash__(self):
        return hash((self._pocetak,self._kraj))
    def __str__(self):
        return str("("+str(self._pocetak)+" , "+str(self._kraj)+")")

class Graf:
    def __init__(self):
        self._izlazni={}
        #kljucevi su cvorovi a vriejdnoti setovi sa cvorovima
        #a:{b,c} a prati b i c
        self._ulazni={}
        self._blokirani={}
        self._pagerank={}
        self._user_to_cvor={}
        #kljucevi useri vrijednost cvor grafa za tog usera
        self._inverted_indeks={}
        #kljuc rijec vrijednosti set usera koji imaju tu rijec u bio
    def pocetni_pagerank(self):
        n=self.broj_cvorova()
        vrijednost=1.0/n
        for cvor in self._izlazni:
            self._pagerank[cvor]=vrijednost
        
    def izracunaj_pagerank(self,d=0.85,e=1e-6):
        teleport=(1-d)/self.broj_cvorova()
        while True:
            novi_pr={}
            razlika=0
            for cvor in self._izlazni:
                pr_cvor=teleport
                for ulazni_cvor in self._ulazni[cvor]:
                    broj_izlaza=len(self._izlazni[ulazni_cvor])
                    if broj_izlaza>0:
                        pr_cvor+=d*(self._pagerank[ulazni_cvor]/broj_izlaza)
                        #treba da je ulazni sto vredniji a da ima sto manje
                        #opcija za kretanje na druge cvorove
                novi_pr[cvor]=pr_cvor
                razlika+=abs(novi_pr[cvor]-self._pagerank[cvor])
            self._pagerank=novi_pr
            if razlika<e:
                break
    def dobij_pagerank_za_cvor(self,cvor):
        return self._pagerank[cvor]

    def provjeri_blok(self,u,v):
        blokirao_u=self._blokirani.get(u,set())
        blikorao_v=self._blokirani.get(v,set())
        return (v in blokirao_u) or (u in blikorao_v)
    def blokira(self,u,v):
        """ prvi blokira drugog """
        if u not in self._blokirani:
            self._blokirani[u] = set()
        self._blokirani[u].add(v)
    def pripada_cvor(self,v):
        if not isinstance(v,Cvor):
            return False
        if v not in self._izlazni:
            return False
        else:
            return True
    def broj_cvorova(self):
        return len(self._izlazni)
    def cvorovi_izlani(self):
        return self._izlazni.keys()
    """ def broj_grana(self):
        total=sum(len(self._izlazni[v]) for v in self._izlazni)
        return total
    def grane(self):
        rez=set()
        for lista in self._izlazni.values():
            rez.update(lista.values())
        return rez
    def dobij_granu(self,v,u):
        if(self.pripada_cvor(v) and self.pripada_cvor(u)):
            
            return self._izlazni[v].get(u)
        print("\t nisu cvorovi")
        return None """
    def stepen(self,v,izlazni=True):
        if self.pripada_cvor(v):
            adj=self._izlazni if izlazni else self._ulazni
            return len(adj[v])
        print("\t nije cvor")
        return None
    def iteriraj_grane(self,v,izlazni=True):
        if self.pripada_cvor(v):
            adj=self._izlazni if izlazni else self._ulazni
            for cvor in adj[v]:
                yield cvor
    def dodaj_cvor(self,x):
        v=Cvor(x)
        self._izlazni[v]=set()
        self._ulazni[v]=set()
        self._user_to_cvor[x]=v
        for rijec in x._rijeci.keys():
            if rijec not in self._inverted_indeks:
                self._inverted_indeks[rijec]=set()
            self._inverted_indeks[rijec].add(x) 
        #return v
    def dodaj_pracenje(self,u,v):
        """ prvi prati drugog """
        if v not in self._izlazni[u]:
            if self.provjeri_blok(u,v):
                print("\t blokiraju se")
            else:
                self._izlazni[u].add(v)
                self._ulazni[v].add(u)
        else:
            print("\t pracenje vec postoji")
