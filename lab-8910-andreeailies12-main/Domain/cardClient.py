from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class CardClient(Entitate):
    nume: str
    prenume: str
    CNP: str
    data_nasterii: str
    data_inregistrarii: str
    puncte_acumulate: float
