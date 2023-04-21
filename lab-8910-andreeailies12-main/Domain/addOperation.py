from Domain.undoRedoOperation import UndoRedoOperation
from Domain.entitate import Entitate
from Repository.repository import Repository


class AddOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, obiectAdaugat: Entitate):
        self.__repository = repository
        self.__obiectAdaugat = obiectAdaugat

    def doUndo(self):
        self.__repository.sterge(self.__obiectAdaugat.id_entitate)

    def doRedo(self):
        self.__repository.adauga(self.__obiectAdaugat)
