from PyQt6.QtWidgets import QMessageBox
from datetime import datetime
from View.StaffDetailsPopup import StaffDetailsPopup


class SHControl:
    """Controller for StaffHome page navigation"""

    def __init__(self, staff_home, dashboard, customer, order, delivery, report, login_view):
        self.staff_home = staff_home
        self.dashboard = dashboard
        self.customer = customer
        self.delivery = delivery
        self.order = order
        self.report = report
        self.login_view = login_view

        # Current staff context
        self.current_staff_id = None
        self.model = None  # Will be set from staff_home

        # Staff details popup
        self.staff_popup = None

        # Connect to stackedWidget's page change signal
        if hasattr(self.staff_home, 'stackedWidget'):
            self.staff_home.stackedWidget.currentChanged.connect(self.on_page_changed)
            print("✓ SHControl: Connected to stackedWidget page change signal")

        self.connect_home_buttons()

    def set_staff_context(self, staff_id):
        """Set current staff ID"""
        self.current_staff_id = staff_id

        # Get model from staff_home if available
        if hasattr(self.staff_home, 'model'):
            self.model = self.staff_home.model
            print(f"✓ SHControl: Model acquired from staff_home")

        print(f"✓ SHControl: Staff context set: StaffID = {staff_id}")

        # Initial refresh if we're already on home page
        if hasattr(self.staff_home, 'home_page_index'):
            current_index = self.staff_home.stackedWidget.currentIndex()
            if current_index == self.staff_home.home_page_index:
                self.refresh_home_page()

    def on_page_changed(self, index):
        """Automatically refresh home page when it becomes visible"""
        if hasattr(self.staff_home, 'home_page_index'):
            if index == self.staff_home.home_page_index:
                print("✓ Home page activated - refreshing data")
                self.refresh_home_page()

                # Also update the model reference if needed
                if not self.model and hasattr(self.staff_home, 'model'):
                    self.model = self.staff_home.model

    def refresh_home_page(self):
        """Refresh all data on the home page"""
        try:
            # Get statistics
            stats = self.get_order_statistics()
            if stats:
                # Update order analytics section
                if hasattr(self.staff_home, "tert1"):  # Completed Today
                    self.staff_home.tert1.setText(str(stats.get('completed_today', 0)))
                    print(f"✓ Updated completed today: {stats.get('completed_today', 0)}")

                if hasattr(self.staff_home, "tert1_3"):  # Pending Issues
                    self.staff_home.tert1_3.setText(str(stats.get('pending_issues', 0)))
                    print(f"✓ Updated pending issues: {stats.get('pending_issues', 0)}")

                # Update pending approvals section
                if hasattr(self.staff_home, "pendingdel_value_2"):  # Pending Delivery
                    self.staff_home.pendingdel_value_2.setText(str(stats.get('pending_delivery', 0)))
                    print(f"✓ Updated pending delivery: {stats.get('pending_delivery', 0)}")

                if hasattr(self.staff_home, "pendingpick_value_2"):  # Pending Pickup
                    self.staff_home.pendingpick_value_2.setText(str(stats.get('pending_pickup', 0)))
                    print(f"✓ Updated pending pickup: {stats.get('pending_pickup', 0)}")

            # Update staff profile section
            self.update_profile_section()

            print("✓ Home page data refreshed successfully")

        except Exception as e:
            print(f"✗ Error refreshing home page: {e}")
            import traceback
            traceback.print_exc()

    def get_order_statistics(self):
        """Get order statistics for the home page"""
        try:
            if not self.model:
                print("✗ Model not available for statistics")
                return {
                    'completed_today': 0,
                    'pending_issues': 0,
                    'pending_delivery': 0,
                    'pending_pickup': 0
                }

            # Get today's date
            today = datetime.now().strftime("%Y-%m-%d")

            cursor = self.model.conn.cursor(dictionary=True)

            # 1. Get orders completed today
            cursor.execute("""
                           SELECT COUNT(*) as completed_today
                           FROM Orders
                           WHERE DATE (DateDelivered) = %s AND Status = 'Completed'
                           """, (today,))
            completed_today = cursor.fetchone()['completed_today']

            # 2. Get pending issues (orders not completed AND not cancelled)
            cursor.execute("""
                           SELECT COUNT(*) as pending_issues
                           FROM Orders
                           WHERE Status NOT IN ('Completed', 'Cancelled')
                           """)
            pending_issues = cursor.fetchone()['pending_issues']

            # 3. Get pending delivery orders (exclude cancelled)
            cursor.execute("""
                           SELECT COUNT(*) as pending_delivery
                           FROM Orders
                           WHERE (Status = 'Ready for Delivery' OR Status = 'Processing')
                             AND Status != 'Cancelled'
                           """)
            pending_delivery = cursor.fetchone()['pending_delivery']

            # 4. Get pending pickup orders (exclude cancelled)
            cursor.execute("""
                           SELECT COUNT(*) as pending_pickup
                           FROM Orders
                           WHERE Status = 'Pending'
                           """)
            pending_pickup = cursor.fetchone()['pending_pickup']

            cursor.close()

            print(
                f"✓ Statistics retrieved: Today={completed_today}, Issues={pending_issues}, Delivery={pending_delivery}, Pickup={pending_pickup}")

            return {
                'completed_today': completed_today,
                'pending_issues': pending_issues,
                'pending_delivery': pending_delivery,
                'pending_pickup': pending_pickup
            }

        except Exception as e:
            print(f"✗ Error getting order statistics: {e}")
            return {
                'completed_today': 0,
                'pending_issues': 0,
                'pending_delivery': 0,
                'pending_pickup': 0
            }

    def update_profile_section(self):
        """Update the profile section with staff information"""
        if not self.current_staff_id or not self.model:
            print("✗ Cannot update profile: No staff ID or model")
            return

        try:
            # Get staff information
            staff_info = self.model.get_staff_by_id(self.current_staff_id)
            if staff_info:
                # Update profile name if label exists
                if hasattr(self.staff_home, "label_29"):
                    name = f"{staff_info.get('EFName', '')} {staff_info.get('ELName', '')}"
                    self.staff_home.label_29.setText(name.strip() or "Your Profile")
                    print(f"✓ Updated profile name: {name.strip()}")

                # You could update more profile stats here if you have labels for them

        except Exception as e:
            print(f"✗ Error updating profile section: {e}")

    def connect_home_buttons(self):
        """Connect navigation buttons on the StaffHome page"""
        print("✓ SHControl: Connecting home buttons...")

        # Sidebar buttons
        if hasattr(self.staff_home, "Homebut_2"):
            self.staff_home.Homebut_2.clicked.connect(self.go_to_home)
            print("✓ Connected Homebut_2")

        if hasattr(self.staff_home, "Dashbut_2"):
            self.staff_home.Dashbut_2.clicked.connect(self.go_to_dashboard)
            print("✓ Connected Dashbut_2")

        if hasattr(self.staff_home, "Userbut_2"):
            self.staff_home.Userbut_2.clicked.connect(self.go_to_customer)
            print("✓ Connected Userbut_2")

        if hasattr(self.staff_home, "Orderbut_2"):
            self.staff_home.Orderbut_2.clicked.connect(self.go_to_orders)
            print("✓ Connected Orderbut_2")

        if hasattr(self.staff_home, "Delivlab_2"):
            self.staff_home.Delivlab_2.clicked.connect(self.go_to_delivery)
            print("✓ Connected Delivlab_2")

        if hasattr(self.staff_home, "Settbut_2"):
            self.staff_home.Settbut_2.clicked.connect(self.go_to_logout)
            print("✓ Connected Settbut_2")

        # Quick action buttons
        if hasattr(self.staff_home, "s1"):
            self.staff_home.s1.clicked.connect(self.go_to_logout)
            print("✓ Connected s1")

        if hasattr(self.staff_home, "b1"):
            self.staff_home.b1.clicked.connect(self.go_to_dashboard)
            print("✓ Connected b1 (Go to Dashboard)")

        if hasattr(self.staff_home, "b4"):
            self.staff_home.b4.clicked.connect(self.go_to_orders)
            print("✓ Connected b4 (Manage Orders)")

        if hasattr(self.staff_home, "h1"):
            self.staff_home.h1.clicked.connect(self.go_to_home)
            print("✓ Connected h1")

        if hasattr(self.staff_home, "d1"):
            self.staff_home.d1.clicked.connect(self.go_to_delivery)
            print("✓ Connected d1")

        if hasattr(self.staff_home, "db1"):
            self.staff_home.db1.clicked.connect(self.go_to_dashboard)
            print("✓ Connected db1")

        if hasattr(self.staff_home, "o1"):
            self.staff_home.o1.clicked.connect(self.go_to_orders)
            print("✓ Connected o1")

        if hasattr(self.staff_home, "u1"):
            self.staff_home.u1.clicked.connect(self.go_to_customer)
            print("✓ Connected u1")

        if hasattr(self.staff_home, "b3"):
            self.staff_home.b3.clicked.connect(self.go_to_create_customer)
            print("✓ Connected b3 (New Customer)")

        if hasattr(self.staff_home, "b5"):
            self.staff_home.b5.clicked.connect(self.go_to_view_contents)
            print("✓ Connected b5 (View Contents)")

        if hasattr(self.staff_home, "b2"):
            self.staff_home.b2.clicked.connect(self.view_profile_details)
            print("✓ Connected b2 (View Profile Details)")

        print("✓ All home buttons connected successfully")

    def go_to_home(self):
        print("✓ Navigating to Home")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.home_page_index)
        # The on_page_changed signal will handle refreshing automatically

    def go_to_dashboard(self):
        print("✓ Navigating to Dashboard")
        self.dashboard.show()

    def go_to_customer(self):
        print("✓ Navigating to Customer Management")
        self.customer.show()

    def go_to_orders(self):
        print("✓ Navigating to Orders")
        self.order.show()

    def go_to_reports(self):
        print("✓ Navigating to Reports")
        self.report.show()

    def go_to_delivery(self):
        print("✓ Navigating to Delivery")
        self.delivery.show()

    def go_to_create_customer(self):
        print("✓ Navigating to Create Customer")
        # Assuming you have a CreateCustomer page in stackedWidget
        if hasattr(self.staff_home, 'CreateCustomer_page_index'):
            self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.CreateCustomer_page_index)
        else:
            print("✗ CreateCustomer_page_index not found")

    def go_to_view_contents(self):
        print("✓ Viewing Contents")
        QMessageBox.information(self.staff_home, "View Contents",
                                "This feature would show all system contents.\nImplementation depends on your requirements.")

    def view_profile_details(self):
        """Show current staff profile details in popup"""
        try:
            if not self.current_staff_id or not self.model:
                QMessageBox.information(self.staff_home, "Profile Details",
                                        "Profile information not available.")
                return

            # Create popup if it doesn't exist
            if not self.staff_popup:
                self.staff_popup = StaffDetailsPopup(parent=self.staff_home, model=self.model)

            # Load staff data and show popup
            if self.staff_popup.loadStaffFromDatabase(self.current_staff_id):
                # Center popup on parent window
                parent_geo = self.staff_home.geometry()
                popup_geo = self.staff_popup.geometry()
                x = parent_geo.x() + (parent_geo.width() - popup_geo.width()) // 2
                y = parent_geo.y() + (parent_geo.height() - popup_geo.height()) // 2
                self.staff_popup.move(x, y)
                self.staff_popup.show()
                print(f"✓ Showing staff profile popup for StaffID: {self.current_staff_id}")
            else:
                QMessageBox.information(self.staff_home, "Profile Details",
                                        "Could not load profile information.")

        except Exception as e:
            print(f"✗ Error showing profile details: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self.staff_home, "Error",
                                f"Could not load profile details: {str(e)}")

    def go_to_logout(self):

        # ✅ CRITICAL FIX: Close all popups FIRST, before showing confirmation
        if self.staff_popup:
            try:
                self.staff_popup.hide()
                self.staff_popup.close()
                self.staff_popup.deleteLater()
                self.staff_popup = None
                print("✓ Closed staff popup before logout confirmation")
            except Exception as e:
                print(f"Warning: Error closing staff popup: {e}")

        # NOW show confirmation dialog (no popups blocking it)
        reply = QMessageBox.question(
            self.staff_home,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print("✓ Logging out...")

            # Clear current staff context
            self.current_staff_id = None
            self.model = None

            # Close staff home
            self.staff_home.close()

            # Clear login fields for security
            self.login_view.username.clear()
            self.login_view.password.clear()

            # Show login view
            self.login_view.show()
            self.login_view.username.setFocus()
        else:
            print("✓ Logout cancelled")