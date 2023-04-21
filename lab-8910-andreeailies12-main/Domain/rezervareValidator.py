import datetime
from Domain.rezervare import Rezervare
from Domain.rezervareError import RezervareError


class RezervareValidator:

    def valideaza(self, rezervare: Rezervare):

        erori = []
        try:
            datetime.datetime.strptime(rezervare.data, '%d.%m.%Y')
        except ValueError:
            erori.append("Data nu a fost scrisa corect!"
                         " Aceasta trebuie scrisa ca n exemplul urmator:"
                         " dd.mm.yyyy (15.02.2003)")

        try:
            datetime.datetime.strptime(rezervare.ora, '%H:%M')
        except ValueError:
            erori.append("Ora nu a fost introdusa corect! "
                         "Aceasta trebuie scrisa ca in exemplul urmator: hh.mm"
                         "(12:37")
        if len(erori) > 0:
            raise RezervareError(erori)
