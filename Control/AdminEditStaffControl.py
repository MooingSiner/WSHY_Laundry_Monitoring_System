import pymysql
from PyQt6.QtWidgets import QMessageBox


class Editstaffcontrol:
    """Controller for Edit Staff page"""

    def __init__(self, model, admin_home, dashboard, manager, order, report,login_view):
        self.admin_home = admin_home
        self.dashboard = dashboard
        self.manager = manager
        self.model = model
        self.order = order
        self.report = report
        self.login_view = login_view

        self.current_employee_id = None
        self.current_staff_id = None
        self.current_role = None
        self.manager_control = None

        # Track if we're in edit mode
        self.is_editing = False

        # Connect buttons
        self.connect_Editstaff_buttons()

    def connect_Editstaff_buttons(self):
        """Connect navigation buttons on the Edit Staff page"""

        # Sidebar buttons
        if hasattr(self.admin_home, "Homebut_10"):
            self.admin_home.Homebut_10.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "Dashbut_10"):
            self.admin_home.Dashbut_10.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "Userbut_10"):
            self.admin_home.Userbut_10.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "Orderbut_10"):
            self.admin_home.Orderbut_10.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "Reportbut_10"):
            self.admin_home.Reportbut_10.clicked.connect(self.go_to_reports)

        if hasattr(self.admin_home, "Settbut_10"):
            self.admin_home.Settbut_10.clicked.connect(self.go_to_logout)

        # Icon buttons
        if hasattr(self.admin_home, "h2_9"):
            self.admin_home.h2_9.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "db2_9"):
            self.admin_home.db2_9.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "u2_9"):
            self.admin_home.u2_9.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "s2_9"):
            self.admin_home.s2_9.clicked.connect(self.go_to_logout)

        if hasattr(self.admin_home, "o2_9"):
            self.admin_home.o2_9.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "r2_9"):
            self.admin_home.r2_9.clicked.connect(self.go_to_reports)

        # Save/Update button
        if hasattr(self.admin_home, "crt_btn_5"):
            self.admin_home.crt_btn_5.clicked.connect(self.edit_staff_data)

        # Cancel button
        if hasattr(self.admin_home, "crt_btn_6"):
            self.admin_home.crt_btn_6.clicked.connect(self.cancel_edit)

    def load_employee_data(self, employee_id, staff_id=None):
        """Load employee data into form fields for editing"""
        try:


            # CRITICAL: Store IDs FIRST before anything else
            self.current_employee_id = employee_id
            self.current_staff_id = staff_id
            self.is_editing = True

            # Get employee data from database
            employee = self.model.get_employee_full_info(employee_id)

            if not employee:

                QMessageBox.critical(
                    self.admin_home,
                    "Error",
                    f"Employee ID {employee_id} not found in database."
                )
                self.is_editing = False
                return False

            # Store the role
            self.current_role = employee.get('role', 'staff')


            # Populate form fields
            if hasattr(self.admin_home, "lineEdit_20"):
                self.admin_home.lineEdit_20.setText(employee.get('EFName', ''))


            if hasattr(self.admin_home, "lineEdit_23"):
                self.admin_home.lineEdit_23.setText(employee.get('EMName', '') or '')


            if hasattr(self.admin_home, "lineEdit_19"):
                self.admin_home.lineEdit_19.setText(employee.get('ELName', ''))


            if hasattr(self.admin_home, "lineEdit_17"):
                self.admin_home.lineEdit_17.setText(employee.get('EEmail', '') or '')


            if hasattr(self.admin_home, "lineEdit_22"):
                self.admin_home.lineEdit_22.setText(employee.get('EPhone', '') or '')


            if hasattr(self.admin_home, "lineEdit_21"):
                self.admin_home.lineEdit_21.setText(employee.get('username', ''))

            # Password field - clear and set placeholder
            if hasattr(self.admin_home, "lineEdit_18"):
                self.admin_home.lineEdit_18.clear()
                self.admin_home.lineEdit_18.setPlaceholderText("keep current password")


            # Set role if you have role selector
            if hasattr(self.admin_home, "roleComboBox"):
                role = employee.get('role', 'staff')
                index = self.admin_home.roleComboBox.findText(role.capitalize())
                if index >= 0:
                    self.admin_home.roleComboBox.setCurrentIndex(index)

            return True

        except Exception as e:

            import traceback
            traceback.print_exc()
            self.is_editing = False
            QMessageBox.critical(
                self.admin_home,
                "Error",
                f"Failed to load employee data:\n{str(e)}"
            )
            return False

    def edit_staff_data(self):
        """Update staff member - reads from form fields"""
        try:

            if not self.current_employee_id:

                QMessageBox.warning(
                    self.admin_home,
                    "No Selection",
                    "No employee is currently loaded for editing."
                )
                return

            # Get data from form fields
            fname = self.admin_home.lineEdit_20.text().strip() if hasattr(self.admin_home, "lineEdit_20") else ""
            mname = self.admin_home.lineEdit_23.text().strip() if hasattr(self.admin_home, "lineEdit_23") else ""
            lname = self.admin_home.lineEdit_19.text().strip() if hasattr(self.admin_home, "lineEdit_19") else ""
            email = self.admin_home.lineEdit_17.text().strip() if hasattr(self.admin_home, "lineEdit_17") else ""
            phone = self.admin_home.lineEdit_22.text().strip() if hasattr(self.admin_home, "lineEdit_22") else ""
            username = self.admin_home.lineEdit_21.text().strip() if hasattr(self.admin_home, "lineEdit_21") else ""
            password = self.admin_home.lineEdit_18.text().strip() if hasattr(self.admin_home, "lineEdit_18") else ""



            # Get role from combo box or use stored role
            role = self.current_role
            if hasattr(self.admin_home, "roleComboBox"):
                role = self.admin_home.roleComboBox.currentText().lower()

            elif hasattr(self.admin_home, "adminRadioButton"):
                if self.admin_home.adminRadioButton.isChecked():
                    role = 'admin'


            # Validate inputs
            if not fname:
                QMessageBox.warning(self.admin_home, "Validation Error", "First name is required")
                return
            if not lname:
                QMessageBox.warning(self.admin_home, "Validation Error", "Last name is required")
                return
            if not username:
                QMessageBox.warning(self.admin_home, "Validation Error", "Username is required")
                return


            # Update employee
            result = self.model.edit_employee(
                employee_id=self.current_employee_id,
                fname=fname,
                mname=mname,
                lname=lname,
                email=email,
                phone=phone,
                username=username,
                password=password if password else None,
                role=role
            )

            if result:

                QMessageBox.information(
                    self.admin_home,
                    "Success",
                    f"Employee {fname} {lname} updated successfully!"
                )

                # Clear form
                self.clear_form()

                # Navigate back to users page and refresh
                self.go_to_users_and_refresh()
            else:

                QMessageBox.warning(
                    self.admin_home,
                    "Error",
                    "Failed to update employee. Username may already exist."
                )

        except Exception as e:

            import traceback
            traceback.print_exc()

            QMessageBox.critical(
                self.admin_home,
                "Error",
                f"An error occurred while updating:\n{str(e)}"
            )

    def clear_form(self):
        """Clear all form fields"""
        # Don't clear IDs if we're in edit mode
        if not self.is_editing:
            self.current_employee_id = None
            self.current_staff_id = None
            self.current_role = None

        if hasattr(self.admin_home, "lineEdit_17"):
            self.admin_home.lineEdit_17.clear()
        if hasattr(self.admin_home, "lineEdit_18"):
            self.admin_home.lineEdit_18.clear()
        if hasattr(self.admin_home, "lineEdit_19"):
            self.admin_home.lineEdit_19.clear()
        if hasattr(self.admin_home, "lineEdit_20"):
            self.admin_home.lineEdit_20.clear()
        if hasattr(self.admin_home, "lineEdit_21"):
            self.admin_home.lineEdit_21.clear()
        if hasattr(self.admin_home, "lineEdit_22"):
            self.admin_home.lineEdit_22.clear()
        if hasattr(self.admin_home, "lineEdit_23"):
            self.admin_home.lineEdit_23.clear()



    def cancel_edit(self):
        """Cancel editing and return to users page"""
        # Clear everything including IDs
        self.current_employee_id = None
        self.current_staff_id = None
        self.current_role = None
        self.is_editing = False
        self.clear_form()
        self.go_to_users_and_refresh()

    def go_to_users_and_refresh(self):
        """Navigate to users page and refresh the table"""


        # Show the users page first
        self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.users_page_index)

        # Then refresh the table if manager_control is available
        if self.manager_control:
            self.manager_control.load_staff_data()


    # Navigation methods
    def go_to_home(self):
        print("Navigating to Home")
        self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.home_page_index)

    def go_to_dashboard(self):
        print("Navigating to Dashboard")
        self.dashboard.show()

    def go_to_users(self):
        print("Navigating to Users")
        self.go_to_users_and_refresh()

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