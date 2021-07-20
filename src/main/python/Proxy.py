from PyQt5 import QtCore as qtc
from typing import Any

class ProxyModel(qtc.QAbstractProxyModel):
    def __init__(self, model, placeholderText='---', parent=None):
        super().__init__(parent)
        self._placeholderText = placeholderText
        self.setSourceModel(model)
        
    def index(self, row: int, column: int, parent: qtc.QModelIndex = ...) -> qtc.QModelIndex:
        return self.createIndex(row, column)

    def parent(self, index: qtc.QModelIndex = ...) -> qtc.QModelIndex:
        return qtc.QModelIndex()

    def rowCount(self, parent: qtc.QModelIndex = ...) -> int:
        return self.sourceModel().rowCount()+1 if self.sourceModel() else 0

    def columnCount(self, parent: qtc.QModelIndex = ...) -> int:
        return self.sourceModel().columnCount() if self.sourceModel() else 0

    def data(self, index: qtc.QModelIndex, role: int = qtc.Qt.DisplayRole) -> Any:
        if index.row() == 0 and role == qtc.Qt.DisplayRole:
            return self._placeholderText
        elif index.row() == 0 and role == qtc.Qt.EditRole:
            return None
        else:
            return super().data(index, role)

    def mapFromSource(self, sourceIndex: qtc.QModelIndex):
        return self.index(sourceIndex.row()+1, sourceIndex.column())

    def mapToSource(self, proxyIndex: qtc.QModelIndex):
        return self.sourceModel().index(proxyIndex.row()-1, proxyIndex.column())

    def mapSelectionFromSource(self, sourceSelection: qtc.QModelIndex):
        return super().mapSelection(sourceSelection)

    def mapSelectionToSource(self, proxySelection: qtc.QModelIndex):
        return super().mapSelectionToSource(proxySelection)
    
    def headerData(self, section: int, orientation: qtc.Qt.Orientation, role: int = qtc.Qt.DisplayRole):
        if not self.sourceModel():
            return None
        if orientation == qtc.Qt.Vertical:
            return self.sourceModel().headerData(section-1, orientation, role)
        else:
            return self.sourceModel().headerData(section, orientation, role)

    def removeRows(self, row: int, count: int, parent: qtc.QModelIndex = ...) -> bool:
        return self.sourceModel().removeRows(row, count -1)
