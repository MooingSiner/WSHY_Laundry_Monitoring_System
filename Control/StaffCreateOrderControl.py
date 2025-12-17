from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QLabel


class CreateOrderControl:
    """Controller for Create Order page"""

    def __init__(self, staff_home, dashboard, customer, order,delivery, report, model, login_view, managerc_control=None, order_control=None):
        self.staff_home = staff_home
        self.dashboard = dashboard
        self.customer = customer
        self.order = order
        self.delivery = delivery
        self.report = report
        self.model = model
        self.login_view = login_view
        self.managerc_control = managerc_control  # Reference to customer manager controller
        self.order_control = order_control  # Reference to order controller (SOControl)

        # Staff ID from login session
        self.staff_id = None

        # Pre-selected customer (if coming from customer manager)
        self.selected_customer_id = None
        self.selected_customer_name = None

        # Pricing constants
        self.WASH_PRICE_PER_KG = 100.00
        self.FAST_DRY_PRICE_PER_KG = 140.00
        self.IRON_PRICE_PER_KG = 50.00
        self.FOLD_PRICE_PER_KG = 30.00

        # Connect UI elements
        self.connect_create_order_buttons()
        self.setup_service_listeners()

    def set_staff_id(self, staff_id):
        """Set the logged-in staff ID (called from LoginController)"""
        self.staff_id = staff_id
        print(f"✓ CreateOrderControl: Staff ID set to {staff_id}")

    def set_order_control(self, order_control):
        """Set reference to order controller for refreshing order list"""
        self.order_control = order_control
        print(f"✓ CreateOrderControl: Order control reference set")

    def set_selected_customer(self, customer_id, customer_name):
        """Set pre-selected customer (called from customer manager)"""
        self.selected_customer_id = customer_id
        self.selected_customer_name = customer_name
        print(f"✓ CreateOrder: Pre-selected customer: {customer_name} (ID: {customer_id})")

    def connect_create_order_buttons(self):
        """Connect all buttons on Create Order page"""

        # Sidebar navigation buttons (CreateOrder page uses _7 suffix)
        if hasattr(self.staff_home, "Homebut_7"):
            self.staff_home.Homebut_7.clicked.connect(self.go_to_home)
        if hasattr(self.staff_home, "Dashbut_7"):
            self.staff_home.Dashbut_7.clicked.connect(self.go_to_dashboard)
        if hasattr(self.staff_home, "Userbut_7"):
            self.staff_home.Userbut_7.clicked.connect(self.go_to_customers)
        if hasattr(self.staff_home, "Orderbut_7"):
            self.staff_home.Orderbut_7.clicked.connect(self.go_to_orders)
        if hasattr(self.staff_home, "Reportbut_7"):
            self.staff_home.Reportbut_7.clicked.connect(self.go_to_reports)
        if hasattr(self.staff_home, "Delivlab_7"):
            self.staff_home.Delivlab_7.clicked.connect(self.go_to_delivery)
        if hasattr(self.staff_home, "Settbut_7"):
            self.staff_home.Settbut_7.clicked.connect(self.go_to_logout)

        # Icon buttons
        if hasattr(self.staff_home, "h1_6"):
            self.staff_home.h1_6.clicked.connect(self.go_to_home)
        if hasattr(self.staff_home, "db1_6"):
            self.staff_home.db1_6.clicked.connect(self.go_to_dashboard)
        if hasattr(self.staff_home, "u1_6"):
            self.staff_home.u1_6.clicked.connect(self.go_to_customers)
        if hasattr(self.staff_home, "o1_6"):
            self.staff_home.o1_6.clicked.connect(self.go_to_orders)
        if hasattr(self.staff_home, "r1_6"):
            self.staff_home.r1_6.clicked.connect(self.go_to_reports)
        if hasattr(self.staff_home, "d1_6"):
            self.staff_home.d1_6.clicked.connect(self.go_to_delivery)
        if hasattr(self.staff_home, "s1_6"):
            self.staff_home.s1_6.clicked.connect(self.go_to_logout)

        # Action buttons
        if hasattr(self.staff_home, "createOrderButton"):
            self.staff_home.createOrderButton.clicked.connect(self.create_order)
        if hasattr(self.staff_home, "cancelButton"):
            self.staff_home.cancelButton.clicked.connect(self.cancel_order)

    def setup_service_listeners(self):
        """Setup listeners for service selection and calculation"""

        if hasattr(self.staff_home, "fastDryCheckbox"):
            self.staff_home.fastDryCheckbox.stateChanged.connect(self.calculate_total)
        if hasattr(self.staff_home, "ironCheckbox"):
            self.staff_home.ironCheckbox.stateChanged.connect(self.calculate_total)
        if hasattr(self.staff_home, "foldCheckbox"):
            self.staff_home.foldCheckbox.stateChanged.connect(self.calculate_total)

        # Weight input
        if hasattr(self.staff_home, "weightInput"):
            self.staff_home.weightInput.textChanged.connect(self.calculate_total)
        if hasattr(self.staff_home, "weightInput"):
            from PyQt6.QtGui import QDoubleValidator
            validator = QDoubleValidator(0.01, 7.00, 2)  # Min 0.01, Max 7.00, 2 decimals
            validator.setNotation(QDoubleValidator.Notation.StandardNotation)
            self.staff_home.weightInput.setValidator(validator)

        # Quantity spinbox
        if hasattr(self.staff_home, "quantitySpinBox"):
            self.staff_home.quantitySpinBox.valueChanged.connect(self.calculate_total)

    def calculate_total(self):
        """Calculate and update order total based on selected services"""
        try:
            # Get weight
            weight_text = self.staff_home.weightInput.text().strip()
            if not weight_text:
                weight = 0.0
            else:
                weight = float(weight_text)

                # ADDED: Real-time weight validation
                if weight > 7.00:
                    # Show visual indication (optional)
                    self.staff_home.weightInput.setStyleSheet("border: 1px solid red;")
                    # You could also disable the create button here
                    if hasattr(self.staff_home, "createOrderButton"):
                        self.staff_home.createOrderButton.setEnabled(False)
                else:
                    self.staff_home.weightInput.setStyleSheet("")  # Reset style
                    if hasattr(self.staff_home, "createOrderButton"):
                        self.staff_home.createOrderButton.setEnabled(True)

            # Get quantity
            quantity = self.staff_home.quantitySpinBox.value()

            # Calculate base wash price (always included)
            wash_total = self.WASH_PRICE_PER_KG * weight * quantity

            # Calculate additional services
            fast_dry_total = 0.0
            iron_total = 0.0
            fold_total = 0.0

            if self.staff_home.fastDryCheckbox.isChecked():
                fast_dry_total = self.FAST_DRY_PRICE_PER_KG * weight * quantity

            if self.staff_home.ironCheckbox.isChecked():
                iron_total = self.IRON_PRICE_PER_KG * weight * quantity

            if self.staff_home.foldCheckbox.isChecked():
                fold_total = self.FOLD_PRICE_PER_KG * weight * quantity

            # Calculate total
            total = wash_total + fast_dry_total + iron_total + fold_total

            # Update summary labels
            self.staff_home.summaryWashPrice.setText(f"₱{wash_total:.2f}")
            self.staff_home.summaryFastDryPrice.setText(f"₱{fast_dry_total:.2f}")
            self.staff_home.summaryIronPrice.setText(f"₱{iron_total:.2f}")
            self.staff_home.summaryFoldPrice.setText(f"₱{fold_total:.2f}")
            self.staff_home.totalPrice.setText(
                f'<html><head/><body><p align="right">'
                f'<span style="font-size:18px; font-weight:600; color:#3855DB;">'
                f'₱{total:.2f}</span></p></body></html>'
            )

        except ValueError:
            # Invalid weight input
            self.staff_home.summaryWashPrice.setText("₱0.00")
            self.staff_home.summaryFastDryPrice.setText("₱0.00")
            self.staff_home.summaryIronPrice.setText("₱0.00")
            self.staff_home.summaryFoldPrice.setText("₱0.00")
            self.staff_home.totalPrice.setText(
                f'<html><head/><body><p align="right">'
                f'<span style="font-size:18px; font-weight:600; color:#3855DB;">'
                f'₱0.00</span></p></body></html>'
            )

    def create_order(self):
        """Create a new order in the database"""

        # Validate inputs
        if not self.validate_order_input():
            return

        try:
            # Check if staff ID is set
            if not self.staff_id:
                QMessageBox.warning(
                    self.staff_home,
                    "Session Error",
                    "Staff ID not found. Please log out and log in again."
                )
                return

            # Get weight and quantity
            weight = float(self.staff_home.weightInput.text().strip())
            quantity = self.staff_home.quantitySpinBox.value()

            # Calculate totals
            wash_total = self.WASH_PRICE_PER_KG * weight * quantity
            fast_dry_total = (self.FAST_DRY_PRICE_PER_KG * weight * quantity
                              if self.staff_home.fastDryCheckbox.isChecked() else 0.0)
            iron_total = (self.IRON_PRICE_PER_KG * weight * quantity
                          if self.staff_home.ironCheckbox.isChecked() else 0.0)
            fold_total = (self.FOLD_PRICE_PER_KG * weight * quantity
                          if self.staff_home.foldCheckbox.isChecked() else 0.0)
            total_amount = wash_total + fast_dry_total + iron_total + fold_total

            # Check if customer is selected
            if not self.selected_customer_id:
                QMessageBox.warning(
                    self.staff_home,
                    "No Customer Selected",
                    "Please select a customer first.\n\nYou can select a customer from the Customer Manager page."
                )
                return

            customer_id = self.selected_customer_id

            # Create order in database
            order_id = self.model.create_order(
                customer_id=customer_id,
                staff_id=self.staff_id,
                total_amount=total_amount,
                status='Pending'  # Initially Pending, not Completed
            )

            if order_id:
                # Log activity
                self.model.log_staff_activity(
                    staff_id=self.staff_id,
                    activity_type='CREATE_ORDER',
                    order_id=order_id,
                    customer_id=customer_id
                )

                # Update last active timestamp
                self.model.update_staff_last_active(self.staff_id)

                print(f"✓ Order {order_id} created and activity logged for Staff ID {self.staff_id}")
            else:
                QMessageBox.critical(
                    self.staff_home,
                    "Error",
                    "Failed to create order in database."
                )
                return

            # Add order service details
            service_id = self.model.add_order_service(
                order_id=order_id,
                service_name="Laundry Service",
                weight_kg=weight,
                price_per_kg=self.WASH_PRICE_PER_KG,
                wash_amount=wash_total,
                fast_dry=self.staff_home.fastDryCheckbox.isChecked(),
                fast_dry_amount=fast_dry_total,
                iron_only=self.staff_home.ironCheckbox.isChecked(),
                iron_only_amount=iron_total,
                fold=self.staff_home.foldCheckbox.isChecked(),
                fold_amount=fold_total,
                total_amount=total_amount
            )

            if not service_id:
                QMessageBox.warning(
                    self.staff_home,
                    "Warning",
                    "Order created but failed to add service details."
                )

            # IMPORTANT: DO NOT CREATE TRANSACTION HERE
            # Transactions should only be created when payment is made
            # or when order is completed
            # This is why we fixed the Model.py to only count completed orders

            # Format order ID
            formatted_order_id = f"WSHY#{order_id:03d}"

            # Show success message
            QMessageBox.information(
                self.staff_home,
                "Success",
                f"Order {formatted_order_id} created successfully!\n\n"
                f"Customer: {self.selected_customer_name}\n"
                f"Staff ID: {self.staff_id}\n"
                f"Total Amount: ₱{total_amount:.2f}\n\n"
                f"Status: Pending (Transaction will be recorded when order is completed)"
            )

            print(f"✓ CreateOrder: Created order {formatted_order_id} by Staff ID {self.staff_id}")

            # Refresh order list immediately if order controller reference is available
            if self.order_control:
                try:
                    self.order_control.load_order_data()
                    print(f"✓ CreateOrder: Order list refreshed automatically")
                except Exception as e:
                    print(f"✗ CreateOrder: Failed to refresh order list: {e}")

            # Clear form
            self.clear_form()

            # Navigate to orders page
            self.go_to_orders()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.staff_home,
                "Error",
                f"An error occurred while creating the order:\n{str(e)}"
            )

    def validate_order_input(self):
        """Validate order input before submission"""

        # Check weight
        weight_text = self.staff_home.weightInput.text().strip()
        if not weight_text:
            QMessageBox.warning(
                self.staff_home,
                "Invalid Input",
                "Please enter the weight (kg)."
            )
            self.staff_home.weightInput.setFocus()
            return False

        try:
            weight = float(weight_text)
            if weight <= 0:
                QMessageBox.warning(
                    self.staff_home,
                    "Invalid Input",
                    "Weight must be greater than 0."
                )
                self.staff_home.weightInput.setFocus()
                return False
            if weight > 7.00:  # ADDED: Maximum weight limit
                QMessageBox.warning(
                    self.staff_home,
                    "Invalid Input",
                    "Weight must not exceed 7.00 kg."
                )
                self.staff_home.weightInput.setFocus()
                return False
        except ValueError:
            QMessageBox.warning(
                self.staff_home,
                "Invalid Input",
                "Please enter a valid number for weight."
            )
            self.staff_home.weightInput.setFocus()
            return False

        # Check quantity
        quantity = self.staff_home.quantitySpinBox.value()
        if quantity <= 0:
            QMessageBox.warning(
                self.staff_home,
                "Invalid Input",
                "Quantity must be at least 1."
            )
            return False

        return True

    def clear_form(self):
        """Clear all form inputs"""
        self.staff_home.weightInput.clear()
        self.staff_home.quantitySpinBox.setValue(1)
        self.staff_home.fastDryCheckbox.setChecked(False)
        self.staff_home.ironCheckbox.setChecked(False)
        self.staff_home.foldCheckbox.setChecked(False)

        # Clear selected customer
        self.selected_customer_id = None
        self.selected_customer_name = None

        # Reset summary
        self.calculate_total()

    def cancel_order(self):
        """Cancel order creation and return to previous page"""
        reply = QMessageBox.question(
            self.staff_home,
            "Cancel Order",
            "Are you sure you want to cancel?\n\nAll entered data will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.clear_form()
            self.go_to_customers()  # Go back to customer page

    # ==================== NAVIGATION METHODS ====================

    def go_to_home(self):
        print("CreateOrder: Navigating to Home")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.home_page_index)

    def go_to_dashboard(self):
        print("CreateOrder: Navigating to Dashboard")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.dashboard_page_index)

    def go_to_customers(self):
        print("CreateOrder: Navigating to Customers")
        if self.managerc_control:
            self.managerc_control.load_customer_data()  # Refresh customer list
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.customer_page_index)

    def go_to_orders(self):
        print("CreateOrder: Navigating to Orders")
        # Refresh order list when navigating to orders page
        if self.order_control:
            try:
                self.order_control.load_order_data()
                print(f"✓ CreateOrder: Order list refreshed on navigation")
            except Exception as e:
                print(f"✗ CreateOrder: Failed to refresh order list: {e}")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.order_page_index)

    def go_to_reports(self):
        print("CreateOrder: Navigating to Reports")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.History_page_index)

    def go_to_delivery(self):
        print("CreateOrder: Navigating to Delivery")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.Delivery_page_index)

    def go_to_logout(self):
        """Logout with confirmation"""
        reply = QMessageBox.question(
            self.staff_home,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print("CreateOrder: Logging out...")
            # Clear any sensitive data
            self.clear_form()
            self.staff_id = None
            # Close staff home
            self.staff_home.close()
            # Clear login fields
            if hasattr(self.login_view, 'username'):
                self.login_view.username.clear()
            if hasattr(self.login_view, 'password'):
                self.login_view.password.clear()
            # Show login view
            self.login_view.show()
            if hasattr(self.login_view, 'username'):
                self.login_view.username.setFocus()