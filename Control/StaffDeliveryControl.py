from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from datetime import datetime

from View.OrderPopup import OrderDetailsPopup
from View.FinalizeOrderPopup import FinalizeOrderPopup


class SDeliveryControl:
    """Controller for Staff Delivery/Pickup Management page (MVC Pattern)"""

    def __init__(self, staff_home, dashboard, customer, order, delivery_view, report, model, login_view):
        self.staff_home = staff_home
        self.dashboard = dashboard
        self.customer = customer
        self.order = order
        self.report = report
        self.delivery_view = delivery_view
        self.model = model
        self.login_view = login_view

        # Current staff context
        self.current_staff_id = None

        # Reference to order controller (will be set by LoginController)
        self.order_controller = None

        # Order details popup
        self.order_popup = None

        # Finalize order popup
        self.finalize_popup = FinalizeOrderPopup(parent=self.staff_home, model=self.model)
        self.finalize_popup.transaction_completed.connect(self.on_transaction_completed)
        print("✓ FinalizeOrderPopup initialized in DeliveryControl")

        # Sort states
        self.sort_ascending_pickup = True
        self.sort_ascending_delivery = True

        # Connect buttons and signals
        self.connect_delivery_buttons()

        # Load initial data
        self.load_pending_pickups()
        self.load_pending_deliveries()

        # Connect to page visibility changes
        if hasattr(self.staff_home, 'stackedWidget'):
            self.staff_home.stackedWidget.currentChanged.connect(self.on_page_changed)

    def format_datetime_display(self, dt):
        """Format datetime with shortened month name (e.g., 'Dec 14, 3:30 PM')"""
        if dt and hasattr(dt, 'strftime'):
            # Use %b for abbreviated month name (Jan, Feb, Mar, etc.)
            return dt.strftime('%b %d, %I:%M %p')
        return 'Not scheduled'

    def on_page_changed(self, index):
        """Refresh tables when delivery page is shown"""
        if hasattr(self.staff_home, 'Delivery_page_index'):
            if index == self.staff_home.Delivery_page_index:
                print("✓ Delivery page activated - refreshing tables")
                self.refresh_all_tables()

    def set_staff_context(self, staff_id):
        """Set current staff ID"""
        self.current_staff_id = staff_id
        self.finalize_popup.set_staff_id(staff_id)

        print(f"✓ Delivery - Staff context set: StaffID = {staff_id}")

    def format_order_id(self, order_id):
        """Format order ID as WSHY#001, WSHY#002, etc."""
        return f"WSHY#{order_id:03d}"

    def connect_delivery_buttons(self):
        """Connect navigation and action buttons on Delivery page"""

        # Sidebar buttons - Delivery page uses _9 suffix
        if hasattr(self.staff_home, "Homebut_9"):
            self.staff_home.Homebut_9.clicked.connect(self.go_to_home)
        if hasattr(self.staff_home, "Dashbut_9"):
            self.staff_home.Dashbut_9.clicked.connect(self.go_to_dashboard)
        if hasattr(self.staff_home, "Userbut_9"):
            self.staff_home.Userbut_9.clicked.connect(self.go_to_customers)
        if hasattr(self.staff_home, "Orderbut_9"):
            self.staff_home.Orderbut_9.clicked.connect(self.go_to_orders)
        if hasattr(self.staff_home, "Reportbut_9"):
            self.staff_home.Reportbut_9.clicked.connect(self.go_to_reports)
        if hasattr(self.staff_home, "Delivlab_9"):
            self.staff_home.Delivlab_9.clicked.connect(self.go_to_delivery)
        if hasattr(self.staff_home, "Settbut_9"):
            self.staff_home.Settbut_9.clicked.connect(self.go_to_logout)

        # Icon buttons
        if hasattr(self.staff_home, "h1_7"):
            self.staff_home.h1_7.clicked.connect(self.go_to_home)
        if hasattr(self.staff_home, "db1_7"):
            self.staff_home.db1_7.clicked.connect(self.go_to_dashboard)
        if hasattr(self.staff_home, "u1_7"):
            self.staff_home.u1_7.clicked.connect(self.go_to_customers)
        if hasattr(self.staff_home, "o1_7"):
            self.staff_home.o1_7.clicked.connect(self.go_to_orders)
        if hasattr(self.staff_home, "r1_7"):
            self.staff_home.r1_7.clicked.connect(self.go_to_reports)
        if hasattr(self.staff_home, "d1_7"):
            self.staff_home.d1_7.clicked.connect(self.go_to_delivery)
        if hasattr(self.staff_home, "s1_7"):
            self.staff_home.s1_7.clicked.connect(self.go_to_logout)

        # Action buttons - Mark as Picked Up
        if hasattr(self.staff_home, "crt_btn_9"):
            self.staff_home.crt_btn_9.clicked.connect(self.mark_as_picked_up)

        # Action buttons - Mark as Delivered
        if hasattr(self.staff_home, "crt_btn_10"):
            self.staff_home.crt_btn_10.clicked.connect(self.mark_as_delivered)

        # Search field for pickup table
        if hasattr(self.staff_home, "line4_2"):
            self.staff_home.line4_2.textChanged.connect(self.search_pickups)

        # Sort button
        if hasattr(self.staff_home, "name_srt_btn_6"):
            self.staff_home.name_srt_btn_6.clicked.connect(self.sort_pickup_table)

        # View Order button
        if hasattr(self.staff_home, "crt_btn_5"):
            self.staff_home.crt_btn_5.clicked.connect(self.view_selected_order)

        # Double-click on tables
        if hasattr(self.staff_home, "tableWidget_5"):
            self.staff_home.tableWidget_5.cellDoubleClicked.connect(self.on_pickup_table_double_click)

        if hasattr(self.staff_home, "tableWidget_6"):
            self.staff_home.tableWidget_6.cellDoubleClicked.connect(self.on_delivery_table_double_click)

    def load_pending_pickups(self):
        """Load orders pending pickup into tableWidget_5"""
        if not hasattr(self.staff_home, "tableWidget_5"):
            print("Error: tableWidget_5 not found")
            return

        try:
            # Get orders with status 'Pending' (waiting for pickup)
            orders = self.model.get_orders_by_status('Pending')

            table = self.staff_home.tableWidget_5
            table.setRowCount(0)
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Name", "Scheduled Time", "Status"])

            for row_num, order in enumerate(orders):
                table.insertRow(row_num)

                # Customer Name
                customer_name = order.get('customer_name', 'Unknown')
                name_item = QTableWidgetItem(customer_name)
                name_item.setData(Qt.ItemDataRole.UserRole, order['OrderID'])
                table.setItem(row_num, 0, name_item)

                # Get scheduled pickup time with shortened month
                order_date = order.get('OrderDate')
                if order_date:
                    scheduled_time = self.format_datetime_display(order_date)
                else:
                    scheduled_time = "Not scheduled yet"

                table.setItem(row_num, 1, QTableWidgetItem(scheduled_time))

                # Status
                status = order.get('Status', 'Pending')
                status_item = QTableWidgetItem(status)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row_num, 2, status_item)
                if status == 'Completed':
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                elif status == 'Pending':
                    status_item.setForeground(Qt.GlobalColor.darkYellow)
                elif status == 'Processing':
                    status_item.setForeground(Qt.GlobalColor.darkBlue)

            # Resize columns
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, header.ResizeMode.Stretch)
            for col in range(1, 3):
                header.setSectionResizeMode(col, header.ResizeMode.ResizeToContents)

            print(f"✓ Loaded {len(orders)} pending pickups")

        except Exception as e:
            print(f"✗ Error loading pending pickups: {e}")
            import traceback
            traceback.print_exc()

    def load_pending_deliveries(self):
        """Load orders pending delivery into tableWidget_6"""
        if not hasattr(self.staff_home, "tableWidget_6"):
            print("Error: tableWidget_6 not found")
            return

        try:
            # Get orders with status 'Processing' or 'Ready' (picked up, waiting for delivery)
            processing_orders = self.model.get_orders_by_status('Processing')
            ready_orders = self.model.get_orders_by_status('Ready')
            orders = processing_orders + ready_orders

            table = self.staff_home.tableWidget_6
            table.setRowCount(0)
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Name", "Pickup Time", "Status"])

            for row_num, order in enumerate(orders):
                table.insertRow(row_num)

                # Customer Name
                customer_name = order.get('customer_name', 'Unknown')
                name_item = QTableWidgetItem(customer_name)
                name_item.setData(Qt.ItemDataRole.UserRole, order['OrderID'])
                table.setItem(row_num, 0, name_item)

                # Get actual pickup time from DatePicked with shortened month
                order_id = order['OrderID']
                order_details = self.model.get_order_by_id(order_id)

                if order_details and order_details.get('DatePicked'):
                    pickup_time = self.format_datetime_display(order_details['DatePicked'])
                else:
                    pickup_time = "Not picked up yet"

                table.setItem(row_num, 1, QTableWidgetItem(pickup_time))

                # Status
                status = order.get('Status', 'Processing')
                status_item = QTableWidgetItem(status)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row_num, 2, status_item)
                if status == 'Completed':
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                elif status == 'Pending':
                    status_item.setForeground(Qt.GlobalColor.darkYellow)
                elif status == 'Processing' or status == 'Ready':
                    status_item.setForeground(Qt.GlobalColor.darkBlue)

            # Resize columns
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, header.ResizeMode.Stretch)
            for col in range(1, 3):
                header.setSectionResizeMode(col, header.ResizeMode.ResizeToContents)

            print(f"✓ Loaded {len(orders)} pending deliveries")

        except Exception as e:
            print(f"✗ Error loading pending deliveries: {e}")
            import traceback
            traceback.print_exc()

    def mark_as_picked_up(self):
        """Mark selected order as picked up"""
        if not hasattr(self.staff_home, "tableWidget_5"):
            return

        selected_items = self.staff_home.tableWidget_5.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self.staff_home,
                "No Selection",
                "Please select an order to mark as picked up."
            )
            return

        # Check if staff is logged in
        if not self.current_staff_id:
            QMessageBox.warning(
                self.staff_home,
                "Session Error",
                "Staff ID not found. Please log out and log in again."
            )
            return

        try:
            selected_row = selected_items[0].row()
            customer_name = self.staff_home.tableWidget_5.item(selected_row, 0).text()
            order_id = self.staff_home.tableWidget_5.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)

            if not order_id:
                return

            formatted_order_id = self.format_order_id(order_id)

            # Get order details
            order_details = self.model.get_order_by_id(order_id)
            if not order_details:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "Could not load order details."
                )
                return

            pickup_time = datetime.now()

            # Update order: set status to 'Processing', set DatePicked, and set StaffID
            try:
                cursor = self.model.conn.cursor()

                # Update order with pickup time and staff who processed it
                query = """
                        UPDATE Orders
                        SET Status     = %s,
                            DatePicked = %s,
                            StaffID    = %s
                        WHERE OrderID = %s
                        """
                cursor.execute(query, ('Processing', pickup_time, self.current_staff_id, order_id))

                # Log activity
                cursor.execute("""
                               INSERT INTO StaffActivityLog
                                   (StaffID, ActivityType, OrderID, CustomerID, ActivityTime)
                               VALUES (%s, %s, %s, %s, %s)
                               """, (self.current_staff_id, 'PICKUP_ORDER', order_id,
                                     order_details.get('CustomerID'), pickup_time))

                # UPDATE LAST ACTIVE TIMESTAMP
                cursor.execute("""
                               UPDATE Staff
                               SET LastActiveAt = %s
                               WHERE StaffID = %s
                               """, (pickup_time, self.current_staff_id))

                self.model.conn.commit()
                cursor.close()

                # Use shortened month in confirmation message
                QMessageBox.information(
                    self.staff_home,
                    "Order Picked Up",
                    f"Order {formatted_order_id} for {customer_name} has been picked up successfully!\n\n"
                    f"Pickup Time: {pickup_time.strftime('%b %d, %Y at %I:%M %p')}"
                )

                print(f"✓ Order {formatted_order_id} marked as picked up by Staff ID {self.current_staff_id} at {pickup_time}")

                # Refresh delivery tables
                self.refresh_all_tables()

                # Also refresh the order management page if order_controller is available
                if self.order_controller:
                    self.order_controller.refresh_order_table()
                    print("✓ Order management page refreshed")

            except Exception as e:
                self.model.conn.rollback()
                print(f"✗ Database error: {e}")
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    f"Failed to update order status:\n{str(e)}"
                )

        except Exception as e:
            print(f"✗ Error marking as picked up: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.staff_home,
                "Error",
                f"Error marking order as picked up:\n{str(e)}"
            )

    def mark_as_delivered(self):
        """Mark selected order as delivered and show finalize payment popup"""
        if not hasattr(self.staff_home, "tableWidget_6"):
            return

        selected_items = self.staff_home.tableWidget_6.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self.staff_home,
                "No Selection",
                "Please select an order to mark as delivered."
            )
            return

        # Check if staff is logged in
        if not self.current_staff_id:
            QMessageBox.warning(
                self.staff_home,
                "Session Error",
                "Staff ID not found. Please log out and log in again."
            )
            return

        try:
            selected_row = selected_items[0].row()
            customer_name = self.staff_home.tableWidget_6.item(selected_row, 0).text()
            order_id = self.staff_home.tableWidget_6.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)

            if not order_id:
                return

            formatted_order_id = self.format_order_id(order_id)

            # Get order details to show total amount
            order_details = self.model.get_order_by_id(order_id)
            if not order_details:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "Could not load order details."
                )
                return

            delivery_time = datetime.now()

            # Update order: set DateDelivered (status will be updated to Completed by finalize popup)
            try:
                cursor = self.model.conn.cursor()

                # Update order with delivery time
                query = """
                        UPDATE Orders
                        SET DateDelivered = %s
                        WHERE OrderID = %s
                        """
                cursor.execute(query, (delivery_time, order_id))

                # Log activity
                cursor.execute("""
                               INSERT INTO StaffActivityLog
                                   (StaffID, ActivityType, OrderID, CustomerID, ActivityTime)
                               VALUES (%s, %s, %s, %s, %s)
                               """, (self.current_staff_id, 'DELIVER_ORDER', order_id,
                                     order_details.get('CustomerID') if order_details else None, delivery_time))

                # UPDATE LAST ACTIVE TIMESTAMP
                cursor.execute("""
                               UPDATE Staff
                               SET LastActiveAt = %s
                               WHERE StaffID = %s
                               """, (delivery_time, self.current_staff_id))

                self.model.conn.commit()
                cursor.close()

                print(f"✓ Order {formatted_order_id} marked as delivered at {delivery_time}")

                # Show finalize payment popup
                self.finalize_popup.setOrderData(order_id)
                self.center_popup(self.finalize_popup)
                self.finalize_popup.show()
                self.finalize_popup.raise_()
                self.finalize_popup.activateWindow()

            except Exception as e:
                self.model.conn.rollback()
                print(f"✗ Database error: {e}")
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    f"Failed to update order delivery time:\n{str(e)}"
                )

        except Exception as e:
            print(f"✗ Error marking as delivered: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.staff_home,
                "Error",
                f"Error marking order as delivered:\n{str(e)}"
            )

    def on_transaction_completed(self, order_id):
        """Called when transaction is completed in finalize popup"""
        print(f"✓ Transaction completed for Order ID {order_id}")

        # Refresh delivery tables to remove completed order
        self.refresh_all_tables()

        # Also refresh the order management page if order_controller is available
        if self.order_controller:
            self.order_controller.refresh_order_table()
            print("✓ Order management page refreshed after delivery completion")

    def view_selected_order(self):
        """View selected order details from either table"""
        # Try pickup table first
        if hasattr(self.staff_home, "tableWidget_5"):
            selected_items = self.staff_home.tableWidget_5.selectedItems()
            if selected_items:
                selected_row = selected_items[0].row()
                order_id = self.staff_home.tableWidget_5.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
                if order_id:
                    self.show_order_details(order_id)
                    return

        # Try delivery table
        if hasattr(self.staff_home, "tableWidget_6"):
            selected_items = self.staff_home.tableWidget_6.selectedItems()
            if selected_items:
                selected_row = selected_items[0].row()
                order_id = self.staff_home.tableWidget_6.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
                if order_id:
                    self.show_order_details(order_id)
                    return

        QMessageBox.warning(
            self.staff_home,
            "No Selection",
            "Please select an order to view."
        )

    def show_order_details(self, order_id):
        """Show order details popup"""
        try:
            formatted_order_id = self.format_order_id(order_id)
            print(f"✓ SDeliveryControl: Loading order details for Order {formatted_order_id}")

            # Create popup with model if it doesn't exist
            if self.order_popup is None:
                self.order_popup = OrderDetailsPopup(parent=self.staff_home, model=self.model)

            # Load data directly from database using the order ID
            success = self.order_popup.loadOrderFromDatabase(order_id)

            if not success:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "Could not load order details."
                )
                return

            self.center_popup(self.order_popup)
            self.order_popup.show()
            self.order_popup.raise_()
            self.order_popup.activateWindow()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.staff_home,
                "Error",
                f"An error occurred while loading order details:\n{str(e)}"
            )

    def center_popup(self, popup):
        """Center popup on main window"""
        main_geometry = self.staff_home.frameGeometry()
        main_center = main_geometry.center()
        popup_x = main_center.x() - popup.width() // 2
        popup_y = main_center.y() - popup.height() // 2
        popup.move(popup_x, popup_y)

    def search_pickups(self):
        """Search pickups by customer name or order ID"""
        if not hasattr(self.staff_home, "line4_2") or not hasattr(self.staff_home, "tableWidget_5"):
            return

        search_term = self.staff_home.line4_2.text().strip()

        if not search_term:
            self.load_pending_pickups()
            return

        try:
            # Search all orders and filter for Pending status
            all_orders = self.model.search_orders(search_term)
            orders = [o for o in all_orders if o.get('Status') == 'Pending']

            table = self.staff_home.tableWidget_5
            table.setRowCount(0)

            for row_num, order in enumerate(orders):
                table.insertRow(row_num)

                customer_name = order.get('customer_name', 'Unknown')
                name_item = QTableWidgetItem(customer_name)
                name_item.setData(Qt.ItemDataRole.UserRole, order['OrderID'])
                table.setItem(row_num, 0, name_item)

                order_date = order.get('OrderDate')
                scheduled_time = self.format_datetime_display(order_date)
                table.setItem(row_num, 1, QTableWidgetItem(scheduled_time))

                status = order.get('Status', 'Pending')
                status_item = QTableWidgetItem(status)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row_num, 2, status_item)
                if status == 'Completed':
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                elif status == 'Pending':
                    status_item.setForeground(Qt.GlobalColor.darkYellow)
                elif status == 'Processing':
                    status_item.setForeground(Qt.GlobalColor.darkBlue)

            print(f"✓ Found {len(orders)} pending pickups matching '{search_term}'")

        except Exception as e:
            print(f"✗ Error searching pickups: {e}")

    def sort_pickup_table(self):
        """Sort pickup table by name"""
        if not hasattr(self.staff_home, "tableWidget_5"):
            return

        if self.sort_ascending_pickup:
            self.staff_home.tableWidget_5.sortItems(0, Qt.SortOrder.AscendingOrder)
            if hasattr(self.staff_home, "name_srt_btn_6"):
                self.staff_home.name_srt_btn_6.setText("Ascending")
        else:
            self.staff_home.tableWidget_5.sortItems(0, Qt.SortOrder.DescendingOrder)
            if hasattr(self.staff_home, "name_srt_btn_6"):
                self.staff_home.name_srt_btn_6.setText("Descending")

        self.sort_ascending_pickup = not self.sort_ascending_pickup

    def on_pickup_table_double_click(self, row, column):
        """Handle double-click on pickup table - show order details"""
        self.view_selected_order()

    def on_delivery_table_double_click(self, row, column):
        """Handle double-click on delivery table - show order details"""
        self.view_selected_order()

    def refresh_all_tables(self):
        """Refresh both pickup and delivery tables"""
        self.load_pending_pickups()
        self.load_pending_deliveries()
        print("✓ Delivery tables refreshed")

    # Navigation Methods

    def go_to_home(self):
        print("Staff: Navigating to Home from Delivery")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.home_page_index)

    def go_to_dashboard(self):
        print("Staff: Navigating to Dashboard from Delivery")
        self.dashboard.show()

    def go_to_customers(self):
        print("Staff: Navigating to Customers from Delivery")
        self.customer.show()

    def go_to_orders(self):
        print("Staff: Navigating to Orders from Delivery")
        self.order.show()

    def go_to_reports(self):
        print("Staff: Navigating to Reports from Delivery")
        self.report.show()

    def go_to_delivery(self):
        self.refresh_all_tables()
        self.delivery_view.show()

    def go_to_logout(self):
        """Logout with confirmation"""

        # ✅ CRITICAL FIX: Close all popups FIRST, before showing confirmation
        if self.order_popup:
            try:
                self.order_popup.hide()
                self.order_popup.close()
                self.order_popup.deleteLater()
                self.order_popup = None
                print("✓ Closed order popup before logout confirmation")
            except Exception as e:
                print(f"Warning: Error closing order popup: {e}")

        if self.finalize_popup:
            try:
                self.finalize_popup.hide()
                self.finalize_popup.close()
                self.finalize_popup.deleteLater()
                self.finalize_popup = None
                print("✓ Closed finalize popup before logout confirmation")
            except Exception as e:
                print(f"Warning: Error closing finalize popup: {e}")

        # NOW show confirmation dialog (no popups blocking it)
        reply = QMessageBox.question(
            self.staff_home,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print("Staff: Logging out from Delivery...")

            self.staff_home.close()

            if hasattr(self.login_view, 'username'):
                self.login_view.username.clear()
            if hasattr(self.login_view, 'password'):
                self.login_view.password.clear()

            self.login_view.show()
            if hasattr(self.login_view, 'username'):
                self.login_view.username.setFocus()
        else:
            print("Staff: Logout cancelled")
