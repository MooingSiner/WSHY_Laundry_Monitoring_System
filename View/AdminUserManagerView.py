from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt


class AManager:
    """User Manager view logic"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.users_widget = self.main_window.stackedWidget.widget(
            self.main_window.users_page_index
        )
        self.setup_user_ui()

    def setup_user_ui(self):
        """Setup user manager-specific UI elements"""

        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")

        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]

            if hasattr(self.main_window, "ok_3"):
                title = getattr(self.main_window, "ok_3")

                title.setFont(QFont(family, 30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            other_buttons = ["nwbut", "nwbut_2", "nwbut_3", "nwbut_4", "gotc"]
            for fbut in other_buttons:
                if hasattr(self.main_window, fbut):
                    but = getattr(self.main_window, fbut)
                    but.setFont(QFont(family, 10))
                    but.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        users_buttons = [
            "Homebut_5", "Userbut_5", "Dashbut_5",
            "Orderbut_5", "Reportbut_5", "Settbut_5"
        ]
        for name in users_buttons:
            if hasattr(self.main_window, name):
                btn = getattr(self.main_window, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        if hasattr(self.main_window, "line"):
            le = getattr(self.main_window, "line")
            le.setPlaceholderText("Search staff by name, email, or phone...")
            le.setFont(QFont("Arial", 10))
            le.setClearButtonEnabled(True)

        if hasattr(self.main_window, "name_srt_btn"):
            btn = getattr(self.main_window, "name_srt_btn")
            btn.setFont(QFont("Arial", 10))
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # UPDATED: Setup table widget with correct name 'tw'
        if hasattr(self.main_window, "tw"):
            table = getattr(self.main_window, "tw")
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
        """Show the user manager page"""
        self.main_window.stackedWidget.setCurrentIndex(
            self.main_window.users_page_index
        )