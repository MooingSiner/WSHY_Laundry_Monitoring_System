from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt


class AManagerC:
    """Customer Manager view logic for Admin"""

    def __init__(self, main_window):
        self.main_window = main_window

        # Get reference to the customer page (USE) in the stacked widget
        self.manegerc_widget = self.main_window.stackedWidget.widget(
            self.main_window.manegerc_page_index
        )

        self.setup_manegerc_ui()

    def setup_manegerc_ui(self):
        """Setup customer manager-specific UI elements"""

        # Add title with Fredoka font
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]

            # Title label
            if hasattr(self.main_window, "ok_4"):
                title = getattr(self.main_window, "ok_4")
                title.setFont(QFont(family, 30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Action buttons
            other_buttons = ["nwbut_5", "nwbut_6", "nwbut_7", "nwbut_8","gotc_2"]
            for fbut in other_buttons:
                if hasattr(self.main_window, fbut):
                    but = getattr(self.main_window, fbut)
                    but.setFont(QFont(family, 10))
                    but.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup fonts for sidebar buttons
        users_buttons = ["Homebut_7", "Userbut_7", "Dashbut_7", "Orderbut_7",
                         "Reportbut_7", "Settbut_7"]
        for name in users_buttons:
            if hasattr(self.main_window, name):
                btn = getattr(self.main_window, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Search box
        if hasattr(self.main_window, "line2"):
            le = getattr(self.main_window, "line2")
            le.setPlaceholderText("Search by Name or ID")
            le.setFont(QFont("Arial", 10))
            le.setClearButtonEnabled(True)

        # Sort button
        if hasattr(self.main_window, "name_srt_btn_2"):
            btn = getattr(self.main_window, "name_srt_btn_2")
            btn.setFont(QFont("Arial", 10))
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Labels
        if hasattr(self.main_window, "label_14"):
            label = getattr(self.main_window, "label_14")
            label.setFont(QFont("Arial", 11))

        if hasattr(self.main_window, "label_15"):
            label = getattr(self.main_window, "label_15")
            label.setFont(QFont("Arial", 11))

        # Setup table widget
        if hasattr(self.main_window, "tableWidget_2"):
            table = getattr(self.main_window, "tableWidget_2")
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
        """Show the customer manager page"""
        self.main_window.stackedWidget.setCurrentIndex(
            self.main_window.manegerc_page_index
        )