from PyQt6.QtWidgets import QMessageBox


class EditCustomerControl:
    """Controller for Edit Customer page"""

    def __init__(self, model, admin_home, dashboard, manager, managerc, order, report,login_view):
        self.admin_home = admin_home
        self.dashboard = dashboard
        self.manager = manager
        self.managerc = managerc
        self.model = model
        self.order = order
        self.report = report
        self.login_view = login_view

        # Store current customer being edited
        self.current_customer_id = None
        self.current_address_id = None

        # Reference to customer manager controller (will be set later)
        self.managerc_control = None

        # Connect buttons
        self.connect_editcustomer_buttons()

    def connect_editcustomer_buttons(self):
        """Connect navigation and action buttons on the Edit Customer page"""

        # Sidebar buttons
        if hasattr(self.admin_home, "Homebut_13"):
            self.admin_home.Homebut_13.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "Dashbut_13"):
            self.admin_home.Dashbut_13.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "Userbut_13"):
            self.admin_home.Userbut_13.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "Orderbut_13"):
            self.admin_home.Orderbut_13.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "Reportbut_13"):
            self.admin_home.Reportbut_13.clicked.connect(self.go_to_reports)

        if hasattr(self.admin_home, "Settbut_13"):
            self.admin_home.Settbut_13.clicked.connect(self.go_to_logout)

        # Icon buttons
        if hasattr(self.admin_home, "h1_6"):
            self.admin_home.h1_6.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "db1_6"):
            self.admin_home.db1_6.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "u1_6"):
            self.admin_home.u1_6.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "s1_6"):
            self.admin_home.s1_6.clicked.connect(self.go_to_logout)

        if hasattr(self.admin_home, "o1_6"):
            self.admin_home.o1_6.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "r1_6"):
            self.admin_home.r1_6.clicked.connect(self.go_to_reports)

        # Action buttons
        if hasattr(self.admin_home, "crt_btn_7"):
            self.admin_home.crt_btn_7.clicked.connect(self.update_customer_data)

        if hasattr(self.admin_home, "crt_btn_8"):
            self.admin_home.crt_btn_8.clicked.connect(self.cancel_edit)

    def load_customer_data(self, customer_id):
        """Load customer data into the form fields"""
        try:
            # Get customer data from database
            customer = self.model.get_customer_by_id(customer_id)

            if not customer:
                QMessageBox.warning(
                    self.admin_home,
                    "Error",
                    "Could not load customer data."
                )
                return False

            # Store current customer ID
            self.current_customer_id = customer_id

            # Load Personal Information
            if hasattr(self.admin_home, "lineEdit_25"):
                self.admin_home.lineEdit_25.setText(customer.get('CFName', ''))

            if hasattr(self.admin_home, "lineEdit_24"):
                self.admin_home.lineEdit_24.setText(customer.get('CMName', '') or '')

            if hasattr(self.admin_home, "lineEdit_30"):
                self.admin_home.lineEdit_30.setText(customer.get('CLName', ''))

            if hasattr(self.admin_home, "lineEdit_32"):
                self.admin_home.lineEdit_32.setText(customer.get('CEmail', '') or '')

            if hasattr(self.admin_home, "lineEdit_27"):
                self.admin_home.lineEdit_27.setText(customer.get('CPhone', '') or '')

            # Load Address Information (get first address)
            addresses = self.model.get_customer_addresses(customer_id)
            if addresses and len(addresses) > 0:
                address = addresses[0]  # Use first address
                self.current_address_id = address.get('AddID')

                if hasattr(self.admin_home, "lineEdit_31"):
                    self.admin_home.lineEdit_31.setText(address.get('StreetAdd', '') or '')

                if hasattr(self.admin_home, "lineEdit_26"):
                    self.admin_home.lineEdit_26.setText(address.get('AppartUnit', '') or '')

                if hasattr(self.admin_home, "lineEdit_29"):
                    self.admin_home.lineEdit_29.setText(address.get('City', '') or '')

                if hasattr(self.admin_home, "lineEdit_28"):
                    self.admin_home.lineEdit_28.setText(address.get('ZipCode', '') or '')
            else:
                # Clear address fields if no address exists
                self.current_address_id = None
                if hasattr(self.admin_home, "lineEdit_31"):
                    self.admin_home.lineEdit_31.clear()
                if hasattr(self.admin_home, "lineEdit_26"):
                    self.admin_home.lineEdit_26.clear()
                if hasattr(self.admin_home, "lineEdit_29"):
                    self.admin_home.lineEdit_29.clear()
                if hasattr(self.admin_home, "lineEdit_28"):
                    self.admin_home.lineEdit_28.clear()

            print(f"✓ Loaded customer data for CustomerID: {customer_id}")
            return True

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.admin_home,
                "Error",
                f"Failed to load customer data:\n{str(e)}"
            )
            return False

    def update_customer_data(self):
        """Update customer information in the database"""
        try:
            if not self.current_customer_id:
                QMessageBox.warning(
                    self.admin_home,
                    "Error",
                    "No customer selected for editing."
                )
                return

            # Get form data - Personal Information
            fname = self.admin_home.lineEdit_25.text().strip() if hasattr(self.admin_home, "lineEdit_25") else ""
            mname = self.admin_home.lineEdit_24.text().strip() if hasattr(self.admin_home, "lineEdit_24") else ""
            lname = self.admin_home.lineEdit_30.text().strip() if hasattr(self.admin_home, "lineEdit_30") else ""
            email = self.admin_home.lineEdit_32.text().strip() if hasattr(self.admin_home, "lineEdit_32") else ""
            phone = self.admin_home.lineEdit_27.text().strip() if hasattr(self.admin_home, "lineEdit_27") else ""

            # Get form data - Address
            street = self.admin_home.lineEdit_31.text().strip() if hasattr(self.admin_home, "lineEdit_31") else ""
            unit = self.admin_home.lineEdit_26.text().strip() if hasattr(self.admin_home, "lineEdit_26") else ""
            city = self.admin_home.lineEdit_29.text().strip() if hasattr(self.admin_home, "lineEdit_29") else ""
            zipcode = self.admin_home.lineEdit_28.text().strip() if hasattr(self.admin_home, "lineEdit_28") else ""

            # Validate required fields
            if not fname or not lname:
                QMessageBox.warning(
                    self.admin_home,
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
                    self.admin_home,
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
                        self.admin_home,
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
                    print(f"✓ Created new address with ID: {new_address_id}")

            QMessageBox.information(
                self.admin_home,
                "Success",
                f"Customer '{fname} {lname}' updated successfully!"
            )

            # Reload customer manager data if available
            if self.managerc_control:
                self.managerc_control.load_customer_data()

            # Navigate back to customer manager
            self.go_to_users()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.admin_home,
                "Error",
                f"An error occurred while updating customer:\n{str(e)}"
            )

    def cancel_edit(self):
        """Cancel editing and return to customer manager"""
        self.clear_form()
        self.go_to_users()

    def clear_form(self):
        """Clear all form fields"""
        # Clear Personal Information
        if hasattr(self.admin_home, "lineEdit_25"):
            self.admin_home.lineEdit_25.clear()
        if hasattr(self.admin_home, "lineEdit_24"):
            self.admin_home.lineEdit_24.clear()
        if hasattr(self.admin_home, "lineEdit_30"):
            self.admin_home.lineEdit_30.clear()
        if hasattr(self.admin_home, "lineEdit_32"):
            self.admin_home.lineEdit_32.clear()
        if hasattr(self.admin_home, "lineEdit_27"):
            self.admin_home.lineEdit_27.clear()

        # Clear Address
        if hasattr(self.admin_home, "lineEdit_31"):
            self.admin_home.lineEdit_31.clear()
        if hasattr(self.admin_home, "lineEdit_26"):
            self.admin_home.lineEdit_26.clear()
        if hasattr(self.admin_home, "lineEdit_29"):
            self.admin_home.lineEdit_29.clear()
        if hasattr(self.admin_home, "lineEdit_28"):
            self.admin_home.lineEdit_28.clear()

        # Reset IDs
        self.current_customer_id = None
        self.current_address_id = None

    # Navigation methods
    def go_to_home(self):
        print("Navigating to Home")
        self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.home_page_index)

    def go_to_dashboard(self):
        print("Navigating to Dashboard")
        self.dashboard.show()

    def go_to_users(self):
        print("Navigating to Customer Manager")
        self.managerc.show()

    def go_to_orders(self):
        print("Navigating to Orders")
        self.order.show()

    def go_to_reports(self):
        print("Navigating to Reports")
        self.report.show()

    def go_to_logout(self):
        from PyQt6.QtWidgets import QMessageBox

        # Create confirmation dialog
        reply = QMessageBox.question(
            self.admin_home,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No  # Default button
        )

        # Check user's response
        if reply == QMessageBox.StandardButton.Yes:
            print("Logging out...")
            # Close admin home
            self.admin_home.close()
            # Clear login fields for security
            self.login_view.username.clear()
            self.login_view.password.clear()
            # Show login view
            self.login_view.show()
            self.login_view.username.setFocus()
        else:
            print("Logout cancelled")