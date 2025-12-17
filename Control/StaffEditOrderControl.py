from PyQt6.QtWidgets import QMessageBox
from decimal import Decimal


class SEditOrderControl:
    """Controller for Staff Edit Order page"""

    def __init__(self, staff_home, dashboard, customer, order, delivery, report, model, login_view,
                 managerc_control=None, order_control=None):
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

        # Current order being edited
        self.current_order_id = None
        self.current_service_id = None
        self.staff_id = None

        # Pricing constants (matching CreateOrderControl)
        self.WASH_PRICE_PER_KG = 100.00
        self.FAST_DRY_PRICE_PER_KG = 140.00
        self.IRON_PRICE_PER_KG = 50.00
        self.FOLD_PRICE_PER_KG = 30.00

        # Connect UI elements
        self.connect_editorder_buttons()
        self.setup_service_listeners()

    def set_staff_id(self, staff_id):
        """Set the logged-in staff ID (called from LoginController)"""
        self.staff_id = staff_id
        print(f"✓ EditOrderControl: Staff ID set to {staff_id}")

    def set_order_control(self, order_control):
        """Set reference to order controller for refreshing order list"""
        self.order_control = order_control
        print(f"✓ EditOrderControl: Order control reference set")

    def connect_editorder_buttons(self):
        """Connect all buttons on Edit Order page"""

        # Sidebar navigation buttons (EditOrder page uses _10 suffix)
        if hasattr(self.staff_home, "Homebut_10"):
            self.staff_home.Homebut_10.clicked.connect(self.go_to_home)
        if hasattr(self.staff_home, "Dashbut_10"):
            self.staff_home.Dashbut_10.clicked.connect(self.go_to_dashboard)
        if hasattr(self.staff_home, "Userbut_10"):
            self.staff_home.Userbut_10.clicked.connect(self.go_to_customers)
        if hasattr(self.staff_home, "Orderbut_10"):
            self.staff_home.Orderbut_10.clicked.connect(self.go_to_orders)
        if hasattr(self.staff_home, "Reportbut_10"):
            self.staff_home.Reportbut_10.clicked.connect(self.go_to_reports)
        if hasattr(self.staff_home, "Delivlab_10"):
            self.staff_home.Delivlab_10.clicked.connect(self.go_to_delivery)
        if hasattr(self.staff_home, "Settbut_10"):
            self.staff_home.Settbut_10.clicked.connect(self.go_to_logout)

        # Icon buttons (EditOrder page uses _8 suffix)
        if hasattr(self.staff_home, "h1_8"):
            self.staff_home.h1_8.clicked.connect(self.go_to_home)
        if hasattr(self.staff_home, "db1_8"):
            self.staff_home.db1_8.clicked.connect(self.go_to_dashboard)
        if hasattr(self.staff_home, "u1_8"):
            self.staff_home.u1_8.clicked.connect(self.go_to_customers)
        if hasattr(self.staff_home, "o1_8"):
            self.staff_home.o1_8.clicked.connect(self.go_to_orders)
        if hasattr(self.staff_home, "r1_8"):
            self.staff_home.r1_8.clicked.connect(self.go_to_reports)
        if hasattr(self.staff_home, "d1_8"):
            self.staff_home.d1_8.clicked.connect(self.go_to_delivery)
        if hasattr(self.staff_home, "s1_8"):
            self.staff_home.s1_8.clicked.connect(self.go_to_logout)

        # Action buttons
        if hasattr(self.staff_home, "createOrderButton_2"):
            self.staff_home.createOrderButton_2.clicked.connect(self.update_order)
        if hasattr(self.staff_home, "cancelButton_2"):
            self.staff_home.cancelButton_2.clicked.connect(self.cancel_edit)

    def setup_service_listeners(self):
        """Setup listeners for service selection and calculation"""

        if hasattr(self.staff_home, "fastDryCheckbox_2"):
            self.staff_home.fastDryCheckbox_2.stateChanged.connect(self.calculate_total)
        if hasattr(self.staff_home, "ironCheckbox_2"):
            self.staff_home.ironCheckbox_2.stateChanged.connect(self.calculate_total)
        if hasattr(self.staff_home, "foldCheckbox_2"):
            self.staff_home.foldCheckbox_2.stateChanged.connect(self.calculate_total)

        # Weight input
        if hasattr(self.staff_home, "weightInput_2"):
            self.staff_home.weightInput_2.textChanged.connect(self.calculate_total)

        # Quantity spinbox
        if hasattr(self.staff_home, "quantitySpinBox_2"):
            self.staff_home.quantitySpinBox_2.valueChanged.connect(self.calculate_total)

    def calculate_total(self):
        """Calculate and update order total based on selected services"""
        try:
            # Get weight
            weight_text = self.staff_home.weightInput_2.text().strip()
            if not weight_text:
                weight = 0.0
            else:
                weight = float(weight_text)

                # ADDED: Real-time weight validation
                if weight > 7.00:
                    # Show visual indication (optional)
                    self.staff_home.weightInput_2.setStyleSheet("border: 1px solid red;")
                    # You could also disable the update button here
                    if hasattr(self.staff_home, "createOrderButton_2"):
                        self.staff_home.createOrderButton_2.setEnabled(False)
                else:
                    self.staff_home.weightInput_2.setStyleSheet("")  # Reset style
                    if hasattr(self.staff_home, "createOrderButton_2"):
                        self.staff_home.createOrderButton_2.setEnabled(True)

            # Get quantity
            quantity = self.staff_home.quantitySpinBox_2.value()

            # Calculate base wash price (always included)
            wash_total = self.WASH_PRICE_PER_KG * weight * quantity

            # Calculate additional services
            fast_dry_total = 0.0
            iron_total = 0.0
            fold_total = 0.0

            if self.staff_home.fastDryCheckbox_2.isChecked():
                fast_dry_total = self.FAST_DRY_PRICE_PER_KG * weight * quantity

            if self.staff_home.ironCheckbox_2.isChecked():
                iron_total = self.IRON_PRICE_PER_KG * weight * quantity

            if self.staff_home.foldCheckbox_2.isChecked():
                fold_total = self.FOLD_PRICE_PER_KG * weight * quantity

            # Calculate total
            total = wash_total + fast_dry_total + iron_total + fold_total

            # Update summary labels
            self.staff_home.summaryWashPrice_2.setText(f"₱{wash_total:.2f}")
            self.staff_home.summaryFastDryPrice_2.setText(f"₱{fast_dry_total:.2f}")
            self.staff_home.summaryIronPrice_2.setText(f"₱{iron_total:.2f}")
            self.staff_home.summaryFoldPrice_2.setText(f"₱{fold_total:.2f}")
            self.staff_home.totalPrice_2.setText(
                f'<html><head/><body><p align="right">'
                f'<span style="font-size:18px; font-weight:600; color:#3855DB;">'
                f'₱{total:.2f}</span></p></body></html>'
            )

        except ValueError:
            # Invalid weight input
            self.staff_home.summaryWashPrice_2.setText("₱0.00")
            self.staff_home.summaryFastDryPrice_2.setText("₱0.00")
            self.staff_home.summaryIronPrice_2.setText("₱0.00")
            self.staff_home.summaryFoldPrice_2.setText("₱0.00")
            self.staff_home.totalPrice_2.setText(
                f'<html><head/><body><p align="right">'
                f'<span style="font-size:18px; font-weight:600; color:#3855DB;">'
                f'₱0.00</span></p></body></html>'
            )

    def load_order_data(self, order_id):
        """Load order data into the form fields"""
        try:
            # Get order details
            order = self.model.get_order_by_id(order_id)

            if not order:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "Could not load order data."
                )
                return False

            # CHECK ORDER STATUS FIRST - Block edit if Processing or Completed
            order_status = order.get('Status', '')
            if order_status in ["Completed", "Processing"]:
                QMessageBox.warning(
                    self.staff_home,
                    "Cannot Edit Order",
                    f"Orders with '{order_status}' status cannot be edited.\n\n"
                    f"Only orders with 'Pending' status can be modified."
                )
                print(f"✗ Edit blocked - Order #{order_id} has status: {order_status}")
                return False

            # Store current order ID
            self.current_order_id = order_id

            # Get first service (assuming one service per order for simplicity)
            services = order.get('services', [])
            if not services:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "No services found for this order."
                )
                return False

            service = services[0]
            self.current_service_id = service.get('OrderServiceID')

            # Load weight
            if hasattr(self.staff_home, "weightInput_2"):
                weight = service.get('WeightKg', 0)
                self.staff_home.weightInput_2.setText(str(weight))
            if hasattr(self.staff_home, "weightInput_2"):
                from PyQt6.QtGui import QDoubleValidator
                validator = QDoubleValidator(0.01, 7.00, 2)  # Min 0.01, Max 7.00, 2 decimals
                validator.setNotation(QDoubleValidator.Notation.StandardNotation)
                self.staff_home.weightInput_2.setValidator(validator)

            # Load quantity
            if hasattr(self.staff_home, "quantitySpinBox_2"):
                # Quantity is typically 1 for laundry services
                self.staff_home.quantitySpinBox_2.setValue(1)

            # Load service checkboxes
            if hasattr(self.staff_home, "fastDryCheckbox_2"):
                fast_dry = service.get('FastDry', 0) == 1
                self.staff_home.fastDryCheckbox_2.setChecked(fast_dry)

            if hasattr(self.staff_home, "ironCheckbox_2"):
                iron_only = service.get('IronOnly', 0) == 1
                self.staff_home.ironCheckbox_2.setChecked(iron_only)

            if hasattr(self.staff_home, "foldCheckbox_2"):
                fold = service.get('Fold', 0) == 1
                self.staff_home.foldCheckbox_2.setChecked(fold)

            # Update summary
            self.calculate_total()

            print(f"✓ EditOrderControl: Loaded order data for Order #{order_id}")
            return True

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.staff_home,
                "Error",
                f"Failed to load order data:\n{str(e)}"
            )
            return False

    def update_order(self):
        """Update the order in the database"""
        # Validate inputs
        if not self.validate_order_input():
            return

        try:
            if not self.current_order_id or not self.current_service_id:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "No order selected for editing."
                )
                return

            # Check if staff ID is set
            if not self.staff_id:
                QMessageBox.warning(
                    self.staff_home,
                    "Session Error",
                    "Staff ID not found. Please log out and log in again."
                )
                return

            # Double-check order status before allowing update (backup validation)
            order = self.model.get_order_by_id(self.current_order_id)
            if order:
                order_status = order.get('Status', '')
                if order_status in ["Completed", "Processing"]:
                    QMessageBox.warning(
                        self.staff_home,
                        "Cannot Update Order",
                        f"Orders with '{order_status}' status cannot be updated.\n\n"
                        f"Only orders with 'Pending' status can be modified."
                    )
                    print(f"✗ Update blocked - Order #{self.current_order_id} has status: {order_status}")
                    # Go back to orders page
                    self.clear_form()
                    self.go_to_orders()
                    return

            # Get weight and quantity
            weight = float(self.staff_home.weightInput_2.text().strip())
            quantity = self.staff_home.quantitySpinBox_2.value()

            # Calculate totals
            wash_total = self.WASH_PRICE_PER_KG * weight * quantity
            fast_dry_total = (self.FAST_DRY_PRICE_PER_KG * weight * quantity
                              if self.staff_home.fastDryCheckbox_2.isChecked() else 0.0)
            iron_total = (self.IRON_PRICE_PER_KG * weight * quantity
                          if self.staff_home.ironCheckbox_2.isChecked() else 0.0)
            fold_total = (self.FOLD_PRICE_PER_KG * weight * quantity
                          if self.staff_home.foldCheckbox_2.isChecked() else 0.0)
            total_amount = wash_total + fast_dry_total + iron_total + fold_total

            # Get service selections as binary
            fast_dry = 1 if self.staff_home.fastDryCheckbox_2.isChecked() else 0
            iron_only = 1 if self.staff_home.ironCheckbox_2.isChecked() else 0
            fold = 1 if self.staff_home.foldCheckbox_2.isChecked() else 0

            # Update order service in database
            try:
                cursor = self.model.conn.cursor()
                query = """
                        UPDATE OrderService
                        SET WeightKg       = %s,
                            PriceperKG     = %s,
                            WashAmount     = %s,
                            FastDry        = %s,
                            FastDryAmount  = %s,
                            IronOnly       = %s,
                            IronOnlyAmount = %s,
                            Fold           = %s,
                            FoldAmount     = %s,
                            TotalAmount    = %s
                        WHERE OrderServiceID = %s \
                        """
                cursor.execute(query, (
                    weight,
                    self.WASH_PRICE_PER_KG,
                    wash_total,
                    fast_dry,
                    fast_dry_total,
                    iron_only,
                    iron_total,
                    fold,
                    fold_total,
                    total_amount,
                    self.current_service_id
                ))

                # Update order total amount
                cursor.execute("""
                               UPDATE Orders
                               SET TotalAmount = %s
                               WHERE OrderID = %s
                               """, (total_amount, self.current_order_id))

                # Log activity
                cursor.execute("""
                               INSERT INTO StaffActivityLog
                                   (StaffID, ActivityType, OrderID, ActivityTime)
                               VALUES (%s, %s, %s, NOW())
                               """, (self.staff_id, 'EDIT_ORDER', self.current_order_id))

                # UPDATE LAST ACTIVE TIMESTAMP
                cursor.execute("""
                               UPDATE Staff
                               SET LastActiveAt = NOW()
                               WHERE StaffID = %s
                               """, (self.staff_id,))

                self.model.conn.commit()
                cursor.close()

                # Format order ID
                formatted_order_id = f"WSHY#{self.current_order_id:03d}"

                # Show success message
                QMessageBox.information(
                    self.staff_home,
                    "Success",
                    f"Order {formatted_order_id} updated successfully!\n\n"
                    f"Staff ID: {self.staff_id}\n"
                    f"Total Amount: ₱{total_amount:.2f}"
                )

                print(f"✓ EditOrder: Updated order {formatted_order_id} by Staff ID {self.staff_id}")

                # Refresh order list immediately if order controller reference is available
                if self.order_control:
                    try:
                        self.order_control.load_order_data()
                        print(f"✓ EditOrder: Order list refreshed automatically")
                    except Exception as e:
                        print(f"✗ EditOrder: Failed to refresh order list: {e}")

                # Clear form
                self.clear_form()

                # Navigate to orders page
                self.go_to_orders()

            except Exception as e:
                self.model.conn.rollback()
                raise e

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.staff_home,
                "Error",
                f"An error occurred while updating the order:\n{str(e)}"
            )

    def validate_order_input(self):
        """Validate order input before submission"""

        # Check weight
        weight_text = self.staff_home.weightInput_2.text().strip()
        if not weight_text:
            QMessageBox.warning(
                self.staff_home,
                "Invalid Input",
                "Please enter the weight (kg)."
            )
            self.staff_home.weightInput_2.setFocus()
            return False

        try:
            weight = float(weight_text)
            if weight <= 0:
                QMessageBox.warning(
                    self.staff_home,
                    "Invalid Input",
                    "Weight must be greater than 0."
                )
                self.staff_home.weightInput_2.setFocus()
                return False
            if weight > 7.00:  # ADDED: Maximum weight limit
                QMessageBox.warning(
                    self.staff_home,
                    "Invalid Input",
                    "Weight must not exceed 7.00 kg."
                )
                self.staff_home.weightInput_2.setFocus()
                return False
        except ValueError:
            QMessageBox.warning(
                self.staff_home,
                "Invalid Input",
                "Please enter a valid number for weight."
            )
            self.staff_home.weightInput_2.setFocus()
            return False

        # Check quantity
        quantity = self.staff_home.quantitySpinBox_2.value()
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
        self.staff_home.weightInput_2.clear()
        self.staff_home.quantitySpinBox_2.setValue(1)
        self.staff_home.fastDryCheckbox_2.setChecked(False)
        self.staff_home.ironCheckbox_2.setChecked(False)
        self.staff_home.foldCheckbox_2.setChecked(False)

        # Reset summary
        self.calculate_total()

        # Reset IDs
        self.current_order_id = None
        self.current_service_id = None

    def cancel_edit(self):
        """Cancel order editing and return to previous page"""
        reply = QMessageBox.question(
            self.staff_home,
            "Cancel Edit",
            "Are you sure you want to cancel?\n\nAll changes will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.clear_form()
            self.go_to_orders()  # Go back to orders page

    # ==================== NAVIGATION METHODS ====================

    def go_to_home(self):
        print("EditOrder: Navigating to Home")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.home_page_index)

    def go_to_dashboard(self):
        print("EditOrder: Navigating to Dashboard")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.dashboard_page_index)

    def go_to_customers(self):
        print("EditOrder: Navigating to Customers")
        if self.managerc_control:
            self.managerc_control.load_customer_data()  # Refresh customer list
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.customer_page_index)

    def go_to_orders(self):
        print("EditOrder: Navigating to Orders")
        # Refresh order list when navigating to orders page
        if self.order_control:
            try:
                self.order_control.load_order_data()
                print(f"✓ EditOrder: Order list refreshed on navigation")
            except Exception as e:
                print(f"✗ EditOrder: Failed to refresh order list: {e}")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.order_page_index)

    def go_to_reports(self):
        print("EditOrder: Navigating to Reports")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.History_page_index)

    def go_to_delivery(self):
        print("EditOrder: Navigating to Delivery")
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
            print("EditOrder: Logging out...")
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