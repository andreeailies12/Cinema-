from Domain.film import Film
from Domain.filmValidator import FilmValidator
from Repository.repositoryJson import RepositoryJson


from Service.filmService import FilmService
from Service.undoRedoService import UndoRedoService


def clearFile(filename):
    with open(filename, "w") as f:
        pass


def test_film_repositoryy():
    filmul = RepositoryJson("test-film.json")
    filmul.adauga(Film("1", "Tu", 1999, 25, "nu"))
    assert len(filmul.read()) == 1
    filmul.modifica(Film("1", "Tu", 2000, 25, "nu"))
    assert filmul.read("1").an_aparitie == 2000
    filmul.sterge("1")
    assert len(filmul.read()) == 0


def test_film_repository():
    filename = 'test-film-repository.json'
    clearFile(filename)
    filmRepository = RepositoryJson(filename)
    filmValidator = FilmValidator()
    undoRedoService = UndoRedoService()

    filmService = FilmService(filmRepository, filmValidator, undoRedoService)

    assert filmRepository.read() == []

    add = Film("1", "Tu", 1999, 25, "nu")
    filmRepository.adauga(add)

    assert filmRepository.read("1") == add

    update = Film("1", "Eu", 2021, 35, "da")
    filmRepository.modifica(update)
    assert filmRepository.read("1") == update

    delete = []
    filmRepository.sterge("1")
    assert filmRepository.read() == delete

    filmService.adauga("1", "Tu", 1999, 25, "nu")
    filmService.adauga("2", "Eu", 2021, 35, "da")
    filme = filmService.get_all()
    assert len(filme) == 2
    assert filme[0].id_entitate == "1"
    assert filme[1].id_entitate == "2"
    assert filme[1].an_aparitie == 2021

    filmService.sterge("1")
    filme = filmService.get_all()
    assert len(filme) == 1
    assert filme[0].id_entitate == "2"

    filmService.modifica("2", "Tu", 1999, 25, "nu")
    filme = filmService.get_all()
    assert len(filme) == 1
    assert filme[0].id_entitate == "2"
    assert filme[0].an_aparitie == 1999

    rezultat = []
    rezultat = filmService.cautare_full_text_filme("n")
    assert len(rezultat) == 1
