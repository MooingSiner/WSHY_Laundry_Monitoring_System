from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt


class CreateCustomer:
    """Dashboard view logic - works with the ADB page in stackedWidget"""

    def __init__(self, main_window):
        self.main_window = main_window

        # Get reference to the dashboard page (ADB) in the stacked widget
        self.CreateCustomer_widget = self.main_window.stackedWidget.widget(
            self.main_window.CreateCustomer_page_index
        )

        self.setup_CreateCustomer_ui()

    def setup_CreateCustomer_ui(self):
        """Setup dashboard-specific UI elements"""

        # Add "Dashboard" title label
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            if hasattr(self.main_window, "ok_8"):
                title= getattr(self.main_window, "ok_8")
                title.setFont(QFont(family,30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            # Check if title label already exists, if not create i

        # Setup fonts for dashboard buttons
        Pl_buttons = ["PI_3","PI_4"]
        for name in Pl_buttons:
            if hasattr(self.main_window, name):
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                name = getattr(self.main_window, name)
                name.setFont(QFont(family, 10))
                name.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        cs_buttons = ["label_42","label_43", "label_44", "label_49", "label_50", "label_51", "label_52","label_53","label_54"]
        for name in cs_buttons:
            if hasattr(self.main_window, name):
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                name = getattr(self.main_window, name)
                name.setFont(QFont(family, 8))
                name.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        side_buttons = ["Homebut_6", "Userbut_6", "Dashbut_6", "Orderbut_6","Reportbut_6", "Settbut_6"]
        for name in side_buttons:
            if hasattr(self.main_window, name):
                btn = getattr(self.main_window, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        click_buttons =["crt_btn_3","crt_btn_4"]
        for name in click_buttons:
            if hasattr(self.main_window, name):
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                btn = getattr(self.main_window, name)
                btn.setFont(QFont(family, 10))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def show(self):
        """Show the dashboard page"""
        self.main_window.stackedWidget.setCurrentIndex(
            self.main_window.CreateCustomer_page_index
        )