import heapq
from strukture import Graf,Cvor

class Trie_cvor:
    def __init__(self):
        self._user=None
        self._djeca={}
        #slovo je kljuc a vrijednot je novi cvor
class Trie:
    def __init__(self):
        self.root=Trie_cvor()
    def dodaj(self,user):
        """ dodaje ime korisnika u trie """
        tren=self.root
        for slovo in user._ime.lower():
            if slovo not in tren._djeca:
                tren._djeca[slovo]=Trie_cvor()
            tren=tren._djeca[slovo]
        tren._user=user
    def sakupljanje_od_cvora_tren(self,tren,lista,graf):
        if tren._user is not None:
            lista.append(graf._user_to_cvor[tren._user])
        for dijete in tren._djeca.values():
            self.sakupljanje_od_cvora_tren(dijete,lista,graf)
    def autocomplete(self,prefiks,graf):
        tren=self.root

        for slovo in prefiks.lower():
            if slovo not in tren._djeca: 
                return []  #ovo ce bit did you mean
            tren=tren._djeca[slovo]    

        lista=[]
        self.sakupljanje_od_cvora_tren(tren,lista,graf)

        top10=heapq.nlargest(10,lista,key=graf.dobij_pagerank_za_cvor)
        return top10
