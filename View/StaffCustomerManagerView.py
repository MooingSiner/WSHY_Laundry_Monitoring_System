from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt


class SManagerC:
    """Customer Manager view logic for Staff"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.customer_widget = self.main_window.stackedWidget.widget(
            self.main_window.customer_page_index
        )
        self.setup_customer_ui()

    def setup_customer_ui(self):
        """Setup customer manager-specific UI elements"""

        # Load Fredoka font
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")

        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]

            # Title label - CSE page
            if hasattr(self.main_window, "ok_4"):
                title = getattr(self.main_window, "ok_4")
                title.setFont(QFont(family, 30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Action buttons - Use Fredoka font
            other_buttons = ["nwbut_5", "nwbut_6", "nwbut_7", "nwbut_8", "nwbut_16"]
            for fbut in other_buttons:
                if hasattr(self.main_window, fbut):
                    but = getattr(self.main_window, fbut)
                    but.setFont(QFont(family, 10))  # Using Fredoka
                    but.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Sidebar buttons (CSE page) - Use Fredoka font
            customers_buttons = [
                "Homebut_5", "Userbut_5", "Dashbut_5",
                "Orderbut_5", "Reportbut_5", "Settbut_5", "Delivlab_6"
            ]
            for name in customers_buttons:
                if hasattr(self.main_window, name):
                    btn = getattr(self.main_window, name)
                    btn.setFont(QFont("Arial", 15))  # Using Fredoka with size 12
                    btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Sort button - Use Fredoka font
            if hasattr(self.main_window, "name_srt_btn_2"):
                btn = getattr(self.main_window, "name_srt_btn_2")
                btn.setFont(QFont(family, 10))  # Using Fredoka
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Search box (can use Arial or Fredoka)
        if hasattr(self.main_window, "line2"):
            le = getattr(self.main_window, "line2")
            le.setPlaceholderText("Search by Name or ID")
            le.setFont(QFont("Arial", 10))
            le.setClearButtonEnabled(True)

        # Labels for sections
        if hasattr(self.main_window, "label_14"):
            label = getattr(self.main_window, "label_14")
            label.setFont(QFont("Arial", 11))

        if hasattr(self.main_window, "label_15"):
            label = getattr(self.main_window, "label_15")
            label.setFont(QFont("Arial", 11))

        # Action label header

        # Setup customer table widget
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
            self.main_window.customer_page_index
        )