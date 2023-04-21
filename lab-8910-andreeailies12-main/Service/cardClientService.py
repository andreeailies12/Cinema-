
from random import randint, choice

from Domain.addOperation import AddOperation
from Domain.cardClient import CardClient
from Domain.cardClientValidator import CardClientValidator
from Domain.delOperation import DelOperation
from Domain.modifyOperation import ModifyOperation

from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService


class CardClientService:
    def __init__(self, cardClientRepository: Repository,
                 cardClientValidator: CardClientValidator,
                 undoRedoService: UndoRedoService):
        self.__cardClientRepository = cardClientRepository
        self.__cardClientValidator = cardClientValidator
        self.__undoRedoService = undoRedoService

    def get_all(self):
        return self.__cardClientRepository.read()

    def adauga(self,
               id_card: str,
               nume: str,
               prenume: str,
               CNP: str,
               data_nasterii: str,
               data_inregistrarii: str,
               puncte_acumulate: float):
        card = CardClient(id_card,
                          nume,
                          prenume,
                          CNP,
                          data_nasterii,
                          data_inregistrarii,
                          puncte_acumulate)
        self.__cardClientValidator.valideaza(card)
        if self.__cardClientRepository.read(card.CNP) is not None:
            raise ValueError("CNP ul trebuie sa fie unic!")
        self.__cardClientRepository.adauga(card)
        self.__undoRedoService.addUndoOperation(
            AddOperation(self.__cardClientRepository, card))

    def sterge(self, id_card):
        cardSters = self.__cardClientRepository.read(id_card)
        self.__cardClientRepository.sterge(id_card)
        self.__undoRedoService.addUndoOperation(
            DelOperation(self.__cardClientRepository, cardSters))

    def modifica(self,
                 id_card: str,
                 nume: str,
                 prenume: str,
                 CNP: str,
                 data_nasterii: str,
                 data_inregistrarii: str,
                 puncte_acumulate: float):
        cardVechi = self.__cardClientRepository.read(id_card)
        card = CardClient(id_card,
                          nume,
                          prenume,
                          CNP,
                          data_nasterii,
                          data_inregistrarii,
                          puncte_acumulate)
        self.__cardClientValidator.valideaza(card)
        self.__cardClientRepository.modifica(card)
        self.__undoRedoService.addUndoOperation(
            ModifyOperation(self.__cardClientRepository, cardVechi, card))

    def cautare_full_text_clienti(self, a):
        clienti = self.__cardClientRepository.read()
        rezultat = []
        for i in clienti:
            CNP = str(i.CNP)
            puncte_acumulate = str(i.puncte_acumulate)
            if a in i.nume or a in i.prenume or a in CNP\
                    or a in i.data_nasterii or a in i.data_inregistrarii\
                    or a in puncte_acumulate:
                rezultat.append(i)
        if len(rezultat) == 0:
            raise KeyError("Nu exista parametrul dat")
        return rezultat

    def random_digits(self):
        lower = 10 ** (13 - 1)
        upper = 10 ** 13 - 1
        return randint(lower, upper)

    def carduri_generate(self, n):
        """
        Genereaza n carduri client
        :param n:
        :return:
        """

        numar_carduri_clienti_generate = 0
        while True:
            id_card = str(randint(1, 10000))
            nume_de_pers = ["Ilies", "Veres",
                            "Valean", "Rotaru",
                            "Szabo", "Morar",
                            "Iancu", "Sandor"]
            nume = choice(nume_de_pers)
            prenume_de_pers = ["Beatrice", "Vlad",
                               "Andreea", "Monica",
                               "Tamara", "Aren",
                               "Maria", "Dan"]
            prenume = choice(prenume_de_pers)
            CNP = int(self.random_digits())
            data_nasterii_a_pers = ["12.01.2002", "22.11.2005",
                                    "25.08.1970", "19.03.2000",
                                    "28.07.1960", "25.06.2010",
                                    "12.02.1989", "18.09.2001"]
            data_nasterii = choice(data_nasterii_a_pers)
            data_inregistrarii_a_pers = ["23.0.2000", "32.25.2003",
                                         "26.11.2015", "35.02.1987",
                                         "18.09.1973", "11.12.2001",
                                         "12.08.1998", "15.07.2008"]
            data_inregistrarii = choice(data_inregistrarii_a_pers)
            puncte_acumulate = randint(0, 100)
            card = CardClient(id_card,
                              nume,
                              prenume,
                              CNP,
                              data_nasterii,
                              data_inregistrarii,
                              puncte_acumulate)
            if self.__cardClientRepository.read(id_card) is None:
                numar_carduri_clienti_generate += 1
                self.__cardClientRepository.adauga(card)
                if numar_carduri_clienti_generate == n:
                    break

    def card_puncte(self):
        return sorted(self.__cardClientRepository.read(),
                      key=lambda cardClient: int(cardClient.puncte_acumulate),
                      reverse=True)

    def incrementarea_cardurilor(self,
                                 data_1: str,
                                 data_2: str,
                                 valoare_data: int):
        """
        Incrementarea cu o valoare dată a punctelor de pe
         toate cardurile a căror zi de naștere se află într-un interval dat.
        :param data_1: prima data
        :param data_2: a doua data
        :param valoare_data: valoarea cu care se mareste numarul de punct
          de pe card
        :return:
"""
        for card in self.__cardClientRepository.read():
            data_n = card.data_nasterii[0] + card.data_nasterii[1]
            if data_n <= data_2 and data_n >= data_1:
                if type(card.puncte_acumulate) is str:
                    pct = card.puncte_acumulate
                    card.puncte_acumulate = int(pct) + valoare_data
                else:
                    card.puncte_acumulate += valoare_data
                self.__cardClientRepository.modifica(card)
