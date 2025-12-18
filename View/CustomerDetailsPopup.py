"""
CustomerDetailsPopup.py
Draggable popup window for displaying customer details
Loads UI from CustomerDetailsPopup.ui created in Qt Designer
Connected to database for real-time customer data
"""
from Model.report_generator import WashyEnhancedReportGenerator
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QFontDatabase, QCursor
from datetime import datetime
import os


class CustomerDetailsPopup(QtWidgets.QWidget):
    """
    Draggable popup window for displaying customer details.
    Loads UI from CustomerDetailsPopup.ui file and fetches data from database.
    """

    def __init__(self, parent=None, model=None, ui_file='C:/Users/NITRO/PycharmProjects/Washyy/View/CustomerDetailsPopup.ui'):
        super().__init__(parent)

        self.model = model  # Database model instance
        self.current_customer_id = None
        # Make window frameless and stay on top
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Dragging variables
        self.dragging = False
        self.drag_position = QPoint()

        # Load UI file
        if os.path.exists(ui_file):
            uic.loadUi(ui_file, self)
            self.setup_loaded_ui()
        else:
            self.create_basic_ui()

        # Load custom font - Apply to heading labels only (matching StaffDetailsPopup)
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            # Apply font to heading labels only
            for label_name in ['label_personal_info', 'label_order_stats', 'label_order_history']:
                label = self.findChild(QtWidgets.QLabel, label_name)
                if label:
                    label.setFont(QFont(family, 10))
                    label.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            other_buttons = ["print"]
            for fbut in other_buttons:
                if hasattr(self, fbut):
                    but = getattr(self, fbut)
                    but.setFont(QFont(family, 10))
                    but.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        if hasattr(self, 'print'):
            self.print.clicked.connect(self.print_customer_pdf)
            self.print.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def setup_loaded_ui(self):
        """Setup UI elements after loading .ui file"""
        # Connect close button
        if hasattr(self, 'pushButton_close'):
            self.pushButton_close.clicked.connect(self.close)
            self.pushButton_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Get reference to title label
        self.title_label = self.findChild(QtWidgets.QLabel, "label_title")

        # Get references to all value labels from UI file
        self.email_value = self.findChild(QtWidgets.QLabel, "value_email")
        self.phone_value = self.findChild(QtWidgets.QLabel, "value_phone")
        self.member_since_value = self.findChild(QtWidgets.QLabel, "value_member_since")
        self.total_orders_value = self.findChild(QtWidgets.QLabel, "value_total_orders")
        self.total_spent_value = self.findChild(QtWidgets.QLabel, "value_total_spent")
        self.last_order_value = self.findChild(QtWidgets.QLabel, "value_last_order")
        self.recent_activity_value = self.findChild(QtWidgets.QLabel, "value_recent_activity")

        # Try both possible names for addresses label
        self.addresses_value = self.findChild(QtWidgets.QLabel, "value_Addresses")
        if not self.addresses_value:
            self.addresses_value = self.findChild(QtWidgets.QLabel, "value_addresses")

        # Make all value labels visible
        all_value_labels = [
            self.email_value,
            self.phone_value,
            self.member_since_value,
            self.total_orders_value,
            self.total_spent_value,
            self.last_order_value,
            self.recent_activity_value,
            self.addresses_value
        ]

        for label in all_value_labels:
            if label:
                label.setVisible(True)
                label.raise_()

    def create_basic_ui(self):
        """Create basic UI if .ui file is not found"""
        self.setFixedSize(500, 450)
        self.container_frame = QtWidgets.QFrame(self)
        self.container_frame.setGeometry(10, 10, 480, 430)
        self.container_frame.setStyleSheet("""
            QFrame { background-color: white; border: 2px solid #3855DB; border-radius: 20px; }
        """)

        # Title bar
        self.title_bar = QtWidgets.QFrame(self.container_frame)
        self.title_bar.setGeometry(0, 0, 480, 50)
        self.title_bar.setStyleSheet("QFrame { background-color: #3855DB; border-top-left-radius: 18px; border-top-right-radius: 18px; }")

        # Title label
        self.title_label = QtWidgets.QLabel("Customer Details", self.title_bar)
        self.title_label.setGeometry(20, 10, 440, 30)
        self.title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

        # Close button
        self.pushButton_close = QtWidgets.QPushButton("✕", self.title_bar)
        self.pushButton_close.setGeometry(440, 10, 30, 30)
        self.pushButton_close.setStyleSheet("""
            QPushButton { background-color: transparent; color: white; font-size: 20px; border: none; }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.2); border-radius: 15px; }
        """)
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Content area
        self.content_widget = QtWidgets.QWidget(self.container_frame)
        self.content_widget.setGeometry(10, 60, 461, 361)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.pos().y() < 60:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def loadCustomerFromDatabase(self, customer_id):
        """Load customer data from database using model"""
        self.current_customer_id = customer_id
        if not self.model:
            return False

        customer_data = self.model.get_customer_by_id(customer_id)

        if not customer_data:
            return False

        formatted_data = self.format_customer_data(customer_data, customer_id)
        self.setCustomerData(formatted_data)
        return True

    def format_customer_data(self, db_data, customer_id):
        """Format database data for popup"""
        # Build full name
        full_name = f"{db_data.get('CFName', '')}"
        if db_data.get('CMName'):
            full_name += f" {db_data.get('CMName')}"
        full_name += f" {db_data.get('CLName', '')}"

        # Total spent safely
        total_spent = db_data.get('total_spent', 0)
        if total_spent is None:
            total_spent = 0
        formatted_spent = f"₱{float(total_spent):,.2f}"

        # Member Since - Enhanced date handling
        member_since = "N/A"
        date_created = db_data.get('DateCreated')

        if date_created:
            try:
                if isinstance(date_created, datetime):
                    member_since = date_created.strftime('%B %d, %Y')
                elif isinstance(date_created, str):
                    formats = [
                        '%Y-%m-%d %H:%M:%S',
                        '%Y-%m-%d',
                        '%m/%d/%Y %H:%M:%S',
                        '%m/%d/%Y',
                        '%d/%m/%Y',
                    ]
                    for fmt in formats:
                        try:
                            date_obj = datetime.strptime(date_created, fmt)
                            member_since = date_obj.strftime('%B %d, %Y')
                            break
                        except ValueError:
                            continue
                    else:
                        member_since = str(date_created)
                else:
                    member_since = str(date_created)
            except Exception:
                member_since = "N/A"

        # Last order
        last_order = "No orders yet"
        if db_data.get('last_order_date'):
            try:
                date_obj = db_data['last_order_date']
                if isinstance(date_obj, str):
                    date_obj = datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')
                if isinstance(date_obj, datetime):
                    days_ago = (datetime.now() - date_obj).days
                    if days_ago == 0:
                        last_order = "Today"
                    elif days_ago == 1:
                        last_order = "Yesterday"
                    else:
                        last_order = f"{days_ago} days ago"
            except Exception:
                last_order = "Error"

        # Recent Order info
        total_orders = db_data.get('total_orders', 0) or 0
        completed_orders = db_data.get('completed_orders', 0) or 0
        pending_orders = db_data.get('pending_orders', 0) or 0
        recent_order = f"{completed_orders} completed, {pending_orders} pending"

        # Get customer addresses from database
        addresses_text = "No addresses on file"
        if self.model:
            try:
                addresses = self.model.get_customer_addresses(customer_id)

                if addresses:
                    address_list = []
                    for addr in addresses:
                        parts = []
                        if addr.get('StreetAdd'):
                            parts.append(addr['StreetAdd'])
                        if addr.get('AppartUnit'):
                            parts.append(addr['AppartUnit'])
                        if addr.get('City'):
                            parts.append(addr['City'])
                        if addr.get('ZipCode'):
                            parts.append(str(addr['ZipCode']))

                        if parts:
                            address_list.append(", ".join(parts))

                    if address_list:
                        addresses_text = " | ".join(address_list)
            except Exception:
                addresses_text = "Error loading addresses"

        formatted = {
            'name': full_name.strip(),
            'email': db_data.get('CEmail', 'N/A') or 'N/A',
            'phone': db_data.get('CPhone', 'N/A'),
            'total_orders': total_orders,
            'total_spent': formatted_spent,
            'member_since': member_since,
            'last_order': last_order,
            'recent_order': recent_order,
            'addresses': addresses_text
        }

        return formatted

    def setCustomerData(self, customer_dict_or_id):
        """Update popup with customer data

        Args:
            customer_dict_or_id: Either a dict with customer data, or an integer customer ID
        """
        # If we receive a customer ID instead of a dict, load from database
        if isinstance(customer_dict_or_id, (int, str)) and str(customer_dict_or_id).isdigit():
            return self.loadCustomerFromDatabase(int(customer_dict_or_id))

        customer_dict = customer_dict_or_id

        if self.title_label:
            self.title_label.setText(customer_dict.get('name', 'Unknown Customer'))
            self.title_label.setVisible(True)

        if self.email_value:
            email_text = customer_dict.get('email', 'N/A')
            self.email_value.setText(email_text if email_text else 'N/A')
            self.email_value.setVisible(True)

        if self.phone_value:
            self.phone_value.setText(customer_dict.get('phone', 'N/A'))
            self.phone_value.setVisible(True)

        if self.member_since_value:
            self.member_since_value.setText(customer_dict.get('member_since', 'N/A'))
            self.member_since_value.setVisible(True)

        if self.total_orders_value:
            self.total_orders_value.setText(str(customer_dict.get('total_orders', 0)))
            self.total_orders_value.setVisible(True)

        if self.total_spent_value:
            self.total_spent_value.setText(customer_dict.get('total_spent', '₱0.00'))
            self.total_spent_value.setVisible(True)

        if self.last_order_value:
            self.last_order_value.setText(customer_dict.get('last_order', 'No orders yet'))
            self.last_order_value.setVisible(True)

        if self.recent_activity_value:
            self.recent_activity_value.setText(customer_dict.get('recent_order', 'No recent orders'))
            self.recent_activity_value.setVisible(True)

        if self.addresses_value:
            address_text = customer_dict.get('addresses', 'No addresses on file')
            self.addresses_value.setText(address_text)
            self.addresses_value.setVisible(True)
            self.addresses_value.update()
            self.addresses_value.raise_()

        # Make all section labels visible
        section_labels = [
            self.findChild(QtWidgets.QLabel, "label_personal_info"),
            self.findChild(QtWidgets.QLabel, "label_email"),
            self.findChild(QtWidgets.QLabel, "label_phone"),
            self.findChild(QtWidgets.QLabel, "label_member_since"),
            self.findChild(QtWidgets.QLabel, "label_order_stats"),
            self.findChild(QtWidgets.QLabel, "label_total_orders"),
            self.findChild(QtWidgets.QLabel, "label_total_spent"),
            self.findChild(QtWidgets.QLabel, "label_last_order"),
            self.findChild(QtWidgets.QLabel, "label_recent_order"),
            self.findChild(QtWidgets.QLabel, "label_order_history")
        ]

        for label in section_labels:
            if label:
                label.setVisible(True)

    def print_customer_pdf(self):
        """Generate PDF report for current customer"""
        if not self.current_customer_id:
            QtWidgets.QMessageBox.warning(
                self,
                "No Customer",
                "No customer loaded to print."
            )
            return

        try:
            db_config = {
                'host': 'localhost',
                'user': 'root',
                'password': '',
                'database': 'washy'
            }

            report_gen = WashyEnhancedReportGenerator(db_config)

            # Show progress cursor
            QtWidgets.QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

            success = report_gen.generate_customer_report(self.current_customer_id)

            QtWidgets.QApplication.restoreOverrideCursor()

            if success:
                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    "Customer report generated successfully!\n\nLocation: Current directory"
                )
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    "Failed to generate PDF report."
                )

        except Exception as e:
            QtWidgets.QApplication.restoreOverrideCursor()
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"Error generating report:\n{str(e)}"
            )
            print(f"❌ PDF Error: {e}")
            import traceback
            traceback.print_exc()

    def closeEvent(self, event):
        """Handle popup close event safely"""
        try:
            # Disconnect any signals
            # Clean up references
            self.model = None
            event.accept()
        except:
            event.accept()

    def __del__(self):
        """Destructor - clean up when popup is destroyed"""
        try:
            self.model = None
        except:
            pass


# Standalone test
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    # Mock data for testing
    mock_customer = {
        'name': 'Jane Doe',
        'email': 'jane.doe@email.com',
        'phone': '+1 234-567-8900',
        'member_since': 'March 10, 2024',
        'total_orders': 25,
        'total_spent': '₱45,000.00',
        'last_order': 'Today',
        'recent_order': '20 completed, 5 pending',
        'addresses': '123 Main St, Manila, 1000 | 456 Oak Ave, Quezon City, 1100'
    }

    popup = CustomerDetailsPopup()
    popup.setCustomerData(mock_customer)
    popup.show()

    sys.exit(app.exec())