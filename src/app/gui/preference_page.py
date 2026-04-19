import traceback
import json
from datetime import datetime
from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import (
    QFrame, QProgressBar, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel,
    QMessageBox, QCheckBox
)
from gui.widgets.css import CHECK_BOX_STYLE, GENERAL_STYLES
from utils.db_crud import *

source_dir = "Preferences page"

class Preferences(QWidget):
    refresh_database = Signal()
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setWindowTitle("Preferences")
        self.main_layout = QVBoxLayout(self)
        self.prefs_sets = []
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedWidth(300)
        self.page_ui()
        self.css_styles()

    def page_ui(self):
        outer_container = QVBoxLayout()

        self.card_frame = QFrame()
        self.card_frame.setObjectName("general")
        card_layout = QVBoxLayout(self.card_frame)

        alert_prefs_container = QVBoxLayout()
        flex_container = QHBoxLayout()
        loader_container = QVBoxLayout()

        self.alert_prefs_label = QLabel("Create alert for: ")
        self.alert_prefs_label.setObjectName("notifer")
        self.warn_check = QCheckBox("Warn event")
        self.error_check = QCheckBox("Error event")
        self.critical_check = QCheckBox("Critical event")
        self.save_prefs_btn = QPushButton("Save")
        self.save_prefs_btn.clicked.connect(self.prefs_btn_clicked)

        self.status_label = QLabel("Status: Ready to Import")
        self.status_label.setObjectName("notifer")
        self.btn_upload = QPushButton("Upload Logs")
        self.btn_upload.clicked.connect(self.process_json)

        alert_prefs_container.addWidget(self.alert_prefs_label)
        alert_prefs_container.addWidget(self.error_check)
        alert_prefs_container.addWidget(self.critical_check)
        alert_prefs_container.addWidget(self.warn_check)
        alert_prefs_container.addWidget(self.save_prefs_btn)
        alert_prefs_container.addSpacing(20)

        flex_container.addWidget(self.btn_upload)
        flex_container.addWidget(self.status_label)

        loader_container.addWidget(self.progress_bar)

        card_layout.addLayout(alert_prefs_container)
        card_layout.addLayout(flex_container)
        card_layout.addLayout(loader_container)

        self.progress_bar.hide()

        outer_container.addWidget(self.card_frame)
        outer_container.addStretch(1)
        self.main_layout.addLayout(outer_container)

    def prefs_btn_clicked(self):
        self.progress_bar.show()
        id = str(uuid.uuid4())
        timestamp = datetime.now()
        warn_val = self.warn_check.isChecked()
        error_val = self.error_check.isChecked()
        critical_val = self.critical_check.isChecked()

        result = fetch_prefs_settings()
        
        if result:
            update_ps = update_prefs_settings(warn_val, error_val, critical_val)
            if update_ps:
                self.progress_bar.hide()
                QMessageBox.information(self, "Success", "User alert preference updated")
            else:
                self.progress_bar.hide()
                QMessageBox.information(self, "Failed", "Something went wrong!")
        else:
            saved_ps = save_prefs_settings(id, timestamp, warn_val, error_val, critical_val)
            if saved_ps:
                self.progress_bar.hide()
                QMessageBox.information(self, "Success", "User alert preference created")
            else:
                self.progress_bar.hide()
                QMessageBox.information(self, "Failed", "Something went wrong!")
        
    def process_json(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Log File", "", "JSON Files (*.json)")
        if not file_path: return

        self.status_label.setText("Uploading...")
        self.progress_bar.show()
        
        # Deferred 2 seconds to allow the UI to update
        # and show the progress bar before heavy JSON processing begins
        QTimer.singleShot(2000, lambda: self.perform_json_processing(file_path))

    def perform_json_processing(self, file_path):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            
            logs = data if isinstance(data, list) else [data]
            all_records = []
            
            for entry in logs:
                try:
                    log_data = (
                        entry["_id"],
                        entry["timestamp"]["$date"],
                        entry["level"],
                        entry["category"],
                        entry["event_type"],
                        entry["source"],
                        entry["message"],
                        entry["stack"],
                        json.dumps(entry["tags"]),
                        entry["app"]["name"],
                        entry["app"]["version"],
                        entry["user"]["id"],
                        entry["user"]["ip"],
                        entry["user"]["method"],
                        entry["user"]["endpoint"],
                        entry["user"]["status"],
                        entry["user"]["user_agent"]
                    )
                    all_records.append(log_data)
                except KeyError as e:
                    self.progress_bar.hide()
                    log_activity("error", type(e).__name__, source_dir, f"Rejected: Missing key {str(e)}", traceback.format_exc(), "process_json loop")
                    QMessageBox.warning(self, "Warn", f"Rejected: Missing key {str(e)}.")
                    self.status_label.setText(f"Rejected: Missing key {str(e)}")
                    return
            if all_records:
                self.progress_bar.hide()
                result = append_log(all_records)
                if result:
                    self.status_label.setText(f"Success: Appended {len(all_records)} records.")
                    QMessageBox.information(self, "Success", f"Appended {len(all_records)} records.")
                    self.refresh_database.emit()
                    if self.prefs_sets:
                        self.status_label.setText("Checking alerts...")
                        self.progress_bar.show()
                        QTimer.singleShot(2000, lambda: self.scan_for_alert(data))
                    return
        except Exception as e:
            self.progress_bar.hide()
            log_activity("error", type(e).__name__, source_dir, f"Invalid File: {str(e)}", traceback.format_exc(), "process_json func")
            QMessageBox.critical(self, "Error", f"Invalid File: {str(e)}")
            return

    def scan_for_alert(self, data):
        active_levels = set()
        if self.prefs_sets:
            levels = ["warn", "error", "critical"]
            for i, is_active in enumerate(self.prefs_sets):
                if is_active:
                    active_levels.add(levels[i])
        
        try:
            alerts = data if isinstance(data, list) else [data]
            all_alert = []
            
            for entry in alerts:
                level = entry.get("level")
                if not level:
                    continue
                
                if level.lower().strip() in active_levels:
                    try:
                        alert_data = (
                            str(uuid.uuid4()),
                            datetime.now(),
                            entry["level"],
                            entry["category"],
                            entry["event_type"],
                            entry["message"],
                            entry["_id"],
                            "unread"
                        )
                        all_alert.append(alert_data)
                    except KeyError as e:
                        self.progress_bar.hide()
                        log_activity("error", type(e).__name__, source_dir, f"Rejected: Missing key {str(e)}", traceback.format_exc(), "scan_for_alert loop")
                        QMessageBox.warning(self, "Warn", f"Rejected: Missing key {str(e)}.")
                        return
            
            if all_alert:
                self.progress_bar.hide()
                result = create_alert(all_alert)
                if result:
                    self.status_label.setText(f"Success: {len(all_alert)} alert(s) created.")
                    QMessageBox.information(self, "Success", f"{len(all_alert)} alert(s) created.")
                    self.refresh_database.emit()
                return
                
        except Exception as e:
            self.progress_bar.hide()
            log_activity("error", type(e).__name__, source_dir, f"Invalid Format: {str(e)}", traceback.format_exc(), "scan_for_alert func")
            QMessageBox.critical(self, "Error", f"Invalid Format: {str(e)}")


    def update_prefs(self, new_prefs_sets):
        self.prefs_sets = new_prefs_sets
        if self.prefs_sets:
            self.warn_check.setChecked(bool(self.prefs_sets[0]))
            self.error_check.setChecked(bool(self.prefs_sets[1]))
            self.critical_check.setChecked(bool(self.prefs_sets[2]))


    # style
    def css_styles(self):
        styles = [
            GENERAL_STYLES,
            CHECK_BOX_STYLE
        ]
        self.setStyleSheet("\n".join(styles))
