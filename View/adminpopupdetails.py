"""
AdminDetailsPopup.py
Draggable popup window for displaying admin details
Loads UI from adminpopup.ui created in Qt Designer
Connected to database for real-time admin data
"""

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QFontDatabase, QCursor
from datetime import datetime
import os


class AdminDetailsPopup(QtWidgets.QWidget):
    """
    Draggable popup window for displaying admin details.
    Loads UI from adminpopup.ui file and fetches data from database.
    """

    def __init__(self, parent=None, model=None, ui_file='C:/Users/NITRO/PycharmProjects/Washyy/View/adminpopup.ui'):
        super().__init__(parent)

        self.model = model  # Database model instance

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
        self.title_label = QtWidgets.QLabel("Admin Details", self.title_bar)
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

    def loadAdminFromDatabase(self, admin_id):
        """Load admin data from database using model"""
        if not self.model:
            print("Error: No model provided")
            return False

        admin_data = self.model.get_admin_by_id(admin_id)

        if not admin_data:
            print(f"Error: Admin {admin_id} not found")
            return False

        formatted_data = self.format_admin_data(admin_data)
        self.setAdminData(formatted_data)
        return True

    def format_admin_data(self, db_data):
        """Format database data for popup - Admin specific"""
        # Build full name
        full_name = f"{db_data.get('EFName', '')}"
        if db_data.get('EMName'):
            full_name += f" {db_data.get('EMName')}"
        full_name += f" {db_data.get('ELName', '')}"

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

        # Get values with defaults - Admin specific metrics
        customers_created = db_data.get('customers_created', 0) or 0
        staff_created = db_data.get('staff_created', 0) or 0

        # Performance summary for recent activity
        recent_activity = f"Last active: {last_active}"

        formatted = {
            'name': full_name.strip(),
            'email': db_data.get('EEmail', 'N/A') or 'N/A',
            'phone': db_data.get('EPhone', 'N/A') or 'N/A',
            'member_since': member_since,
            'customers_made': customers_created,
            'staff_made': staff_created,
            'recent_activity': recent_activity
        }

        return formatted

    def setAdminData(self, admin_dict_or_id):
        """Update popup with admin data

        Args:
            admin_dict_or_id: Either a dict with admin data, or an integer admin ID
        """
        # If we receive an admin ID instead of a dict, load from database
        if isinstance(admin_dict_or_id, (int, str)) and str(admin_dict_or_id).isdigit():
            return self.loadAdminFromDatabase(int(admin_dict_or_id))

        admin_dict = admin_dict_or_id

        # Update title
        if self.title_label:
            self.title_label.setText(admin_dict.get('name', 'Unknown Admin'))
            self.title_label.setVisible(True)

        # Update email
        if self.email_value:
            self.email_value.setText(admin_dict.get('email', 'N/A'))
            self.email_value.setVisible(True)

        # Update phone
        if self.phone_value:
            self.phone_value.setText(admin_dict.get('phone', 'N/A'))
            self.phone_value.setVisible(True)

        # Update member since (Date Applied)
        if self.member_since_value:
            self.member_since_value.setText(admin_dict.get('member_since', 'N/A'))
            self.member_since_value.setVisible(True)

        # Update customers made
        if self.order_process_value:
            self.order_process_value.setText(str(admin_dict.get('customers_made', 0)))
            self.order_process_value.setVisible(True)

        # Update staff made
        if self.deliv_made_value:
            self.deliv_made_value.setText(str(admin_dict.get('staff_made', 0)))
            self.deliv_made_value.setVisible(True)

        # Hide the last order value label (not used for admin)
        if self.last_order_value:
            self.last_order_value.setVisible(False)

        # Update recent activity
        if self.recent_activity_value:
            self.recent_activity_value.setText(admin_dict.get('recent_activity', 'No activity'))
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
            self.findChild(QtWidgets.QLabel, "label_recent_activity")
        ]

        for label in section_labels:
            if label:
                label.setVisible(True)

        print(f"✓ AdminDetailsPopup: Loaded admin {admin_dict.get('name', 'Unknown')}")

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
    mock_admin = {
        'name': 'Jane Doe',
        'email': 'jane.doe@washy.com',
        'phone': '+1 234-567-8900',
        'member_since': 'January 1, 2024',
        'customers_made': 50,
        'staff_made': 5,
        'recent_activity': 'Last active: Today'
    }

    popup = AdminDetailsPopup()
    popup.setAdminData(mock_admin)
    popup.show()

    sys.exit(app.exec())
