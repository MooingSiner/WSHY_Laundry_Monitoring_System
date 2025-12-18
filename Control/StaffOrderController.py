from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QColor

from View.OrderPopup import OrderDetailsPopup


class SOControl:
    """Controller for Staff Order Management page"""

    def __init__(self, staff_home, dashboard, customer, order, delivery, report, model, login_view,
                 edit_order_control=None):
        self.staff_home = staff_home
        self.dashboard = dashboard
        self.customer = customer
        self.order = order
        self.delivery = delivery
        self.report = report
        self.model = model
        self.login_view = login_view
        self.edit_order_control = edit_order_control

        self.order_popup = None
        self.staff_id = None
        self.sort_ascending_order = True

        # Connect buttons from Order page
        self.connect_order_buttons()

        # Load initial order data when initialized
        self.load_order_data()

        # Connect to page visibility changes to auto-refresh
        if hasattr(self.staff_home, 'stackedWidget'):
            self.staff_home.stackedWidget.currentChanged.connect(self.on_page_changed)

        # Store the page index for order page if available
        if hasattr(self.staff_home, 'order_page_index'):
            self.order_page_index = self.staff_home.order_page_index
        else:
            # Try to find order page index dynamically
            self.order_page_index = self.find_order_page_index()

    def find_order_page_index(self):
        """Find the index of the order page in the stacked widget"""
        if not hasattr(self.staff_home, 'stackedWidget'):
            return -1

        for i in range(self.staff_home.stackedWidget.count()):
            widget = self.staff_home.stackedWidget.widget(i)
            if widget and hasattr(widget, 'objectName'):
                if widget.objectName() == "ManageOrder":
                    print(f"✓ Found Order page at index: {i}")
                    return i
        return -1

    def on_page_changed(self, index):
        """Refresh order table when order page is shown"""
        # Check if this is the order page
        if index == self.order_page_index:
            print("✓ Order page activated - auto-refreshing order table")
            self.refresh_order_table()

    def set_staff_id(self, staff_id):
        """Set the logged-in staff ID"""
        self.staff_id = staff_id
        print(f"✓ SOControl: Staff ID set to {staff_id}")

    def set_edit_order_control(self, edit_order_control):
        """Set reference to edit order control"""
        self.edit_order_control = edit_order_control

    def format_order_id(self, order_id):
        """Format order ID as WSHY#001, WSHY#002, etc."""
        return f"WSHY#{order_id:03d}"

    def connect_order_buttons(self):
        """Connect navigation and action buttons on the Order page"""

        # Sidebar navigation buttons (ManageOrder page uses _6 suffix)
        if hasattr(self.staff_home, "Homebut_6"):
            self.staff_home.Homebut_6.clicked.connect(self.go_to_home)

        if hasattr(self.staff_home, "Dashbut_6"):
            self.staff_home.Dashbut_6.clicked.connect(self.go_to_dashboard)

        if hasattr(self.staff_home, "Userbut_6"):
            self.staff_home.Userbut_6.clicked.connect(self.go_to_users)

        if hasattr(self.staff_home, "Orderbut_6"):
            self.staff_home.Orderbut_6.clicked.connect(self.go_to_orders)

        if hasattr(self.staff_home, "Reportbut_6"):
            self.staff_home.Reportbut_6.clicked.connect(self.go_to_reports)

        if hasattr(self.staff_home, "Delivlab_5"):
            self.staff_home.Delivlab_5.clicked.connect(self.go_to_delivery)

        if hasattr(self.staff_home, "Settbut_6"):
            self.staff_home.Settbut_6.clicked.connect(self.go_to_logout)

        # Icon buttons (ManageOrder page uses _4 suffix)
        if hasattr(self.staff_home, "h1_4"):
            self.staff_home.h1_4.clicked.connect(self.go_to_home)

        if hasattr(self.staff_home, "db1_4"):
            self.staff_home.db1_4.clicked.connect(self.go_to_dashboard)

        if hasattr(self.staff_home, "s1_4"):
            self.staff_home.s1_4.clicked.connect(self.go_to_logout)

        if hasattr(self.staff_home, "o1_4"):
            self.staff_home.o1_4.clicked.connect(self.go_to_orders)

        if hasattr(self.staff_home, "r1_4"):
            self.staff_home.r1_4.clicked.connect(self.go_to_reports)

        if hasattr(self.staff_home, "u1_4"):
            self.staff_home.u1_4.clicked.connect(self.go_to_users)

        if hasattr(self.staff_home, "d1_4"):
            self.staff_home.d1_4.clicked.connect(self.go_to_delivery)

        # Order action buttons on ManageOrder page
        if hasattr(self.staff_home, "nwbut_12"):  # View button
            self.staff_home.nwbut_12.clicked.connect(self.show_order_details)

        if hasattr(self.staff_home, "nwbut_10"):  # Edit button
            self.staff_home.nwbut_10.clicked.connect(self.edit_order)

        if hasattr(self.staff_home, "nwbut_9"):  # Delete button
            self.staff_home.nwbut_9.clicked.connect(self.delete_order)

        # Connect cancel button
        if hasattr(self.staff_home, "cnl"):  # Cancel button
            self.staff_home.cnl.clicked.connect(self.cancel_order)

        # Connect search field (line3 on ManageOrder page)
        if hasattr(self.staff_home, "line3"):
            self.staff_home.line3.textChanged.connect(self.search_order)

        # Connect sort button (name_srt_btn_3 on ManageOrder page)
        if hasattr(self.staff_home, "name_srt_btn_3"):
            self.staff_home.name_srt_btn_3.clicked.connect(self.sort_orders)

        # Connect order table double-click (tableWidget_3 on ManageOrder page)
        if hasattr(self.staff_home, "tableWidget_3"):
            self.staff_home.tableWidget_3.cellDoubleClicked.connect(
                self.on_order_table_double_click
            )

    def load_order_data(self):
        """Load all order data into the table with customer names"""
        if not hasattr(self.staff_home, "tableWidget_3"):
            print("Error: tableWidget_3 not found")
            return

        try:
            order_list = self.model.get_all_orders()
            table = self.staff_home.tableWidget_3
            table.setRowCount(0)
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(
                ["Order ID", "Customer Name", "Status", "Total Amount", "OrderID_Hidden"])
            table.setColumnHidden(4, True)

            for row_num, order in enumerate(order_list):
                table.insertRow(row_num)

                # Order ID - formatted as WSHY#001
                formatted_id = self.format_order_id(order['OrderID'])
                table.setItem(row_num, 0, QTableWidgetItem(formatted_id))

                # Customer Name - get from CustomerID
                customer_name = "Unknown"
                if order.get('CustomerID'):
                    customer_data = self.model.get_customer_by_id(order['CustomerID'])
                    if customer_data:
                        full_name = f"{customer_data['CFName']} {customer_data['CMName'] or ''} {customer_data['CLName']}".strip()
                        customer_name = ' '.join(full_name.split())
                table.setItem(row_num, 1, QTableWidgetItem(customer_name))

                # Status with color coding
                status_item = QTableWidgetItem(order.get('Status', 'Unknown'))
                status = order.get('Status', 'Unknown')

                # Apply colors based on status
                if status == 'Completed':
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                elif status == 'Pending':
                    status_item.setForeground(Qt.GlobalColor.darkYellow)
                elif status == 'Processing':
                    status_item.setForeground(Qt.GlobalColor.darkBlue)
                elif status == 'Cancelled':
                    status_item.setForeground(Qt.GlobalColor.darkRed)

                table.setItem(row_num, 2, status_item)

                # Total Amount
                table.setItem(row_num, 3, QTableWidgetItem(f"₱{order.get('TotalAmount', 0):.2f}"))

                # Hidden OrderID
                order_id_item = QTableWidgetItem()
                order_id_item.setData(Qt.ItemDataRole.UserRole, order['OrderID'])
                table.setItem(row_num, 4, order_id_item)

            # Stretch first two columns, others resize to content
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, header.ResizeMode.Stretch)
            header.setSectionResizeMode(1, header.ResizeMode.Stretch)
            for col in range(2, 4):
                header.setSectionResizeMode(col, header.ResizeMode.ResizeToContents)

            print(f"✓ Loaded {len(order_list)} orders with customer names")

        except Exception as e:
            print(f"✗ Error loading order data: {e}")
            import traceback
            traceback.print_exc()

    def refresh_order_table(self):
        """Public method to refresh the order table - can be called from other controllers"""
        print("✓ Refreshing order table...")
        self.load_order_data()

    def cancel_order(self):
        """Cancel selected order - only works for Pending orders"""
        if not hasattr(self.staff_home, "tableWidget_3"):
            return

        selected_items = self.staff_home.tableWidget_3.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self.staff_home,
                "No Selection",
                "Please select an order to cancel."
            )
            return

        try:
            selected_row = selected_items[0].row()
            order_id_display = self.staff_home.tableWidget_3.item(selected_row, 0).text()
            status_item = self.staff_home.tableWidget_3.item(selected_row, 2)
            current_status = status_item.text() if status_item else "Unknown"

            # Get OrderID from hidden column
            order_id_item = self.staff_home.tableWidget_3.item(selected_row, 4)
            if not order_id_item:
                return

            order_id = order_id_item.data(Qt.ItemDataRole.UserRole)

            # Check if order is already cancelled
            if current_status == 'Cancelled':
                QMessageBox.warning(
                    self.staff_home,
                    "Already Cancelled",
                    f"Order {order_id_display} is already cancelled."
                )
                return

            # Check if order can be cancelled (only Pending orders)
            if current_status not in ['Pending']:
                QMessageBox.warning(
                    self.staff_home,
                    "Cannot Cancel",
                    f"Cannot cancel order {order_id_display}.\n\n"
                    f"Only orders with 'Pending' status can be cancelled.\n"
                    f"Current status: {current_status}"
                )
                return

            # Confirm cancellation
            reply = QMessageBox.question(
                self.staff_home,
                "Confirm Cancellation",
                f"Are you sure you want to cancel Order {order_id_display}?\n\n"
                f"This action will change the order status to 'Cancelled'.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Update order status to 'Cancelled'
                success = self.model.update_order_status(order_id, 'Cancelled')

                if success:
                    # Update the table immediately
                    status_item.setText('Cancelled')
                    status_item.setForeground(Qt.GlobalColor.darkRed)

                    print(f"✓ Cancelled order: {order_id_display}")
                    QMessageBox.information(
                        self.staff_home,
                        "Success",
                        f"Order {order_id_display} has been cancelled successfully!"
                    )
                else:
                    QMessageBox.warning(
                        self.staff_home,
                        "Error",
                        "Failed to cancel order."
                    )

        except Exception as e:
            print(f"✗ Error cancelling order: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.staff_home,
                "Error",
                f"Error cancelling order: {e}"
            )

    def show_order_details(self):
        """Show order details popup"""
        if not hasattr(self.staff_home, "tableWidget_3"):
            return

        selected_items = self.staff_home.tableWidget_3.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self.staff_home,
                "No Selection",
                "Please select an order first."
            )
            return

        try:
            selected_row = selected_items[0].row()

            # Get OrderID from hidden column 4
            order_id_item = self.staff_home.tableWidget_3.item(selected_row, 4)

            if not order_id_item:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "Could not retrieve order ID from table."
                )
                return

            # Get the actual order ID from UserRole data
            order_id = order_id_item.data(Qt.ItemDataRole.UserRole)

            print(f"✓ SOControl: Loading order details for Order {self.format_order_id(order_id)}")

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

    def search_order(self):
        """Search orders by order ID, customer name, or status"""
        if not hasattr(self.staff_home, "line3"):
            return

        search_term = self.staff_home.line3.text().strip()

        if not search_term:
            self.load_order_data()
            return

        try:
            order_list = self.model.search_orders(search_term)
            table = self.staff_home.tableWidget_3
            table.setRowCount(0)
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(
                ["Order ID", "Customer Name", "Status", "Total Amount", "OrderID_Hidden"])
            table.setColumnHidden(4, True)

            for row_num, order in enumerate(order_list):
                table.insertRow(row_num)

                # Order ID - formatted as WSHY#001
                formatted_id = self.format_order_id(order['OrderID'])
                table.setItem(row_num, 0, QTableWidgetItem(formatted_id))

                # Customer Name
                customer_name = "Unknown"
                if order.get('CustomerID'):
                    customer_data = self.model.get_customer_by_id(order['CustomerID'])
                    if customer_data:
                        full_name = f"{customer_data['CFName']} {customer_data['CMName'] or ''} {customer_data['CLName']}".strip()
                        customer_name = ' '.join(full_name.split())
                table.setItem(row_num, 1, QTableWidgetItem(customer_name))

                # Status with color coding
                status_item = QTableWidgetItem(order.get('Status', 'Unknown'))
                status = order.get('Status', 'Unknown')

                if status == 'Completed':
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                elif status == 'Pending':
                    status_item.setForeground(Qt.GlobalColor.darkYellow)
                elif status == 'Processing':
                    status_item.setForeground(Qt.GlobalColor.darkBlue)
                elif status == 'Cancelled':
                    status_item.setForeground(Qt.GlobalColor.darkRed)

                table.setItem(row_num, 2, status_item)

                # Total Amount
                table.setItem(row_num, 3, QTableWidgetItem(f"₱{order.get('TotalAmount', 0):.2f}"))

                # Hidden OrderID
                order_id_item = QTableWidgetItem()
                order_id_item.setData(Qt.ItemDataRole.UserRole, order['OrderID'])
                table.setItem(row_num, 4, order_id_item)

            # Stretch first two columns, others resize to content
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, header.ResizeMode.Stretch)
            header.setSectionResizeMode(1, header.ResizeMode.Stretch)
            for col in range(2, 4):
                header.setSectionResizeMode(col, header.ResizeMode.ResizeToContents)

            print(f"✓ Found {len(order_list)} orders matching '{search_term}'")

        except Exception as e:
            print(f"✗ Error searching orders: {e}")
            import traceback
            traceback.print_exc()

    def view_order_details(self):
        """View order details"""
        if not hasattr(self.staff_home, "tableWidget_3"):
            return

        selected_items = self.staff_home.tableWidget_3.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.staff_home, "No Selection", "Please select an order first.")
            return

        selected_row = selected_items[0].row()
        order_id_item = self.staff_home.tableWidget_3.item(selected_row, 4)

        if not order_id_item:
            return

        order_id = order_id_item.data(Qt.ItemDataRole.UserRole)

        # Get full order details
        order_details = self.model.get_order_by_id(order_id)

        if not order_details:
            QMessageBox.warning(self.staff_home, "Error", "Could not load order details.")
            return

        self.show_order_details()

    def on_order_table_double_click(self, row, column):
        """Handle double-click on order table"""
        self.view_order_details()

    def edit_order(self):
        """Edit order - loads data into edit form and navigates to edit page"""
        if not hasattr(self.staff_home, "tableWidget_3"):
            return

        selected_items = self.staff_home.tableWidget_3.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self.staff_home,
                "No Selection",
                "Please select an order to edit."
            )
            return

        try:
            selected_row = selected_items[0].row()

            # Get status from the table
            status_item = self.staff_home.tableWidget_3.item(selected_row, 2)
            current_status = status_item.text() if status_item else "Unknown"

            # Check if order is cancelled
            if current_status == 'Cancelled':
                QMessageBox.warning(
                    self.staff_home,
                    "Cannot Edit",
                    "Cancelled orders cannot be edited.\n\n"
                    "Once an order is cancelled, its data is locked and cannot be modified."
                )
                return

            # Get OrderID from hidden column
            order_id_item = self.staff_home.tableWidget_3.item(selected_row, 4)

            if not order_id_item:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "Could not retrieve order ID from table."
                )
                return

            order_id = order_id_item.data(Qt.ItemDataRole.UserRole)

            # Check if edit order control is available
            if not self.edit_order_control:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "Edit order controller not initialized."
                )
                return

            print(f"✓ SOControl: Loading order {self.format_order_id(order_id)} for editing")

            # Load order data into edit form
            success = self.edit_order_control.load_order_data(order_id)

            if success:
                # Navigate to edit order page using the EditOrder_page_index attribute
                if hasattr(self.staff_home, 'EditOrder_page_index'):
                    self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.EditOrder_page_index)
                    print(f"✓ Navigated to Edit Order page (index: {self.staff_home.EditOrder_page_index})")
                else:
                    QMessageBox.warning(
                        self.staff_home,
                        "Navigation Error",
                        "Edit Order page index not found."
                    )
                    print("⚠ EditOrder_page_index not found in staff_home")

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.staff_home,
                "Error",
                f"Failed to load order for editing:\n{str(e)}"
            )

    def delete_order(self):
        """Delete order - Cancelled orders cannot be deleted"""
        if not hasattr(self.staff_home, "tableWidget_3"):
            return

        selected_items = self.staff_home.tableWidget_3.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.staff_home, "No Selection", "Please select an order to delete.")
            return

        selected_row = selected_items[0].row()
        order_id_display = self.staff_home.tableWidget_3.item(selected_row, 0).text()

        # Get status from the table
        status_item = self.staff_home.tableWidget_3.item(selected_row, 2)
        current_status = status_item.text() if status_item else "Unknown"

        # Check if order is cancelled
        if current_status == 'Cancelled':
            QMessageBox.warning(
                self.staff_home,
                "Cannot Delete",
                f"Cancelled orders cannot be deleted.\n\n"
                f"Order {order_id_display} has been cancelled and its data is protected."
            )
            return

        order_id_item = self.staff_home.tableWidget_3.item(selected_row, 4)

        if not order_id_item:
            return

        order_id = order_id_item.data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(
            self.staff_home,
            "Confirm Delete",
            f"Are you sure you want to delete Order {order_id_display}?\n\nThis will also delete all associated services and transactions.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.model.delete_order(order_id)
                if success:
                    self.staff_home.tableWidget_3.removeRow(selected_row)
                    print(f"✓ Deleted order: {order_id_display}")
                    QMessageBox.information(self.staff_home, "Success", "Order deleted successfully!")
                else:
                    QMessageBox.warning(self.staff_home, "Error", "Failed to delete order.")
            except Exception as e:
                print(f"✗ Error deleting order: {e}")
                QMessageBox.critical(self.staff_home, "Error", f"Error deleting order: {e}")

    def sort_orders(self):
        """Sort order table by Order ID"""
        if not hasattr(self.staff_home, "tableWidget_3"):
            return

        if self.sort_ascending_order:
            self.staff_home.tableWidget_3.sortItems(0, Qt.SortOrder.AscendingOrder)
            if hasattr(self.staff_home, "name_srt_btn_3"):
                self.staff_home.name_srt_btn_3.setText("Order ID ▲")
        else:
            self.staff_home.tableWidget_3.sortItems(0, Qt.SortOrder.DescendingOrder)
            if hasattr(self.staff_home, "name_srt_btn_3"):
                self.staff_home.name_srt_btn_3.setText("Order ID ▼")

        self.sort_ascending_order = not self.sort_ascending_order

    # ==================== NAVIGATION METHODS ====================

    def go_to_home(self):
        print("Navigating to Home")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.home_page_index)

    def go_to_dashboard(self):
        print("Navigating to Dashboard")
        self.dashboard.show()

    def go_to_orders(self):
        print("Navigating to Orders")
        # Ensure we're showing the correct page
        if hasattr(self.staff_home, 'order_page_index'):
            self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.order_page_index)
        else:
            self.order.show()

        # Force refresh when navigating via button click
        self.refresh_order_table()

    def go_to_users(self):
        print("Navigating to Users/Customers")
        self.customer.show()

    def go_to_reports(self):
        print("Navigating to Reports")
        self.report.show()

    def go_to_delivery(self):
        self.delivery.show()

    def go_to_logout(self):
        """Handle logout with confirmation"""

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

        # NOW show confirmation dialog (no popups blocking it)
        reply = QMessageBox.question(
            self.staff_home,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print("Logging out...")

            self.staff_home.close()

            # Clear login fields for security
            if hasattr(self.login_view, 'username'):
                self.login_view.username.clear()
            if hasattr(self.login_view, 'password'):
                self.login_view.password.clear()

            # Show login view
            self.login_view.show()
            if hasattr(self.login_view, 'username'):
                self.login_view.username.setFocus()
        else:
            print("Logout cancelled")