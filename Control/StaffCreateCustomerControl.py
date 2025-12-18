import pymysql
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox
from PyQt6.QtCore import Qt


class SCreateCustomerControl:
    """Controller for Staff Customer Creation page"""

    def __init__(self, model, staff_home, dashboard,customer, order,delivery, report, login_view, managerc_controller=None):
        """
        managerc_controller: optional reference to the SManagerCControl instance that manages the customer list.
        """
        self.staff_home = staff_home
        self.dashboard = dashboard
        self.model = model
        self.order = order
        self.delivery = delivery
        self.customer = customer
        self.report = report
        self.login_view = login_view

        # Staff ID from login session
        self.staff_id = None

        # Controller that owns the customer list view (SManagerCControl)
        self.managerc_controller = managerc_controller

        # Connect buttons and setup
        self.connect_customer_buttons()

    def set_staff_id(self, staff_id):
        """Set the logged-in staff ID (called from LoginController)"""
        self.staff_id = staff_id
        print(f"✓ SCreateCustomerControl: Staff ID set to {staff_id}")

    def connect_customer_buttons(self):
        """Connect navigation and action buttons"""

        # Sidebar navigation buttons (CreateCustomer page uses _3 suffix)
        if hasattr(self.staff_home, "Homebut_3"):
            self.staff_home.Homebut_3.clicked.connect(self.go_to_home)

        if hasattr(self.staff_home, "Dashbut_3"):
            self.staff_home.Dashbut_3.clicked.connect(self.go_to_dashboard)

        if hasattr(self.staff_home, "Userbut_3"):
            self.staff_home.Userbut_3.clicked.connect(self.go_to_customers)

        if hasattr(self.staff_home, "Orderbut_3"):
            self.staff_home.Orderbut_3.clicked.connect(self.go_to_orders)

        if hasattr(self.staff_home, "Reportbut_3"):
            self.staff_home.Reportbut_3.clicked.connect(self.go_to_reports)

        if hasattr(self.staff_home, "Delivlab_3"):
            self.staff_home.Delivlab_3.clicked.connect(self.go_to_delivery)

        if hasattr(self.staff_home, "Settbut_3"):
            self.staff_home.Settbut_3.clicked.connect(self.go_to_logout)

        # Icon buttons (these use _2 suffix for CreateCustomer page)
        if hasattr(self.staff_home, "h1_2"):
            self.staff_home.h1_2.clicked.connect(self.go_to_home)

        if hasattr(self.staff_home, "db1_2"):
            self.staff_home.db1_2.clicked.connect(self.go_to_dashboard)

        if hasattr(self.staff_home, "u1_2"):
            self.staff_home.u1_2.clicked.connect(self.go_to_customers)

        if hasattr(self.staff_home, "s1_2"):
            self.staff_home.s1_2.clicked.connect(self.go_to_logout)

        if hasattr(self.staff_home, "o1_2"):
            self.staff_home.o1_2.clicked.connect(self.go_to_orders)

        if hasattr(self.staff_home, "r1_2"):
            self.staff_home.r1_2.clicked.connect(self.go_to_reports)

        if hasattr(self.staff_home, "d1_2"):
            self.staff_home.d1_2.clicked.connect(self.go_to_delivery)

        # Action buttons
        if hasattr(self.staff_home, "crt_btn"):
            self.staff_home.crt_btn.clicked.connect(self.create_customer_data)

        if hasattr(self.staff_home, "crt_btn_2"):
            self.staff_home.crt_btn_2.clicked.connect(self.cancel_create)

    def create_customer_data(self):
        """Create new customer from form fields"""
        try:
            # Get customer data from form fields
            fname = self.staff_home.lineEdit.text().strip() if hasattr(self.staff_home, "lineEdit") else ""
            mname = self.staff_home.lineEdit_2.text().strip() if hasattr(self.staff_home, "lineEdit_2") else ""
            lname = self.staff_home.lineEdit_3.text().strip() if hasattr(self.staff_home, "lineEdit_3") else ""
            email = self.staff_home.lineEdit_4.text().strip() if hasattr(self.staff_home, "lineEdit_4") else ""
            phone = self.staff_home.lineEdit_5.text().strip() if hasattr(self.staff_home, "lineEdit_5") else ""

            # Get address data from form fields
            street_add = self.staff_home.lineEdit_6.text().strip() if hasattr(self.staff_home, "lineEdit_6") else ""
            appart_unit = self.staff_home.lineEdit_7.text().strip() if hasattr(self.staff_home, "lineEdit_7") else ""
            city = self.staff_home.lineEdit_8.text().strip() if hasattr(self.staff_home, "lineEdit_8") else ""
            zip_code = self.staff_home.lineEdit_9.text().strip() if hasattr(self.staff_home, "lineEdit_9") else ""

            # Validate required inputs
            if not fname:
                QMessageBox.warning(self.staff_home, "Validation", "First name is required.")
                return
            if not lname:
                QMessageBox.warning(self.staff_home, "Validation", "Last name is required.")
                return
            if not phone:
                QMessageBox.warning(self.staff_home, "Validation", "Phone number is required.")
                return

            # Validate address fields (required for Address table)
            if not street_add:
                QMessageBox.warning(self.staff_home, "Validation", "Street address is required.")
                return
            if not city:
                QMessageBox.warning(self.staff_home, "Validation", "City is required.")
                return
            if not zip_code:
                QMessageBox.warning(self.staff_home, "Validation", "Zip code is required.")
                return

            # Create customer with address and logged-in staff ID
            customer_id = self.model.create_customer(
                fname=fname,
                mname=mname,
                lname=lname,
                email=email,
                phone=phone,
                street_add=street_add,
                appart_unit=appart_unit,
                city=city,
                zip_code=zip_code,
                staff_id=self.staff_id,  # Use logged-in staff ID
                admin_id=None
            )

            if customer_id:
                # Log activity
                self.model.log_staff_activity(
                    staff_id=self.staff_id,
                    activity_type='CREATE_CUSTOMER',
                    customer_id=customer_id
                )

                # UPDATE LAST ACTIVE TIMESTAMP
                self.model.update_staff_last_active(self.staff_id)

                # Only ONE success message needed
                QMessageBox.information(
                    self.staff_home,
                    "Success",
                    f"Customer created successfully!"
                )
                print(f"✓ Staff {self.staff_id}: Customer created successfully! CustomerID: {customer_id}")

                # Clear form fields
                self.clear_form()

                # Refresh customer list immediately if controller reference available
                try:
                    if getattr(self, "managerc_controller", None):
                        self.managerc_controller.load_customer_data()
                except Exception:
                    import traceback
                    traceback.print_exc()

                # Navigate back to Customer Manager page
                self.go_to_customers()

                return customer_id
            else:
                QMessageBox.warning(self.staff_home, "Error", "Failed to create customer.")
                return None

        except Exception as e:
            print(f"✗ Staff: Error creating customer: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.staff_home, "Error", f"Error creating customer:\n{e}")
            return None

    def clear_form(self):
        """Clear all form fields"""
        if hasattr(self.staff_home, "lineEdit"):
            self.staff_home.lineEdit.clear()
        if hasattr(self.staff_home, "lineEdit_2"):
            self.staff_home.lineEdit_2.clear()
        if hasattr(self.staff_home, "lineEdit_3"):
            self.staff_home.lineEdit_3.clear()
        if hasattr(self.staff_home, "lineEdit_4"):
            self.staff_home.lineEdit_4.clear()
        if hasattr(self.staff_home, "lineEdit_5"):
            self.staff_home.lineEdit_5.clear()
        if hasattr(self.staff_home, "lineEdit_6"):
            self.staff_home.lineEdit_6.clear()
        if hasattr(self.staff_home, "lineEdit_7"):
            self.staff_home.lineEdit_7.clear()
        if hasattr(self.staff_home, "lineEdit_8"):
            self.staff_home.lineEdit_8.clear()
        if hasattr(self.staff_home, "lineEdit_9"):
            self.staff_home.lineEdit_9.clear()

    def cancel_create(self):
        """Cancel customer creation and go back"""
        self.clear_form()
        # Navigate back to customer list and refresh
        try:
            if getattr(self, "managerc_controller", None):
                self.managerc_controller.load_customer_data()
        except Exception:
            pass
        self.go_to_customers()

    # Navigation methods
    def go_to_home(self):
        print("Staff: Navigating to Home")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.home_page_index)

    def go_to_dashboard(self):
        print("Staff: Navigating to Dashboard")
        self.dashboard.show()

    def go_to_customers(self):
        print("Staff: Navigating to Customers")
        # Defensive reload: attempt to refresh before showing
        try:
            if getattr(self, "managerc_controller", None):
                self.managerc_controller.load_customer_data()
        except Exception:
            import traceback
            traceback.print_exc()

        # Show the customer list page
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
        from PyQt6.QtWidgets import QMessageBox

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
            # Clear staff ID
            self.staff_id = None
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