import jsonpickle

from Domain.entitate import Entitate
from Repository.repositoryInMemory import RepositoryInMemory


class RepositoryJson(RepositoryInMemory):
    def __init__(self, filename):
        # self.filme = {} - am acces fiindca ii public
        super().__init__()
        # apelez constructorul clasei de baza, imi creez dictionarul gol
        self.filename = filename
        # primul filename se refera la ce e in interiorul clasei

    def __read_file(self):  # operatie privata, doar aici se apeleaza
        try:
            with open(self.filename, "r") as f:  # modul e citire "r"
                return jsonpickle.loads(f.read())
                # imi deschide fisierul cu numele retinut in filename
                # si imi returneaza ce a citit acolo
        except Exception:
            return {}

    def __write_file(self):
        with open(self.filename, "w") as f:
            f.write(jsonpickle.dumps(self.entitati, indent=2))
            # dumps- imi ia ceva si converteste la json

    def read(self, id_entitate=None):  # get_all
        self.entitati = self.__read_file()
        return super().read(id_entitate)

    def adauga(self, entitate: Entitate):
        self.entitati = self.__read_file()
        super().adauga(entitate)  # apelez
        self.__write_file()  # scriu in fisier

    def sterge(self, id_entitate):
        self.entitati = self.__read_file()
        super().sterge(id_entitate)
        self.__write_file()

    def modifica(self, entitate: Entitate):
        self.entitati = self.__read_file()
        super().modifica(entitate)
        self.__write_file()
# super().sterge - te duce la sterge din filmRepository
# self.sterge() - te duce la de sterge de aici
