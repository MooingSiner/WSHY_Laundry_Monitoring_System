import os

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QFontDatabase, QPixmap, QPainter, QFont
from datetime import datetime
import Model.Resc_rc



class AdminHome(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the main UI file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "AdminMainWindow.ui")
        uic.loadUi(ui_path, self)

        # Load image from QRC resource
        self.image = QPixmap(":/images/4.png")

        # Get page indices by finding widgets by objectName
        self.home_page_index = self.find_page_index("AH")
        self.dashboard_page_index = self.find_page_index("ADB")
        self.users_page_index = self.find_page_index("US")
        self.manegerc_page_index = self.find_page_index("USE")
        self.CreateStaff_page_index = self.find_page_index("CreateStaff")
        self.order_page_index = self.find_page_index("ManageOrder")
        self.report_page_index = self.find_page_index("History")
        self.CreateCustomer_page_index = self.find_page_index("CreateCustomer")
        self.EditStaff_page_index = self.find_page_index("EditStaff")
        self.EditCustomer_page_index = self.find_page_index("EditCustomer")

        # Database model (will be set after login)
        self.model = None

        # Current admin ID (will be set by login)
        self.current_admin_id = None

        self.setup_ui()

        print(f"✓ AdminHome initialized with {self.stackedWidget.count()} pages")
        print(f"✓ Home page index: {self.home_page_index}")

    def get_admin_id(self):
        """Get current admin ID"""
        return self.current_admin_id

    def find_page_index(self, object_name):
        """Find stacked widget page index by object name"""
        for i in range(self.stackedWidget.count()):
            widget = self.stackedWidget.widget(i)
            if widget.objectName() == object_name:
                print(f"✓ Found {object_name} at index {i}")
                return i
        print(f"✗ Could not find {object_name}")
        return 0

    def set_admin_context(self, admin_id, model):
        """Set current admin ID and model after login"""
        self.current_admin_id = admin_id
        self.model = model
        print(f"✓ AdminHome: Admin context set - AdminID={admin_id}")

    def refresh_home_data(self):
        """Public method to refresh home data (can be called externally)"""
        self.load_home_data()  # Call the actual method

    def setup_ui(self):
        # Logo
        icon = QLabel(self)
        icon.setPixmap(QPixmap("C:/Users/NITRO/PycharmProjects/Washyy/images/logo2.png").scaled(64, 76))
        icon.setGeometry(40, 32, 80, 80)

        # Washy label
        label = QLabel("Washy", self)
        label.setGeometry(110, 35, 150, 80)
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-Bold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            label.setFont(QFont(family, 22))
            if hasattr(self, "ok"):
                ok = getattr(self, "ok")
                ok.setFont(QFont(family, 30))
                ok.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Sidebar button fonts
        sidebar_buttons = ["Homebut_2", "Userbut_2", "Orderbut_2", "Settbut_2",
                           "Reportbut_2", "Dashbut_2"]
        for name in sidebar_buttons:
            if hasattr(self, name):
                btn = getattr(self, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Other buttons
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            other_buttons = ["b1", "b2", "b3", "b4", "b5"]
            for button in other_buttons:
                if hasattr(self, button):
                    btn = getattr(self, button)
                    btn.setFont(QFont(family, 10))
        if font_id!= -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            other_label = ["l6","label_31","label_29","label_16","l2_3"]
            for label in other_label:
                if hasattr(self, label):
                    lb = getattr(self, label)
                    lb.setFont(QFont(family, 11))

        if hasattr(self, "label_16"):
            label = getattr(self, "label_16")
            label.setFont(QFont("Arial", 11))

    # In AdminHomeView.py - REPLACE the load_home_data method with this:

    def load_home_data(self):
        """Load order analytics and pending approvals data"""
        print("🔵 ADMIN load_home_data() CALLED!")  # Debug line
        try:
            # Check if model is available
            if not self.model:
                print("✗ Cannot load home data: Model not set")
                return

            print(f"🔵 Model is available: {self.model}")  # Debug line
            print(f"🔵 Current admin ID: {self.current_admin_id}")  # Debug line

            # Get today's date
            today = datetime.now().strftime("%Y-%m-%d")

            # Get order statistics
            stats = self.get_order_statistics()
            print(f"🔵 Stats returned: {stats}")  # Debug line

            if stats:
                # Update order analytics section
                if hasattr(self, "tert1"):  # Completed Today
                    self.tert1.setText(str(stats.get('completed_today', 0)))
                    print(f"✓ Updated completed today: {stats.get('completed_today', 0)}")
                else:
                    print("⚠️ Widget 'tert1' not found")

                if hasattr(self, "tert1_3"):  # Pending Issues
                    print(f"🔵 About to update tert1_3 with: {stats.get('pending_issues', 0)}")
                    self.tert1_3.setText(str(stats.get('pending_issues', 0)))
                    print(f"✓ Updated pending issues: {stats.get('pending_issues', 0)}")
                    print(f"🔵 Widget text is now: {self.tert1_3.text()}")
                else:
                    print("⚠️ Widget 'tert1_3' not found")

                # Update pending approvals section
                if hasattr(self, "tert4_4"):  # Pending Delivery
                    self.tert4_4.setText(str(stats.get('pending_delivery', 0)))
                    print(f"✓ Updated pending delivery: {stats.get('pending_delivery', 0)}")
                else:
                    print("⚠️ Widget 'pendingdel_value_2' not found")

                if hasattr(self, "label_34"):  # Pending Pickup
                    self.label_34.setText(str(stats.get('pending_pickup', 0)))
                    print(f"✓ Updated pending pickup: {stats.get('pending_pickup', 0)}")
                else:
                    print("⚠️ Widget 'pendingpick_value_2' not found")

                # Update profile section with admin name
                if hasattr(self, "label_29") and self.current_admin_id:
                    self.update_profile_name()

        except Exception as e:
            import traceback
            print(f"✗ Error loading home data: {e}")
            traceback.print_exc()

    def get_order_statistics(self):
        """Get order statistics for the home page"""
        print("🔵 ADMIN get_order_statistics() CALLED!")  # Debug line
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
            result = cursor.fetchone()
            completed_today = result['completed_today'] if result else 0
            print(f"🔵 Query 1 - Completed today: {completed_today}")

            # 2. Get pending issues (orders not completed AND not cancelled)
            query2 = """
                     SELECT COUNT(*) as pending_issues
                     FROM Orders
                     WHERE Status NOT IN ('Completed', 'Cancelled')
                     """
            print(f"🔵 Executing query 2: {query2}")
            cursor.execute(query2)
            result = cursor.fetchone()
            pending_issues = result['pending_issues'] if result else 0
            print(f"🔵 Query 2 - Pending issues: {pending_issues}")

            # 3. Get pending delivery orders (exclude cancelled)
            cursor.execute("""
                           SELECT COUNT(*) as pending_delivery
                           FROM Orders
                           WHERE (Status = 'Ready for Delivery' OR Status = 'Processing')
                             AND Status != 'Cancelled'
                           """)
            result = cursor.fetchone()
            pending_delivery = result['pending_delivery'] if result else 0
            print(f"🔵 Query 3 - Pending delivery: {pending_delivery}")

            # 4. Get pending pickup orders (exclude cancelled)
            cursor.execute("""
                           SELECT COUNT(*) as pending_pickup
                           FROM Orders
                           WHERE Status = 'Pending'
                           """)
            result = cursor.fetchone()
            pending_pickup = result['pending_pickup'] if result else 0
            print(f"🔵 Query 4 - Pending pickup: {pending_pickup}")

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
            import traceback
            print(f"✗ Error getting order statistics: {e}")
            traceback.print_exc()
            return {
                'completed_today': 0,
                'pending_issues': 0,
                'pending_delivery': 0,
                'pending_pickup': 0
            }

    def update_profile_name(self):
        """Update the profile name with admin information"""
        try:
            if not self.current_admin_id or not self.model:
                return

            # Get admin information
            admin_info = self.model.get_staff_by_id(self.current_admin_id)
            if admin_info:
                # Update profile name
                name = f"{admin_info.get('EFName', '')} {admin_info.get('ELName', '')}"
                if name.strip():
                    self.label_29.setText(name.strip())
                    print(f"✓ Updated profile name: {name.strip()}")
                else:
                    self.label_29.setText("Admin Profile")

        except Exception as e:
            print(f"✗ Error updating profile name: {e}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.width(), self.height(), self.image)
        painter.end()