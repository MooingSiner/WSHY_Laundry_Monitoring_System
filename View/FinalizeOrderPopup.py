

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QFont, QFontDatabase, QCursor
from datetime import datetime
import os


class FinalizeOrderPopup(QtWidgets.QWidget):

    # Signal emitted when transaction is completed
    transaction_completed = pyqtSignal(int)  # Emits order_id

    def __init__(self, parent=None, model=None, staff_id=None, ui_file='C:/Users/NITRO/PycharmProjects/Washyy/View/FinalizePopup.ui'):
        super().__init__(parent)

        self.model = model  # Database model instance
        self.staff_id = staff_id  # Current logged-in staff ID
        self.current_order_id = None
        self.current_order_data = None

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
            print(f"Error: UI file '{ui_file}' not found!")
            self.create_basic_ui()

        # Load custom font
        self.load_custom_fonts()

    def load_custom_fonts(self):
        """Load custom Fredoka font"""
        font_path = "C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf"
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                family = QFontDatabase.applicationFontFamilies(font_id)[0]

                # Apply font to all labels
                for obj in self.findChildren(QtWidgets.QLabel):
                    obj.setFont(QFont(family, 10))
                    obj.setFocusPolicy(Qt.FocusPolicy.NoFocus)

                # Apply font to buttons
                button_names = ["b1", "b2", "crt_btn_10", "crt_btn_8"]
                for button_name in button_names:
                    if hasattr(self, button_name):
                        btn = getattr(self, button_name)
                        btn.setFont(QFont(family, 10))

    def set_staff_id(self, staff_id):
        """Set the staff ID for transactions"""
        self.staff_id = staff_id
        print(f"✓ FinalizeOrderPopup: Staff ID set to {staff_id}")

    def format_order_id(self, order_id):
        """Format order ID as WSHY#001, WSHY#002, etc."""
        return f"WSHY#{order_id:03d}"

    def setup_loaded_ui(self):
        """Setup UI elements after loading .ui file"""
        # Connect close button (X in title bar)
        close_button = self.findChild(QtWidgets.QPushButton, "pushButton_close")
        if close_button:
            close_button.clicked.connect(self.close)
            close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            print("✓ Close button (X) connected")

        # Get reference to title label
        self.title_label = self.findChild(QtWidgets.QLabel, "label_title")

        # Get references to all value labels from UI file
        self.value_wash = self.findChild(QtWidgets.QLabel, "value_wash")
        self.label_process = self.findChild(QtWidgets.QLabel, "label_process")
        self.value_procesd = self.findChild(QtWidgets.QLabel, "value_procesd")
        self.label_process_2 = self.findChild(QtWidgets.QLabel, "label_process_2")
        self.label_process_3 = self.findChild(QtWidgets.QLabel, "label_process_3")
        self.value_grand = self.findChild(QtWidgets.QLabel, "value_grand")

        # Get date labels
        self.value_date_picked = self.findChild(QtWidgets.QLabel, "value_date_picked")
        self.value_date_delivered = self.findChild(QtWidgets.QLabel, "value_date")

        # Payment method radio buttons
        self.cash_radio = self.findChild(QtWidgets.QRadioButton, "cash")
        self.card_radio = self.findChild(QtWidgets.QRadioButton, "card")

        # Set default payment method
        if self.cash_radio:
            self.cash_radio.setChecked(True)
            self.cash_radio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            print("✓ Cash radio button found and set as default")

        if self.card_radio:
            self.card_radio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            print("✓ Card radio button found")

        # Connect Complete Transaction button (crt_btn_10)
        self.complete_btn = self.findChild(QtWidgets.QPushButton, "crt_btn_10")
        if self.complete_btn:
            self.complete_btn.clicked.connect(self.complete_transaction)
            self.complete_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            print("✓ Complete Transaction button (crt_btn_10) connected")
        else:
            print("⚠ Complete Transaction button (crt_btn_10) NOT FOUND")

        # Connect Cancel button (crt_btn_8)
        self.cancel_btn = self.findChild(QtWidgets.QPushButton, "crt_btn_8")
        if self.cancel_btn:
            self.cancel_btn.clicked.connect(self.cancel_transaction)
            self.cancel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            print("✓ Cancel button (crt_btn_8) connected")
        else:
            print("⚠ Cancel button (crt_btn_8) NOT FOUND")

        # Alternative button names (b1, b2) if crt_btn doesn't exist
        if not self.complete_btn:
            self.complete_btn = self.findChild(QtWidgets.QPushButton, "b1")
            if self.complete_btn:
                self.complete_btn.clicked.connect(self.complete_transaction)
                self.complete_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                print("✓ Complete Transaction button (b1) connected")

        if not self.cancel_btn:
            self.cancel_btn = self.findChild(QtWidgets.QPushButton, "b2")
            if self.cancel_btn:
                self.cancel_btn.clicked.connect(self.cancel_transaction)
                self.cancel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                print("✓ Cancel button (b2) connected")

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
        self.title_bar.setStyleSheet(
            "QFrame { background-color: #3855DB; border-top-left-radius: 18px; border-top-right-radius: 18px; }")

        # Title label
        self.title_label = QtWidgets.QLabel("Finalize Payment - WSHY#000", self.title_bar)
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

        # Content area (simplified for basic UI)
        content = QtWidgets.QWidget(self.container_frame)
        content.setGeometry(20, 60, 440, 320)

        # Complete button
        self.complete_btn = QtWidgets.QPushButton("Complete Transaction", content)
        self.complete_btn.setGeometry(150, 250, 150, 40)
        self.complete_btn.setStyleSheet("""
            QPushButton {
                background-color: #3855DB;
                color: white;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #2746C3; }
        """)
        self.complete_btn.clicked.connect(self.complete_transaction)
        self.complete_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Cancel button
        self.cancel_btn = QtWidgets.QPushButton("Cancel", content)
        self.cancel_btn.setGeometry(20, 250, 100, 40)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9d9;
                color: #333;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #c0c0c0; }
        """)
        self.cancel_btn.clicked.connect(self.cancel_transaction)
        self.cancel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

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

    def loadOrderFromDatabase(self, order_id):
        """Load order data from database using model"""
        if not self.model:
            print("Error: No model provided")
            return False

        order_data = self.model.get_order_by_id(order_id)

        if not order_data:
            print(f"Error: Order {order_id} not found")
            return False

        self.setOrderData(order_data)
        return True

    def setOrderData(self, order_data):
        """Update popup with order data for finalization"""
        # If we receive an order ID instead of a dict, load from database
        if isinstance(order_data, (int, str)) and str(order_data).isdigit():
            return self.loadOrderFromDatabase(int(order_data))

        # Store current order data
        self.current_order_data = order_data
        self.current_order_id = order_data.get('OrderID')

        # Update title
        order_id = order_data.get('OrderID', 'Unknown')
        if self.title_label:
            formatted_id = self.format_order_id(order_id) if isinstance(order_id, int) else order_id
            self.title_label.setText(f"Finalize Payment - {formatted_id}")

        # Calculate totals from services
        total_wash = 0.0
        total_fast_dry = 0.0
        total_iron = 0.0
        total_fold = 0.0

        services = order_data.get('services', [])
        for service in services:
            total_wash += float(service.get('WashAmount', 0))
            total_fast_dry += float(service.get('FastDryAmount', 0))
            total_iron += float(service.get('IronOnlyAmount', 0))
            total_fold += float(service.get('FoldAmount', 0))

        # Display order summary
        if self.value_wash:
            self.value_wash.setText(f"₱{total_wash:.2f}")

        if self.label_process:
            self.label_process.setText(f"₱{total_fast_dry:.2f}")

        if self.label_process_2:
            self.label_process_2.setText(f"₱{total_iron:.2f}")

        if self.label_process_3:
            self.label_process_3.setText(f"₱{total_fold:.2f}")

        # DATE PICKED - Format properly
        if self.value_date_picked:
            date_picked = order_data.get('DatePicked', None)
            if not date_picked:
                date_picked = order_data.get('DatePickUp')

            if date_picked:
                if isinstance(date_picked, str):
                    try:
                        try:
                            date_picked = datetime.strptime(date_picked, '%Y-%m-%d %H:%M:%S')
                        except:
                            date_picked = datetime.strptime(date_picked, '%Y-%m-%d')
                    except:
                        pass

                if isinstance(date_picked, datetime):
                    formatted_date = date_picked.strftime('%B %d, %Y at %I:%M %p')
                    self.value_date_picked.setText(formatted_date)
                else:
                    self.value_date_picked.setText(str(date_picked))
            else:
                self.value_date_picked.setText('Not picked up yet')

        # DATE DELIVERED
        if self.value_date_delivered:
            date_delivered = order_data.get('DateDelivered', None)

            if date_delivered:
                if isinstance(date_delivered, str):
                    try:
                        try:
                            date_delivered = datetime.strptime(date_delivered, '%Y-%m-%d %H:%M:%S')
                        except:
                            date_delivered = datetime.strptime(date_delivered, '%Y-%m-%d')
                    except:
                        pass

                if isinstance(date_delivered, datetime):
                    formatted_date = date_delivered.strftime('%B %d, %Y at %I:%M %p')
                    self.value_date_delivered.setText(formatted_date)
                else:
                    self.value_date_delivered.setText(str(date_delivered))
            else:
                # Show current date/time for new deliveries
                current_date = datetime.now()
                formatted_date = current_date.strftime('%B %d, %Y at %I:%M %p')
                self.value_date_delivered.setText(formatted_date)

        # Grand Total
        if self.value_grand:
            grand_total = float(order_data.get('TotalAmount', 0))
            self.value_grand.setText(f"₱{grand_total:.2f}")

        formatted_id = self.format_order_id(order_id) if isinstance(order_id, int) else order_id
        print(f"✓ FinalizeOrderPopup: Loaded order {formatted_id} for payment")

    def get_selected_payment_method(self):
        """Get the selected payment method"""
        if self.cash_radio and self.cash_radio.isChecked():
            return "Cash"
        elif self.card_radio and self.card_radio.isChecked():
            return "Card"
        return "Cash"  # Default

    def cancel_transaction(self):
        """Cancel the transaction and close popup"""
        reply = QtWidgets.QMessageBox.question(
            self,
            "Cancel Transaction",
            "Are you sure you want to cancel this transaction?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            print("✓ Transaction cancelled by user")
            self.close()

    def complete_transaction(self):
        """Complete the transaction and mark order as completed"""
        print("✓ Complete Transaction button clicked")

        if not self.current_order_id or not self.current_order_data:
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                "No order data available to complete transaction."
            )
            return

        if not self.model:
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                "Database model not available."
            )
            return

        # Get payment details
        payment_method = self.get_selected_payment_method()
        amount_paid = float(self.current_order_data.get('TotalAmount', 0))

        try:
            print(f"✓ Processing transaction: OrderID={self.current_order_id}, "
                  f"Amount={amount_paid}, Method={payment_method}, StaffID={self.staff_id}")

            # Add transaction to database
            transaction_id = self.model.add_transaction(
                order_id=self.current_order_id,
                amount_paid=amount_paid,
                payment_method=payment_method,
                staff_id=self.staff_id
            )

            if transaction_id:
                # Update order status to Completed
                success = self.model.update_order_status(self.current_order_id, 'Completed')

                # Update staff last active timestamp
                if self.staff_id:
                    self.model.update_staff_last_active(self.staff_id)

                # ✅ LOG ACTIVITY
                if self.staff_id:
                    customer_id = self.current_order_data.get('CustomerID')
                    self.model.log_staff_activity(
                        staff_id=self.staff_id,
                        activity_type='COMPLETE_TRANSACTION',
                        order_id=self.current_order_id,
                        customer_id=customer_id
                    )

                if success:
                    formatted_id = self.format_order_id(self.current_order_id)
                    print(f"✓ Transaction completed: OrderID={self.current_order_id}, "
                          f"TransactionID={transaction_id}, StaffID={self.staff_id}")

                    # Show success message
                    QtWidgets.QMessageBox.information(
                        self,
                        "Transaction Complete",
                        f"Order {formatted_id} has been completed successfully!\n\n"
                        f"Amount Paid: ₱{amount_paid:.2f}\n"
                        f"Payment Method: {payment_method}"
                    )

                    # Emit signal that transaction is completed
                    self.transaction_completed.emit(self.current_order_id)

                    # Close the popup
                    self.close()
                else:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Warning",
                        f"Transaction recorded (ID: {transaction_id}), but failed to update order status."
                    )
            else:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Error",
                    "Failed to complete transaction. Please try again."
                )

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"An error occurred while completing the transaction:\n{str(e)}"
            )
            print(f"✗ Error completing transaction: {e}")
            import traceback
            traceback.print_exc()


# Standalone test
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    # Mock data for testing
    mock_order = {
        'OrderID': 1,
        'OrderDate': datetime.now(),
        'DatePicked': datetime(2025, 12, 14, 10, 30, 0),
        'DateDelivered': datetime(2025, 12, 15, 14, 45, 0),
        'Status': 'Processing',
        'customer_name': 'John Doe',
        'CustomerID': 1,
        'TotalAmount': 850.00,
        'services': [
            {
                'ServiceName': 'Wash & Dry',
                'WeightKg': 5.0,
                'PriceperKG': 100.00,
                'WashAmount': 500.00,
                'FastDry': True,
                'FastDryAmount': 280.00,
                'IronOnly': False,
                'IronOnlyAmount': 0.00,
                'Fold': True,
                'FoldAmount': 70.00,
                'TotalAmount': 850.00
            }
        ]
    }

    popup = FinalizeOrderPopup(staff_id=1)
    popup.setOrderData(mock_order)
    popup.show()

    sys.exit(app.exec())