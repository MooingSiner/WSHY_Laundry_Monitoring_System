from PyQt6.QtWidgets import QMessageBox


class ADashBControl:
    """Controller for Dashboard page navigation and data management"""

    def __init__(self, admin_home, dashboard, maneger, order, report, model,login_view):
        self.admin_home = admin_home
        self.dashboard = dashboard
        self.maneger = maneger
        self.order = order
        self.report = report
        self.model = model  # Add model reference
        self.login_view = login_view

        # Connect buttons from Dashboard page (SDB)
        self.connect_dashboard_buttons()

    def connect_dashboard_buttons(self):
        """Connect navigation buttons on the Dashboard page"""

        # Sidebar buttons on Dashboard page
        if hasattr(self.admin_home, "Homebut"):
            self.admin_home.Homebut.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "Dashbut"):
            self.admin_home.Dashbut.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "Userbut"):
            self.admin_home.Userbut.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "Orderbut"):
            self.admin_home.Orderbut.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "Reportbut"):
            self.admin_home.Reportbut.clicked.connect(self.go_to_reports)

        if hasattr(self.admin_home, "Settbut"):
            self.admin_home.Settbut.clicked.connect(self.go_to_logout)

        # Icon buttons on Dashboard page
        if hasattr(self.admin_home, "h2"):
            self.admin_home.h2.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "db2"):
            self.admin_home.db2.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "u2"):
            self.admin_home.u2.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "s2"):
            self.admin_home.s2.clicked.connect(self.go_to_logout)

        if hasattr(self.admin_home, "o2"):
            self.admin_home.o2.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "r2"):
            self.admin_home.r2.clicked.connect(self.go_to_reports)


    def go_to_home(self):
        print("Navigating to Home from Dashboard")
        self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.home_page_index)

    def go_to_dashboard(self):
        print("Already on Dashboard")
        self.dashboard.show()

    def go_to_users(self):
        print("Navigating to Users from Dashboard")
        self.maneger.show()

    def go_to_orders(self):
        print("Navigating to Orders from Dashboard")
        self.order.show()

    def go_to_reports(self):
        print("Navigating to Reports from Dashboard")
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
