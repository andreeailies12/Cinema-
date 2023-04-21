from Domain.cardClientValidator import CardClientValidator
from Domain.filmValidator import FilmValidator
from Domain.rezervareValidator import RezervareValidator
from Repository.repositoryJson import RepositoryJson
from Service.cardClientService import CardClientService
from Service.filmService import FilmService
from Service.rezervareService import RezervareService
from Service.undoRedoService import UndoRedoService
from UI.Console import Consola
from tests.test_card import test_card_repository
from tests.test_film import test_film_repository
from tests.test_fuctionalitati import test_rezervare_service

from tests.test_rezervare import test_rezervare_repository


def main():
    undoRedoService = UndoRedoService()

    filmRepositoryJson = RepositoryJson("filme.json")
    filmValidator = FilmValidator()
    filmService = FilmService(filmRepositoryJson,
                              filmValidator,
                              undoRedoService)

    cardClientRepositoryJson = RepositoryJson("carduri.json")
    cardClientValidator = CardClientValidator()
    cardClientService = CardClientService(cardClientRepositoryJson,
                                          cardClientValidator,
                                          undoRedoService)

    rezervareRepositoryJson = RepositoryJson("rezervari.json")
    rezervareValidator = RezervareValidator()
    rezervareService = RezervareService(rezervareRepositoryJson,
                                        filmRepositoryJson,
                                        cardClientRepositoryJson,
                                        rezervareValidator,
                                        undoRedoService)

    consola = Consola(filmService,
                      cardClientService,
                      rezervareService,
                      undoRedoService)

    consola.run_menu()


test_film_repository()
test_card_repository()
test_rezervare_repository()
test_rezervare_service()
main()
