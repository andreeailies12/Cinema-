from dataclasses import dataclass


@dataclass
class FilmError(Exception):
    mesaj: any

    def __str__(self):
        return f'FilmError: {self.mesaj}'
