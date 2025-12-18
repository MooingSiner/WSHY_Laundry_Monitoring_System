"""
StaffDetailsPopup.py
Draggable popup window for displaying staff details
Loads UI from StaffDetailPopup.ui created in Qt Designer
Connected to database for real-time staff data
"""
from Model.report_generator import WashyEnhancedReportGenerator
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QFontDatabase, QCursor
from datetime import datetime
import os


class StaffDetailsPopup(QtWidgets.QWidget):
    """
    Draggable popup window for displaying staff details.
    Loads UI from StaffDetailPopup.ui file and fetches data from database.
    """

    def __init__(self, parent=None, model=None, ui_file='C:/Users/NITRO/PycharmProjects/Washyy/View/StaffDetailPopup.ui'):
        super().__init__(parent)

        self.model = model  # Database model instance
        self.current_order_id = None
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

        # Load custom font
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            # Apply font to heading labels only
            for label_name in ['label_personal_info', 'label_order_stats', 'label_recent_activity']:
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
            self.print.clicked.connect(self.print_staff_pdf)
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
        self.order_process_value = self.findChild(QtWidgets.QLabel, "value_order_process")
        self.deliv_made_value = self.findChild(QtWidgets.QLabel, "value_deliv_made")
        self.last_order_value = self.findChild(QtWidgets.QLabel, "value_last_order")
        self.recent_activity_value = self.findChild(QtWidgets.QLabel, "value_recent_activity")

        # Make all value labels visible
        all_value_labels = [
            self.email_value,
            self.phone_value,
            self.member_since_value,
            self.order_process_value,
            self.deliv_made_value,
            self.last_order_value,
            self.recent_activity_value
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
        self.title_label = QtWidgets.QLabel("Staff Details", self.title_bar)
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

    def loadStaffFromDatabase(self, staff_id):
        """Load staff data from database using model"""
        self.current_staff_id = staff_id
        if not self.model:
            print("Error: No model provided")
            return False

        staff_data = self.model.get_staff_by_id(staff_id)

        if not staff_data:
            print(f"Error: Staff {staff_id} not found")
            return False

        formatted_data = self.format_staff_data(staff_data)
        self.setStaffData(formatted_data)
        return True

    def print_staff_pdf(self):
        """Generate PDF report for current staff"""
        if not self.current_staff_id:
            QtWidgets.QMessageBox.warning(
                self,
                "No Staff",
                "No staff member loaded to print."
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

            success = report_gen.generate_staff_report(self.current_staff_id)

            QtWidgets.QApplication.restoreOverrideCursor()

            if success:
                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    "Staff report generated successfully!\n\nLocation: Current directory"
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

    def format_staff_data(self, db_data):
        """Format database data for popup"""
        # Build full name
        full_name = f"{db_data.get('EFName', '')}"
        if db_data.get('EMName'):
            full_name += f" {db_data.get('EMName')}"
        full_name += f" {db_data.get('ELName', '')}"

        # FIXED: Total transactions - already filtered by completed orders in SQL
        total_transactions = db_data.get('total_transactions', 0)
        if total_transactions is None:
            total_transactions = 0

        # FIXED: Convert to float safely
        try:
            if isinstance(total_transactions, (int, float)):
                total_transactions_float = float(total_transactions)
            else:
                # Try to convert string to float
                total_transactions_float = float(str(total_transactions).replace(',', '').replace('₱', ''))
        except (ValueError, TypeError):
            total_transactions_float = 0.0

        formatted_transactions = f"₱{total_transactions_float:,.2f}"

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
                    else:
                        member_since = str(date_obj)
                else:
                    member_since = str(date_obj)
            except Exception:
                member_since = "N/A"

        # Last Active with time
        last_active = "Never"
        if db_data.get('LastActiveAt'):
            try:
                date_obj = db_data['LastActiveAt']
                if isinstance(date_obj, str):
                    date_obj = datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')
                if isinstance(date_obj, datetime):
                    days_ago = (datetime.now() - date_obj).days
                    if days_ago == 0:
                        # Today - show time
                        last_active = f"Today at {date_obj.strftime('%I:%M %p')}"
                    elif days_ago == 1:
                        # Yesterday - show time
                        last_active = f"Yesterday at {date_obj.strftime('%I:%M %p')}"
                    elif days_ago < 7:
                        # Within a week - show day and time
                        last_active = f"{date_obj.strftime('%A at %I:%M %p')}"
                    else:
                        # More than a week - show date and time
                        last_active = f"{date_obj.strftime('%b %d at %I:%M %p')}"
            except Exception:
                last_active = "Never"

        # Get values with defaults
        orders = db_data.get('orders_processed', 0) or 0
        customers = db_data.get('customers_created', 0) or 0
        transactions_count = db_data.get('transactions_count', 0) or 0

        # Performance summary for recent activity
        recent_activity = f" {last_active}"

        formatted = {
            'name': full_name.strip(),
            'email': db_data.get('EEmail', 'N/A') or 'N/A',
            'phone': db_data.get('EPhone', 'N/A') or 'N/A',
            'member_since': member_since,
            'orders_processed': orders,
            'deliveries_made': customers,  # Using customers_created for deliveries
            'transactions_made': formatted_transactions,
            'recent_activity': recent_activity
        }

        return formatted

    def setStaffData(self, staff_dict_or_id):
        """Update popup with staff data

        Args:
            staff_dict_or_id: Either a dict with staff data, or an integer staff ID
        """
        # If we receive a staff ID instead of a dict, load from database
        if isinstance(staff_dict_or_id, (int, str)) and str(staff_dict_or_id).isdigit():
            return self.loadStaffFromDatabase(int(staff_dict_or_id))

        staff_dict = staff_dict_or_id

        # Update title
        if self.title_label:
            self.title_label.setText(staff_dict.get('name', 'Unknown Staff'))
            self.title_label.setVisible(True)

        # Update email
        if self.email_value:
            self.email_value.setText(staff_dict.get('email', 'N/A'))
            self.email_value.setVisible(True)

        # Update phone
        if self.phone_value:
            self.phone_value.setText(staff_dict.get('phone', 'N/A'))
            self.phone_value.setVisible(True)

        # Update member since (Date Applied)
        if self.member_since_value:
            self.member_since_value.setText(staff_dict.get('member_since', 'N/A'))
            self.member_since_value.setVisible(True)

        # Update orders processed
        if self.order_process_value:
            self.order_process_value.setText(str(staff_dict.get('orders_processed', 0)))
            self.order_process_value.setVisible(True)

        # Update deliveries made
        if self.deliv_made_value:
            self.deliv_made_value.setText(str(staff_dict.get('deliveries_made', 0)))
            self.deliv_made_value.setVisible(True)

        # Update transactions made
        if self.last_order_value:
            self.last_order_value.setText(staff_dict.get('transactions_made', '₱0.00'))
            self.last_order_value.setVisible(True)

        # Update recent activity
        if self.recent_activity_value:
            self.recent_activity_value.setText(staff_dict.get('recent_activity', 'No activity'))
            self.recent_activity_value.setVisible(True)

        # Make all section labels visible
        section_labels = [
            self.findChild(QtWidgets.QLabel, "label_personal_info"),
            self.findChild(QtWidgets.QLabel, "label_email"),
            self.findChild(QtWidgets.QLabel, "label_phone"),
            self.findChild(QtWidgets.QLabel, "label_dateap"),
            self.findChild(QtWidgets.QLabel, "label_order_stats"),
            self.findChild(QtWidgets.QLabel, "label_order_process"),
            self.findChild(QtWidgets.QLabel, "label_deliv_made"),
            self.findChild(QtWidgets.QLabel, "label_transact_made"),
            self.findChild(QtWidgets.QLabel, "label_recent_activity")
        ]

        for label in section_labels:
            if label:
                label.setVisible(True)

        print(f"✓ StaffDetailsPopup: Loaded staff {staff_dict.get('name', 'Unknown')}")

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
    mock_staff = {
        'name': 'John Smith',
        'email': 'john.smith@washy.com',
        'phone': '+1 234-567-8900',
        'member_since': 'January 15, 2024',
        'orders_processed': 150,
        'deliveries_made': 45,
        'transactions_made': '₱75,000.00',
        'recent_activity': 'Last active: Today'
    }

    popup = StaffDetailsPopup()
    popup.setStaffData(mock_staff)
    popup.show()

    sys.exit(app.exec())