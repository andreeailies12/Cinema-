from Domain.cardClient import CardClient
from Domain.cardClientValidator import CardClientValidator
from Repository.repositoryJson import RepositoryJson
from Service.cardClientService import CardClientService
from Service.undoRedoService import UndoRedoService


def test_card_repositoryy():
    cardul = RepositoryJson("test-card.json")
    cardul.adauga(CardClient("3", "Tatar", "Cosmin", "1234567891234",
                             "12.02.2002", "15.06.2009", 25))
    assert len(cardul.read()) == 1
    cardul.modifica(CardClient("3", "Tatar", "Cosmin", "1234567891234",
                               "12.02.2002", "15.06.2009", 26))
    assert cardul.read("3").puncte_acumulate == 26
    cardul.sterge("3")
    assert len(cardul.read()) == 0


def clearFile(filename):
    with open(filename, "w") as f:
        pass


def test_card_repository():
    filename = 'test-card-repository.json'
    clearFile(filename)
    cardClientRepository = RepositoryJson(filename)
    cardClientValidator = CardClientValidator()
    undoRedoService = UndoRedoService()
    cardClientService = CardClientService(cardClientRepository,
                                          cardClientValidator, undoRedoService)

    assert cardClientRepository.read() == []
    add = CardClient("1", "Tatar", "Cosmin", "1234567891234", "12.02.2002",
                     "15.06.2009", 25)
    cardClientRepository.adauga(add)
    assert cardClientRepository.read("1") == add

    update = CardClient("1", "Tatar", "Alex", "1234567891234", "12.02.2002",
                        "15.06.2015", 50)
    cardClientRepository.modifica(update)
    assert cardClientRepository.read("1") == update

    delete = []
    cardClientRepository.sterge("1")
    assert cardClientRepository.read() == delete

    cardClientService.adauga("1", "Tatar", "Cosmin", "2234567891236",
                             "12.02.2002", "15.06.2009", 25)
    cardClientService.adauga("2", "Tatar", "Cosmin", "1234567891235",
                             "12.02.2002", "15.06.2009", 25)
    cardClient = cardClientService.get_all()
    assert len(cardClient) == 2
    assert cardClient[0].id_entitate == "1"
    assert cardClient[1].id_entitate == "2"
    assert cardClient[1].puncte_acumulate == 25

    cardClientService.sterge("1")
    cardClient = cardClientService.get_all()
    assert len(cardClient) == 1
    assert cardClient[0].id_entitate == "2"

    cardClientService.modifica("2", "Tatar", "Cosmin", "1234567891235",
                               "12.02.1999", "15.06.2009", 17)

    cardClient = cardClientService.get_all()
    assert len(cardClient) == 1
    assert cardClient[0].id_entitate == "2"
    assert cardClient[0].puncte_acumulate == 17

    rezultat = []
    rezultat = cardClientService.cautare_full_text_clienti("n")
    assert len(rezultat) == 1
