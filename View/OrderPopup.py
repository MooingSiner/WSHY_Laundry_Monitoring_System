"""
OrderDetailsPopup.py
Draggable popup window for displaying order details
Loads UI from OrderDetailsPopup.ui created in Qt Designer
Connected to database for real-time order data
"""
from Model.report_generator import WashyEnhancedReportGenerator
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QFontDatabase, QCursor
from PyQt6.QtWidgets import QTableWidgetItem
from datetime import datetime
import os


class OrderDetailsPopup(QtWidgets.QWidget):
    """
    Draggable popup window for displaying order details.
    Loads UI from OrderDetailsPopup.ui file and fetches data from database.
    """
    def __init__(self, parent=None, model=None, ui_file='C:/Users/NITRO/PycharmProjects/Washyy/View/OrderDetailsPopup.ui'):
        super().__init__(parent)
        self.model = model

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
        self.current_order_id = None

        # Load UI file
        if os.path.exists(ui_file):
            uic.loadUi(ui_file, self)
            self.setup_loaded_ui()
        else:
            print(f"Error: UI file '{ui_file}' not found!")
            self.create_basic_ui()

        # Load custom font for headings
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            for label_name in ['label_title', 'label_order_info', 'label_order_items',
                              'label_summary', 'label_grand', 'label_address',
                              'label_personal_info_3', 'label_address_2']:
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
            self.print.clicked.connect(self.print_order_pdf)
            self.print.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            print("✅ Print button connected")

    def format_order_id(self, order_id):
        """Format order ID as WSHY#001, WSHY#002, etc."""
        return f"WSHY#{order_id:03d}"

    def setup_loaded_ui(self):
        """Setup UI elements after loading .ui file"""
        # Connect close button
        if hasattr(self, 'pushButton_close'):
            self.pushButton_close.clicked.connect(self.close)
            self.pushButton_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Get reference to title label
        self.title_label = self.findChild(QtWidgets.QLabel, "label_title")

        # Get references to all value labels from UI file
        self.value_status = self.findChild(QtWidgets.QLabel, "value_status")
        self.value_payment = self.findChild(QtWidgets.QLabel, "value_payment")
        self.value_orderby = self.findChild(QtWidgets.QLabel, "value_orderby")
        self.value_procesd = self.findChild(QtWidgets.QLabel, "value_procesd")
        self.value_address = self.findChild(QtWidgets.QLabel, "value_address")
        self.value_wash = self.findChild(QtWidgets.QLabel, "value_wash")
        self.value_subtotal = self.findChild(QtWidgets.QLabel, "value_subtotal")
        self.value_subtotal_3 = self.findChild(QtWidgets.QLabel, "value_subtotal_3")

        # Date labels
        self.value_datepicked = self.findChild(QtWidgets.QLabel, "value_datepicked")
        self.value_date_deliver = self.findChild(QtWidgets.QLabel, "value_date_deliver")
        self.value_order_created = self.findChild(QtWidgets.QLabel, "value_order_created")

        # Apply Arial font to all value labels
        arial_font = QFont("Arial", 9)
        value_labels = [
            self.value_status, self.value_payment, self.value_orderby,
            self.value_procesd, self.value_address, self.value_wash,
            self.value_subtotal, self.value_subtotal_3, self.value_datepicked,
            self.value_date_deliver, self.value_order_created
        ]

        for label in value_labels:
            if label:
                label.setFont(arial_font)
                label.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Get order table
        self.ordertable = self.findChild(QtWidgets.QTableWidget, "ordertable")
        if self.ordertable:
            self.setup_order_table()

    def setup_order_table(self):
        """Setup the order items table"""
        self.ordertable.setColumnCount(4)
        self.ordertable.setHorizontalHeaderLabels(["Service", "Details", "Unit Price", "Total Amount"])
        self.ordertable.horizontalHeader().setStretchLastSection(True)
        self.ordertable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ordertable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.ordertable.setAlternatingRowColors(True)
        self.ordertable.verticalHeader().setVisible(False)

        # Apply Arial font to table items
        arial_font = QFont("Arial", 9)
        self.ordertable.setFont(arial_font)

        # Apply Arial font to header
        header = self.ordertable.horizontalHeader()
        header.setFont(arial_font)

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
        self.title_label = QtWidgets.QLabel("Order Details WSHY#000", self.title_bar)
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
        """Update popup with order data"""

        # If we receive an order ID instead of a dict, load from database
        if isinstance(order_data, (int, str)) and str(order_data).isdigit():
            return self.loadOrderFromDatabase(int(order_data))

        # Update title
        order_id = order_data.get('OrderID', 'Unknown')
        self.current_order_id = order_id if isinstance(order_id, int) else None
        if self.title_label:
            formatted_id = self.format_order_id(order_id) if isinstance(order_id, int) else order_id
            self.title_label.setText(f"Order Details {formatted_id}")

        # ORDER CREATED DATE
        if self.value_order_created:
            order_date = order_data.get('OrderDate')
            if order_date:
                if isinstance(order_date, str):
                    try:
                        order_date = datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S')
                    except:
                        pass
                if isinstance(order_date, datetime):
                    self.value_order_created.setText(order_date.strftime('%B %d, %Y at %I:%M %p'))
                else:
                    self.value_order_created.setText(str(order_date))
            else:
                self.value_order_created.setText('N/A')

        # DATE PICKED UP
        if self.value_datepicked:
            date_picked = order_data.get('DatePicked')
            if date_picked:
                if isinstance(date_picked, str):
                    try:
                        date_picked = datetime.strptime(date_picked, '%Y-%m-%d %H:%M:%S')
                    except:
                        pass
                if isinstance(date_picked, datetime):
                    self.value_datepicked.setText(date_picked.strftime('%B %d, %Y at %I:%M %p'))
                else:
                    self.value_datepicked.setText(str(date_picked))
            else:
                self.value_datepicked.setText('Not picked up yet')

        # DATE DELIVERED
        if self.value_date_deliver:
            date_delivered = order_data.get('DateDelivered')
            if date_delivered:
                if isinstance(date_delivered, str):
                    try:
                        date_delivered = datetime.strptime(date_delivered, '%Y-%m-%d %H:%M:%S')
                    except:
                        pass
                if isinstance(date_delivered, datetime):
                    self.value_date_deliver.setText(date_delivered.strftime('%B %d, %Y at %I:%M %p'))
                else:
                    self.value_date_deliver.setText(str(date_delivered))
            else:
                self.value_date_deliver.setText('Not delivered yet')

        # STATUS - UPDATED TO INCLUDE CANCELLED
        if self.value_status:
            status = order_data.get('Status', 'Unknown')
            self.value_status.setText(status)
            # Color code the status
            color = {
                'Pending': '#FFA500',
                'Processing': '#3855DB',
                'Completed': '#28A745',
                'Cancelled': '#DC3545'  # Dark red for cancelled
            }.get(status, '#000000')
            self.value_status.setStyleSheet(f"color: {color}; font-weight: bold;")

        # PAYMENT METHOD
        if self.value_payment:
            transactions = order_data.get('transactions', [])
            if transactions and len(transactions) > 0:
                payment_method = transactions[0].get('PaymentMethod', 'N/A')
                self.value_payment.setText(payment_method)
            else:
                self.value_payment.setText('Not paid yet')

        # ORDERED BY
        if self.value_orderby:
            customer_name = order_data.get('customer_name', 'N/A')
            self.value_orderby.setText(customer_name)

        # PROCESSED BY
        if self.value_procesd:
            staff_id = order_data.get('StaffID')
            if staff_id:
                try:
                    staff_data = self.model.get_staff_by_id(staff_id)
                    if staff_data:
                        staff_name = f"{staff_data.get('EFName', '')} {staff_data.get('ELName', '')}"
                        self.value_procesd.setText(staff_name.strip())
                    else:
                        self.value_procesd.setText(f"Staff #{staff_id}")
                except:
                    self.value_procesd.setText(f"Staff #{staff_id}")
            else:
                self.value_procesd.setText('N/A')

        # ADDRESS
        if self.value_address:
            customer_id = order_data.get('CustomerID')
            if customer_id and self.model:
                try:
                    addresses = self.model.get_customer_addresses(customer_id)
                    if addresses and len(addresses) > 0:
                        addr = addresses[0]
                        parts = []
                        if addr.get('StreetAdd'):
                            parts.append(addr['StreetAdd'])
                        if addr.get('AppartUnit'):
                            parts.append(addr['AppartUnit'])
                        if addr.get('City'):
                            parts.append(addr['City'])
                        if addr.get('ZipCode'):
                            parts.append(str(addr['ZipCode']))

                        address_text = ", ".join(parts) if parts else 'N/A'
                        self.value_address.setText(address_text)
                    else:
                        self.value_address.setText('No address on file')
                except:
                    self.value_address.setText('Error loading address')
            else:
                self.value_address.setText('N/A')

        # Order Items Table
        total_wash = 0.0
        subtotal = 0.0
        total_amount = 0.0

        if self.ordertable:
            self.ordertable.setRowCount(0)
            services = order_data.get('services', [])

            for service in services:
                weight = float(service.get('WeightKg', 0))
                price_per_kg = float(service.get('PriceperKG', 0))
                wash_amount = float(service.get('WashAmount', 0))

                fast_dry = bool(service.get('FastDry', False))
                fast_dry_amount = float(service.get('FastDryAmount', 0))

                iron_only = bool(service.get('IronOnly', False))
                iron_only_amount = float(service.get('IronOnlyAmount', 0))

                fold = bool(service.get('Fold', False))
                fold_amount = float(service.get('FoldAmount', 0))

                service_total = float(service.get('TotalAmount', 0))

                # Always show all add-on services
                # Fast Dry
                row = self.ordertable.rowCount()
                self.ordertable.insertRow(row)
                self.ordertable.setItem(row, 0, QTableWidgetItem("Fast Dry"))
                if fast_dry and fast_dry_amount > 0:
                    self.ordertable.setItem(row, 1, QTableWidgetItem(f"{weight} kg"))
                    self.ordertable.setItem(row, 3, QTableWidgetItem(f"₱{fast_dry_amount:.2f}"))
                else:
                    self.ordertable.setItem(row, 1, QTableWidgetItem("False"))
                    self.ordertable.setItem(row, 3, QTableWidgetItem("₱0.00"))
                self.ordertable.setItem(row, 2, QTableWidgetItem("₱140.00/kg"))

                # Iron Only
                row = self.ordertable.rowCount()
                self.ordertable.insertRow(row)
                self.ordertable.setItem(row, 0, QTableWidgetItem("Iron Only"))
                if iron_only and iron_only_amount > 0:
                    self.ordertable.setItem(row, 1, QTableWidgetItem(f"{weight} kg"))
                    self.ordertable.setItem(row, 3, QTableWidgetItem(f"₱{iron_only_amount:.2f}"))
                else:
                    self.ordertable.setItem(row, 1, QTableWidgetItem("False"))
                    self.ordertable.setItem(row, 3, QTableWidgetItem("₱0.00"))
                self.ordertable.setItem(row, 2, QTableWidgetItem("₱50.00/kg"))

                # Fold
                row = self.ordertable.rowCount()
                self.ordertable.insertRow(row)
                self.ordertable.setItem(row, 0, QTableWidgetItem("Fold"))
                if fold and fold_amount > 0:
                    self.ordertable.setItem(row, 1, QTableWidgetItem(f"{weight} kg"))
                    self.ordertable.setItem(row, 3, QTableWidgetItem(f"₱{fold_amount:.2f}"))
                else:
                    self.ordertable.setItem(row, 1, QTableWidgetItem("False"))
                    self.ordertable.setItem(row, 3, QTableWidgetItem("₱0.00"))
                self.ordertable.setItem(row, 2, QTableWidgetItem("₱30.00/kg"))

                # Accumulate totals
                total_wash += wash_amount
                subtotal += iron_only_amount + fold_amount + fast_dry_amount
                total_amount += service_total

        # Summary Section
        if self.value_wash:
            self.value_wash.setText(f"₱{total_wash:.2f}")

        if self.value_subtotal:
            self.value_subtotal.setText(f"₱{subtotal:.2f}")

        if self.value_subtotal_3:
            grand_total = float(order_data.get('TotalAmount', total_amount))
            self.value_subtotal_3.setText(f"₱{grand_total:.2f}")

        formatted_id = self.format_order_id(order_id) if isinstance(order_id, int) else order_id
        print(f"✓ OrderDetailsPopup: Loaded order {formatted_id}")

    def print_order_pdf(self):
        """Generate PDF report for current order"""
        if not self.current_order_id:
            QtWidgets.QMessageBox.warning(
                self,
                "No Order",
                "No order loaded to print."
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

            filename = f"C:\\Users\\NITRO\\PycharmProjects\\Washyy\\View\\Reports\\Order_WSHY{self.current_order_id:03d}.pdf"

            QtWidgets.QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

            success = report_gen.generate_order_report(self.current_order_id, filename)

            QtWidgets.QApplication.restoreOverrideCursor()

            if success:
                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    f"Order report saved as:\n{filename}\n\nLocation: Current directory"
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