from Domain.film import Film
from Domain.filmError import FilmError


class FilmValidator:
    def valideaza(self, film: Film):
        erori = []
        if film.pret_bilet < 0:
            erori.append("Pretul trebuie sa fie strict mai mare decat 0!")
        if film.in_program not in ['da', 'nu']:
            erori.append("Se specifica doar daca"
                         " filmul este sau nu in program!")
        if len(erori) > 0:
            raise FilmError(erori)
