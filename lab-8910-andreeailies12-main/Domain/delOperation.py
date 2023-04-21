from Domain.entitate import Entitate
from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class DelOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, obiectSters: Entitate):
        self.__repository = repository
        self.__obiectSters = obiectSters

    def doUndo(self):
        self.__repository.adauga(self.__obiectSters)

    def doRedo(self):
        self.__repository.sterge(self.__obiectSters.id_entitate)
