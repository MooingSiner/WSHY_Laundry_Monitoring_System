from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt


class SDelivery:
    """Staff Delivery/Pickup view logic - works with the Delivery page in stackedWidget"""

    def __init__(self, main_window):
        self.main_window = main_window

        # Get reference to the Delivery page in the stacked widget
        self.delivery_widget = self.main_window.stackedWidget.widget(
            self.main_window.Delivery_page_index
        )

        self.setup_delivery_ui()

    def setup_delivery_ui(self):
        """Setup delivery-specific UI elements"""

        # Load custom font
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]

            # Title label - "Delivery/Pickup" or similar
            if hasattr(self.main_window, "ok_11"):
                title = getattr(self.main_window, "ok_11")
                title.setFont(QFont(family, 30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Section labels
            if hasattr(self.main_window, "label_5"):  # "Pending Pickups" label
                label = getattr(self.main_window, "label_5")
                label.setFont(QFont(family, 14))
                label.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            if hasattr(self.main_window, "label_6"):  # "Pending Deliveries" label
                label = getattr(self.main_window, "label_6")
                label.setFont(QFont(family, 14))
                label.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Action buttons - use Fredoka font
            action_buttons = ["crt_btn_9", "crt_btn_10", "crt_btn_4", "crt_btn_5", "crt_btn_6", "name_srt_btn_6"]
            for button_name in action_buttons:
                if hasattr(self.main_window, button_name):
                    btn = getattr(self.main_window, button_name)
                    btn.setFont(QFont(family, 10))
                    btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Search field
        if hasattr(self.main_window, "line4_2"):
            le = getattr(self.main_window, "line4_2")
            le.setPlaceholderText("Search by Name, ID, etc.")
            le.setFont(QFont("Arial", 10))

        # Setup fonts for sidebar navigation buttons (Delivery page uses _9 suffix)
        sidebar_buttons = ["Homebut_9", "Userbut_9", "Dashbut_9", "Orderbut_9",
                           "Reportbut_9", "Delivlab_9", "Settbut_9"]
        for name in sidebar_buttons:
            if hasattr(self.main_window, name):
                btn = getattr(self.main_window, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup pickup table (tableWidget_5)
        if hasattr(self.main_window, "tableWidget_5"):
            table = getattr(self.main_window, "tableWidget_5")
            table.setFont(QFont("Arial", 10))
            table.setSortingEnabled(True)
            table.setSelectionBehavior(table.SelectionBehavior.SelectRows)
            table.setSelectionMode(table.SelectionMode.SingleSelection)
            table.setAlternatingRowColors(True)
            table.setShowGrid(True)
            table.setEditTriggers(table.EditTrigger.NoEditTriggers)
            table.horizontalHeader().setStretchLastSection(True)
            table.verticalHeader().setVisible(False)  # Hide row numbers
            print("✓ Setup pickup table (tableWidget_5)")

        # Setup delivery table (tableWidget_6)
        if hasattr(self.main_window, "tableWidget_6"):
            table = getattr(self.main_window, "tableWidget_6")
            table.setFont(QFont("Arial", 10))
            table.setSortingEnabled(True)
            table.setSelectionBehavior(table.SelectionBehavior.SelectRows)
            table.setSelectionMode(table.SelectionMode.SingleSelection)
            table.setAlternatingRowColors(True)
            table.setShowGrid(True)
            table.setEditTriggers(table.EditTrigger.NoEditTriggers)
            table.horizontalHeader().setStretchLastSection(True)
            table.verticalHeader().setVisible(False)  # Hide row numbers
            print("✓ Setup delivery table (tableWidget_6)")

    def show(self):
        """Show the delivery page"""
        self.main_window.stackedWidget.setCurrentIndex(
            self.main_window.Delivery_page_index
        )
        print("✓ Showing Delivery/Pickup page")