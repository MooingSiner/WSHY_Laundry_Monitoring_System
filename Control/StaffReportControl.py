from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

from View.OrderPopup import OrderDetailsPopup


class SReportControl:
    """Controller for Staff Report/History page"""

    def __init__(self, staff_home, dashboard, customer, order, delivery, report, model, login_view):
        self.staff_home = staff_home
        self.dashboard = dashboard
        self.customer = customer
        self.order = order
        self.report = report
        self.delivery = delivery
        self.model = model
        self.login_view = login_view

        self.order_popup = None
        self.sort_ascending_history = True
        self.current_filter = "All"  # Track current filter

        self.connect_report_buttons()

        # Load all orders initially
        self.load_history_data()

    def format_order_id(self, order_id):
        """Format order ID as WSHY#001, WSHY#002, etc."""
        return f"WSHY#{order_id:03d}"

    def connect_report_buttons(self):
        """Connect navigation and action buttons on the Report/History page"""

        # Sidebar buttons - History page uses _4 suffix
        if hasattr(self.staff_home, "Homebut_4"):
            self.staff_home.Homebut_4.clicked.connect(self.go_to_home)

        if hasattr(self.staff_home, "Dashbut_4"):
            self.staff_home.Dashbut_4.clicked.connect(self.go_to_dashboard)

        if hasattr(self.staff_home, "Userbut_4"):
            self.staff_home.Userbut_4.clicked.connect(self.go_to_customers)

        if hasattr(self.staff_home, "Orderbut_4"):
            self.staff_home.Orderbut_4.clicked.connect(self.go_to_orders)

        if hasattr(self.staff_home, "Reportbut_4"):
            self.staff_home.Reportbut_4.clicked.connect(self.go_to_reports)

        if hasattr(self.staff_home, "Delivlab_4"):
            self.staff_home.Delivlab_4.clicked.connect(self.go_to_delivery)

        if hasattr(self.staff_home, "Settbut_4"):
            self.staff_home.Settbut_4.clicked.connect(self.go_to_logout)

        # Icon buttons - History page uses _3 suffix
        if hasattr(self.staff_home, "h1_3"):
            self.staff_home.h1_3.clicked.connect(self.go_to_home)

        if hasattr(self.staff_home, "db1_3"):
            self.staff_home.db1_3.clicked.connect(self.go_to_dashboard)

        if hasattr(self.staff_home, "s1_3"):
            self.staff_home.s1_3.clicked.connect(self.go_to_logout)

        if hasattr(self.staff_home, "o1_3"):
            self.staff_home.o1_3.clicked.connect(self.go_to_orders)

        if hasattr(self.staff_home, "r1_3"):
            self.staff_home.r1_3.clicked.connect(self.go_to_reports)

        if hasattr(self.staff_home, "u1_3"):
            self.staff_home.u1_3.clicked.connect(self.go_to_customers)

        if hasattr(self.staff_home, "d1_3"):
            self.staff_home.d1_3.clicked.connect(self.go_to_delivery)

        # Action buttons
        if hasattr(self.staff_home, "nwbut_13"):  # View button
            self.staff_home.nwbut_13.clicked.connect(self.show_order_details)

        if hasattr(self.staff_home, "nwbut_11"):  # Edit button
            self.staff_home.nwbut_11.clicked.connect(self.edit_order)

        if hasattr(self.staff_home, "nwbut_14"):  # Delete button
            self.staff_home.nwbut_14.clicked.connect(self.delete_order)

        # Connect search field
        if hasattr(self.staff_home, "line4"):
            self.staff_home.line4.textChanged.connect(self.search_history)

        # Connect filter/sort button
        if hasattr(self.staff_home, "name_srt_btn_4"):
            self.staff_home.name_srt_btn_4.clicked.connect(self.toggle_filter)

        # Connect table double-click
        if hasattr(self.staff_home, "tableWidget_4"):
            self.staff_home.tableWidget_4.cellDoubleClicked.connect(
                self.on_history_table_double_click
            )

    def load_history_data(self, filter_status=None):
        """Load all order history data into the table"""
        if not hasattr(self.staff_home, "tableWidget_4"):
            print("Error: tableWidget_4 not found")
            return

        try:
            # Get orders based on filter
            if filter_status:
                order_list = self.model.get_orders_by_status(filter_status)
            else:
                order_list = self.model.get_all_orders()

            table = self.staff_home.tableWidget_4
            table.setRowCount(0)
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(
                ["Order ID", "Status", "Date", "Total Amount", "OrderID_Hidden"]
            )
            table.setColumnHidden(4, True)

            for row_num, order in enumerate(order_list):
                table.insertRow(row_num)

                # Order ID - formatted as WSHY#001
                formatted_id = self.format_order_id(order['OrderID'])
                table.setItem(row_num, 0, QTableWidgetItem(formatted_id))

                # Status
                status_item = QTableWidgetItem(order.get('Status', 'Unknown'))
                status = order.get('Status', 'Unknown')
                if status == 'Completed':
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                elif status == 'Pending':
                    status_item.setForeground(Qt.GlobalColor.darkYellow)
                elif status == 'Processing':
                    status_item.setForeground(Qt.GlobalColor.darkBlue)
                table.setItem(row_num, 1, status_item)

                # Order Date
                order_date = order.get('OrderDate')
                order_date_str = order_date.strftime('%Y-%m-%d') if order_date and hasattr(
                    order_date, 'strftime'
                ) else ('N/A' if not order_date else str(order_date))
                table.setItem(row_num, 2, QTableWidgetItem(order_date_str))

                # Total Amount
                table.setItem(row_num, 3, QTableWidgetItem(f"₱{order.get('TotalAmount', 0):.2f}"))

                # Hidden OrderID
                order_id_item = QTableWidgetItem()
                order_id_item.setData(Qt.ItemDataRole.UserRole, order['OrderID'])
                table.setItem(row_num, 4, order_id_item)

            # Stretch first column, others resize to content
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, header.ResizeMode.Stretch)
            for col in range(1, 4):
                header.setSectionResizeMode(col, header.ResizeMode.ResizeToContents)

            print(f"✓ Staff: Loaded {len(order_list)} orders in history")

        except Exception as e:
            print(f"✗ Staff: Error loading history data: {e}")
            import traceback
            traceback.print_exc()

    def search_history(self):
        """Search order history"""
        if not hasattr(self.staff_home, "line4"):
            return

        search_term = self.staff_home.line4.text().strip()

        if not search_term:
            self.load_history_data()
            return

        try:
            order_list = self.model.search_orders(search_term)
            table = self.staff_home.tableWidget_4
            table.setRowCount(0)
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(
                ["Order ID", "Status", "Date", "Total Amount", "OrderID_Hidden"]
            )
            table.setColumnHidden(4, True)

            for row_num, order in enumerate(order_list):
                table.insertRow(row_num)

                # Order ID - formatted as WSHY#001
                formatted_id = self.format_order_id(order['OrderID'])
                table.setItem(row_num, 0, QTableWidgetItem(formatted_id))

                # Status
                status_item = QTableWidgetItem(order.get('Status', 'Unknown'))
                status = order.get('Status', 'Unknown')
                if status == 'Completed':
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                elif status == 'Pending':
                    status_item.setForeground(Qt.GlobalColor.darkYellow)
                elif status == 'Processing':
                    status_item.setForeground(Qt.GlobalColor.darkBlue)
                table.setItem(row_num, 1, status_item)

                # Order Date
                order_date = order.get('OrderDate')
                order_date_str = order_date.strftime('%Y-%m-%d') if order_date and hasattr(
                    order_date, 'strftime'
                ) else ('N/A' if not order_date else str(order_date))
                table.setItem(row_num, 2, QTableWidgetItem(order_date_str))

                # Total Amount
                table.setItem(row_num, 3, QTableWidgetItem(f"₱{order.get('TotalAmount', 0):.2f}"))

                # Hidden OrderID
                order_id_item = QTableWidgetItem()
                order_id_item.setData(Qt.ItemDataRole.UserRole, order['OrderID'])
                table.setItem(row_num, 4, order_id_item)

            # Stretch first column, others resize to content
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, header.ResizeMode.Stretch)
            for col in range(1, 4):
                header.setSectionResizeMode(col, header.ResizeMode.ResizeToContents)

            print(f"✓ Staff: Found {len(order_list)} orders matching '{search_term}'")

        except Exception as e:
            print(f"✗ Staff: Error searching history: {e}")
            import traceback
            traceback.print_exc()

    def toggle_filter(self):
        """Toggle between different status filters"""
        filters = ["All", "Completed", "Pending", "Processing"]

        # Get current filter index
        current_index = filters.index(self.current_filter)
        # Move to next filter
        next_index = (current_index + 1) % len(filters)
        self.current_filter = filters[next_index]

        # Update button text
        if hasattr(self.staff_home, "name_srt_btn_4"):
            self.staff_home.name_srt_btn_4.setText(self.current_filter)

        # Load data with filter
        if self.current_filter == "All":
            self.load_history_data()
        else:
            self.load_history_data(self.current_filter)

    def show_order_details(self):
        """Show order details popup"""
        if not hasattr(self.staff_home, "tableWidget_4"):
            return

        selected_items = self.staff_home.tableWidget_4.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self.staff_home,
                "No Selection",
                "Please select an order first."
            )
            return

        try:
            selected_row = selected_items[0].row()

            # Get OrderID from hidden column 4 (NOT from display column 0)
            order_id_item = self.staff_home.tableWidget_4.item(selected_row, 4)

            if not order_id_item:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "Could not retrieve order ID from table."
                )
                return

            # Get the actual order ID from UserRole data
            order_id = order_id_item.data(Qt.ItemDataRole.UserRole)

            print(f"✓ SReportControl: Loading order details for Order {self.format_order_id(order_id)}")

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

    def view_order_details(self):
        """View order details (alias for show_order_details)"""
        self.show_order_details()

    def on_history_table_double_click(self, row, column):
        """Handle double-click on history table"""
        self.show_order_details()

    def edit_order(self):
        """Edit order"""
        if not hasattr(self.staff_home, "tableWidget_4"):
            return

        selected_items = self.staff_home.tableWidget_4.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.staff_home, "No Selection", "Please select an order to edit.")
            return

        print("Staff: Edit order - TODO: Implement order edit")
        # TODO: Implement order edit dialog

    def delete_order(self):
        """Delete order from history"""
        if not hasattr(self.staff_home, "tableWidget_4"):
            return

        selected_items = self.staff_home.tableWidget_4.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.staff_home, "No Selection", "Please select an order to delete.")
            return

        selected_row = selected_items[0].row()
        order_id_display = self.staff_home.tableWidget_4.item(selected_row, 0).text()
        order_id_item = self.staff_home.tableWidget_4.item(selected_row, 4)

        if not order_id_item:
            return

        order_id = order_id_item.data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(
            self.staff_home,
            "Confirm Delete",
            f"Are you sure you want to delete Order {order_id_display}?\n\nThis will permanently remove all order data.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.model.delete_order(order_id)
                if success:
                    self.staff_home.tableWidget_4.removeRow(selected_row)
                    print(f"✓ Staff: Deleted order: {order_id_display}")
                    QMessageBox.information(self.staff_home, "Success", "Order deleted successfully!")
                else:
                    QMessageBox.warning(self.staff_home, "Error", "Failed to delete order.")
            except Exception as e:
                print(f"✗ Staff: Error deleting order: {e}")
                QMessageBox.critical(self.staff_home, "Error", f"Error deleting order: {e}")

    # ==================== NAVIGATION METHODS ====================

    def go_to_home(self):
        print("Staff: Navigating to Home")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.home_page_index)

    def go_to_dashboard(self):
        print("Staff: Navigating to Dashboard")
        self.dashboard.show()

    def go_to_customers(self):
        print("Staff: Navigating to Customers")
        self.customer.show()

    def go_to_orders(self):
        print("Staff: Navigating to Orders")
        self.order.show()

    def go_to_reports(self):
        print("Staff: Navigating to Reports")
        self.load_history_data()  # Refresh data
        self.report.show()

    def go_to_delivery(self):
        print("Staff: Navigating to Delivery")
        self.delivery.show()

    def go_to_logout(self):
        """Handle logout with confirmation"""
        reply = QMessageBox.question(
            self.staff_home,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print("Staff: Logging out...")
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
            print("Staff: Logout cancelled")
