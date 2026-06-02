import os
from PySide6.QtCore import QTimer, Signal, Qt
from PySide6.QtWidgets import (
    QProgressBar, QStackedWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QFrame
)
from gui.widgets.css import CREATE_KEY_STYLES, GENERAL_STYLES
from utils.db_crud import Database


class PragmaKeyManager(QWidget):
    successful = Signal()


    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setWindowTitle("Create PRAGMA Key")
        self.setFixedSize(800, 400)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.stack = QStackedWidget()
        
        self.init_loading_screen()
        self.init_create_screen()
        self.css_styles()
        
        self.main_layout.addWidget(self.stack)
        
        QTimer.singleShot(3000, self.check_existing_key)


    def init_loading_screen(self):
        self.loading_page = QFrame()
        self.loading_page.setObjectName("general")
        self.loading_page.setFixedWidth(400)
        layout = QVBoxLayout(self.loading_page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        label = QLabel("Checking for existing key...")
        label.setObjectName("notifer")
        label.setAlignment(Qt.AlignCenter)

        self.check_progress = QProgressBar()
        self.check_progress.setRange(0, 0)
        self.check_progress.setFixedWidth(300)

        layout.addWidget(label)
        layout.addWidget(self.check_progress)
        self.stack.addWidget(self.loading_page)


    def init_create_screen(self):
        self.create_page = QFrame()
        self.create_page.setObjectName("general")
        self.create_page.setFixedWidth(400)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedWidth(300)

        layout = QVBoxLayout(self.create_page)
        self.title = QLabel("Create Your PRAGMA Key")
        self.title.setObjectName("notifer")
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Create PRAGMA KEY")
        self.key_input.setEchoMode(QLineEdit.Password)
        
        self.proceed_btn = QPushButton("Proceed")
        self.proceed_btn.clicked.connect(self.handle_validation)
        
        layout.addWidget(self.title)
        layout.addWidget(self.key_input)
        layout.addWidget(self.proceed_btn)
        layout.addWidget(self.progress_bar)
        self.progress_bar.hide()
        
        self.stack.addWidget(self.create_page)


    def start_database(self):
        self.db.init_db()
        QTimer.singleShot(2000, lambda: self.successful.emit())
        QTimer.singleShot(2500, lambda: self.progress_bar.hide())


    def check_existing_key(self):
        found_db_key = self.db.get_db_key()
        storage = self.db.get_db_path()
        db_exists = storage.exists()

        # If database is found but no key to decrypt it
        # User is required to provide the decryption key
        if db_exists and not found_db_key:
            self.title.setText("Enter PRAGMA Key")
            self.key_input.setPlaceholderText("Enter PRAGMA Key")
            self.stack.setCurrentWidget(self.create_page)
            QMessageBox.information(
                self, 
                "Database Found", 
                "An existing database was found. Please enter the correct key to unlock it."
            )
            return

        # If both database and key are not found
        # User is required to provide progma key to create a new database
        if not db_exists and not found_db_key:
            self.title.setText("Create Your PRAGMA Key")
            self.key_input.setPlaceholderText("Create PRAGMA KEY")
            self.stack.setCurrentWidget(self.create_page)
            return

        # If key is found but no database
        # System use the existing key to create a new database
        if not db_exists and found_db_key:
            self.start_database()
            return

        # If both database and key are found
        # System check if the key can decrypt the database
        key_check = self.db.verify_db_key()
        
        if key_check is False:
            self.title.setText("Enter PRAGMA Key")
            self.key_input.setPlaceholderText("Enter PRAGMA Key")
            self.stack.setCurrentWidget(self.create_page)
            QMessageBox.critical(
                self,
                "Key Mismatch",
                f"The key you entered does not match the existing database.\n\n"
                f"If you have forgotten your key, you must delete the old database file to start fresh.\n\n"
                f"Database location:\n{storage}"
            )
            return
        else:
            self.start_database()


    def handle_validation(self):
        self.progress_bar.show()
        pragma_key = self.key_input.text().strip()

        # PRAMGA key must be at least 8 characters long
        if not pragma_key or len(pragma_key) < 8:
            self.progress_bar.hide()
            QMessageBox.warning(self, "Error", "Key must be at least 8 characters.")
            return

        if pragma_key:
            storage = self.db.get_db_path()
            key_created = self.db.create_keycode(pragma_key)

            if key_created:
                key_check = self.db.verify_db_key()

                if key_check is False:
                    self.progress_bar.hide()
                    QMessageBox.critical(
                        self,
                        "Key Mismatch",
                        f"The key you entered does not match the existing database.\n\n"
                        f"If you have forgotten your key, you must delete the old database file to start fresh.\n\n"
                        f"Database location:\n{storage}"
                    )
                    return
                
                self.start_database()
            else:
                self.progress_bar.hide()
                QMessageBox.warning(self, "PragmaKey Failed", "Try again!")
                return


    # style
    def css_styles(self):
        styles = [
            CREATE_KEY_STYLES,
            GENERAL_STYLES
        ]
        self.setStyleSheet("\n".join(styles))
