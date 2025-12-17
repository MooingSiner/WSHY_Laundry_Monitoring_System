from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt


class EditStaff:
    """Dashboard view logic - works with the ADB page in stackedWidget"""

    def __init__(self, main_window):
        self.main_window = main_window

        # Get reference to the dashboard page (ADB) in the stacked widget
        self.EditStaff_widget = self.main_window.stackedWidget.widget(
            self.main_window.EditStaff_page_index
        )

        self.setup_EditStaff_ui()

    def setup_EditStaff_ui(self):
        """Setup dashboard-specific UI elements"""

        # Add "Dashboard" title label
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            if hasattr(self.main_window, "ok_9"):
                title= getattr(self.main_window, "ok_9")
                title.setFont(QFont(family,30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            # Check if title label already exists, if not create i

        # Setup fonts for dashboard buttons
        Pl_buttons = ["PI_5","PI_6"]
        for name in Pl_buttons:
            if hasattr(self.main_window, name):
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                name = getattr(self.main_window, name)
                name.setFont(QFont(family, 10))
                name.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        cs_buttons = ["label_58","label_59", "label_60", "label_61", "label_62", "label_63", "label_64"]
        for name in cs_buttons:
            if hasattr(self.main_window, name):
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                name = getattr(self.main_window, name)
                name.setFont(QFont(family, 8))
                name.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        side_buttons = ["Homebut_10", "Userbut_10", "Dashbut_10", "Orderbut_10","Reportbut_10", "Settbut_10"]
        for name in side_buttons:
            if hasattr(self.main_window, name):
                btn = getattr(self.main_window, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        click_buttons =["crt_btn_5","crt_btn_6"]
        for name in click_buttons:
            if hasattr(self.main_window, name):
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                btn = getattr(self.main_window, name)
                btn.setFont(QFont(family, 10))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def show(self):
        """Show the dashboard page"""
        self.main_window.stackedWidget.setCurrentIndex(
            self.main_window.EditStaff_page_index
        )