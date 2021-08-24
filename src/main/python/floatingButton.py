

from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
class FloatingButtonWidget(qtw.QPushButton):

    def __init__(self, parent):
        super().__init__(parent)
        self.paddingLeft = 228
        self.paddingTop = 103
        self.setText("Background Information")
        self.setMinimumWidth(200)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet("""
            QPushButton{
                        padding:10px 10px;border:1px solid rgba(12, 75, 85, 0.8);color:rgba(12, 75, 85, 1);background:white;border-radius:8px;font-size:12px;font-weight:900
                    }
            QPushButton:hover{
                padding:10px 10px;border:1px solid rgba(12, 75, 85,0.8);color:#fff;background:#127281;border-radius:8px;font-size:12px;font-weight:900
            }
        """)

    def update_position(self):
        try:
            if hasattr(self.parent(), 'viewport'):
                parent_rect = self.parent().viewport().rect()
            else:
                parent_rect = self.parent().rect()

            if not parent_rect:
                return

            x = parent_rect.width() - self.width() - self.paddingLeft
            y = self.paddingTop
            self.setGeometry(x, y, self.width(), self.height())
        except Exception as e:
            print(e)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_position()

    def mousePressEvent(self, event):
        print(event)

