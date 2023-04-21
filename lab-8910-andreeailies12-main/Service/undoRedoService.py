from Domain.undoRedoOperation import UndoRedoOperation


class UndoRedoService:
    def __init__(self):
        self.__undoOperations: list[UndoRedoOperation] = []
        self.__redoOperations: list[UndoRedoOperation] = []

    def addUndoOperation(self, undoRedoOperation: UndoRedoOperation):
        self.__undoOperations.append(undoRedoOperation)
        self.__redoOperations.clear()

    def undo(self):
        if self.__undoOperations:
            lastUndoOperation = self.__undoOperations.pop()
            self.__redoOperations.append(lastUndoOperation)
            lastUndoOperation.doUndo()  # pop- returneaza ultimul elem
            # din lista si il si scoate din lista

    def redo(self):
        if self.__redoOperations:
            lastRedoOperation = self.__redoOperations.pop()
            self.__undoOperations.append(lastRedoOperation)
            lastRedoOperation.doRedo()
