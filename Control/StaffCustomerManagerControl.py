from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

from View.CustomerDetailsPopup import CustomerDetailsPopup


class SManagerCControl:
    """Controller for Staff Customer Manager page"""

    def __init__(self, staff_home, dashboard, customer, order, delivery, createorder, report, model, editcustomer, editcustomer_control, login_view):
        self.staff_home = staff_home
        self.dashboard = dashboard
        self.customer = customer
        self.order = order
        self.createorder = createorder
        self.report = report
        self.model = model
        self.delivery = delivery
        self.editcustomer = editcustomer  # Edit customer VIEW
        self.editcustomer_control = editcustomer_control  # Edit customer CONTROLLER
        self.login_view = login_view

        self.sort_ascending_customer = True

        # CRITICAL: Set bidirectional reference
        self.editcustomer_control.managerc_control = self

        # 🔧 ADD THIS: Connect to page change signal for auto-refresh
        if hasattr(self.staff_home, 'stackedWidget'):
            self.staff_home.stackedWidget.currentChanged.connect(self.on_page_changed)
            print("✅ SManagerCControl: Connected to stackedWidget page change signal")

            # 🔧 NEW: Also connect to the customer widget itself if it's a QWidget
        if hasattr(self.customer, 'parent') and hasattr(self.customer.parent(), 'currentChanged'):
            self.customer.parent().currentChanged.connect(self.on_page_changed)

        # Connect buttons from Customer Manager page
        self.connect_managerc_buttons()
        self.customer_popup = None
        self.staff_id = None

        # Load customer data when initialized
        self.load_customer_data()

    def on_page_changed(self, index):
        """Automatically refresh customer data when customer page becomes visible"""
        # 🔧 IMPROVED: Check multiple conditions
        try:
            # Method 1: Check if we have a customer_page_index attribute
            if hasattr(self.staff_home, 'customer_page_index'):
                if index == self.staff_home.customer_page_index:
                    print("✅ Customer page activated via index - refreshing data")
                    self.load_customer_data()
                    return

            # Method 2: Check the widget name
            if hasattr(self.staff_home, 'stackedWidget'):
                current_widget = self.staff_home.stackedWidget.currentWidget()
                if current_widget == self.customer:
                    print("✅ Customer page activated via widget - refreshing data")
                    self.load_customer_data()
                    return
        except Exception as e:
            print(f"⚠️ Error in on_page_changed: {e}")

    def connect_managerc_buttons(self):
        """Connect navigation buttons on the Staff Customer Manager page (CSE)"""

        # Sidebar buttons - CSE page uses _5 suffix
        if hasattr(self.staff_home, "Homebut_5"):
            self.staff_home.Homebut_5.clicked.connect(self.go_to_home)
        if hasattr(self.staff_home, "Dashbut_5"):
            self.staff_home.Dashbut_5.clicked.connect(self.go_to_dashboard)
        if hasattr(self.staff_home, "Userbut_5"):
            self.staff_home.Userbut_5.clicked.connect(self.go_to_customers)
        if hasattr(self.staff_home, "Orderbut_5"):
            self.staff_home.Orderbut_5.clicked.connect(self.go_to_orders)
        if hasattr(self.staff_home, "Reportbut_5"):
            self.staff_home.Reportbut_5.clicked.connect(self.go_to_reports)
        if hasattr(self.staff_home, "Delivlab_6"):
            self.staff_home.Delivlab_6.clicked.connect(self.go_to_delivery)
        if hasattr(self.staff_home, "Settbut_5"):
            self.staff_home.Settbut_5.clicked.connect(self.go_to_logout)

        # Icon buttons - CSE page uses _5 suffix
        if hasattr(self.staff_home, "h1_5"):
            self.staff_home.h1_5.clicked.connect(self.go_to_home)
        if hasattr(self.staff_home, "db1_5"):
            self.staff_home.db1_5.clicked.connect(self.go_to_dashboard)
        if hasattr(self.staff_home, "u1_5"):
            self.staff_home.u1_5.clicked.connect(self.go_to_customers)
        if hasattr(self.staff_home, "s1_5"):
            self.staff_home.s1_5.clicked.connect(self.go_to_logout)
        if hasattr(self.staff_home, "o1_5"):
            self.staff_home.o1_5.clicked.connect(self.go_to_orders)
        if hasattr(self.staff_home, "r1_5"):
            self.staff_home.r1_5.clicked.connect(self.go_to_reports)
        if hasattr(self.staff_home, "d1_5"):
            self.staff_home.d1_5.clicked.connect(self.go_to_delivery)

        # Customer action buttons
        if hasattr(self.staff_home, "nwbut_8"):
            self.staff_home.nwbut_8.clicked.connect(self.go_to_create_customer)
        if hasattr(self.staff_home, "nwbut_6"):
            self.staff_home.nwbut_6.clicked.connect(self.show_customer_details)
        if hasattr(self.staff_home, "nwbut_7"):
            self.staff_home.nwbut_7.clicked.connect(self.edit_customer)
        if hasattr(self.staff_home, "nwbut_5"):
            self.staff_home.nwbut_5.clicked.connect(self.delete_customer)
        if hasattr(self.staff_home, "nwbut_16"):
            self.staff_home.nwbut_16.clicked.connect(self.create_order_for_customer)

        # Connect search field
        if hasattr(self.staff_home, "line2"):
            self.staff_home.line2.textChanged.connect(self.search_customer)

        # Connect sort button
        if hasattr(self.staff_home, "name_srt_btn_2"):
            self.staff_home.name_srt_btn_2.clicked.connect(self.sort_customer_by_name)

        # Customer table double-click
        if hasattr(self.staff_home, "tableWidget_2"):
            self.staff_home.tableWidget_2.cellDoubleClicked.connect(self.on_customer_table_double_click)

    def load_customer_data(self):
        """Load all customer data into the table with correct structure and stretch first column"""
        if not hasattr(self.staff_home, "tableWidget_2"):
            print("Error: tableWidget_2 not found")
            return

        try:
            customer_list = self.model.get_all_customers()
            table = self.staff_home.tableWidget_2
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
                last_order_str = last_order.strftime('%Y-%m-%d') if last_order and hasattr(last_order, 'strftime') else ('No orders' if not last_order else str(last_order))
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

            print(f"✓ Staff: Loaded {len(customer_list)} customers")

        except Exception as e:
            print(f"✗ Staff: Error loading customer data: {e}")
            import traceback
            traceback.print_exc()

    def set_staff_id(self, staff_id):
        """Set the logged-in staff ID"""
        self.staff_id = staff_id
        print(f"✓ SManagerCControl: Staff ID set to {staff_id}")

    def search_customer(self):
        """Search customers and stretch first column during search"""
        if not hasattr(self.staff_home, "line2") or not hasattr(self.staff_home, "tableWidget_2"):
            return

        search_term = self.staff_home.line2.text().strip()
        table = self.staff_home.tableWidget_2
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
                last_order_str = last_order.strftime('%Y-%m-%d') if last_order and hasattr(last_order, 'strftime') else ('No orders' if not last_order else str(last_order))
                table.setItem(row_num, 2, QTableWidgetItem(last_order_str))
                customer_id_item = QTableWidgetItem()
                customer_id_item.setData(Qt.ItemDataRole.UserRole, customer['CustomerID'])
                table.setItem(row_num, 3, customer_id_item)

            print(f"✓ Staff: Found {len(customer_list)} customers matching '{search_term}'")

        except Exception as e:
            print(f"✗ Staff: Error searching customers: {e}")
            import traceback
            traceback.print_exc()

    def show_customer_details(self):
        """Show customer details popup"""
        if not hasattr(self.staff_home, "tableWidget_2"):
            return

        selected_items = self.staff_home.tableWidget_2.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.staff_home, "No Selection", "Please select a customer first.")
            return

        selected_row = selected_items[0].row()
        customer_id_item = self.staff_home.tableWidget_2.item(selected_row, 3)

        if not customer_id_item:
            return

        customer_id = customer_id_item.data(Qt.ItemDataRole.UserRole)

        # ✅ ALWAYS create a fresh popup instance
        self.customer_popup = CustomerDetailsPopup(parent=self.staff_home, model=self.model)

        # Load data directly from database using the customer ID
        success = self.customer_popup.loadCustomerFromDatabase(customer_id)

        if not success:
            QMessageBox.warning(self.staff_home, "Error", "Could not load customer details.")
            return

        self.center_popup(self.customer_popup)
        self.customer_popup.show()
        self.customer_popup.raise_()
        self.customer_popup.activateWindow()

    def on_customer_table_double_click(self, row, column):
        """Handle double-click on customer table"""
        self.show_customer_details()

    def edit_customer(self):
        """Edit selected customer"""
        if not hasattr(self.staff_home, "tableWidget_2"):
            print("Error: Table widget not found")
            return

        selected_items = self.staff_home.tableWidget_2.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self.staff_home,
                "No Selection",
                "Please select a customer to edit."
            )
            return

        try:
            selected_row = selected_items[0].row()
            customer_name = self.staff_home.tableWidget_2.item(selected_row, 0).text()

            # Get CustomerID from column 3 (hidden)
            customer_id_item = self.staff_home.tableWidget_2.item(selected_row, 3)
            if not customer_id_item:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "Could not retrieve customer ID from table."
                )
                return

            customer_id = customer_id_item.data(Qt.ItemDataRole.UserRole)

            print(f"✓ Staff: Editing customer: {customer_name} (ID: {customer_id})")

            # Load data FIRST, then show the page
            success = self.editcustomer_control.load_customer_data(customer_id)

            if success:
                # Show edit page using stackedWidget
                self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.EditCustomer_page_index)
            else:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "Failed to load customer data for editing."
                )

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.staff_home,
                "Error",
                f"An error occurred while preparing to edit:\n{str(e)}"
            )

    def delete_customer(self):
        """Delete customer"""
        if not hasattr(self.staff_home, "tableWidget_2"):
            return

        selected_items = self.staff_home.tableWidget_2.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.staff_home, "No Selection", "Please select a customer to delete.")
            return

        selected_row = selected_items[0].row()
        customer_name = self.staff_home.tableWidget_2.item(selected_row, 0).text()
        customer_id_item = self.staff_home.tableWidget_2.item(selected_row, 3)

        if not customer_id_item:
            return

        customer_id = customer_id_item.data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(
            self.staff_home,
            "Confirm Delete",
            f"Are you sure you want to delete {customer_name}?\n\nThis will also delete all associated orders and addresses.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.model.delete_customer(customer_id)
                if success:
                    self.staff_home.tableWidget_2.removeRow(selected_row)
                    print(f"✓ Staff: Deleted customer: {customer_name}")
                    QMessageBox.information(self.staff_home, "Success", "Customer deleted successfully!")
                else:
                    QMessageBox.warning(self.staff_home, "Error", "Failed to delete customer.")
            except Exception as e:
                print(f"✗ Staff: Error deleting customer: {e}")
                QMessageBox.critical(self.staff_home, "Error", f"Error deleting customer: {e}")

    def create_order_for_customer(self):
        """Navigate to Create Order page with selected customer pre-loaded"""
        if not hasattr(self.staff_home, "tableWidget_2"):
            print("Error: Table widget not found")
            return

        selected_items = self.staff_home.tableWidget_2.selectedItems()

        if not selected_items:
            QMessageBox.information(
                self.staff_home,
                "No Selection",
                "Please select a customer from the table first."
            )
            return

        try:
            selected_row = selected_items[0].row()
            customer_name = self.staff_home.tableWidget_2.item(selected_row, 0).text()

            # Get CustomerID from column 3 (hidden)
            customer_id_item = self.staff_home.tableWidget_2.item(selected_row, 3)
            if not customer_id_item:
                QMessageBox.warning(
                    self.staff_home,
                    "Error",
                    "Could not retrieve customer ID from table."
                )
                return

            customer_id = customer_id_item.data(Qt.ItemDataRole.UserRole)

            print(f"✓ Staff: Creating order for customer: {customer_name} (ID: {customer_id})")

            # Pass customer info to Create Order controller
            if hasattr(self, 'createorder_control'):
                self.createorder_control.set_selected_customer(customer_id, customer_name)
                print(f"✓ Staff: Customer set in CreateOrderControl")
            else:
                print("✗ ERROR: createorder_control attribute not found in SManagerCControl!")
                QMessageBox.critical(
                    self.staff_home,
                    "Configuration Error",
                    "Create Order controller not properly linked.\n\nPlease contact support."
                )
                return

            # Navigate to Create Order page
            self.createorder.show()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.staff_home,
                "Error",
                f"An error occurred:\n{str(e)}"
            )

    def sort_customer_by_name(self):
        """Sort customer table by Name"""
        if not hasattr(self.staff_home, "tableWidget_2"):
            return

        if self.sort_ascending_customer:
            self.staff_home.tableWidget_2.sortItems(0, Qt.SortOrder.AscendingOrder)
            if hasattr(self.staff_home, "name_srt_btn_2"):
                self.staff_home.name_srt_btn_2.setText("Ascending")
        else:
            self.staff_home.tableWidget_2.sortItems(0, Qt.SortOrder.DescendingOrder)
            if hasattr(self.staff_home, "name_srt_btn_2"):
                self.staff_home.name_srt_btn_2.setText("Descending")

        self.sort_ascending_customer = not self.sort_ascending_customer

    # ==================== NAVIGATION METHODS ====================

    def go_to_home(self):
        print("Staff: Navigating to Home")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.home_page_index)

    def go_to_dashboard(self):
        print("Staff: Navigating to Dashboard")
        self.dashboard.show()

    def go_to_customers(self):
        print("Staff: Navigating to Customers")
        self.load_customer_data()  # Force refresh
        self.customer.show()

    def go_to_orders(self):
        print("Staff: Navigating to Orders")
        self.order.show()

    def go_to_reports(self):
        print("Staff: Navigating to Reports")
        self.report.show()

    def go_to_delivery(self):
        print("Staff: Navigating to Delivery")
        self.delivery.show()

    def go_to_logout(self):

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
            self.staff_home,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print("Staff: Logging out...")

            # Close staff home
            self.staff_home.close()

            # Clear login fields for security
            self.login_view.username.clear()
            self.login_view.password.clear()

            # Show login view
            self.login_view.show()
            self.login_view.username.setFocus()
        else:
            print("Staff: Logout cancelled")

    def go_to_create_customer(self):
        """Navigate to Create Customer View"""
        print("Staff: Navigating to Create Customer")
        self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.CreateCustomer_page_index)

    def center_popup(self, popup):
        """Center popup on main window"""
        main_geometry = self.staff_home.frameGeometry()
        main_center = main_geometry.center()
        popup_x = main_center.x() - popup.width() // 2
        popup_y = main_center.y() - popup.height() // 2
        popup.move(popup_x, popup_y)