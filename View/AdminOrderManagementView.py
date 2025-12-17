from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt



class AOrders:
    """Dashboard view logic - works with the ADB page in stackedWidget"""

    def __init__(self, main_window):
        self.main_window = main_window

        # Get reference to the dashboard page (ADB) in the stacked widget
        self.order_widget = self.main_window.stackedWidget.widget(
            self.main_window.order_page_index
        )

        self.setup_order_ui()

    def setup_order_ui(self):
        """Setup dashboard-specific UI elements"""

        # Add "Dashboard" title label
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            if hasattr(self.main_window, "ok_6"):
                title= getattr(self.main_window, "ok_6")
                title.setFont(QFont(family,30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            # Check if title label already exists, if not create i

            if hasattr(self.main_window, "line3"):
                le = getattr(self.main_window, "line3")
                le.setPlaceholderText("Search")
                le.setFont(QFont("Arial", 10))

        # Setup fonts for dashboard buttons
        order_buttons = ["Homebut_8", "Userbut_8", "Dashbut_8", "Orderbut_8",
                             "Reportbut_8", "Settbut_8"]
        for name in order_buttons:
            if hasattr(self.main_window, name):
                btn = getattr(self.main_window, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        other_buttons = ["nwbut_9","nwbut_10","view"]
        for fbut in other_buttons:
            if hasattr(self.main_window, fbut):
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                but = getattr(self.main_window, fbut)
                but.setFont(QFont(family, 10))
                but.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        if hasattr(self.main_window, "tableWidget_3"):
            table = getattr(self.main_window, "tableWidget_3")
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
            self.main_window.order_page_index
        )