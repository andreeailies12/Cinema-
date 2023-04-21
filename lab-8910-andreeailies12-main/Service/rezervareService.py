import datetime

from Domain.addOperation import AddOperation
from Domain.delOperation import DelOperation
from Domain.modifyOperation import ModifyOperation
from Domain.rezervare import Rezervare
from Domain.rezervareValidator import RezervareValidator

from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService


class RezervareService:
    def __init__(self, rezervareRepository: Repository,
                 filmRepository: Repository,
                 cardClientRepository: Repository,
                 rezervareValidator: RezervareValidator,
                 undoRedoService: UndoRedoService):

        self.__rezervareRepository = rezervareRepository
        self.__filmRepository = filmRepository
        self.__cardClientRepository = cardClientRepository
        self.__rezervareValidator = rezervareValidator
        self.__undoRedoService = undoRedoService

    def get_all(self):
        return self.__rezervareRepository.read()

    def adauga(self, id_rezervare: str, id_film: str, id_card: str,
               data: str, ora: str):
        rezervare = Rezervare(id_rezervare, id_film, id_card, data,
                              ora)
        film = self.__filmRepository.read(id_film)
        card = self.__cardClientRepository.read(id_card)
        if film is not None:
            if film.in_program == "da":
                self.__rezervareValidator.valideaza(rezervare)
                self.__rezervareRepository.adauga(rezervare)
                self.__undoRedoService.addUndoOperation(
                    AddOperation(self.__rezervareRepository, rezervare))
                if card is not None:
                    pct = card.puncte_acumulate
                    punctele_acumulate = 0.1 * film.pret_bilet
                    card.puncte_acumulate = float(pct) + punctele_acumulate
                    total_puncte = card.puncte_acumulate
                    self.__cardClientRepository.modifica(card)
                    return total_puncte
            else:
                raise KeyError("Filmul nu este in program, astfel rezervarea "
                               "nu poate fi facuta!")
        else:
            raise KeyError("Nu exista niciun film cu id-ul dat!")

    def sterge(self, id_rezervare):
        rezervareStearsa = self.__rezervareRepository.read(id_rezervare)
        self.__rezervareRepository.sterge(id_rezervare)
        self.__undoRedoService.addUndoOperation(
            DelOperation(self.__rezervareRepository, rezervareStearsa))

    def modifica(self,
                 id_rezervare: str,
                 id_film: str,
                 id_card: str,
                 data: str,
                 ora: str):
        if self.__filmRepository.read(id_film) is None:
            raise KeyError("Nu exista niciun film cu id-ul dat!")
        #  if self.__cardClientRepository.read(id_card) is None:
            #  raise KeyError("Nu exista niciun card cu id-ul dat!")
        rezervareVeche = self.__rezervareRepository.read(id_rezervare)
        rezervare = Rezervare(id_rezervare, id_film, id_card, data, ora)
        self.__rezervareValidator.valideaza(rezervare)
        self.__rezervareRepository.modifica(rezervare)
        self.__undoRedoService.addUndoOperation(
            ModifyOperation(self.__rezervareRepository, rezervareVeche,
                            rezervare))

    def dupa_ora(self, start, end):
        rezultat = []
        for rezervare in self.__rezervareRepository.read():
            ora = rezervare.ora
            x = ora.split(":")

            if start <= str(x[0]) <= end:
                rezultat.append(rezervare)

            if len(rezultat):
                return rezultat
            else:
                raise KeyError(
                    "Nu exista nicio rezervare in acest interval orar!")

    def filme_desc_nr_rezervari(self):
        """
        se ordoneaza filmele descrescator in functe de numarul de rezervari
        :return:
        """
        nr_rezervari = {}
        for film in self.__filmRepository.read():
            nr_rezervari[film.id_entitate] = 0
        for rezervare in self.__rezervareRepository.read():
            nr_rezervari[rezervare.id_film] += 1
        rezultat = []
        for id_film in nr_rezervari:
            rezultat.append({
                "film": self.__filmRepository.read(id_film),
                "numarRezervari": nr_rezervari[id_film]
            })
        return sorted(rezultat, key=lambda x: x["numarRezervari"],
                      reverse=True)

    def afisare_rezervari_ore(self, ora_start: str, ora_final: str):
        """rezervari = []
        for rezervare in self.__rezervareRepository.read():
            if rezervare.ora >= ora_start and rezervare.ora <= ora_final:

                rezervari.append(rezervare)
        return rezervari"""

        rezervari = []
        for rezervare in self.__rezervareRepository.read():
            if rezervare.ora >= ora_start and rezervare.ora <= ora_final:
                rezervari.append(rezervare)

        interval = list(filter(lambda rezervare: rezervare.ora, rezervari))
        return interval

    def stergere_rezervari(self, data_2: str, data_1: str):
        """
        stergerea rezervarilor cu un id dat
        :param data_2: a doua data
        :param data_1: prima data
        :return:
        """

        ziua_1 = int(data_1[0] + data_1[0])
        ziua_2 = int(data_2[0] + data_2[0])
        luna_1 = int(data_1[3] + data_1[4])
        luna_2 = int(data_2[3] + data_2[4])
        anul_1 = int(data_1[6] + data_1[7] + data_1[8] + data_1[9])
        anul_2 = int(data_2[6] + data_2[7] + data_2[8] + data_2[9])
        prima_data = datetime.date(anul_1, luna_1, ziua_1)
        a_doua_data = datetime.date(anul_2, luna_2, ziua_2)

        if a_doua_data < prima_data:
            prima_data, a_doua_data = a_doua_data, prima_data

        rezervari_sterse = []
        r = {}

        for rezervare in self.__rezervareRepository.read():
            data = rezervare.data
            ziua = int(data[0] + data[1])
            luna = int(data[3] + data[4])
            anul = int(data[6] + data[7] + data[8] + data[9])
            data_r = datetime.date(anul, luna, ziua)
            r[rezervare.id_entitate] = data_r
            if prima_data <= data_r <= a_doua_data:
                rezervari_sterse.append(rezervare)
                self.__rezervareRepository.sterge(rezervare.id_entitate)

        """ziua_1 = int(data_1[0] + data_1[0])
        ziua_2 = int(data_2[0] + data_2[0])
        luna_1 = int(data_1[3] + data_1[4])
        luna_2 = int(data_2[3] + data_2[4])
        anul_1 = int(data_1[6] + data_1[7] + data_1[8] + data_1[9])
        anul_2 = int(data_2[6] + data_2[7] + data_2[8] + data_2[9])
        prima_data = datetime.date(anul_1, luna_1, ziua_1)
        a_doua_data = datetime.date(anul_2, luna_2, ziua_2)

        if a_doua_data < prima_data:
            prima_data, a_doua_data = a_doua_data, prima_data

        rs = []
        r = {}

        for rezervare in self.__rezervareRepository.read():
            data = rezervare.data
            ziua = int(data[0] + data[1])
            luna = int(data[3] + data[4])
            anul = int(data[6] + data[7] + data[8] + data[9])
            data_r = datetime.date(anul, luna, ziua)
            r[rezervare.id_entitate] = data_r

        rs= list(filter(lambda rezervare: prima_data<= r[rezervare.id_entitate]
        <= a_doua_data,self.__rezervareRepository.read()))
        for rezervare in rs:
            self.__rezervareRepository.sterge(rezervare.id_entitate)"""

    def stergere_film(self, id_film: str):
        """for rezervare in self.__rezervareRepository.read():
            if rezervare.id_film == id_film:
                self.__rezervareRepository.sterge(rezervare.id_entitate)"""
        film_sters = list(filter(lambda rezervare: rezervare.id_film,
                                 self.__rezervareRepository.read()))
        for rezervare in film_sters:
            obiecte_sterse = self.__filmRepository.read(id_film)
            self.__rezervareRepository.sterge(rezervare.id_entitate)

    def stergere_card(self, id_card: str):
        """for rezervare in self.__rezervareRepository.read():
            if rezervare.id_card == id_card:
                self.__rezervareRepository.sterge(rezervare.id_entitate)"""
        card_sters = list(filter(lambda rezervare: rezervare.id_card,
                                 self.__rezervareRepository.read()))
        for rezervare in card_sters:
            obiecte_sterse = self.__cardClientRepository.read(id_card)
            self.__rezervareRepository.sterge(rezervare.id_entitate)
