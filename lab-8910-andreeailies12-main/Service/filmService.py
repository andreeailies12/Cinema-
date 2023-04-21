from random import randint, choice

from Domain.addOperation import AddOperation
from Domain.delOperation import DelOperation
from Domain.film import Film
from Domain.filmValidator import FilmValidator
from Domain.modifyOperation import ModifyOperation

from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService


class FilmService:
    def __init__(self, filmRepository: Repository,
                 filmValidator: FilmValidator,
                 undoRedoService: UndoRedoService):
        self.__filmRepository = filmRepository
        self.__filmValidator = filmValidator
        self.__undoRedoService = undoRedoService

    def get_all(self):
        return self.__filmRepository.read()

    def adauga(self, id_film: str, titlu: str,
               an_aparitie: int, pret_bilet: float, in_program: str):
        film = Film(id_film, titlu, an_aparitie, pret_bilet, in_program)
        self.__filmValidator.valideaza(film)
        self.__filmRepository.adauga(film)
        self.__undoRedoService.addUndoOperation(
            AddOperation(self.__filmRepository, film))

    def sterge(self, id_film: str):
        filmSters = self.__filmRepository.read(id_film)
        self.__filmRepository.sterge(id_film)

        self.__undoRedoService.addUndoOperation(
            DelOperation(self.__filmRepository, filmSters))

    def modifica(self, id_film: str, titlu: str,
                 an_aparitie: int, pret_bilet: float, in_program: str):
        filmVechi = self.__filmRepository.read(id_film)
        film = Film(id_film, titlu, an_aparitie, pret_bilet, in_program)
        self.__filmValidator.valideaza(film)
        self.__filmRepository.modifica(film)
        self.__undoRedoService.addUndoOperation(
            ModifyOperation(self.__filmRepository, filmVechi, film))

    def cautare_full_text_filme(self, a):
        filme = self.__filmRepository.read()
        rezultat = []
        for i in filme:
            an_aparitie = str(i.an_aparitie)
            pret_bilet = str(i.pret_bilet)
            if a in i.titlu or \
                    a in an_aparitie \
                    or a in pret_bilet\
                    or a in i.in_program:
                rezultat.append(i)
        if not rezultat:
            raise KeyError("Nu exista parametrul dat")
        return rezultat

    def filme_generate(self, n):
        """
        Se genereaza a filme
        :param n: cate filme is generate, int
        :return:
        """
        numar_filme_generate = 0
        while True:
            id_film = str(randint(1, 1000))
            titluri = ["Tu", "Cenusareasa", "Hachiko",
                       "The Notebook", "Bird Box", "LOL"]
            titlu = choice(titluri)
            an_aparitie = randint(1700, 2021)
            pret_bilet = randint(2, 60)
            in_program_exemplu = ["da", "nu"]
            in_program = choice(in_program_exemplu)
            film = Film(id_film,
                        titlu,
                        an_aparitie,
                        pret_bilet,
                        in_program)
            if self.__filmRepository.read(id_film) is None:
                numar_filme_generate = numar_filme_generate + 1
                self.__filmRepository.adauga(film)
                if numar_filme_generate == n:
                    break
