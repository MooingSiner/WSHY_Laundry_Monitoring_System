from PyQt6.QtWidgets import QMessageBox


class SEditCustomerControl:
    """Controller for Staff Edit Customer page"""

    def __init__(self, model, staff_home, dashboard,customer, order,delivery, report, login_view):
        self.staff_home = staff_home
        self.dashboard = dashboard
        self.customer = customer
        self.model = model
        self.order = order
        self.delivery = delivery
        self.report = report
        self.login_view = login_view

        # Store current customer being edited
        self.current_customer_id = None
        self.current_address_id = None
        self.staff_id = None
        # Reference to customer manager controller (will be set later)
        self.managerc_control = None

        # Connect buttons
        self.connect_editcustomer_buttons()

    def connect_editcustomer_buttons(self):
        """Connect navigation and action buttons on the Edit Customer page"""

        # Sidebar buttons - EditCustomer page uses _8 suffix
        if hasattr(self.staff_home, "Homebut_8"):
            self.staff_home.Homebut_8.clicked.connect(self.go_to_home)

        if hasattr(self.staff_home, "Dashbut_8"):
            self.staff_home.Dashbut_8.clicked.connect(self.go_to_dashboard)

        if hasattr(self.staff_home, "Userbut_8"):
            self.staff_home.Userbut_8.clicked.connect(self.go_to_customers)

        if hasattr(self.staff_home, "Orderbut_8"):
            self.staff_home.Orderbut_8.clicked.connect(self.go_to_orders)

        if hasattr(self.staff_home, "Reportbut_8"):
            self.staff_home.Reportbut_8.clicked.connect(self.go_to_reports)

        if hasattr(self.staff_home, "Delivlab_8"):
            self.staff_home.Delivlab_8.clicked.connect(self.go_to_delivery)

        if hasattr(self.staff_home, "Settbut_8"):
            self.staff_home.Settbut_8.clicked.connect(self.go_to_logout)

        # Icon buttons - EditCustomer page uses _2 suffix
        if hasattr(self.staff_home, "h2_2"):
            self.staff_home.h2_2.clicked.connect(self.go_to_home)

        if hasattr(self.staff_home, "db2_2"):
            self.staff_home.db2_2.clicked.connect(self.go_to_dashboard)

        if hasattr(self.staff_home, "u2_2"):
            self.staff_home.u2_2.clicked.connect(self.go_to_customers)

        if hasattr(self.staff_home, "s2_2"):
            self.staff_home.s2_2.clicked.connect(self.go_to_logout)

        if hasattr(self.staff_home, "o2_2"):
            self.staff_home.o2_2.clicked.connect(self.go_to_orders)

        if hasattr(self.staff_home, "r2_2"):
            self.staff_home.r2_2.clicked.connect(self.go_to_reports)

        if hasattr(self.staff_home, "d2_2"):
            self.staff_home.d2_2.clicked.connect(self.go_to_delivery)

        # Action buttons
        if hasattr(self.staff_home, "crt_btn_7"):
            self.staff_home.crt_btn_7.clicked.connect(self.update_customer_data)

        if hasattr(self.staff_home, "crt_btn_8"):
            self.staff_home.crt_btn_8.clicked.connect(self.cancel_edit)

    def load_customer_data(self, customer_id):
        """Load customer data into the form fields"""
        try:
            # Get customer data from database
            customer = self.model.get_customer_by_id(customer_id)

            if not customer:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "Could not load customer data."
                )
                return False

            # Store current customer ID
            self.current_customer_id = customer_id

            # Load Personal Information
            if hasattr(self.staff_home, "lineEdit_25"):
                self.staff_home.lineEdit_25.setText(customer.get('CFName', ''))

            if hasattr(self.staff_home, "lineEdit_24"):
                self.staff_home.lineEdit_24.setText(customer.get('CMName', '') or '')

            if hasattr(self.staff_home, "lineEdit_30"):
                self.staff_home.lineEdit_30.setText(customer.get('CLName', ''))

            if hasattr(self.staff_home, "lineEdit_32"):
                self.staff_home.lineEdit_32.setText(customer.get('CEmail', '') or '')

            if hasattr(self.staff_home, "lineEdit_27"):
                self.staff_home.lineEdit_27.setText(customer.get('CPhone', '') or '')

            # Load Address Information (get first address)
            addresses = self.model.get_customer_addresses(customer_id)
            if addresses and len(addresses) > 0:
                address = addresses[0]  # Use first address
                self.current_address_id = address.get('AddID')

                if hasattr(self.staff_home, "lineEdit_31"):
                    self.staff_home.lineEdit_31.setText(address.get('StreetAdd', '') or '')

                if hasattr(self.staff_home, "lineEdit_26"):
                    self.staff_home.lineEdit_26.setText(address.get('AppartUnit', '') or '')

                if hasattr(self.staff_home, "lineEdit_29"):
                    self.staff_home.lineEdit_29.setText(address.get('City', '') or '')

                if hasattr(self.staff_home, "lineEdit_28"):
                    self.staff_home.lineEdit_28.setText(address.get('ZipCode', '') or '')
            else:
                # Clear address fields if no address exists
                self.current_address_id = None
                if hasattr(self.staff_home, "lineEdit_31"):
                    self.staff_home.lineEdit_31.clear()
                if hasattr(self.staff_home, "lineEdit_26"):
                    self.staff_home.lineEdit_26.clear()
                if hasattr(self.staff_home, "lineEdit_29"):
                    self.staff_home.lineEdit_29.clear()
                if hasattr(self.staff_home, "lineEdit_28"):
                    self.staff_home.lineEdit_28.clear()

            print(f"✓ Staff: Loaded customer data for CustomerID: {customer_id}")
            return True

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.staff_home,
                "Error",
                f"Failed to load customer data:\n{str(e)}"
            )
            return False

    def set_staff_id(self, staff_id):
        """Set the logged-in staff ID (called from LoginController)"""
        self.staff_id = staff_id
        print(f"✓ SEditCustomerControl: Staff ID set to {staff_id}")

    def update_customer_data(self):
        """Update customer information in the database"""
        try:
            if not self.current_customer_id:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "No customer selected for editing."
                )
                return

            # Get form data - Personal Information
            fname = self.staff_home.lineEdit_25.text().strip() if hasattr(self.staff_home, "lineEdit_25") else ""
            mname = self.staff_home.lineEdit_24.text().strip() if hasattr(self.staff_home, "lineEdit_24") else ""
            lname = self.staff_home.lineEdit_30.text().strip() if hasattr(self.staff_home, "lineEdit_30") else ""
            email = self.staff_home.lineEdit_32.text().strip() if hasattr(self.staff_home, "lineEdit_32") else ""
            phone = self.staff_home.lineEdit_27.text().strip() if hasattr(self.staff_home, "lineEdit_27") else ""

            # Get form data - Address
            street = self.staff_home.lineEdit_31.text().strip() if hasattr(self.staff_home, "lineEdit_31") else ""
            unit = self.staff_home.lineEdit_26.text().strip() if hasattr(self.staff_home, "lineEdit_26") else ""
            city = self.staff_home.lineEdit_29.text().strip() if hasattr(self.staff_home, "lineEdit_29") else ""
            zipcode = self.staff_home.lineEdit_28.text().strip() if hasattr(self.staff_home, "lineEdit_28") else ""

            # Validate required fields
            if not fname or not lname:
                QMessageBox.warning(
                    self.staff_home,
                    "Validation Error",
                    "First Name and Last Name are required."
                )
                return

            # Update customer information
            success = self.model.update_customer(
                self.current_customer_id,
                fname, mname, lname, email, phone
            )

            if not success:
                QMessageBox.critical(
                    self.staff_home,
                    "Error",
                    "Failed to update customer information."
                )
                return

            # Update or create address
            if self.current_address_id:
                # Update existing address
                address_success = self.model.update_customer_address(
                    self.current_address_id,
                    street, unit, city, zipcode
                )
                if not address_success:
                    QMessageBox.warning(
                        self.staff_home,
                        "Warning",
                        "Customer updated but address update failed."
                    )
            elif street or unit or city or zipcode:
                # Create new address if any address field has data
                new_address_id = self.model.add_customer_address(
                    self.current_customer_id,
                    street, unit, city, zipcode
                )
                if new_address_id:
                    self.current_address_id = new_address_id
                    print(f"✓ Staff: Created new address with ID: {new_address_id}")

            # Log activity
            if self.staff_id:
                self.model.log_staff_activity(
                    staff_id=self.staff_id,
                    activity_type='EDIT_CUSTOMER',
                    customer_id=self.current_customer_id
                )

                # UPDATE LAST ACTIVE TIMESTAMP
                self.model.update_staff_last_active(self.staff_id)
                print(f"✓ Updated LastActiveAt for StaffID {self.staff_id} after editing customer")

            QMessageBox.information(
                self.staff_home,
                "Success",
                f"Customer '{fname} {lname}' updated successfully!"
            )

            # Reload customer manager data if available
            if self.managerc_control:
                self.managerc_control.load_customer_data()

            # Navigate back to customer manager
            self.go_to_customers()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.staff_home,
                "Error",
                f"An error occurred while updating customer:\n{str(e)}"
            )

    def cancel_edit(self):
        """Cancel editing and return to customer manager"""
        self.clear_form()
        self.go_to_customers()

    def clear_form(self):
        """Clear all form fields"""
        # Clear Personal Information
        if hasattr(self.staff_home, "lineEdit_25"):
            self.staff_home.lineEdit_25.clear()
        if hasattr(self.staff_home, "lineEdit_24"):
            self.staff_home.lineEdit_24.clear()
        if hasattr(self.staff_home, "lineEdit_30"):
            self.staff_home.lineEdit_30.clear()
        if hasattr(self.staff_home, "lineEdit_32"):
            self.staff_home.lineEdit_32.clear()
        if hasattr(self.staff_home, "lineEdit_27"):
            self.staff_home.lineEdit_27.clear()

        # Clear Address
        if hasattr(self.staff_home, "lineEdit_31"):
            self.staff_home.lineEdit_31.clear()
        if hasattr(self.staff_home, "lineEdit_26"):
            self.staff_home.lineEdit_26.clear()
        if hasattr(self.staff_home, "lineEdit_29"):
            self.staff_home.lineEdit_29.clear()
        if hasattr(self.staff_home, "lineEdit_28"):
            self.staff_home.lineEdit_28.clear()

        # Reset IDs
        self.current_customer_id = None
        self.current_address_id = None

    # Navigation methods
    def go_to_home(self):
        print("Staff: Navigating to Home")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.home_page_index)

    def go_to_dashboard(self):
        print("Staff: Navigating to Dashboard")
        self.dashboard.show()

    def go_to_customers(self):
        print("Staff: Navigating to Customer Manager")
        # Reload customer list before showing
        if self.managerc_control:
            self.managerc_control.load_customer_data()
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.customer_page_index)

    def go_to_orders(self):
        print("Staff: Navigating to Orders")
        self.order.show()

    def go_to_reports(self):
        print("Staff: Navigating to Reports")
        self.report.show()

    def go_to_delivery(self):
        print("Staff: Navigating to Delivery")
        self.delivery.show()

    def go_to_logout(self):
        # Create confirmation dialog
        reply = QMessageBox.question(
            self.staff_home,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No  # Default button
        )

        # Check user's response
        if reply == QMessageBox.StandardButton.Yes:
            print("Staff: Logging out...")
            # Close staff home
            self.staff_home.close()
            # Clear login fields for security
            self.login_view.username.clear()
            self.login_view.password.clear()
            # Show login view
            self.login_view.show()
            self.login_view.username.setFocus()
        else:
            print("Staff: Logout cancelled")