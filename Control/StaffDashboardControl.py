from PyQt6.QtWidgets import QMessageBox


class SDashBControl:
    """Controller for Staff Dashboard page navigation"""

    def __init__(self, staff_home, dashboard, customer, order,delivery, report, login_view):
        self.staff_home = staff_home
        self.dashboard = dashboard
        self.customer = customer
        self.delivery = delivery
        self.order = order
        self.report = report
        self.login_view = login_view

        # Connect buttons from Staff Dashboard page
        self.connect_dashboard_buttons()

    def connect_dashboard_buttons(self):
        """Connect navigation buttons on the Staff Dashboard page"""

        # Sidebar buttons on Dashboard page (without _2 suffix)
        if hasattr(self.staff_home, "Homebut"):
            self.staff_home.Homebut.clicked.connect(self.go_to_home)

        if hasattr(self.staff_home, "Dashbut"):
            self.staff_home.Dashbut.clicked.connect(self.go_to_dashboard)

        if hasattr(self.staff_home, "Userbut"):
            self.staff_home.Userbut.clicked.connect(self.go_to_customer)

        if hasattr(self.staff_home, "Orderbut"):
            self.staff_home.Orderbut.clicked.connect(self.go_to_orders)

        if hasattr(self.staff_home, "Reportbut"):
            self.staff_home.Reportbut.clicked.connect(self.go_to_reports)

        if hasattr(self.staff_home, "Delivlab"):
            self.staff_home.Delivlab.clicked.connect(self.go_to_delivery)

        if hasattr(self.staff_home, "Settbut"):
            self.staff_home.Settbut.clicked.connect(self.go_to_logout)

        # Icon buttons on Staff Dashboard page
        if hasattr(self.staff_home, "h2"):
            self.staff_home.h2.clicked.connect(self.go_to_home)

        if hasattr(self.staff_home, "db2"):
            self.staff_home.db2.clicked.connect(self.go_to_dashboard)

        if hasattr(self.staff_home, "u2"):
            self.staff_home.u2.clicked.connect(self.go_to_customer)

        if hasattr(self.staff_home, "s2"):
            self.staff_home.s2.clicked.connect(self.go_to_logout)

        if hasattr(self.staff_home, "o2"):
            self.staff_home.o2.clicked.connect(self.go_to_orders)

        if hasattr(self.staff_home, "d2"):
            self.staff_home.d2.clicked.connect(self.go_to_delivery)

        if hasattr(self.staff_home, "r2"):
            self.staff_home.r2.clicked.connect(self.go_to_reports)

    def go_to_home(self):
        print("Staff: Navigating to Home")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.home_page_index)

    def go_to_dashboard(self):
        print("Staff: Already on Dashboard")
        self.dashboard.show()

    def go_to_customer(self):
        print("Staff: Navigating to Customers")
        self.customer.show()

    def go_to_orders(self):
        print("Staff: Navigating to Orders")
        self.order.show()

    def go_to_reports(self):
        print("Staff: Navigating to Reports")
        self.report.show()

    def go_to_delivery(self):
        print("Staff: Navigating to Delivery")
        # Add delivery page navigation when ready
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