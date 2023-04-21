from Domain.cardClientValidator import CardClientValidator
from Domain.film import Film
from Domain.filmValidator import FilmValidator
from Domain.rezervare import Rezervare
from Domain.rezervareValidator import RezervareValidator
from Repository.repository import Repository
from Repository.repositoryInMemory import RepositoryInMemory
from Repository.repositoryJson import RepositoryJson
from Service.cardClientService import CardClientService
from Service.filmService import FilmService
from Service.rezervareService import RezervareService
from Service.undoRedoService import UndoRedoService


def clearFile(filename):
    with open(filename, "w") as f:
        pass


def test_rezervare_repository():
    filename = 'test-rezervare-repository.json'
    clearFile(filename)
    rezervareRepository = RepositoryJson(filename)
    rezervareValidator = RezervareValidator()
    undoRedoService = UndoRedoService()
    cardClientRepository = RepositoryJson("test_rezervare.json")
    #  filmRepository =RepositoryJson("test_film.json")
    filmValidator = FilmValidator()
    undoRedoService = UndoRedoService()
    #  cardClientRepository = RepositoryJson("test_card.json")
    filename = 'test-card-repository.json'
    clearFile(filename)
    cardClientRepository = RepositoryJson(filename)
    cardClientValidator = CardClientValidator()
    cardClientService = CardClientService(cardClientRepository,
                                          cardClientValidator, undoRedoService)
    filename = 'test-film-repository.json'
    clearFile(filename)
    filmRepository = RepositoryJson(filename)

    filmService = FilmService(filmRepository, filmValidator, undoRedoService)

    #  filmService.adauga("1", "Tu", 1999, 25, "nu")

    assert rezervareRepository.read() == []

    add = Rezervare("3", "1", "2", "12.03.2002", "12:20")
    rezervareRepository.adauga(add)
    assert rezervareRepository.read("3") == add

    update = Rezervare("3", "1", "2", "12.03.2015", "18:45")
    rezervareRepository.modifica(update)
    assert rezervareRepository.read("3") == update

    delete = []
    rezervareRepository.sterge("3")
    assert rezervareRepository.read() == delete

    rezervareService = RezervareService(rezervareRepository, filmRepository,
                                        cardClientRepository,
                                        rezervareValidator, undoRedoService)
    filmService.adauga("5", "Eu", 2021, 35, "da")
    cardClientService.adauga("2", "Tatar", "Cosmin", "1234567891235",
                             "12.02.2002", "15.06.2009", 25)
    rezervareService.adauga("1", "5", "2", "12.03.2002", "12:20")
    rezervareService.adauga("3", "5", "2", "12.03.2002", "12:20")
    rezervare = rezervareService.get_all()
    assert len(rezervare) == 2
    assert rezervare[0].id_entitate == "1"
    assert rezervare[1].id_entitate == "3"

    rezervareService.sterge("1")
    rezervare = rezervareService.get_all()
    assert len(rezervare) == 1
    assert rezervare[0].id_entitate == "3"

    rezervareService.modifica("3", "5", "2", "12.03.2002", "15:00")
    rezervare = rezervareService.get_all()
    assert len(rezervare) == 1
    assert rezervare[0].id_entitate == "3"

    """rezultat = []
    filename = 'test-film-repository.json'
    clearFile(filename)
    filmRepository = RepositoryJson(filename)
    filmService = FilmService(filmRepository, filmValidator, undoRedoService)

    filename = 'test-rezervare-repository.json'
    clearFile(filename)
    rezervareRepository = RepositoryJson(filename)
    rezervareValidator = RezervareValidator()
    rezervareService = RezervareService(rezervareRepository, filmRepository,
                                        cardClientRepository,
                                        rezervareValidator, undoRedoService)

    filmService.adauga("7", "Eu", 2021, 35, "da")
    filmService.adauga("6", "tu", 2021, 35, "da")
    rezervareService.adauga("2", "7", "2", "12.03.2002", "12:20")
    rezervareService.adauga("4", "7", "2", "12.03.2002", "12:20")
    rezultat.append(rezervareService.filme_desc_nr_rezervari())

    assert len(rezultat) == 2"""
