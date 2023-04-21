from Domain.entitate import Entitate
from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class MultiDeleteOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, obiecteSterse: list[Entitate]):
        self.__repository = repository
        self.__obiecteSterse = obiecteSterse

    def doUndo(self):
        for entitate in self.__obiecteSterse:
            self.__repository.adauga(entitate)

    def doRedo(self):
        for entitate in self.__obiecteSterse:
            self.__repository.sterge(entitate.id_entitate)
