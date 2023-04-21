from Domain.entitate import Entitate
from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class ModifyOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, obiectVechi: Entitate,
                 obiectNou: Entitate):
        self.__repository = repository
        self.__obiectVechi = obiectVechi
        self.__obiectNou = obiectNou

    def doUndo(self):
        self.__repository.modifica(self.__obiectVechi)

    def doRedo(self):
        self.__repository.modifica(self.__obiectNou)
