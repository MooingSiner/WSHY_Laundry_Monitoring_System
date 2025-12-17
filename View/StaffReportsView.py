from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt


class SReports:
    """Staff Reports/History view logic - works with the History page in stackedWidget"""

    def __init__(self, main_window):
        self.main_window = main_window

        # Get reference to the History page in the stacked widget
        self.report_widget = self.main_window.stackedWidget.widget(
            self.main_window.report_page_index
        )

        self.setup_report_ui()

    def setup_report_ui(self):
        """Setup History/Report page-specific UI elements"""

        # Add "Transaction & History" title label
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]

            # Title
            if hasattr(self.main_window, "ok_7"):
                title = getattr(self.main_window, "ok_7")
                title.setText("Transaction & History")
                title.setFont(QFont(family, 30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Search field
            if hasattr(self.main_window, "line4"):
                le = getattr(self.main_window, "line4")
                le.setPlaceholderText("Search by Name, ID, Status, etc.")
                le.setFont(QFont("Arial", 10))

            # Action buttons
            other_buttons = ["nwbut_11", "nwbut_13", "nwbut_14"]
            for fbut in other_buttons:
                if hasattr(self.main_window, fbut):
                    but = getattr(self.main_window, fbut)
                    but.setFont(QFont(family, 10))
                    but.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Filter/Sort button
            if hasattr(self.main_window, "name_srt_btn_4"):
                btn = getattr(self.main_window, "name_srt_btn_4")
                btn.setText("All")  # Initial filter state
                btn.setFont(QFont(family, 10))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Labels
            if hasattr(self.main_window, "label_36"):
                lbl = getattr(self.main_window, "label_36")
                lbl.setFont(QFont(family, 10))
                lbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            if hasattr(self.main_window, "label_39"):
                lbl = getattr(self.main_window, "label_39")
                lbl.setFont(QFont(family, 8))
                lbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup fonts for sidebar buttons - History page uses _4 suffix
        report_buttons = ["Homebut_4", "Userbut_4", "Dashbut_4", "Orderbut_4",
                          "Reportbut_4", "Delivlab_4", "Settbut_4"]
        for name in report_buttons:
            if hasattr(self.main_window, name):
                btn = getattr(self.main_window, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup table widget
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

    def show(self):
        """Show the History/Report page"""
        self.main_window.stackedWidget.setCurrentIndex(
            self.main_window.report_page_index
        )