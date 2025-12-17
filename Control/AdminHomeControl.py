from PyQt6.QtWidgets import QMessageBox
from View.adminpopupdetails import AdminDetailsPopup


class AHControl:
    """Controller for AdminHome page navigation"""

    def __init__(self, admin_home, dashboard,maneger,order,report,cstaff,login_view):
        self.admin_home = admin_home
        self.dashboard = dashboard
        self.maneger = maneger
        self.order = order
        self.report = report
        self.cstaff = cstaff
        self.login_view = login_view

        # Current admin context
        self.current_admin_id = None
        self.model = None  # Will be set from admin_home

        # Admin details popup
        self.admin_popup = None

        # Connect to stackedWidget's page change signal - THIS IS MISSING
        if hasattr(self.admin_home, 'stackedWidget'):
            self.admin_home.stackedWidget.currentChanged.connect(self.on_page_changed)
            print("✓ AHControl: Connected to stackedWidget page change signal")

        self.connect_home_buttons()

    def set_admin_context(self, admin_id):
        """Set current admin ID"""
        self.current_admin_id = admin_id

        # Get model from admin_home if available
        if hasattr(self.admin_home, 'model'):
            self.model = self.admin_home.model
            print(f"✓ AHControl: Model acquired from admin_home")

        print(f"✓ AHControl: Admin context set: AdminID = {admin_id}")

        # Also set the context in AdminHome view
        if hasattr(self.admin_home, 'set_admin_context'):
            self.admin_home.set_admin_context(admin_id, self.model)

        # Initial refresh if we're already on home page
        if hasattr(self.admin_home, 'home_page_index'):
            current_index = self.admin_home.stackedWidget.currentIndex()
            if current_index == self.admin_home.home_page_index:
                self.refresh_home_page()

    def on_page_changed(self, index):
        """Automatically refresh home page when it becomes visible - THIS IS MISSING"""
        if hasattr(self.admin_home, 'home_page_index'):
            if index == self.admin_home.home_page_index:
                print("✓ Home page activated - refreshing data")
                self.refresh_home_page()

                # Also update the model reference if needed
                if not self.model and hasattr(self.admin_home, 'model'):
                    self.model = self.admin_home.model

    def refresh_home_page(self):
        """Refresh all data on the home page - THIS IS MISSING"""
        try:
            # Call the home data refresh method in AdminHome
            if hasattr(self.admin_home, 'load_home_data'):
                self.admin_home.load_home_data()
                print("✓ Home page data refreshed successfully")
            else:
                print("✗ AdminHome doesn't have load_home_data method")

            # Also update admin profile section
            self.update_profile_section()

        except Exception as e:
            print(f"✗ Error refreshing home page: {e}")
            import traceback
            traceback.print_exc()

    def update_profile_section(self):
        """Update the profile section with admin information"""
        if not self.current_admin_id or not self.model:
            print("✗ Cannot update profile: No admin ID or model")
            return

        try:
            # Get ADMIN information (not staff!)
            admin_info = self.model.get_admin_by_id(self.current_admin_id)
            if admin_info:
                # Update profile name if label exists
                if hasattr(self.admin_home, "label_29"):
                    name = f"{admin_info.get('EFName', '')} {admin_info.get('ELName', '')}"
                    self.admin_home.label_29.setText(name.strip() or "Admin Profile")
                    print(f"✓ Updated profile name: {name.strip()}")

        except Exception as e:
            print(f"✗ Error updating profile section: {e}")

    def connect_home_buttons(self):
        """Connect navigation buttons on the AdminHome page"""
        print("✓ AHControl: Connecting home buttons...")

        # Sidebar buttons
        if hasattr(self.admin_home, "Homebut_2"):
            self.admin_home.Homebut_2.clicked.connect(self.go_to_home)
            print("✓ Connected Homebut_2")

        if hasattr(self.admin_home, "Dashbut_2"):
            self.admin_home.Dashbut_2.clicked.connect(self.go_to_dashboard)
            print("✓ Connected Dashbut_2")

        if hasattr(self.admin_home, "Userbut_2"):
            self.admin_home.Userbut_2.clicked.connect(self.go_to_users)
            print("✓ Connected Userbut_2")

        if hasattr(self.admin_home, "Orderbut_2"):
            self.admin_home.Orderbut_2.clicked.connect(self.go_to_orders)
            print("✓ Connected Orderbut_2")

        if hasattr(self.admin_home, "Reportbut_2"):
            self.admin_home.Reportbut_2.clicked.connect(self.go_to_reports)
            print("✓ Connected Reportbut_2")

        if hasattr(self.admin_home, "Settbut_2"):
            self.admin_home.Settbut_2.clicked.connect(self.go_to_logout)
            print("✓ Connected Settbut_2")

        # Quick action buttons (admin-specific - don't change these)
        if hasattr(self.admin_home, "s1"):
            self.admin_home.s1.clicked.connect(self.go_to_logout)
            print("✓ Connected s1")

        if hasattr(self.admin_home, "b1"):
            self.admin_home.b1.clicked.connect(self.go_to_dashboard)
            print("✓ Connected b1 (Go to Dashboard)")

        if hasattr(self.admin_home, "b4"):
            self.admin_home.b4.clicked.connect(self.go_to_orders)
            print("✓ Connected b4 (Manage Orders)")

        # THESE BUTTONS ARE MISSING IN AHControl BUT EXIST IN SHControl:
        if hasattr(self.admin_home, "h1"):
            self.admin_home.h1.clicked.connect(self.go_to_home)
            print("✓ Connected h1")

        if hasattr(self.admin_home, "db1"):
            self.admin_home.db1.clicked.connect(self.go_to_dashboard)
            print("✓ Connected db1")

        if hasattr(self.admin_home, "o1"):
            self.admin_home.o1.clicked.connect(self.go_to_orders)
            print("✓ Connected o1")

        if hasattr(self.admin_home, "r1"):
            self.admin_home.r1.clicked.connect(self.go_to_reports)
            print("✓ Connected r1")

        if hasattr(self.admin_home, "u1"):
            self.admin_home.u1.clicked.connect(self.go_to_users)
            print("✓ Connected u1")

        # Admin-specific button (Create Staff)
        if hasattr(self.admin_home, "b3"):
            self.admin_home.b3.clicked.connect(self.go_to_createstaff)
            print("✓ Connected b3 (Create Staff)")

        # These buttons might exist but weren't connected in AHControl:
        if hasattr(self.admin_home, "b5"):
            self.admin_home.b5.clicked.connect(self.go_to_view_contents)
            print("✓ Connected b5 (View Contents)")

        if hasattr(self.admin_home, "b2"):
            self.admin_home.b2.clicked.connect(self.view_profile_details)
            print("✓ Connected b2 (View Profile Details)")

        print("✓ All home buttons connected successfully")

    def go_to_home(self):
        print("✓ Navigating to Home")
        self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.home_page_index)
        # The on_page_changed signal will handle refreshing automatically

    def go_to_dashboard(self):
        print("✓ Navigating to Dashboard")
        self.dashboard.show()

    def go_to_users(self):
        print("✓ Navigating to Users")
        self.maneger.show()

    def go_to_orders(self):
        print("✓ Navigating to Orders")
        self.order.show()

    def go_to_reports(self):
        print("✓ Navigating to Reports")
        self.report.show()

    def go_to_createstaff(self):
        print("✓ Navigating to Create Staff")
        self.cstaff.show()

    def go_to_create_customer(self):
        print("✓ Navigating to Create Customer")
        # Assuming you have a CreateCustomer page in stackedWidget
        if hasattr(self.admin_home, 'CreateCustomer_page_index'):
            self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.CreateCustomer_page_index)
        else:
            print("✗ CreateCustomer_page_index not found")

    def go_to_view_contents(self):
        print("✓ Viewing Contents")
        QMessageBox.information(self.admin_home, "View Contents",
                                "This feature would show all system contents.\nImplementation depends on your requirements.")

    def view_profile_details(self):
        """Show current admin profile details in popup"""
        try:
            if not self.current_admin_id or not self.model:
                QMessageBox.information(self.admin_home, "Profile Details",
                                        "Profile information not available.")
                return

            # Create popup if it doesn't exist - USE AdminDetailsPopup
            if not self.admin_popup:
                self.admin_popup = AdminDetailsPopup(parent=self.admin_home, model=self.model)

            # Load admin data directly using the ID
            if self.admin_popup.loadAdminFromDatabase(self.current_admin_id):
                # Center popup on parent window
                parent_geo = self.admin_home.geometry()
                popup_geo = self.admin_popup.geometry()
                x = parent_geo.x() + (parent_geo.width() - popup_geo.width()) // 2
                y = parent_geo.y() + (parent_geo.height() - popup_geo.height()) // 2
                self.admin_popup.move(x, y)
                self.admin_popup.show()
                print(f"✓ Showing admin profile popup for AdminID: {self.current_admin_id}")
            else:
                QMessageBox.information(self.admin_home, "Profile Details",
                                        "Could not load profile information.")

        except Exception as e:
            print(f"✗ Error showing profile details: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self.admin_home, "Error",
                                f"Could not load profile details: {str(e)}")

    def format_admin_data(self, db_data):
        """Format admin data for display in popup - same format as staff"""
        from datetime import datetime

        # Build full name
        full_name = f"{db_data.get('EFName', '')}"
        if db_data.get('EMName'):
            full_name += f" {db_data.get('EMName')}"
        full_name += f" {db_data.get('ELName', '')}"

        # Total transactions safely
        total_transactions = db_data.get('total_transactions', 0)
        if total_transactions is None:
            total_transactions = 0
        formatted_transactions = f"₱{float(total_transactions):,.2f}"

        # Date Applied (Member Since)
        member_since = "N/A"
        if db_data.get('SDateApplied'):
            try:
                date_obj = db_data['SDateApplied']
                if isinstance(date_obj, datetime):
                    member_since = date_obj.strftime('%B %d, %Y')
                elif isinstance(date_obj, str):
                    for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%m/%d/%Y']:
                        try:
                            parsed = datetime.strptime(date_obj, fmt)
                            member_since = parsed.strftime('%B %d, %Y')
                            break
                        except ValueError:
                            continue
            except Exception:
                member_since = "N/A"

        # Last Active
        last_active = "Never"
        if db_data.get('LastActiveAt'):
            try:
                date_obj = db_data['LastActiveAt']
                if isinstance(date_obj, str):
                    date_obj = datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')
                if isinstance(date_obj, datetime):
                    days_ago = (datetime.now() - date_obj).days
                    if days_ago == 0:
                        last_active = "Today"
                    elif days_ago == 1:
                        last_active = "Yesterday"
                    else:
                        last_active = f"{days_ago} days ago"
            except Exception:
                last_active = "Never"

        # Get values with defaults
        orders = db_data.get('orders_processed', 0) or 0
        customers = db_data.get('customers_created', 0) or 0

        # Performance summary for recent activity
        recent_activity = f"Last active: {last_active}"

        formatted = {
            'name': full_name.strip(),
            'email': db_data.get('EEmail', 'N/A') or 'N/A',
            'phone': db_data.get('EPhone', 'N/A') or 'N/A',
            'member_since': member_since,
            'orders_processed': orders,
            'deliveries_made': customers,
            'transactions_made': formatted_transactions,
            'recent_activity': recent_activity
        }

        return formatted

    def go_to_logout(self):
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
            print("✓ Logging out...")
            # Clear current admin context
            self.current_admin_id = None
            self.model = None

            # Close admin home
            self.admin_home.close()
            # Clear login fields for security
            self.login_view.username.clear()
            self.login_view.password.clear()
            # Show login view
            self.login_view.show()
            self.login_view.username.setFocus()
        else:
            print("✓ Logout cancelled")