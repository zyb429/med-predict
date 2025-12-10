STYLESHEET = """
/* === Глобальные настройки шрифта === */
* {
    font-family: "Roboto", "Segoe UI", "Helvetica", "Arial", sans-serif;
    font-size: 10pt;
}

QMainWindow {
    background-color: #f5f7fa;
}
 
#header {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4a90e2, stop:1 #357abd);
    border: none;
}
 
#headerTitle {
    color: white;
    font-size: 22px;
    font-weight: bold;
}
 
#card, #selectorCard {
    background-color: white;
    border-radius: 12px;
    border: none;
}
 
#sectionTitle, #cardTitle {
    color: #2c3e50;
    font-size: 17px;
    font-weight: bold;
    margin-bottom: 5px;
}
 
#descriptionLabel {
    color: #636e72;
    font-size: 14px;
    font-style: italic;
}
 
#modelCombo {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 12px 16px;
    background: white;
    font-size: 15px;
    color: #2c3e50;
}
 
#modelCombo:hover {
    border: 2px solid #bdc3c7;
}
 
#modelCombo:focus {
    border: 2px solid #4a90e2;
}
 
#modelCombo::drop-down {
    border: none;
    padding-right: 15px;
}
 
#modelCombo QAbstractItemView {
    border: 2px solid #4a90e2;
    border-radius: 8px;
    background-color: white;
    selection-background-color: #4a90e2;
    selection-color: white;
    padding: 8px;
    outline: none;
    font-size: 14px;
}
 
#modelCombo QAbstractItemView::item {
    padding: 10px;
    border-radius: 6px;
    color: #2c3e50;
}
 
#modelCombo QAbstractItemView::item:hover {
    background-color: #e3f2fd;
    color: #2c3e50;
}
 
#modelCombo QAbstractItemView::item:selected {
    background-color: #4a90e2;
    color: white;
}
 
#fieldLabel {
    color: #2c3e50;
    font-size: 14px;
    font-weight: 600;
}
 
QLineEdit {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 12px 16px;
    background: white;
    font-size: 15px;
    color: #2c3e50;
}
 
QLineEdit:hover {
    border: 2px solid #bdc3c7;
}
 
QLineEdit:focus {
    border: 2px solid #4a90e2;
}
 
#errorLabel {
    color: #e74c3c;
    font-size: 12px;
    padding-left: 2px;
}
 
#primaryButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4a90e2, stop:1 #357abd);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 15px;
    font-weight: bold;
    padding: 15px 30px;
}
 
#primaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #357abd, stop:1 #2868a8);
}
 
#primaryButton[pressed="true"] {
    background: #2868a8;
    padding-top: 17px;
    padding-bottom: 13px;
}
 
#secondaryButton {
    background-color: #e3f2fd;
    color: #4a90e2;
    border: 2px solid #4a90e2;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 600;
    padding: 15px 30px;
}
 
#secondaryButton:hover {
    background-color: #bbdefb;
    border: 2px solid #357abd;
    color: #357abd;
}
 
#secondaryButton[pressed="true"] {
    background-color: #90caf9;
    padding-top: 17px;
    padding-bottom: 13px;
}
 
#exportButton {
    background-color: #27ae60;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 15px;
    font-weight: bold;
    padding: 15px 30px;
}
 
#exportButton:hover {
    background-color: #229954;
}
 
#exportButton[pressed="true"] {
    background-color: #1e8449;
    padding-top: 17px;
    padding-bottom: 13px;
}
 
#resultTitle {
    color: #2c3e50;
    font-size: 14px;
    font-weight: 600;
}
 
#resultValue {
    color: #4a90e2;
    font-size: 30px;
    font-weight: bold;
}
 
#conclusionTitle {
    color: #2c3e50;
    font-size: 15px;
    font-weight: bold;
}
 
#conclusionText {
    color: #2c3e50;
    font-size: 17px;
    font-weight: 600;
    padding: 10px;
}
 
QScrollArea {
    border: none;
    background: transparent;
}
 
QScrollBar:vertical {
    border: none;
    background: #f5f7fa;
    width: 10px;
    border-radius: 5px;
}
 
QScrollBar::handle:vertical {
    background: #bdc3c7;
    border-radius: 5px;
    min-height: 20px;
}
 
QScrollBar::handle:vertical:hover {
    background: #95a5a6;
}
 
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
 
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
 
QMessageBox {
    background-color: white;
}
 
QMessageBox QLabel {
    color: #2c3e50;
    font-size: 14px;
}
 
QMessageBox QPushButton {
    background-color: #4a90e2;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 25px;
    font-weight: bold;
    min-width: 80px;
}
 
QMessageBox QPushButton:hover {
    background-color: #357abd;
}
"""
