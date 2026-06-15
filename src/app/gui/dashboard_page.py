from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QTableView, QTextEdit, QSplitter
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QColor
from collections import Counter
from PySide6.QtCore import QSortFilterProxyModel, Qt
from utils.db_crud import Database
from gui.widgets.card import SummaryCard, SmallSummaryCard
from gui.widgets.log_table import LogTableModel
from gui.widgets.css import GENERAL_STYLES, LOG_TABLE_STYLES

class Dashboard(QWidget):
    refresh_database = Signal()


    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setAutoFillBackground(True)
        self.setWindowTitle("Dashboard")
        self.main_layout = QVBoxLayout(self) 

        self.event_logs = []
        self.filtered_logs = []

        self.summary_ui()
        self.table_and_detail_ui()
        self.css_styles()


    # summary
    def summary_ui(self):
        container = QHBoxLayout()

        # Pie Chart
        self.pie = QPieSeries()

        chart = QChart()
        chart.addSeries(self.pie)
        chart.setBackgroundBrush(QColor("white"))
        chart.legend().setAlignment(Qt.AlignBottom)
        self.chart_view = QChartView(chart)
        self.chart_view.setFixedHeight(200)
        self.chart_view.setFixedWidth(350)

        stats = Counter(l["level"] for l in (self.event_logs or []))
        self.info_event_count = str(stats.get("info", 0))
        self.warn_event_count = str(stats.get("warn", 0))
        self.error_event_count = str(stats.get("error", 0))
        self.critical_event_count = str(stats.get("critical", 0))

        self.total_event_count = str(len(self.event_logs or []))
        self.start_date, self.end_date = self.db.select_date_interval() if self.event_logs else ("", "")

        # Log Level Card
        log_level_container = QVBoxLayout()
        self.info_card = SmallSummaryCard("Info", self.info_event_count, "#2563eb")
        self.warn_card = SmallSummaryCard("Warn", self.warn_event_count, "#f59e0b")
        self.error_card = SmallSummaryCard("Error", self.error_event_count, "#F84E4E")
        self.critical_card = SmallSummaryCard("Critical", self.critical_event_count, "#dc2626")
        log_level_container.addWidget(self.info_card)
        log_level_container.addWidget(self.warn_card)
        log_level_container.addWidget(self.error_card)
        log_level_container.addWidget(self.critical_card)
        
        self.total_card = SummaryCard("Total Logs", self.total_event_count, "#0ea5a0")
        self.date_range_card = SummaryCard("Date range", f"{self.start_date}\n          -\n{self.end_date}", "#0ea5a0")
        container.addWidget(self.total_card)
        container.addWidget(self.date_range_card)
        container.addLayout(log_level_container)
        container.addWidget(self.chart_view)

        container.addStretch(1)
        self.main_layout.addLayout(container)


    # table & pane
    def filter_logs(self, text):
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy.setFilterFixedString(text)


    def refresh_pie_chart(self):
        self.pie.clear()
        if not self.event_logs:
            return
        levels = {}
        for l in self.event_logs:
            levels[l["level"]] = levels.get(l["level"], 0) + 1
        for k, v in levels.items():
            self.pie.append(k, v)


    def table_and_detail_ui(self):
        splitter = QSplitter(Qt.Horizontal)
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search logs...")
        self.search_box.textChanged.connect(self.filter_logs)

        self.table = QTableView()
        self.model = LogTableModel(self.filtered_logs)
        
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy.setFilterKeyColumn(-1)
        
        self.table.setModel(self.proxy)
        self.table.clicked.connect(self.inspect_log)

        self.detail = QTextEdit()
        self.detail.setReadOnly(True)

        splitter.addWidget(self.table)
        splitter.addWidget(self.detail)
        splitter.setSizes([700, 300])

        self.layout().addWidget(splitter)
        self.layout().addWidget(self.search_box)


    def inspect_log(self, selected_log):
        source_index = self.proxy.mapToSource(selected_log)
        log = self.filtered_logs[source_index.row()]
        log_dict = dict(log)
        formatted = "\n\n".join(f">> {k}: {v if v is not None else ''}" for k, v in log_dict.items())
        self.detail.setText(formatted)


    def update_data(self, new_logs):
        self.event_logs = new_logs
        self.filtered_logs = new_logs
        self.model.refresh_event_log_ui(self.filtered_logs)
        self.refresh_ui(self.event_logs)


    def refresh_ui(self, new_event_logs=None):
        self.event_logs = new_event_logs if new_event_logs is not None else []
        stats = Counter(l["level"] for l in (self.event_logs or []))
        self.info_card.update_smallsummarycard_value(stats.get("info", 0))
        self.warn_card.update_smallsummarycard_value(stats.get("warn", 0))
        self.error_card.update_smallsummarycard_value(stats.get("error", 0))
        self.critical_card.update_smallsummarycard_value(stats.get("critical", 0))
        self.total_card.update_summarycard_value(len(self.event_logs or []))
        self.start_date, self.end_date = self.db.select_date_interval() if self.event_logs else ("", "")
        self.date_range_card.update_summarycard_value(f"{self.start_date}\n          -\n{self.end_date}")
        self.refresh_pie_chart()


    # style
    def css_styles(self):
        styles = [
            GENERAL_STYLES,
            LOG_TABLE_STYLES
        ]
        self.setStyleSheet("\n".join(styles))
