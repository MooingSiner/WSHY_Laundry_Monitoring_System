import pymysql
from PyQt6.QtWidgets import QMessageBox


# Remove this line - you're using pymysql, not mysql.connector
# from mysql.connector import connection


class Createstaffcontrol:
    """Controller for Dashboard page navigation"""

    def __init__(self, model, admin_home, dashboard, maneger, order, report,login_view, maneger_controller=None):
        self.admin_home = admin_home
        self.dashboard = dashboard
        self.maneger = maneger
        self.model = model
        self.order = order
        self.report = report
        self.login_view = login_view
        # new: reference to manager controller so we can call load_staff_data()
        self.maneger_controller = maneger_controller

        # Connect buttons from Dashboard page (ADB)
        self.connect_createstaff_buttons()

    def connect_createstaff_buttons(self):
        """Connect navigation buttons on the Dashboard page"""

        # Sidebar buttons on Dashboard page
        if hasattr(self.admin_home, "Homebut_4"):
            self.admin_home.Homebut_4.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "Dashbut_4"):
            self.admin_home.Dashbut_4.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "Userbut_4"):
            self.admin_home.Userbut_4.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "Orderbut_4"):
            self.admin_home.Orderbut_4.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "Reportbut_4"):
            self.admin_home.Reportbut_4.clicked.connect(self.go_to_reports)

        if hasattr(self.admin_home, "Settbut_4"):
            self.admin_home.Settbut_4.clicked.connect(self.go_to_logout)

        # Icon buttons on Dashboard page
        if hasattr(self.admin_home, "h2_6"):
            self.admin_home.h2_6.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "db2_6"):
            self.admin_home.db2_6.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "u2_6"):
            self.admin_home.u2_6.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "s2_6"):
            self.admin_home.s2_6.clicked.connect(self.go_to_logout)

        if hasattr(self.admin_home, "o2_6"):
            self.admin_home.o2_6.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "r2_6"):
            self.admin_home.r2_6.clicked.connect(self.go_to_reports)


        if hasattr(self.admin_home, "crt_btn"):
            self.admin_home.crt_btn.clicked.connect(self.create_staff_data)
            if hasattr(self.admin_home, "crt_btn_2"):
                self.admin_home.crt_btn_2.clicked.connect(self.go_to_users)
                self.admin_home.crt_btn_2.clicked.connect(self.clear_form)

    def go_to_home(self):
        print("Navigating to Home")
        self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.home_page_index)

    def go_to_dashboard(self):
        print("Navigating to Dashboard")
        self.dashboard.show()

    def go_to_users(self):
        print("Navigating to Users")
        # If we have the manager controller, ensure it reloads data before showing the view
        try:
            if getattr(self, "maneger_controller", None):
                self.maneger_controller.load_staff_data()
            else:
                # fallback: if manager view exists, attempt to call its controller via a known attribute
                if hasattr(self.maneger, "load_staff_data"):
                    try:
                        # some codebases attach load to view; call defensively
                        self.maneger.load_staff_data()
                    except Exception:
                        pass
        except Exception:
            import traceback
            traceback.print_exc()

        # show the manager view
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

    def create_staff_data(self):
        """Create staff member - reads from form fields"""
        # Get form data
        fname = self.admin_home.lineEdit.text() if hasattr(self.admin_home, "lineEdit") else ""
        mname = self.admin_home.lineEdit_2.text() if hasattr(self.admin_home, "lineEdit_2") else ""
        lname = self.admin_home.lineEdit_3.text() if hasattr(self.admin_home, "lineEdit_3") else ""
        email = self.admin_home.lineEdit_4.text() if hasattr(self.admin_home, "lineEdit_4") else ""
        phone = self.admin_home.lineEdit_5.text() if hasattr(self.admin_home, "lineEdit_5") else ""
        user = self.admin_home.lineEdit_6.text() if hasattr(self.admin_home, "lineEdit_6") else ""
        passw = self.admin_home.lineEdit_7.text() if hasattr(self.admin_home, "lineEdit_7") else ""

        role = 'staff'
        if hasattr(self.admin_home, "roleComboBox"):
            role = self.admin_home.roleComboBox.currentText().lower()
        elif hasattr(self.admin_home, "adminRadioButton") and self.admin_home.adminRadioButton.isChecked():
            role = 'admin'

        # Validate inputs before calling model
        if not fname.strip() or not lname.strip() or not user.strip() or not passw.strip():
            QMessageBox.warning(self.admin_home, "Input Error", "Please fill in all required fields.")
            return

        # Call model
        result = self.model.create_employee(fname, mname, lname, email, phone, user, passw, role)

        if result:
            self.clear_form()
            if getattr(self, "maneger_controller", None):
                self.maneger_controller.load_staff_data()
            if getattr(self, "maneger", None):
                self.maneger.show()

    def clear_form(self):
        """Clear all form fields after successful creation"""
        if hasattr(self.admin_home, "lineEdit"):
            self.admin_home.lineEdit.clear()
        if hasattr(self.admin_home, "lineEdit_2"):
            self.admin_home.lineEdit_2.clear()
        if hasattr(self.admin_home, "lineEdit_3"):
            self.admin_home.lineEdit_3.clear()
        if hasattr(self.admin_home, "lineEdit_4"):
            self.admin_home.lineEdit_4.clear()
        if hasattr(self.admin_home, "lineEdit_5"):
            self.admin_home.lineEdit_5.clear()
        if hasattr(self.admin_home, "lineEdit_6"):
            self.admin_home.lineEdit_6.clear()
        if hasattr(self.admin_home, "lineEdit_7"):
            self.admin_home.lineEdit_7.clear()