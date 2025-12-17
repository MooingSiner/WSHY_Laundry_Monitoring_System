from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt


class SEditCustomer:
    """Staff Edit Customer view logic - works with the EditCustomer page in stackedWidget"""

    def __init__(self, main_window):
        self.main_window = main_window

        # Get reference to the EditCustomer page in the stacked widget
        self.EditCustomer_widget = self.main_window.stackedWidget.widget(
            self.main_window.EditCustomer_page_index
        )

        self.setup_EditCustomer_ui()

    def setup_EditCustomer_ui(self):
        """Setup EditCustomer-specific UI elements"""

        # Add "Edit Customer" title label
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]

            # Title
            if hasattr(self.main_window, "ok_10"):
                title = getattr(self.main_window, "ok_10")
                title.setText("Edit Customer")
                title.setFont(QFont(family, 30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Section labels (Personal Information, Address)
            section_labels = ["PI_7", "PI_8"]
            for name in section_labels:
                if hasattr(self.main_window, name):
                    lbl = getattr(self.main_window, name)
                    lbl.setFont(QFont(family, 10))
                    lbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Field labels
            field_labels = ["label_68", "label_72", "label_70", "label_65", "label_73",
                            "label_66", "label_67", "label_69", "label_71"]
            for name in field_labels:
                if hasattr(self.main_window, name):
                    lbl = getattr(self.main_window, name)
                    lbl.setFont(QFont(family, 8))
                    lbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Action buttons
            action_buttons = ["crt_btn_7", "crt_btn_8"]
            for name in action_buttons:
                if hasattr(self.main_window, name):
                    btn = getattr(self.main_window, name)
                    btn.setFont(QFont(family, 10))
                    btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Sidebar buttons - EditCustomer page uses _8 suffix
        side_buttons = ["Homebut_8", "Userbut_8", "Dashbut_8", "Orderbut_8",
                        "Reportbut_8", "Delivlab_8", "Settbut_8"]
        for name in side_buttons:
            if hasattr(self.main_window, name):
                btn = getattr(self.main_window, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def show(self):
        """Show the EditCustomer page"""
        self.main_window.stackedWidget.setCurrentIndex(
            self.main_window.EditCustomer_page_index
        )