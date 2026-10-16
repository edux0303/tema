import networkx as nx
from itertools import combinations

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._arrivo = None
        self._maxPassi = None
        self._pesoBest = None
    def buildGraph(self,minimo,massimo):
        self._grafo.clear()
        self._idMap = {}

        nodi = DAO.getNodi(minimo,massimo)
        self._idMap = {at.id: at for at in nodi}
        self._grafo.add_nodes_from(nodi)
        filmOk = set()
        for film in DAO.getFilm(minimo, massimo):
            filmOk.add(film.id)
        for p, f in DAO.getCoppia():
            if p in self._idMap and f in filmOk:
                self._idMap[p].film.add(f)

        # arco se hanno almeno un film in comune, peso = numero di film in comune
        for a, b in combinations(nodi, 2):
            comuni = a.film & b.film
            if len(comuni) > 0:
                self._grafo.add_edge(a, b, weight=len(comuni))

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes(), key=lambda x: x.name)

    def getGradoMax(self):
        best = None
        gradoMax = -1
        for n in self._grafo.nodes:
            grado = self._grafo.degree(n)
            if grado > gradoMax:
                gradoMax = grado
                best = n

        return best, gradoMax


    def getIncidenti(self):
        peso = -1
        attore = None
        for n in self._grafo.nodes:
            p = self._grafo.degree(n, weight="weight")
            if p>peso:
                peso = p
                attore = n
        return attore,peso

    def get5(self):
        archi =[]
        for u,v,dati in self._grafo.edges(data=True):
          nomi = sorted([u.name,v.name])
          archi.append((nomi[0], nomi[1], dati["weight"]))
        archi.sort(key=lambda x: (-x[2], x[0],x[1]))
        return archi[:5]

    def getGiovaneAnziano(self):
        conData = [a for a in self._grafo.nodes if a.date_of_birth is not None]
        if len(conData) == 0:
            return None, None
        giovane = max(conData, key=lambda a: a.date_of_birth)
        anziano = min(conData, key=lambda a: a.date_of_birth)
        return giovane, anziano



    def getGruppo(self,start,N):

        self._solBest = []
        self._pesoBest = -1

        self._ricorsione([start], len(start.film), N)

        return self._solBest, self._pesoBest


    def _ricorsione(self,parziale, pesoParziale, N):
        if len(parziale) == N:
            if pesoParziale > self._pesoBest:
                self._pesoBest = pesoParziale
                self._solBest = list(parziale)

            return

        candidati = set()
        for attore in self._grafo.nodes:
            for v in self._grafo.neighbors(attore):
                if self._ammissibile(v, parziale):
                    candidati.add(v)

        candidati =sorted(candidati,key=lambda x: -len(x.film))

        for c in candidati:
            parziale.append(c)
            self._ricorsione(parziale, pesoParziale+ len(c.film), N)
            parziale.pop()



    def _ammissibile(self,c,parziale):
        if c in parziale:
            return False
        conta = 0

        for p in parziale:
            if self._grafo.has_edge(c, p):
                conta += 1

        return conta == 1