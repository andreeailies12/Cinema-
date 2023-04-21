import datetime
from Domain.cardClient import CardClient
from Domain.cardClientError import CardClientError


class CardClientValidator:
    def valideaza(self, card: CardClient):
        erori = []

        if len(str(card.CNP)) != 13:
            erori.append("CNP ul trebuie sa contina 13 cifre")

        try:
            datetime.datetime.strptime(card.data_nasterii, '%d.%m.%Y')
            datetime.datetime.strptime(card.data_inregistrarii, '%d.%m.%Y')
        except ValueError:
            erori.append("Data nu a fost scrisa corect!"
                         " Aceasta trebuie scrisa ca n exemplul urmator: "
                         "dd.mm.yyyy."
                         "(15.02.2003)")
        if erori != []:
            raise CardClientError(erori)
