from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QColor

# Add this import - SAME AS SOControl
from View.OrderPopup import OrderDetailsPopup


class AOrderControl:
    """Controller for Admin Order Management page"""

    def __init__(self, admin_home, dashboard, manager, order, report, model, login_view):
        self.admin_home = admin_home
        self.dashboard = dashboard
        self.manager = manager
        self.order = order
        self.report = report
        self.model = model
        self.login_view = login_view

        # Initialize the popup instance like in SOControl
        self.order_popup = None
        self.sort_ascending_order = True

        # Connect to page change signal for auto-refresh
        if hasattr(self.admin_home, 'stackedWidget'):
            self.admin_home.stackedWidget.currentChanged.connect(self.on_page_changed)
            print("✓ AOrderControl: Connected to stackedWidget page change signal")

        # Connect buttons from Order page
        self.connect_order_buttons()

        # Load order data when initialized
        self.load_order_data()

    def on_page_changed(self, index):
        """Automatically refresh order data when order page becomes visible"""
        if hasattr(self.admin_home, 'order_page_index'):
            if index == self.admin_home.order_page_index:
                print("✓ Admin: Order page activated - refreshing data")
                self.load_order_data()

    def format_order_id(self, order_id):
        """Format order ID as WSHY#001, WSHY#002, etc. - same as SOControl"""
        return f"WSHY#{order_id:03d}"

    def connect_order_buttons(self):
        """Connect navigation and action buttons on the Order page"""

        # Sidebar buttons
        if hasattr(self.admin_home, "Homebut_8"):
            self.admin_home.Homebut_8.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "Dashbut_8"):
            self.admin_home.Dashbut_8.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "Userbut_8"):
            self.admin_home.Userbut_8.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "Orderbut_8"):
            self.admin_home.Orderbut_8.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "Reportbut_8"):
            self.admin_home.Reportbut_8.clicked.connect(self.go_to_reports)

        if hasattr(self.admin_home, "Settbut_8"):
            self.admin_home.Settbut_8.clicked.connect(self.go_to_logout)

        # Icon buttons
        if hasattr(self.admin_home, "h2_7"):
            self.admin_home.h2_7.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "db2_7"):
            self.admin_home.db2_7.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "s2_7"):
            self.admin_home.s2_7.clicked.connect(self.go_to_logout)

        if hasattr(self.admin_home, "o2_7"):
            self.admin_home.o2_7.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "r2_7"):
            self.admin_home.r2_7.clicked.connect(self.go_to_reports)

        if hasattr(self.admin_home, "u2_7"):
            self.admin_home.u2_7.clicked.connect(self.go_to_users)

        # 🔧 FIXED: Connect View button using the correct method name
        if hasattr(self.admin_home, "view"):  # View button
            self.admin_home.view.clicked.connect(self.show_order_details)

        if hasattr(self.admin_home, "nwbut_9"):  # Delete button
            self.admin_home.nwbut_9.clicked.connect(self.delete_order)

        # Connect search field
        if hasattr(self.admin_home, "line3"):
            self.admin_home.line3.textChanged.connect(self.search_order)

        # Connect sort button
        if hasattr(self.admin_home, "name_srt_btn_3"):
            self.admin_home.name_srt_btn_3.clicked.connect(self.sort_orders)

        # Connect order table double-click
        if hasattr(self.admin_home, "tableWidget_3"):
            self.admin_home.tableWidget_3.cellDoubleClicked.connect(
                self.on_order_table_double_click
            )
            print("✓ Connected tableWidget_3 double-click")
        else:
            print("✗ tableWidget_3 not found in Admin")

    def load_order_data(self):
        """Load all order data into the table"""
        if not hasattr(self.admin_home, "tableWidget_3"):
            print("✗ Error: tableWidget_3 not found in Admin")
            return

        try:
            order_list = self.model.get_all_orders()
            table = self.admin_home.tableWidget_3
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

            print(f"✓ Admin: Loaded {len(order_list)} orders")

        except Exception as e:
            print(f"✗ Admin: Error loading order data: {e}")
            import traceback
            traceback.print_exc()

    def refresh_order_table(self):
        """Public method to refresh the order table"""
        print("✓ Admin: Refreshing order table...")
        self.load_order_data()

    def search_order(self):
        """Search orders by order ID, customer name, or status"""
        if not hasattr(self.admin_home, "line3"):
            return

        search_term = self.admin_home.line3.text().strip()

        if not search_term:
            self.load_order_data()
            return

        try:
            order_list = self.model.search_orders(search_term)
            table = self.admin_home.tableWidget_3
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

            print(f"✓ Admin: Found {len(order_list)} orders matching '{search_term}'")

        except Exception as e:
            print(f"✗ Admin: Error searching orders: {e}")
            import traceback
            traceback.print_exc()

    def show_order_details(self):
        """Show order details popup"""
        if not hasattr(self.admin_home, "tableWidget_3"):
            return

        selected_items = self.admin_home.tableWidget_3.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self.admin_home,
                "No Selection",
                "Please select an order first."
            )
            return

        try:
            selected_row = selected_items[0].row()
            order_id_item = self.admin_home.tableWidget_3.item(selected_row, 4)

            if not order_id_item:
                QMessageBox.warning(
                    self.admin_home,
                    "Error",
                    "Could not retrieve order ID from table."
                )
                return

            order_id = order_id_item.data(Qt.ItemDataRole.UserRole)

            print(f"✓ AOrderControl: Loading order details for Order {self.format_order_id(order_id)}")

            # Create popup with model if it doesn't exist - EXACT SAME AS STAFF
            if self.order_popup is None:
                self.order_popup = OrderDetailsPopup(parent=self.admin_home, model=self.model)
                print("✓ Created NEW popup instance for Admin")

            # Load data
            success = self.order_popup.loadOrderFromDatabase(order_id)

            if not success:
                QMessageBox.warning(
                    self.admin_home,
                    "Error",
                    "Could not load order details."
                )
                return

            # Center and show
            self.center_popup(self.order_popup)
            self.order_popup.show()
            self.order_popup.raise_()
            self.order_popup.activateWindow()

            print(f"✓ Popup shown, dragging should work now")

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.admin_home,
                "Error",
                f"An error occurred:\n{str(e)}"
            )

    def center_popup(self, popup):
        """Center popup on main window - EXACT COPY FROM SOCONTROL"""
        main_geometry = self.admin_home.frameGeometry()
        main_center = main_geometry.center()
        popup_x = main_center.x() - popup.width() // 2
        popup_y = main_center.y() - popup.height() // 2
        popup.move(popup_x, popup_y)

    def delete_order(self):
        """Delete order"""
        if not hasattr(self.admin_home, "tableWidget_3"):
            QMessageBox.warning(self.admin_home, "Error", "Order table not found.")
            return

        selected_items = self.admin_home.tableWidget_3.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.admin_home, "No Selection", "Please select an order to delete.")
            return

        selected_row = selected_items[0].row()
        order_id_display = self.admin_home.tableWidget_3.item(selected_row, 0).text()
        order_id_item = self.admin_home.tableWidget_3.item(selected_row, 4)

        if not order_id_item:
            QMessageBox.warning(self.admin_home, "Error", "Could not get order ID.")
            return

        order_id = order_id_item.data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(
            self.admin_home,
            "Confirm Delete",
            f"Are you sure you want to delete Order {order_id_display}?\n\nThis will also delete all associated services and transactions.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.model.delete_order(order_id)
                if success:
                    self.admin_home.tableWidget_3.removeRow(selected_row)
                    print(f"✓ Admin: Deleted order: {order_id_display}")
                    QMessageBox.information(self.admin_home, "Success", "Order deleted successfully!")
                else:
                    QMessageBox.warning(self.admin_home, "Error", "Failed to delete order.")
            except Exception as e:
                print(f"✗ Admin: Error deleting order: {e}")
                QMessageBox.critical(self.admin_home, "Error", f"Error deleting order: {e}")

    def sort_orders(self):
        """Sort order table by Order ID"""
        if not hasattr(self.admin_home, "tableWidget_3"):
            return

        if self.sort_ascending_order:
            self.admin_home.tableWidget_3.sortItems(0, Qt.SortOrder.AscendingOrder)
            if hasattr(self.admin_home, "name_srt_btn_3"):
                self.admin_home.name_srt_btn_3.setText("Order ID ▲")
        else:
            self.admin_home.tableWidget_3.sortItems(0, Qt.SortOrder.DescendingOrder)
            if hasattr(self.admin_home, "name_srt_btn_3"):
                self.admin_home.name_srt_btn_3.setText("Order ID ▼")

        self.sort_ascending_order = not self.sort_ascending_order

    def on_order_table_double_click(self, row, column):
        """Handle double-click on order table"""
        self.show_order_details()

    # ==================== NAVIGATION METHODS ====================

    def go_to_home(self):
        print("Admin: Navigating to Home")
        self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.home_page_index)

    def go_to_dashboard(self):
        print("Admin: Navigating to Dashboard")
        self.dashboard.show()

    def go_to_users(self):
        print("Admin: Navigating to Users")
        self.ashow()

    def go_to_orders(self):
        print("Admin: Navigating to Orders")
        # Refresh the table before showing the page
        self.refresh_order_table()
        self.order.show()

    def go_to_reports(self):
        print("Admin: Navigating to Reports")
        self.report.show()

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
            self.admin_home,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print("Admin: Logging out...")

            self.admin_home.close()

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
            print("Admin: Logout cancelled")

