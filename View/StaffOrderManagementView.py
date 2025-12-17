from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt


class SOrders:
    """Staff Order Management view logic - works with the ManageOrder page in stackedWidget"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.order_widget = self.main_window.stackedWidget.widget(
            self.main_window.order_page_index
        )

        self.setup_order_ui()

    def setup_order_ui(self):
        """Setup order page-specific UI elements"""

        # Add "Manage Order" title label
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]

            # Title
            if hasattr(self.main_window, "ok_6"):
                title = getattr(self.main_window, "ok_6")
                title.setText("Manage Order")
                title.setFont(QFont(family, 30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Search field
            if hasattr(self.main_window, "line3"):
                le = getattr(self.main_window, "line3")
                le.setPlaceholderText("Search by Name, ID, Status, etc.")
                le.setFont(QFont("Arial", 10))

            # Action buttons
            other_buttons = ["nwbut_9", "nwbut_10", "nwbut_12", "nwbut_15","cnl"]
            for fbut in other_buttons:
                if hasattr(self.main_window, fbut):
                    but = getattr(self.main_window, fbut)
                    but.setFont(QFont(family, 10))
                    but.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Sort button
            if hasattr(self.main_window, "name_srt_btn_3"):
                btn = getattr(self.main_window, "name_srt_btn_3")
                btn.setFont(QFont(family, 10))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Labels
            if hasattr(self.main_window, "label_17"):
                lbl = getattr(self.main_window, "label_17")
                lbl.setFont(QFont(family, 10))
                lbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            if hasattr(self.main_window, "label_19"):
                lbl = getattr(self.main_window, "label_19")
                lbl.setFont(QFont(family, 8))
                lbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup fonts for sidebar buttons - ManageOrder page uses _6 suffix
        order_buttons = ["Homebut_6", "Userbut_6", "Dashbut_6", "Orderbut_6",
                         "Reportbut_6", "Delivlab_5", "Settbut_6"]
        for name in order_buttons:
            if hasattr(self.main_window, name):
                btn = getattr(self.main_window, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup table widget
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
        """Show the order page"""
        self.main_window.stackedWidget.setCurrentIndex(
            self.main_window.order_page_index
        )