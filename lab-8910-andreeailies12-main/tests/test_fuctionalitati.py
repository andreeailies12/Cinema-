import jsonpickle

from Domain.cardClient import CardClient
from Domain.cardClientValidator import CardClientValidator
from Domain.film import Film
from Domain.filmValidator import FilmValidator
from Domain.rezervare import Rezervare
from Domain.rezervareValidator import RezervareValidator
from Repository.repositoryInMemory import RepositoryInMemory
from Service.cardClientService import CardClientService
from Service.filmService import FilmService
from Service.rezervareService import RezervareService
from Service.undoRedoService import UndoRedoService


def clearFile(filename):
    with open(filename, "w") as f:
        pass


def test_rezervare_service():
    open("test-rezervare.json", "w").close()
    with open("test-rezervare.json", "w") as f:
        f.write(jsonpickle.dumps({}))

    filmRepository = RepositoryInMemory()
    cardClientRepository = RepositoryInMemory()
    rezervareRepository = RepositoryInMemory()
    filmValidator = FilmValidator()
    cardClientValidator = CardClientValidator()
    rezervareValidator = RezervareValidator()
    undoRedoService = UndoRedoService()
    filmService = FilmService(filmRepository, filmValidator, undoRedoService)
    rezervareService = RezervareService(rezervareRepository, filmRepository,
                                        cardClientRepository,
                                        rezervareValidator, undoRedoService)
    cardClientService = CardClientService(cardClientRepository,
                                          cardClientValidator,
                                          undoRedoService)

    film1 = Film("1", "Tu", 1999, 25, "nu")
    film2 = Film("2", "Eu", 2000, 25, "da")
    film3 = Film("3", "Tu1", 1999, 30, "da")
    film4 = Film("4", "Tu2", 2005, 25, "da")
    card1 = CardClient("1", "Tatar", "Cosmin", "1234567891234",
                       "12.02.2002", "15.06.2009", 25)
    card2 = CardClient("2", "Tatar", "Cosmin", "1234567891234",
                       "12.02.1999", "15.06.2009", 25)
    rezervare1 = Rezervare("1", "2", "1", "12.03.2015", "18:45")
    rezervare2 = Rezervare("2", "2", "1", "12.03.2016", "15:25")
    rezervare3 = Rezervare("3", "3", "1", "12.03.2015", "20:45")

    filmRepository.adauga(film1)
    filmRepository.adauga(film2)
    filmRepository.adauga(film3)
    filmRepository.adauga(film4)
    cardClientRepository.adauga(card1)
    cardClientRepository.adauga(card2)
    rezervareRepository.adauga(rezervare1)
    rezervareRepository.adauga(rezervare2)
    rezervareRepository.adauga(rezervare3)

    rezultat = []
    rezultat = rezervareService.afisare_rezervari_ore("12:20", "15:30")
    assert len(rezultat) == 1
    rezultat = rezervareService.afisare_rezervari_ore("12:20", "20:30")
    assert len(rezultat) == 2

    cardClientService.card_puncte()
    lista = cardClientRepository.read()
    assert len(lista) == 2
    assert lista[0].id_entitate == "1"
    assert lista[1].id_entitate == "2"

    rezervareService.filme_desc_nr_rezervari()
    lista1 = filmRepository.read()
    assert len(lista1) == 4

    lista2 = cardClientRepository.read(
        cardClientService.incrementarea_cardurilor(
            "12.02.1989", "12.02.2001", 1000))
    #  lista2 = cardClientRepository.read()
    assert len(lista2) == 2
