from dataclasses import dataclass


@dataclass
class CardClientError(Exception):
    mesaj: any

    def __str__(self):
        return f'CardClientError: {self.mesaj}'
