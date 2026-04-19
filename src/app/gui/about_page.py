import os
import subprocess
import sys
import traceback
from PySide6.QtCore import QCoreApplication, QThreadPool, Slot
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QDialog,
    QPushButton, QMessageBox, QProgressDialog
)
from gui.widgets.dialog_win import ConfirmDialog
from gui.widgets.css import GENERAL_STYLES
from gui.widgets.card import DetailCard
from utils.db_crud import *
from utils.check_update import *
from packaging.version import Version


source_dir = "about page"
app_version = os.getenv("APP_VERSION",  default="0.0.0")
app_name = os.getenv("APP_NAME",  default="ShiedEye App")
github_update_url = os.getenv("GITHUB_UPDATE_URL",  default=None)
developer_name = os.getenv("DEVELOPER_NAME", default="ShieldEye Team")
developer_contact = os.getenv("DEVELOPER_CONTACT", default="ShieldEye Team")
github_url = os.getenv("GITHUB_URL", default=None)
website_url = os.getenv("WEBSITE_URL", default=None)
shieldeye_website_url = os.getenv("SHIELDEYE_WEBSITE_URL", default=None)

class About(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setWindowTitle("About")
        self.main_layout = QVBoxLayout(self) 
        self.page_ui()
        self.css_styles()

    def page_ui(self):
        container = QVBoxLayout()
        group_container = QHBoxLayout()

        app_name_label = f"App Name: {app_name}"
        app_version_label =f"Version: {app_version}"
        developer_label = f"Developer: {developer_name}"
        contact_label = f"Contact: {developer_contact}"
        github_url_label = f"Github: {github_url}"
        website_label = f"Website: {website_url}"

        container.addWidget(DetailCard(app_name_label, app_version_label, developer_label, contact_label, github_url_label, website_label, "#0ea5a0"))

        self.check_update_button = QPushButton("Check update")
        self.check_update_button.clicked.connect(self.start_update_check)
        self.threadpool = QThreadPool.globalInstance()

        self.live_webpage_button = QPushButton("Webpage version")
        self.live_webpage_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(f"{shieldeye_website_url}")))

        group_container.addWidget(self.check_update_button)
        group_container.addWidget(self.live_webpage_button)
        group_container.addSpacing(20)
        container.addLayout(group_container)

        container.addStretch(1)
        self.main_layout.addLayout(container)

    def start_update_check(self):
        if github_update_url:
            self.check_update_button.setEnabled(False)
            self.check_update_button.setText("Checking...")
            
            checker = UpdateChecker(github_update_url)
            checker.signals.finished.connect(self.on_update_found)
            checker.signals.error.connect(self.on_update_error)
            
            self.threadpool.start(checker)
        else:
            QMessageBox.warning(None, "Update Error", "GitHub URL is null")


    @Slot(dict)
    def on_update_found(self, data):
        self.check_update_button.setEnabled(True)
        self.check_update_button.setText("Check update")
        if Version(data["version"]) <= Version(app_version):
            QMessageBox.information(None, "Updated", "ShieldEye app is updated")
            return
        dialog = UpdateDetailDialog(data, self)
        if dialog.exec() == QDialog.Accepted:
            self.start_file_download(data)

    @Slot(str)
    def on_update_error(self, message):
        self.check_update_button.setEnabled(True)
        self.check_update_button.setText("Check update")
        QMessageBox.warning(None, "Update Error", f"Failed: {message}")

    def start_file_download(self, data):
        self.progress_bar = QProgressDialog("Downloading update...", "Cancel", 0, 100, self)
        self.progress_bar.setAutoClose(True)
        self.progress_bar.show()

        uploader = UpdateDownloader(data["download_url"], data["hash"])
        uploader.signals.progress.connect(self.progress_bar.setValue)
        uploader.signals.error.connect(lambda err: QMessageBox.critical(None, "Error", str(err)))
        uploader.signals.finished.connect(self.execute_installer)
        
        self.threadpool.start(uploader)

    def execute_installer(self, file_path):
        if self.progress_bar:
            self.progress_bar.setValue(100)
            self.progress_bar.close()
        
        title = "Update ShieldEye"
        message = "Do you want to install the latest version of ShieldEye now?"
        QMessageBox.information(self, "Download Complete", f"New version downloaded to: {file_path}")
        
        dialog = ConfirmDialog(title, message, self)
        if dialog.exec() == QDialog.Accepted:
            try:
                # Windows
                if os.name == "nt":
                    # start /wait ensures installer finishes before restarting
                    cmd = f'start /wait "" "{file_path}" && "{sys.executable}" "{sys.argv[0]}"'
                    subprocess.Popen(cmd, shell=True)
                    sys.exit()

                # Linux
                else:
                    os.chmod(file_path, 0o755)

                    # Detect if app is running as installed binary (.deb) or from source
                    if getattr(sys, 'frozen', False):
                        restart_cmd = "shieldeye"
                    else:
                        restart_cmd = f"{sys.executable} {os.path.abspath(sys.argv[0])}"

                    # Command flow: Install → confirm done → Restart App
                    install_cmd = f"pkexec apt install -y {os.path.abspath(file_path)}"
                    full_chain = f"{install_cmd}; echo 'Install done. Restarting...'; sleep 2; {restart_cmd}"

                    # Try common terminals in order of preference
                    launched = False
                    terminals = [
                        ['x-terminal-emulator', '-e', f"bash -c '{full_chain}'"],
                        ['gnome-terminal', '--', 'bash', '-c', full_chain],
                        ['konsole', '-e', f"bash -c '{full_chain}'"],
                        ['xterm', '-e', f"bash -c '{full_chain}'"],
                    ]
                    for cmd in terminals:
                        try:
                            subprocess.Popen(cmd)
                            launched = True
                            break
                        except FileNotFoundError:
                            continue

                    if not launched:
                        QMessageBox.critical(
                            self,
                            "Error",
                            "Could not find a terminal emulator to run the installer.\n"
                            f"Please install manually:\n  sudo apt install {file_path}"
                        )
                        return

                    QCoreApplication.quit()
                    sys.exit()

            except Exception as e:
                log_activity("error", "Update Error", source_dir, str(e), traceback.format_exc(), "execute_installer func")
                QMessageBox.critical(self, "Error", f"Failed to launch installer: {e}")

    # style
    def css_styles(self):
        styles = [
            GENERAL_STYLES
        ]
        self.setStyleSheet("\n".join(styles))
