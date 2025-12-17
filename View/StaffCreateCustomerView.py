from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt


class SCreateCustomer:
    """Staff Create Customer view logic - works with the CreateCustomer page in stackedWidget"""

    def __init__(self, staff_home):
        self.staff_home = staff_home

        # Get reference to the CreateCustomer page in the stacked widget
        self.CreateCustomer_widget = self.staff_home.stackedWidget.widget(
            self.staff_home.CreateCustomer_page_index
        )

        self.setup_CreateCustomer_ui()

    def setup_CreateCustomer_ui(self):
        """Setup Create Customer page UI elements"""

        # Add title label with custom font
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]

            # Title for Create Customer page
            if hasattr(self.staff_home, "ok_5"):
                title = getattr(self.staff_home, "ok_5")
                title.setFont(QFont(family, 30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup fonts for section labels (Personal Information, Address)
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            section_labels = ["PI", "PI_2"]
            for name in section_labels:
                if hasattr(self.staff_home, name):
                    label = getattr(self.staff_home, name)
                    label.setFont(QFont(family, 13))
                    label.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup fonts for field labels
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            field_labels = [
                "label_18", "label_21", "label_22", "label_23", "label_24",  # Personal info
                "label_25", "label_37", "label_42", "label_43"  # Address info
            ]
            for name in field_labels:
                if hasattr(self.staff_home, name):
                    label = getattr(self.staff_home, name)
                    label.setFont(QFont(family, 9))
                    label.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup fonts for sidebar buttons
        side_buttons = [
            "Homebut_3", "Userbut_3", "Dashbut_3",
            "Orderbut_3", "Reportbut_3", "Settbut_3", "Delivlab_3"
        ]
        for name in side_buttons:
            if hasattr(self.staff_home, name):
                btn = getattr(self.staff_home, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup fonts for action buttons
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            action_buttons = ["crt_btn", "crt_btn_2"]
            for name in action_buttons:
                if hasattr(self.staff_home, name):
                    btn = getattr(self.staff_home, name)
                    btn.setFont(QFont(family, 10))
                    btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup input fields
        input_fields = [
            "lineEdit", "lineEdit_2", "lineEdit_3", "lineEdit_4", "lineEdit_5",
            "lineEdit_6", "lineEdit_7", "lineEdit_8", "lineEdit_9"
        ]
        for name in input_fields:
            if hasattr(self.staff_home, name):
                field = getattr(self.staff_home, name)
                field.setFont(QFont("Arial", 10))

    def show(self):
        """Show the Create Customer page"""
        self.staff_home.stackedWidget.setCurrentIndex(
            self.staff_home.CreateCustomer_page_index
        )