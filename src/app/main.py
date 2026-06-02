import os
import sys
from dotenv import load_dotenv
load_dotenv()
import traceback
from PySide6.QtCore import Qt, QTimer, QCoreApplication
from PySide6.QtGui import QFont, QIcon, QPixmap, QPalette, QBrush
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget,
    QStackedWidget, QMessageBox
)
from gui.create_key_page import PragmaKeyManager
from gui.dashboard_page import Dashboard
from gui.about_page import About
from gui.notifications_page import Notifications
from gui.preference_page import Preferences
from utils.db_crud import Database

source_dir = "base app"
app_name = os.getenv("APP_NAME",  default="ShiedEye App")
basedir = os.path.dirname(__file__)
icon_path = os.path.join(basedir, "assets", "icons", "logo.png")
bg_img_path = os.path.join(basedir, "assets", "themes", "background.png")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()

        self.setStyleSheet("""
            QStackedWidget, .Dashboard, .Notifications, .Preferences, .About {
                background-color: #07102a;
            }
            QPushButton {
                background-color: #2b5797;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                min-width: 200px;
                max-width: 200px;
            }
            QPushButton:hover {
                background-color: #3e79db;
            }
            QPushButton:pressed {
                background-color: #1e3a63;
            }
        """)

        self.root_widget = QWidget()
        self.root_layout = QVBoxLayout()
        self.root_widget.setLayout(self.root_layout)
        self.setCentralWidget(self.root_widget)

        self.create_key_page = PragmaKeyManager()
        self.create_key_page.successful.connect(self.on_prakey_success)
        self.root_layout.addWidget(self.create_key_page)


    def start_main_app(self):
        self.main_app_widget = QWidget()
        main_app_layout = QVBoxLayout()
        self.main_app_widget.setLayout(main_app_layout)

        # Nav buttons
        btn_container = QHBoxLayout()
        self.nav_widget = QWidget()
        self.nav_widget.setLayout(btn_container)

        dashboard_button = QPushButton("Dashboard")
        alert_button = QPushButton("Alerts")
        prefs_button = QPushButton("Preferences")
        about_button = QPushButton("About")

        btn_container.addWidget(dashboard_button)
        btn_container.addWidget(alert_button)
        btn_container.addWidget(prefs_button)
        btn_container.addWidget(about_button)

        # Stacked widget
        self.stacked_widget = QStackedWidget()

        self.dashboard = Dashboard()
        self.notifications = Notifications()
        self.preferences = Preferences()
        self.about = About()

        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.notifications)
        self.stacked_widget.addWidget(self.preferences)
        self.stacked_widget.addWidget(self.about)

        dashboard_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.dashboard))
        alert_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.notifications))
        prefs_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.preferences))
        about_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.about))

        main_app_layout.addWidget(self.nav_widget)
        main_app_layout.addWidget(self.stacked_widget)

        self.root_layout.addWidget(self.main_app_widget)

        self.set_background()
        self.dashboard.refresh_database.connect(self.refresh_all_data)
        self.notifications.refresh_database.connect(self.refresh_all_data)
        self.preferences.refresh_database.connect(self.refresh_all_data)

        # Delayed 100ms to ensure the main window is fully rendered
        # before showing a critical error dialog on startup
        QTimer.singleShot(100, self.delayed_sql_check)


    def on_prakey_success(self):
        self.create_key_page.hide()
        self.start_main_app()
        self.refresh_all_data()


    def delayed_sql_check(self):
        result = self.db.verify_sql_version()
        if isinstance(result, str):
            QMessageBox.critical(self, "Error", result)


    def refresh_all_data(self):
        try:
            self.event_logs = self.db.fetch_log()
            self.alert_logs = self.db.fetch_alert_log()
            self.prefs_sets = self.db.fetch_prefs_settings()

            self.dashboard.update_data(self.event_logs)
            self.notifications.update_data(self.alert_logs)
            self.preferences.update_prefs(self.prefs_sets)
        except Exception as e:
            self.db.log_activity("error", type(e).__name__, source_dir, f"File: {str(e)}", traceback.format_exc(), "refresh_all_data func")
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
            return


    def set_background(self):
        img = QPixmap(bg_img_path)
        scaled_img = img.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaled_img))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

if sys.platform == "win32":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

QCoreApplication.setOrganizationName("HoloOlagokeLabs")
QCoreApplication.setOrganizationDomain("holoolagoke.com")
QCoreApplication.setApplicationName("ShieldEye")

app = QApplication(sys.argv)
app.setFont(QFont("Segoe UI", 10))
win = MainWindow()
win.setWindowIcon(QIcon(icon_path))
win.setWindowTitle(f"{app_name}")
win.setMinimumSize(800, 600)
win.resize(1280, 720)
win.showMaximized()
sys.exit(app.exec())