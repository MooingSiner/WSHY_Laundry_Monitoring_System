from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontDatabase, QFont, QDoubleValidator
from PyQt6.QtCore import Qt


class SEditOrder:
    """Staff Edit Order view logic - works with the EditOrder page in stackedWidget"""

    def __init__(self, main_window):
        self.main_window = main_window

        # Get reference to the EditOrder page in the stacked widget
        self.EditOrder_widget = self.main_window.stackedWidget.widget(
            self.main_window.EditOrder_page_index
        )

        self.setup_EditOrder_ui()

    def setup_EditOrder_ui(self):
        """Setup EditOrder-specific UI elements with proper fonts"""

        # Load Fredoka font
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")

        if font_id == -1:
            print("Warning: Could not load Fredoka-SemiBold.ttf font")
            fredoka_family = "Arial"  # Fallback
        else:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                fredoka_family = families[0]
                print(f"Successfully loaded font: {fredoka_family}")
            else:
                print("Warning: Font loaded but no family found")
                fredoka_family = "Arial"

        # Title with Fredoka
        if hasattr(self.main_window, "ok_9"):
            title = self.main_window.ok_9
            title.setFont(QFont(fredoka_family, 30))
            title.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        else:
            print("Warning: ok_9 widget not found")

        # All labels with Fredoka
        fredoka_labels = [
            "servicesTitle_2", "summaryTitle_2", "fastDryPriceLabel_2",
            "washPriceLabel_2", "weightLabel_2", "quantityLabel_2",
            "summaryWashLabel_2", "summaryFastDryLabel_2", "summaryIronLabel_2",
            "summaryFoldLabel_2", "totalLabel_2", "fastDryPriceLabel_5", "fastDryPriceLabel_6"
        ]
        for label_name in fredoka_labels:
            if hasattr(self.main_window, label_name):
                label = getattr(self.main_window, label_name)
                label.setFont(QFont(fredoka_family, 9))
                label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            else:
                print(f"Warning: {label_name} widget not found")

        # Price display labels (slightly smaller)
        price_labels = [
            "summaryWashPrice_2", "summaryFastDryPrice_2",
            "summaryIronPrice_2", "summaryFoldPrice_2", "totalPrice_2"
        ]
        for label_name in price_labels:
            if hasattr(self.main_window, label_name):
                label = getattr(self.main_window, label_name)
                label.setFont(QFont(fredoka_family, 10))
            else:
                print(f"Warning: {label_name} widget not found")

        # Buttons with Fredoka
        fredoka_buttons = [
            "createOrderButton_2", "cancelButton_2",
            "fastDryCheckbox_2", "ironCheckbox_2", "foldCheckbox_2"
        ]
        for button_name in fredoka_buttons:
            if hasattr(self.main_window, button_name):
                button = getattr(self.main_window, button_name)
                button.setFont(QFont(fredoka_family, 10))
                button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            else:
                print(f"Warning: {button_name} widget not found")

        # Line edits and spinbox with Arial
        if hasattr(self.main_window, "weightInput_2"):
            weight_input = self.main_window.weightInput_2
            weight_input.setFont(QFont("Arial", 10))
            weight_input.setPlaceholderText("0.00")
            # Add validator for decimal numbers
            validator = QDoubleValidator(0.0, 999.99, 2)
            validator.setNotation(QDoubleValidator.Notation.StandardNotation)
            weight_input.setValidator(validator)
        else:
            print("Warning: weightInput_2 widget not found")

        if hasattr(self.main_window, "quantitySpinBox_2"):
            quantity_spin = self.main_window.quantitySpinBox_2
            quantity_spin.setFont(QFont("Arial", 10))
        else:
            print("Warning: quantitySpinBox_2 widget not found")

        # Sidebar buttons with Arial
        sidebar_buttons = [
            "Homebut_10", "Userbut_10", "Dashbut_10",
            "Orderbut_10", "Delivlab_10", "Reportbut_10", "Settbut_10"
        ]
        for name in sidebar_buttons:
            if hasattr(self.main_window, name):
                btn = getattr(self.main_window, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            else:
                print(f"Warning: {name} widget not found")

    def reset_form(self):
        """Reset form to default values"""
        if hasattr(self.main_window, "weightInput_2"):
            self.main_window.weightInput_2.clear()
        if hasattr(self.main_window, "quantitySpinBox_2"):
            self.main_window.quantitySpinBox_2.setValue(1)
        if hasattr(self.main_window, "fastDryCheckbox_2"):
            self.main_window.fastDryCheckbox_2.setChecked(False)
        if hasattr(self.main_window, "ironCheckbox_2"):
            self.main_window.ironCheckbox_2.setChecked(False)
        if hasattr(self.main_window, "foldCheckbox_2"):
            self.main_window.foldCheckbox_2.setChecked(False)

    def show(self):
        """Show the EditOrder page"""
        self.reset_form()
        self.main_window.stackedWidget.setCurrentIndex(
            self.main_window.EditOrder_page_index
        )