from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

from View.CustomerDetailsPopup import CustomerDetailsPopup


class AManagerControlC:
    """Controller for Customer Manager page"""

    def __init__(self, admin_home, dashboard, manager, managerc, order, report, cust, model, editcustomer, editcustomer_control,login_view):
        self.admin_home = admin_home
        self.dashboard = dashboard
        self.manager = manager
        self.managerc = managerc
        self.order = order
        self.report = report
        self.cust = cust
        self.model = model
        self.editcustomer = editcustomer  # Edit customer VIEW
        self.editcustomer_control = editcustomer_control  # Edit customer CONTROLLER
        self.login_view = login_view

        self.sort_ascending_customer = True

        # CRITICAL: Set bidirectional reference
        self.editcustomer_control.managerc_control = self

        # Connect buttons from Customer Manager page
        self.connect_managerc_buttons()
        self.customer_popup = None

        # Load customer data when initialized
        self.load_customer_data()

    def connect_managerc_buttons(self):
        """Connect navigation buttons on the Customer Manager page"""
        # Sidebar buttons (kept as is)
        if hasattr(self.admin_home, "Homebut_7"):
            self.admin_home.Homebut_7.clicked.connect(self.go_to_home)
        if hasattr(self.admin_home, "Dashbut_7"):
            self.admin_home.Dashbut_7.clicked.connect(self.go_to_dashboard)
        if hasattr(self.admin_home, "Userbut_7"):
            self.admin_home.Userbut_7.clicked.connect(self.go_to_users)
        if hasattr(self.admin_home, "gotc_2"):
            self.admin_home.gotc_2.clicked.connect(self.go_to_users)
        if hasattr(self.admin_home, "Orderbut_7"):
            self.admin_home.Orderbut_7.clicked.connect(self.go_to_orders)
        if hasattr(self.admin_home, "Reportbut_7"):
            self.admin_home.Reportbut_7.clicked.connect(self.go_to_reports)
        if hasattr(self.admin_home, "Settbut_7"):
            self.admin_home.Settbut_7.clicked.connect(self.go_to_logout)

        # Icon buttons
        if hasattr(self.admin_home, "h2_5"):
            self.admin_home.h2_5.clicked.connect(self.go_to_home)
        if hasattr(self.admin_home, "db2_5"):
            self.admin_home.db2_5.clicked.connect(self.go_to_dashboard)
        if hasattr(self.admin_home, "u2_5"):
            self.admin_home.u2_5.clicked.connect(self.go_to_users)
        if hasattr(self.admin_home, "s2_5"):
            self.admin_home.s2_5.clicked.connect(self.go_to_logout)
        if hasattr(self.admin_home, "o2_5"):
            self.admin_home.o2_5.clicked.connect(self.go_to_orders)
        if hasattr(self.admin_home, "r2_5"):
            self.admin_home.r2_5.clicked.connect(self.go_to_reports)

        # Customer action buttons
        if hasattr(self.admin_home, "nwbut_8"):
            self.admin_home.nwbut_8.clicked.connect(self.go_to_ccv)
        if hasattr(self.admin_home, "nwbut_6"):
            self.admin_home.nwbut_6.clicked.connect(self.show_customer_details)
        if hasattr(self.admin_home, "nwbut_7"):
            self.admin_home.nwbut_7.clicked.connect(self.edit_customer)
        if hasattr(self.admin_home, "nwbut_5"):
            self.admin_home.nwbut_5.clicked.connect(self.delete_customer)

        # Connect search field (fixed to line2)
        if hasattr(self.admin_home, "line2"):
            self.admin_home.line2.textChanged.connect(self.search_customer)

        # Connect sort button
        if hasattr(self.admin_home, "name_srt_btn_2"):
            self.admin_home.name_srt_btn_2.clicked.connect(self.sort_customer_by_name)

        # Customer table double-click
        if hasattr(self.admin_home, "tableWidget_2"):
            self.admin_home.tableWidget_2.cellDoubleClicked.connect(self.on_customer_table_double_click)

    def load_customer_data(self):
        """Load all customer data into the table with correct structure and stretch first column"""
        if not hasattr(self.admin_home, "tableWidget_2"):
            print("Error: tableWidget_2 not found")
            return

        try:
            customer_list = self.model.get_all_customers()
            table = self.admin_home.tableWidget_2
            table.setRowCount(0)
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["Name", "Total Orders", "Last Order", "CustomerID"])
            table.setColumnHidden(3, True)

            for row_num, customer in enumerate(customer_list):
                table.insertRow(row_num)

                # Full Name
                full_name = f"{customer['CFName']} {customer['CMName'] or ''} {customer['CLName']}".strip()
                table.setItem(row_num, 0, QTableWidgetItem(' '.join(full_name.split())))

                # Total Orders
                table.setItem(row_num, 1, QTableWidgetItem(str(customer.get('total_orders', 0))))

                # Last Order
                last_order = customer.get('last_order_date')
                last_order_str = last_order.strftime('%Y-%m-%d') if last_order and hasattr(last_order,
                                                                                           'strftime') else (
                    'No orders' if not last_order else str(last_order))
                table.setItem(row_num, 2, QTableWidgetItem(last_order_str))

                # CustomerID (hidden)
                customer_id_item = QTableWidgetItem()
                customer_id_item.setData(Qt.ItemDataRole.UserRole, customer['CustomerID'])
                table.setItem(row_num, 3, customer_id_item)

            # Stretch first column, other columns to contents
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, header.ResizeMode.Stretch)
            for col in range(1, 3):
                header.setSectionResizeMode(col, header.ResizeMode.ResizeToContents)

            print(f"✓ Loaded {len(customer_list)} customers")

        except Exception as e:
            print(f"✗ Error loading customer data: {e}")
            import traceback
            traceback.print_exc()

    def search_customer(self):
        """Search customers and stretch first column during search"""
        if not hasattr(self.admin_home, "line2") or not hasattr(self.admin_home, "tableWidget_2"):
            return

        search_term = self.admin_home.line2.text().strip()
        table = self.admin_home.tableWidget_2
        header = table.horizontalHeader()

        # Store original resize modes once
        if not hasattr(self, "original_resize_modes_customer"):
            self.original_resize_modes_customer = []
            for col in range(table.columnCount()):
                self.original_resize_modes_customer.append(header.sectionResizeMode(col))

        if not search_term:
            # Restore original modes
            if hasattr(self, "original_resize_modes_customer"):
                for col, mode in enumerate(self.original_resize_modes_customer):
                    header.setSectionResizeMode(col, mode)
            self.load_customer_data()
            return

        # Stretch first column, other columns to contents
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)
        for col in range(1, 3):
            header.setSectionResizeMode(col, header.ResizeMode.ResizeToContents)

        try:
            customer_list = self.model.search_customers(search_term)

            # Clear and setup table
            table.setRowCount(0)
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["Name", "Total Orders", "Last Order", "CustomerID"])
            table.setColumnHidden(3, True)

            for row_num, customer in enumerate(customer_list):
                table.insertRow(row_num)
                full_name = f"{customer['CFName']} {customer['CMName'] or ''} {customer['CLName']}".strip()
                table.setItem(row_num, 0, QTableWidgetItem(' '.join(full_name.split())))
                table.setItem(row_num, 1, QTableWidgetItem(str(customer.get('total_orders', 0))))
                last_order = customer.get('last_order_date')
                last_order_str = last_order.strftime('%Y-%m-%d') if last_order and hasattr(last_order,
                                                                                           'strftime') else (
                    'No orders' if not last_order else str(last_order))
                table.setItem(row_num, 2, QTableWidgetItem(last_order_str))
                customer_id_item = QTableWidgetItem()
                customer_id_item.setData(Qt.ItemDataRole.UserRole, customer['CustomerID'])
                table.setItem(row_num, 3, customer_id_item)

            print(f"✓ Found {len(customer_list)} customers matching '{search_term}'")

        except Exception as e:
            print(f"✗ Error searching customers: {e}")
            import traceback
            traceback.print_exc()

    def show_customer_details(self):
        """Show customer details popup"""
        if not hasattr(self.admin_home, "tableWidget_2"):
            return

        selected_items = self.admin_home.tableWidget_2.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.admin_home, "No Selection", "Please select a customer first.")
            return

        selected_row = selected_items[0].row()
        customer_id_item = self.admin_home.tableWidget_2.item(selected_row, 3)  # Column 3 has CustomerID

        if not customer_id_item:
            return

        customer_id = customer_id_item.data(Qt.ItemDataRole.UserRole)

        # Create popup with model if it doesn't exist
        if self.customer_popup is None:
            self.customer_popup = CustomerDetailsPopup(parent=self.admin_home, model=self.model)

        # Load data directly from database using the customer ID
        success = self.customer_popup.loadCustomerFromDatabase(customer_id)

        if not success:
            QMessageBox.warning(self.admin_home, "Error", "Could not load customer details.")
            return

        self.center_popup(self.customer_popup)
        self.customer_popup.show()
        self.customer_popup.raise_()
        self.customer_popup.activateWindow()

    def on_customer_table_double_click(self, row, column):
        """Handle double-click on customer table"""
        self.show_customer_details()


    def edit_customer(self):
        """Edit selected customer - FOLLOWING STAFF PATTERN"""
        if not hasattr(self.admin_home, "tableWidget_2"):
            print("Error: Table widget not found")
            return

        selected_items = self.admin_home.tableWidget_2.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self.admin_home,
                "No Selection",
                "Please select a customer to edit."
            )
            return

        try:
            selected_row = selected_items[0].row()
            customer_name = self.admin_home.tableWidget_2.item(selected_row, 0).text()

            # Get CustomerID from column 3 (hidden)
            customer_id_item = self.admin_home.tableWidget_2.item(selected_row, 3)
            if not customer_id_item:
                QMessageBox.warning(
                    self.admin_home,
                    "Error",
                    "Could not retrieve customer ID from table."
                )
                return

            customer_id = customer_id_item.data(Qt.ItemDataRole.UserRole)

            print(f"✓ Editing customer: {customer_name} (ID: {customer_id})")

            # CRITICAL FIX: Load data FIRST, then show the page
            success = self.editcustomer_control.load_customer_data(customer_id)

            if success:
                # Show edit page using stackedWidget
                self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.EditCustomer_page_index)
            else:
                QMessageBox.warning(
                    self.admin_home,
                    "Error",
                    "Failed to load customer data for editing."
                )

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.admin_home,
                "Error",
                f"An error occurred while preparing to edit:\n{str(e)}"
            )

    def delete_customer(self):
        """Delete customer"""
        if not hasattr(self.admin_home, "tableWidget_2"):
            return

        selected_items = self.admin_home.tableWidget_2.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.admin_home, "No Selection", "Please select a customer to delete.")
            return

        selected_row = selected_items[0].row()
        customer_name = self.admin_home.tableWidget_2.item(selected_row, 0).text()
        customer_id_item = self.admin_home.tableWidget_2.item(selected_row, 3)

        if not customer_id_item:
            return

        customer_id = customer_id_item.data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(
            self.admin_home,
            "Confirm Delete",
            f"Are you sure you want to delete {customer_name}?\n\nThis will also delete all associated orders and addresses.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.model.delete_customer(customer_id)
                if success:
                    self.admin_home.tableWidget_2.removeRow(selected_row)
                    print(f"✓ Deleted customer: {customer_name}")
                    QMessageBox.information(self.admin_home, "Success", "Customer deleted successfully!")
                else:
                    QMessageBox.warning(self.admin_home, "Error", "Failed to delete customer.")
            except Exception as e:
                print(f"✗ Error deleting customer: {e}")
                QMessageBox.critical(self.admin_home, "Error", f"Error deleting customer: {e}")

    def sort_customer_by_name(self):
        """Sort customer table by Name"""
        if not hasattr(self.admin_home, "tableWidget_2"):
            return

        if self.sort_ascending_customer:
            self.admin_home.tableWidget_2.sortItems(0, Qt.SortOrder.AscendingOrder)
            if hasattr(self.admin_home, "name_srt_btn_2"):
                self.admin_home.name_srt_btn_2.setText("Name ▲")
        else:
            self.admin_home.tableWidget_2.sortItems(0, Qt.SortOrder.DescendingOrder)
            if hasattr(self.admin_home, "name_srt_btn_2"):
                self.admin_home.name_srt_btn_2.setText("Name ▼")

        self.sort_ascending_customer = not self.sort_ascending_customer

    # ==================== NAVIGATION METHODS ====================

    def go_to_home(self):
        print("Navigating to Home")
        self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.home_page_index)

    def go_to_dashboard(self):
        print("Navigating to Dashboard")
        self.dashboard.show()

    def go_to_users(self):
        print("Navigating to Users")
        self.load_customer_data()  # Force refresh
        self.manager.show()

    def go_to_orders(self):
        print("Navigating to Orders")
        self.order.show()

    def go_to_reports(self):
        print("Navigating to Reports")
        self.report.show()

    def go_to_logout(self):
        from PyQt6.QtWidgets import QMessageBox

        # ✅ CRITICAL FIX: Close all popups FIRST, before showing confirmation
        if self.customer_popup:
            try:
                self.customer_popup.hide()
                self.customer_popup.close()
                self.customer_popup.deleteLater()
                self.customer_popup = None
                print("✓ Closed customer popup before logout confirmation")
            except Exception as e:
                print(f"Warning: Error closing customer popup: {e}")

        # NOW show confirmation dialog (no popups blocking it)
        reply = QMessageBox.question(
            self.admin_home,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print("Logging out...")

            # Close admin home
            self.admin_home.close()

            # Clear login fields for security
            self.login_view.username.clear()
            self.login_view.password.clear()

            # Show login view
            self.login_view.show()
            self.login_view.username.setFocus()
        else:
            print("Logout cancelled")

    def go_to_ccv(self):
        """Navigate to Create Customer View"""
        self.cust.show()

    def center_popup(self, popup):
        """Center popup on main window"""
        main_geometry = self.admin_home.frameGeometry()
        main_center = main_geometry.center()
        popup_x = main_center.x() - popup.width() // 2
        popup_y = main_center.y() - popup.height() // 2
        popup.move(popup_x, popup_y)