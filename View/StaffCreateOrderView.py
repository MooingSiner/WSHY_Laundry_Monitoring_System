from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontDatabase, QFont, QDoubleValidator
from PyQt6.QtCore import Qt


class CreateOrderManager:
    """Create Order view logic"""

    def __init__(self, staff_home):
        self.staff_home = staff_home

        self.create_order_widget = self.staff_home.stackedWidget.widget(
            self.staff_home.CreateOrder_page_index
        )
        self.setup_create_order_ui()

    def setup_create_order_ui(self):
        """Setup create order UI elements with proper fonts"""

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
        if hasattr(self.staff_home, "ok_8"):
            title = self.staff_home.ok_8
            title.setFont(QFont(fredoka_family, 30))
            title.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        else:
            print("Warning: ok_8 widget not found")

        # All labels with Fredoka
        fredoka_labels = [
            "servicesTitle", "summaryTitle", "fastDryPriceLabel",
            "washPriceLabel", "weightLabel", "quantityLabel",
            "summaryWashLabel", "summaryFastDryLabel", "summaryIronLabel",
            "summaryFoldLabel", "totalLabel","fastDryPriceLabel_3","fastDryPriceLabel_4"
        ]
        for label_name in fredoka_labels:
            if hasattr(self.staff_home, label_name):
                label = getattr(self.staff_home, label_name)
                label.setFont(QFont(fredoka_family, 9))
                label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            else:
                print(f"Warning: {label_name} widget not found")

        # Price display labels (slightly smaller)
        price_labels = [
            "summaryWashPrice", "summaryFastDryPrice",
            "summaryIronPrice", "summaryFoldPrice", "totalPrice"
        ]
        for label_name in price_labels:
            if hasattr(self.staff_home, label_name):
                label = getattr(self.staff_home, label_name)
                label.setFont(QFont(fredoka_family, 10))
            else:
                print(f"Warning: {label_name} widget not found")

        # Buttons with Fredoka
        fredoka_buttons = [
            "createOrderButton", "cancelButton",
            "fastDryCheckbox", "ironCheckbox", "foldCheckbox"
        ]
        for button_name in fredoka_buttons:
            if hasattr(self.staff_home, button_name):
                button = getattr(self.staff_home, button_name)
                button.setFont(QFont(fredoka_family, 10))
                button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            else:
                print(f"Warning: {button_name} widget not found")

        # Line edits and spinbox with Arial
        if hasattr(self.staff_home, "weightInput"):
            weight_input = self.staff_home.weightInput
            weight_input.setFont(QFont("Arial", 10))
            weight_input.setPlaceholderText("0.00")
            # Add validator for decimal numbers
            validator = QDoubleValidator(0.0, 999.99, 2)
            validator.setNotation(QDoubleValidator.Notation.StandardNotation)
            weight_input.setValidator(validator)
        else:
            print("Warning: weightInput widget not found")

        if hasattr(self.staff_home, "quantitySpinBox"):
            quantity_spin = self.staff_home.quantitySpinBox
            quantity_spin.setFont(QFont("Arial", 10))
        else:
            print("Warning: quantitySpinBox widget not found")

        # Sidebar buttons with Arial
        sidebar_buttons = [
            "Homebut_7", "Userbut_7", "Dashbut_7",
            "Orderbut_7", "Delivlab_7", "Reportbut_7", "Settbut_7"
        ]
        for name in sidebar_buttons:
            if hasattr(self.staff_home, name):
                btn = getattr(self.staff_home, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            else:
                print(f"Warning: {name} widget not found")

    def reset_form(self):
        """Reset form to default values"""
        if hasattr(self.staff_home, "weightInput"):
            self.staff_home.weightInput.clear()
        if hasattr(self.staff_home, "quantitySpinBox"):
            self.staff_home.quantitySpinBox.setValue(1)
        if hasattr(self.staff_home, "fastDryCheckbox"):
            self.staff_home.fastDryCheckbox.setChecked(False)
        if hasattr(self.staff_home, "ironCheckbox"):
            self.staff_home.ironCheckbox.setChecked(False)
        if hasattr(self.staff_home, "foldCheckbox"):
            self.staff_home.foldCheckbox.setChecked(False)

    def show(self):
        """Show the create order page"""
        self.reset_form()
        self.staff_home.stackedWidget.setCurrentIndex(
            self.staff_home.CreateOrder_page_index
        )