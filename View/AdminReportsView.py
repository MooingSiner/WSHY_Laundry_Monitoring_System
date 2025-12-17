from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt


class AReport:
    """Dashboard view logic - works with the ADB page in stackedWidget"""

    def __init__(self, main_window):
        self.main_window = main_window

        # Get reference to the dashboard page (ADB) in the stacked widget
        self.report_widget = self.main_window.stackedWidget.widget(
            self.main_window.report_page_index
        )

        self.setup_report_ui()

    def setup_report_ui(self):
        """Setup dashboard-specific UI elements"""

        # Add "Dashboard" title label
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            if hasattr(self.main_window, "ok_7"):
                title= getattr(self.main_window, "ok_7")
                title.setFont(QFont(family,30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            # Check if title label already exists, if not create i

        if hasattr(self.main_window, "line4"):
            le = getattr(self.main_window, "line4")
            le.setPlaceholderText("Search")
            le.setFont(QFont("Arial", 10))

        # Setup fonts for dashboard buttons
        report_buttons = ["Homebut_9", "Userbut_9", "Dashbut_9", "Orderbut_9",
                             "Reportbut_9", "Settbut_9"]
        for name in report_buttons:
            if hasattr(self.main_window, name):
                btn = getattr(self.main_window, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        other_buttons = ["nwbut_11","nwbut_13","nwbut_14", "gotc_4"]
        for fbut in other_buttons:
            if hasattr(self.main_window, fbut):
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                but = getattr(self.main_window, fbut)
                but.setFont(QFont(family, 10))
                but.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        if hasattr(self.main_window, "tableWidget_4"):
            table = getattr(self.main_window, "tableWidget_4")
            table.setFont(QFont("Arial", 10))
            table.setSortingEnabled(True)
            table.setSelectionBehavior(table.SelectionBehavior.SelectRows)
            table.setSelectionMode(table.SelectionMode.SingleSelection)
            table.setAlternatingRowColors(True)
            table.setShowGrid(True)
            table.setEditTriggers(table.EditTrigger.NoEditTriggers)
            table.horizontalHeader().setStretchLastSection(True)
            table.verticalHeader().setVisible(False)

    def show(self):
        """Show the dashboard page"""
        self.main_window.stackedWidget.setCurrentIndex(
            self.main_window.report_page_index
        )