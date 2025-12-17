import pymysql
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox
from PyQt6.QtCore import Qt


class CreateCustomerControl:
    """Controller for Customer Management page"""

    def __init__(self, model, admin_home, dashboard, maneger, order, report, login_view, manegerc_controller=None):
        self.admin_home = admin_home
        self.dashboard = dashboard
        self.maneger = maneger
        self.model = model
        self.order = order
        self.report = report
        self.login_view = login_view

        # ADD THIS: Admin ID tracking
        self.admin_id = None  # 🔧 NEW

        # Controller that owns the customer list view (AManegerControlC)
        self.manegerc_controller = manegerc_controller

        # Connect buttons and setup table
        self.connect_customer_buttons()

    # ADD THIS METHOD: Set admin ID (called from LoginController)
    def set_admin_id(self, admin_id):
        """Set the logged-in admin ID"""
        self.admin_id = admin_id
        print(f"✓ CreateCustomerControl: Admin ID set to {admin_id}")

    def connect_customer_buttons(self):
        """Connect navigation and action buttons"""

        # Sidebar navigation buttons
        if hasattr(self.admin_home, "Homebut_6"):
            self.admin_home.Homebut_6.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "Dashbut_6"):
            self.admin_home.Dashbut_6.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "Userbut_6"):
            self.admin_home.Userbut_6.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "Orderbut_6"):
            self.admin_home.Orderbut_6.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "Reportbut_6"):
            self.admin_home.Reportbut_6.clicked.connect(self.go_to_reports)

        if hasattr(self.admin_home, "Settbut_6"):
            self.admin_home.Settbut_6.clicked.connect(self.go_to_logout)

        # Icon buttons
        if hasattr(self.admin_home, "h1_3"):
            self.admin_home.h1_3.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "db1_3"):
            self.admin_home.db1_3.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "u1_3"):
            self.admin_home.u1_3.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "s1_3"):
            self.admin_home.s1_3.clicked.connect(self.go_to_logout)

        if hasattr(self.admin_home, "o1_3"):
            self.admin_home.o1_3.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "r1_3"):
            self.admin_home.r1_3.clicked.connect(self.go_to_reports)

        # Action buttons - Fixed the attribute name
        if hasattr(self.admin_home, "crt_btn_4"):
            self.admin_home.crt_btn_4.clicked.connect(self.create_customer_data)

        if hasattr(self.admin_home, "crt_btn_3"):
            self.admin_home.crt_btn_3.clicked.connect(self.cancel_create)

    def create_customer_data(self):
        """Create new customer from form fields"""
        try:
            # Get customer data from form fields
            fname = self.admin_home.lineEdit_8.text().strip() if hasattr(self.admin_home, "lineEdit_8") else ""
            mname = self.admin_home.lineEdit_16.text().strip() if hasattr(self.admin_home, "lineEdit_16") else ""
            lname = self.admin_home.lineEdit_10.text().strip() if hasattr(self.admin_home, "lineEdit_10") else ""
            email = self.admin_home.lineEdit_15.text().strip() if hasattr(self.admin_home, "lineEdit_15") else ""
            phone = self.admin_home.lineEdit_9.text().strip() if hasattr(self.admin_home, "lineEdit_9") else ""

            # Get address data from form fields
            street_add = self.admin_home.lineEdit_11.text().strip() if hasattr(self.admin_home, "lineEdit_11") else ""
            appart_unit = self.admin_home.lineEdit_13.text().strip() if hasattr(self.admin_home, "lineEdit_13") else ""
            city = self.admin_home.lineEdit_14.text().strip() if hasattr(self.admin_home, "lineEdit_14") else ""
            zip_code = self.admin_home.lineEdit_12.text().strip() if hasattr(self.admin_home, "lineEdit_12") else ""

            # Validate required inputs
            if not fname:
                QMessageBox.warning(self.admin_home, "Validation", "First name is required.")
                return
            if not lname:
                QMessageBox.warning(self.admin_home, "Validation", "Last name is required.")
                return
            if not phone:
                QMessageBox.warning(self.admin_home, "Validation", "Phone number is required.")
                return

            # Validate address fields (required for Address table)
            if not street_add:
                QMessageBox.warning(self.admin_home, "Validation", "Street address is required.")
                return
            if not city:
                QMessageBox.warning(self.admin_home, "Validation", "City is required.")
                return
            if not zip_code:
                QMessageBox.warning(self.admin_home, "Validation", "Zip code is required.")
                return

            # Get staff_id or admin_id (replace with actual logged-in user ID if available)
            staff_id = None
            admin_id = None

            # Create customer with address
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
                staff_id=None,  # Staff don't create customers through admin interface
                admin_id=self.admin_id  # 🔧 FIXED: Use logged-in admin ID
            )

            if customer_id:
                QMessageBox.information(self.admin_home, "Success", "Customer created successfully.")
                print(f"✓ Customer created successfully! ID: {customer_id}")

                # Clear form fields
                self.clear_form()

                # --- NEW: refresh customer list immediately if controller reference available ---
                try:
                    if getattr(self, "manegerc_controller", None):
                        self.manegerc_controller.load_customer_data()
                    else:
                        # fallback: try to find a controller attached to the manager view
                        if hasattr(self.maneger, "controller"):
                            try:
                                self.maneger.controller.load_customer_data()
                            except Exception:
                                pass
                except Exception:
                    import traceback
                    traceback.print_exc()

                # Navigate back to Customer Manager page and ensure it's visible
                try:
                    # If you have a stacked widget index for customer manager, set it:
                    if hasattr(self.admin_home, "manegerc_page_index"):
                        self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.manegerc_page_index)
                except Exception:
                    pass

                # show the manager view to ensure the user sees the updated list
                try:
                    if getattr(self, "maneger", None):
                        self.maneger.show()
                except Exception:
                    pass

                return customer_id
            else:
                QMessageBox.warning(self.admin_home, "Error", "Failed to create customer.")
                return None

        except Exception as e:
            print(f"✗ Error creating customer: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.admin_home, "Error", f"Error creating customer:\n{e}")
            return None

    def clear_form(self):
        """Clear all form fields"""
        if hasattr(self.admin_home, "lineEdit_8"):
            self.admin_home.lineEdit_8.clear()
        if hasattr(self.admin_home, "lineEdit_9"):
            self.admin_home.lineEdit_9.clear()
        if hasattr(self.admin_home, "lineEdit_10"):
            self.admin_home.lineEdit_10.clear()
        if hasattr(self.admin_home, "lineEdit_11"):
            self.admin_home.lineEdit_11.clear()
        if hasattr(self.admin_home, "lineEdit_12"):
            self.admin_home.lineEdit_12.clear()
        if hasattr(self.admin_home, "lineEdit_13"):
            self.admin_home.lineEdit_13.clear()
        if hasattr(self.admin_home, "lineEdit_14"):
            self.admin_home.lineEdit_14.clear()
        if hasattr(self.admin_home, "lineEdit_15"):
            self.admin_home.lineEdit_15.clear()
        if hasattr(self.admin_home, "lineEdit_16"):
            self.admin_home.lineEdit_16.clear()

    def cancel_create(self):
        """Cancel customer creation and go back"""
        self.clear_form()
        # Navigate back to customer list or previous page and refresh
        try:
            if getattr(self, "manegerc_controller", None):
                self.manegerc_controller.load_customer_data()
        except Exception:
            pass
        self.go_to_users()

    # Navigation methods
    def go_to_home(self):
        print("Navigating to Home")
        self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.home_page_index)

    def go_to_dashboard(self):
        print("Navigating to Dashboard")
        self.dashboard.show()

    def go_to_users(self):
        print("Navigating to Users")
        # Defensive reload: attempt to refresh before showing
        try:
            if getattr(self, "manegerc_controller", None):
                self.manegerc_controller.load_customer_data()
            elif hasattr(self.maneger, "controller"):
                try:
                    self.maneger.controller.load_customer_data()
                except Exception:
                    pass
        except Exception:
            import traceback
            traceback.print_exc()

        # show the manager (customer list) view
        if getattr(self, "maneger", None):
            self.maneger.show()

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


