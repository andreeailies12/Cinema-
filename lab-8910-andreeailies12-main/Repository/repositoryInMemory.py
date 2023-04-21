from Domain.entitate import Entitate
from Repository.repository import Repository


class RepositoryInMemory(Repository):
    def __init__(self):  # constructor
        self.entitati = {}

    def read(self, id_entitate=None):  # get_by_id
        if id_entitate is None:
            return list(self.entitati.values())

        if id_entitate in self.entitati:
            return self.entitati[id_entitate]
        else:
            return None

    def adauga(self, entitate: Entitate):
        if self.read(entitate.id_entitate) is not None:
            raise KeyError("Exista deja un entitate cu id ul dat!")
        self.entitati[entitate.id_entitate] = entitate

    def sterge(self, id_entitate: str):
        if self.read(id_entitate) is None:
            raise KeyError("Nu exista un entitate cu id ul dat!")
        del self.entitati[id_entitate]

    def modifica(self, entitate: Entitate):
        if self.read(entitate.id_entitate) is None:
            raise KeyError("Nu exista un entitate cu id ul dat")
        self.entitati[entitate.id_entitate] = entitate
