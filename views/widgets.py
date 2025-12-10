from PyQt6.QtWidgets import (
    QFrame,
    QLineEdit,
    QPushButton,
    QLabel,
    QGraphicsDropShadowEffect,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class Card(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 70))
        self.setGraphicsEffect(shadow)

class ModernLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._has_error = False
        self._focused = False
        self.update_style()

    def set_error(self, has_error: bool):
        self._has_error = has_error
        self.update_style()

    def update_style(self):
        if self._has_error:
            self.setStyleSheet("QLineEdit { border: 2px solid #e74c3c; }")
        elif self._focused:
            self.setStyleSheet("QLineEdit { border: 2px solid #4a90e2; }")
        else:
            self.setStyleSheet("QLineEdit { border: 2px solid #e0e0e0; }")

    def focusInEvent(self, event):
        self._focused = True
        self.update_style()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self._focused = False
        self.update_style()
        super().focusOutEvent(event)

class AnimatedButton(QPushButton):
    def __init__(self, text, primary=False, parent=None):
        super().__init__(text, parent)
        self.primary = primary
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(50)
        if primary:
            self.setObjectName("primaryButton")
        else:
            self.setObjectName("secondaryButton")

    def mousePressEvent(self, event):
        self.setProperty("pressed", True)
        self.style().unpolish(self)
        self.style().polish(self)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setProperty("pressed", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().mouseReleaseEvent(event)

class ResultCard(Card):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setObjectName("resultTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        self.value_label = QLabel("-")
        self.value_label.setObjectName("resultValue")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)

    def set_value(self, text, color=None):
        self.value_label.setText(text)
        if color:
            self.value_label.setStyleSheet(f"color: {color};")
        else:
            self.value_label.setStyleSheet("")

def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        elif child.layout():
            clear_layout(child.layout())
