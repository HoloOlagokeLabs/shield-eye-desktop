GENERAL_STYLES = """
    QProgressBar {
        border: 2px solid #3d3d3d;
        border-radius: 5px;
    }
    QProgressBar::chunk {
        background-color: #0078d4;
    }
    QPushButton {
        background-color: #0078d4;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    QLineEdit {
        border: none;
    }
    QLabel {
        border: none;
    }
    QLabel#notifer {
        font-size: 18px;
        font-weight: bold;
        border: none;
    }
    QFrame#general {
        background-color: #4fe9f7;
        border-radius: 12px;
        padding: 16px;
    }
"""

CHECK_BOX_STYLE = """
    QCheckBox {
        border-radius: 12px;
        padding: 2px;
        font-size: 14px;
        width: 70px;
    }
"""

CREATE_KEY_STYLES = """
    QFrame {
        border: 2px solid #3d3d3d;
        border-radius: 15px;
        padding: 20px;
    }
    QLineEdit {
        border: 1px solid #555;
        border-radius: 5px;
        padding: 8px;
    }
"""

LOG_TABLE_STYLES = """
    QWidget {
        font-size: 13px;
    }
    QTableView {
        gridline-color: #123047;
    }
    QLineEdit {
        border: 1px solid #555;
        border-radius: 5px;
        padding: 8px;
    }
    QHeaderView::section {
        padding: 4px;
        border: 1px solid #123047;
    }
"""

ALERT_BTN_STYLES = """
    QPushButton {
        color: white;
        border-radius: 5px;
        padding: 8px;
        font-size: 14px;
        min-width: 100px;
        max-width: 100px;
    }
    QPushButton#readAlertBtn {
        background-color: #a5ec72;
        border: 1px solid #94d665; 
    }
    QPushButton#readAllAlertBtn {
        background-color: #a3bd52;
        border: 1px solid #94d665; 
    }
    QPushButton#deleteAlertBtn {
        background-color: #FA0000;
        border: 1px solid #CC0808; 
    }
    QPushButton#deleteAllAlertBtn {
        background-color: #FF0828;
        border: 1px solid #CC0808; 
    }
"""
