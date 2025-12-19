from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QInputDialog
from datetime import datetime
import os

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QInputDialog
from datetime import datetime
import os


class AReportControl:
    """Controller for Admin Report/History page"""

    def __init__(self, admin_home, dashboard, user, order, report, model, login_view):
        self.admin_home = admin_home
        self.dashboard = dashboard
        self.manager = user
        self.order = order
        self.report = report
        self.model = model
        self.login_view = login_view

        self.sort_ascending_history = True
        self.current_filter = "Completed"
        self.refresh_timer = None
        self.is_destroyed = False
        self.last_order_count = 0
        self.last_customer_count = 0
        self.connections_made = False

        # ✅ ADD THIS LINE - Store popup as instance variable
        self.order_popup = None  # <-- THIS WAS MISSING!

        # Connect to page change signal for auto-refresh
        if hasattr(self.admin_home, 'stackedWidget'):
            self.admin_home.stackedWidget.currentChanged.connect(self.on_page_changed)

        # Initial connection setup
        self.connect_report_buttons()

        # Load completed orders initially
        QTimer.singleShot(100, self.safe_load_history_data)

    def safe_load_history_data(self):
        """Safely load history data with error handling"""
        if not self.is_destroyed:
            try:
                self.load_history_data()
            except Exception as e:
                print(f"✗ Safe load failed: {e}")

    def setup_refresh_timer(self):
        """Setup timer to periodically check for changes"""
        if self.refresh_timer:
            self.refresh_timer.stop()
            self.refresh_timer.deleteLater()

        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.safe_check_for_updates)
        self.refresh_timer.start(10000)

        try:
            self.last_order_count = len(self.model.get_all_orders())
            self.last_customer_count = len(self.model.get_all_customers())
        except:
            pass

    def safe_check_for_updates(self):
        """Safe wrapper for check_for_updates"""
        if not self.is_destroyed:
            try:
                self.check_for_updates()
            except Exception as e:
                print(f"✗ Safe check failed: {e}")

    def check_for_updates(self):
        """Check if data has changed and refresh if needed"""
        try:
            if self.is_destroyed:
                return

            current_order_count = len(self.model.get_all_orders())
            current_customer_count = len(self.model.get_all_customers())

            if hasattr(self.admin_home, 'report_page_index'):
                if self.admin_home.stackedWidget.currentIndex() == self.admin_home.report_page_index:
                    if (current_order_count != self.last_order_count or
                            current_customer_count != self.last_customer_count):
                        print("✓ Reports: Data changed - refreshing")
                        self.load_history_data()
                        self.last_order_count = current_order_count
                        self.last_customer_count = current_customer_count
        except Exception as e:
            print(f"✗ Reports: Error checking updates: {e}")

    def on_page_changed(self, index):
        """Automatically refresh report data when report page becomes visible"""
        if self.is_destroyed:
            return

        if hasattr(self.admin_home, 'report_page_index'):
            if index == self.admin_home.report_page_index:
                print("✓ Reports: Page activated - refreshing data")
                # Reconnect buttons to ensure they work after navigation
                self.ensure_connections()
                self.setup_refresh_timer()
                self.load_history_data()
            else:
                if self.refresh_timer:
                    self.refresh_timer.stop()

    def ensure_connections(self):
        """Ensure all button connections are active"""
        if not self.connections_made or self.is_destroyed:
            print("✓ Reports: Re-establishing button connections")
            self.connect_report_buttons()
            self.connections_made = True

    def disconnect_all(self):
        """Safely disconnect all signals before reconnecting"""
        try:
            # Disconnect sidebar buttons
            buttons = [
                'Homebut_9', 'Dashbut_9', 'Userbut_9', 'Orderbut_9',
                'Reportbut_9', 'Settbut_9', 'h1_8', 'db1_8', 's1_8',
                'o1_8', 'r1_8', 'u1_8', 'd1_8', 'nwbut_14', 'nwbut_13',
                'nwbut_11', 'nwbut_12', 'name_srt_btn_4'
            ]

            for button_name in buttons:
                if hasattr(self.admin_home, button_name):
                    button = getattr(self.admin_home, button_name)
                    try:
                        button.clicked.disconnect()
                    except TypeError:
                        pass  # No connections to disconnect

            # Disconnect search field
            if hasattr(self.admin_home, "line4"):
                try:
                    self.admin_home.line4.textChanged.disconnect()
                except TypeError:
                    pass

            # Disconnect table double-click
            if hasattr(self.admin_home, "tableWidget_4"):
                try:
                    self.admin_home.tableWidget_4.cellDoubleClicked.disconnect()
                except TypeError:
                    pass

        except Exception as e:
            print(f"Note: Error during disconnect (normal on first run): {e}")

    def connect_report_buttons(self):
        """Connect navigation and action buttons on the Report/History page"""

        # Safely disconnect existing connections first
        self.disconnect_all()

        # Sidebar buttons
        if hasattr(self.admin_home, "Homebut_9"):
            self.admin_home.Homebut_9.clicked.connect(self.go_to_home)
        if hasattr(self.admin_home, "Dashbut_9"):
            self.admin_home.Dashbut_9.clicked.connect(self.go_to_dashboard)
        if hasattr(self.admin_home, "Userbut_9"):
            self.admin_home.Userbut_9.clicked.connect(self.go_to_users)
        if hasattr(self.admin_home, "Orderbut_9"):
            self.admin_home.Orderbut_9.clicked.connect(self.go_to_orders)
        if hasattr(self.admin_home, "Reportbut_9"):
            self.admin_home.Reportbut_9.clicked.connect(self.go_to_reports)
        if hasattr(self.admin_home, "Settbut_9"):
            self.admin_home.Settbut_9.clicked.connect(self.go_to_logout)

        # Icon buttons
        if hasattr(self.admin_home, "h1_8"):
            self.admin_home.h1_8.clicked.connect(self.go_to_home)
        if hasattr(self.admin_home, "db1_8"):
            self.admin_home.db1_8.clicked.connect(self.go_to_dashboard)
        if hasattr(self.admin_home, "s1_8"):
            self.admin_home.s1_8.clicked.connect(self.go_to_logout)
        if hasattr(self.admin_home, "o1_8"):
            self.admin_home.o1_8.clicked.connect(self.go_to_orders)
        if hasattr(self.admin_home, "r1_8"):
            self.admin_home.r1_8.clicked.connect(self.go_to_reports)
        if hasattr(self.admin_home, "u1_8"):
            self.admin_home.u1_8.clicked.connect(self.go_to_users)
        if hasattr(self.admin_home, "d1_8"):
            self.admin_home.d1_8.clicked.connect(self.go_to_users)

        # Action buttons
        if hasattr(self.admin_home, "nwbut_14"):
            self.admin_home.nwbut_14.clicked.connect(self.generate_report)
        if hasattr(self.admin_home, "nwbut_13"):
            self.admin_home.nwbut_13.clicked.connect(self.view_order_details)
        if hasattr(self.admin_home, "nwbut_11"):
            self.admin_home.nwbut_11.clicked.connect(self.edit_order)
        if hasattr(self.admin_home, "nwbut_12"):
            self.admin_home.nwbut_12.clicked.connect(self.delete_order)

        # Connect search field
        if hasattr(self.admin_home, "line4"):
            self.admin_home.line4.textChanged.connect(self.search_history)

        # Connect filter/sort button
        if hasattr(self.admin_home, "name_srt_btn_4"):
            self.admin_home.name_srt_btn_4.setText(self.current_filter)
            self.admin_home.name_srt_btn_4.clicked.connect(self.toggle_filter)

        # Connect table double-click
        if hasattr(self.admin_home, "tableWidget_4"):
            self.admin_home.tableWidget_4.cellDoubleClicked.connect(
                self.on_history_table_double_click
            )

        print("✓ Reports: All button connections established")

    def load_history_data(self, filter_status=None):
        """Load order history data into the table"""
        if self.is_destroyed:
            return

        if not hasattr(self.admin_home, "tableWidget_4"):
            print("Error: tableWidget_4 not found")
            return

        table = self.admin_home.tableWidget_4
        table.blockSignals(True)

        try:
            if filter_status is None:
                filter_status = self.current_filter

            # Get orders based on filter
            if filter_status == "All":
                order_list = self.model.get_all_orders()
            elif filter_status == "Completed":
                order_list = self.model.get_orders_by_status("Completed")
            else:
                order_list = self.model.get_orders_by_status(filter_status)

            table.clearContents()
            table.setRowCount(0)

            header = table.horizontalHeader()

            if table.columnCount() != 6:
                table.setColumnCount(6)
                table.setHorizontalHeaderLabels(
                    ["Order ID", "Order ID", "Status", "Date", "Total Amount", "OrderID_Hidden"]
                )
                table.setColumnHidden(0, True)
                table.setColumnHidden(5, True)

                header.setSectionResizeMode(1, header.ResizeMode.Stretch)
                header.setSectionResizeMode(2, header.ResizeMode.ResizeToContents)
                header.setSectionResizeMode(3, header.ResizeMode.ResizeToContents)
                header.setSectionResizeMode(4, header.ResizeMode.ResizeToContents)

            completed_count = 0
            for row_num, order in enumerate(order_list):
                status = order.get('Status', 'Unknown')

                if filter_status == "Completed" and status != "Completed":
                    continue

                if status == "Completed":
                    completed_count += 1

                table.insertRow(row_num)

                # Raw Order ID (hidden)
                table.setItem(row_num, 0, QTableWidgetItem(str(order['OrderID'])))

                # Formatted Order ID (visible)
                formatted_id = f"WSHY#{order['OrderID']:03d}"
                table.setItem(row_num, 1, QTableWidgetItem(formatted_id))

                # Status with color
                status_item = QTableWidgetItem(status)
                if status == 'Completed':
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                elif status == 'Pending':
                    status_item.setForeground(Qt.GlobalColor.darkYellow)
                elif status == 'Processing':
                    status_item.setForeground(Qt.GlobalColor.darkBlue)
                elif status == 'Cancelled':
                    status_item.setForeground(Qt.GlobalColor.darkRed)
                table.setItem(row_num, 2, status_item)

                # Order Date
                order_date = order.get('OrderDate')
                order_date_str = order_date.strftime('%Y-%m-%d %H:%M') if order_date and hasattr(
                    order_date, 'strftime'
                ) else ('N/A' if not order_date else str(order_date))
                table.setItem(row_num, 3, QTableWidgetItem(order_date_str))

                # Total Amount
                table.setItem(row_num, 4, QTableWidgetItem(f"₱{order.get('TotalAmount', 0):.2f}"))

                # Hidden OrderID for data retrieval
                order_id_item = QTableWidgetItem()
                order_id_item.setData(Qt.ItemDataRole.UserRole, order['OrderID'])
                table.setItem(row_num, 5, order_id_item)

            print(f"✓ Reports: Loaded {completed_count} completed orders (filter: {filter_status})")

        except Exception as e:
            print(f"✗ Reports: Error loading history data: {e}")
            import traceback
            traceback.print_exc()
            if not self.is_destroyed:
                QMessageBox.critical(
                    self.admin_home,
                    "Error",
                    f"Failed to load history data: {str(e)}"
                )
        finally:
            try:
                table.blockSignals(False)
            except:
                pass

    def search_history(self):
        """Search order history with current filter applied"""
        if self.is_destroyed:
            return

        if not hasattr(self.admin_home, "tableWidget_4"):
            return

        if not hasattr(self.admin_home, "line4"):
            return

        search_term = self.admin_home.line4.text().strip()
        table = self.admin_home.tableWidget_4

        if not search_term:
            self.load_history_data()
            return

        table.blockSignals(True)

        try:
            # Get filtered orders first
            if self.current_filter == "All":
                filtered_orders = self.model.get_all_orders()
            elif self.current_filter == "Completed":
                filtered_orders = self.model.get_orders_by_status("Completed")
            else:
                filtered_orders = self.model.get_orders_by_status(self.current_filter)

            # Search within filtered results
            search_results = []
            for order in filtered_orders:
                search_lower = search_term.lower()

                formatted_id = f"WSHY#{order['OrderID']:03d}".lower()
                if search_lower in formatted_id:
                    search_results.append(order)
                    continue

                customer_name = order.get('customer_name', '').lower()
                if search_lower in customer_name:
                    search_results.append(order)
                    continue

                status = order.get('Status', '').lower()
                if search_lower in status:
                    search_results.append(order)
                    continue

                order_date = order.get('OrderDate')
                if order_date:
                    date_str = order_date.strftime('%Y-%m-%d').lower()
                    if search_lower in date_str:
                        search_results.append(order)
                        continue

            table.clearContents()
            table.setRowCount(0)

            header = table.horizontalHeader()

            if table.columnCount() != 6:
                table.setColumnCount(6)
                table.setHorizontalHeaderLabels(
                    ["Order ID", "Formatted ID", "Status", "Date", "Total Amount", "OrderID_Hidden"]
                )
                table.setColumnHidden(0, True)
                table.setColumnHidden(5, True)

                header.setSectionResizeMode(1, header.ResizeMode.Stretch)
                header.setSectionResizeMode(2, header.ResizeMode.ResizeToContents)
                header.setSectionResizeMode(3, header.ResizeMode.ResizeToContents)
                header.setSectionResizeMode(4, header.ResizeMode.ResizeToContents)

            # Add search results
            for row_num, order in enumerate(search_results):
                table.insertRow(row_num)

                # Raw Order ID (hidden)
                table.setItem(row_num, 0, QTableWidgetItem(str(order['OrderID'])))

                # Formatted Order ID (visible)
                formatted_id = f"WSHY#{order['OrderID']:03d}"
                table.setItem(row_num, 1, QTableWidgetItem(formatted_id))

                # Status with color
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

                # Order Date
                order_date = order.get('OrderDate')
                order_date_str = order_date.strftime('%Y-%m-%d %H:%M') if order_date and hasattr(
                    order_date, 'strftime'
                ) else ('N/A' if not order_date else str(order_date))
                table.setItem(row_num, 3, QTableWidgetItem(order_date_str))

                # Total Amount
                table.setItem(row_num, 4, QTableWidgetItem(f"₱{order.get('TotalAmount', 0):.2f}"))

                # Hidden OrderID
                order_id_item = QTableWidgetItem()
                order_id_item.setData(Qt.ItemDataRole.UserRole, order['OrderID'])
                table.setItem(row_num, 5, order_id_item)

            print(f"✓ Reports: Found {len(search_results)} orders matching '{search_term}'")

        except Exception as e:
            print(f"✗ Reports: Error searching history: {e}")
            import traceback
            traceback.print_exc()
            if not self.is_destroyed:
                QMessageBox.critical(
                    self.admin_home,
                    "Error",
                    f"Failed to search history: {str(e)}"
                )
        finally:
            try:
                table.blockSignals(False)
            except:
                pass

    def toggle_filter(self):
        """Toggle between different status filters"""
        if self.is_destroyed:
            return

        filters = ["Completed", "All", "Pending", "Processing", "Cancelled"]

        try:
            current_index = filters.index(self.current_filter)
        except ValueError:
            current_index = 0
            self.current_filter = filters[0]

        next_index = (current_index + 1) % len(filters)
        self.current_filter = filters[next_index]

        if hasattr(self.admin_home, "name_srt_btn_4"):
            self.admin_home.name_srt_btn_4.setText(self.current_filter)

        self.load_history_data()

    def cleanup(self):
        """Clean up resources before destruction"""
        self.is_destroyed = True

        if self.refresh_timer:
            self.refresh_timer.stop()
            self.refresh_timer.deleteLater()
            self.refresh_timer = None

        if hasattr(self.admin_home, 'stackedWidget'):
            try:
                self.admin_home.stackedWidget.currentChanged.disconnect(self.on_page_changed)
            except:
                pass

        # Disconnect all button connections
        self.disconnect_all()

    # ============================================================================
    # FIXED AdminReportsControl.py - TWO CRITICAL CHANGES
    # ============================================================================

    # CHANGE 1: Add popup instance variable in __init__
    # ----------------------------------------------------------------------------
    def __init__(self, admin_home, dashboard, user, order, report, model, login_view):
        self.admin_home = admin_home
        self.dashboard = dashboard
        self.manager = user
        self.order = order
        self.report = report
        self.model = model
        self.login_view = login_view

        self.sort_ascending_history = True
        self.current_filter = "Completed"
        self.refresh_timer = None
        self.is_destroyed = False
        self.last_order_count = 0
        self.last_customer_count = 0
        self.connections_made = False

        # ✅ ADD THIS LINE - Store popup as instance variable
        self.order_popup = None  # <-- THIS WAS MISSING!

        # Connect to page change signal for auto-refresh
        if hasattr(self.admin_home, 'stackedWidget'):
            self.admin_home.stackedWidget.currentChanged.connect(self.on_page_changed)

        # Initial connection setup
        self.connect_report_buttons()

        # Load completed orders initially
        QTimer.singleShot(100, self.safe_load_history_data)

    # CHANGE 2: Store popup in view_order_details() and use it in go_to_logout()
    # ----------------------------------------------------------------------------
    def view_order_details(self):
        """View order details using OrderDetailsPopup"""
        if self.is_destroyed:
            return

        if not hasattr(self.admin_home, "tableWidget_4"):
            QMessageBox.warning(self.admin_home, "Error", "History table not found.")
            return

        selected_items = self.admin_home.tableWidget_4.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.admin_home, "No Selection", "Please select an order first.")
            return

        selected_row = selected_items[0].row()
        order_id_item = self.admin_home.tableWidget_4.item(selected_row, 5)

        if not order_id_item:
            QMessageBox.warning(self.admin_home, "Error", "Could not get order ID.")
            return

        order_id = order_id_item.data(Qt.ItemDataRole.UserRole)

        try:
            from View.OrderPopup import OrderDetailsPopup

            # ✅ ALWAYS create fresh popup - REMOVE the "if None" check
            self.order_popup = OrderDetailsPopup(self.admin_home, self.model)

            success = self.order_popup.loadOrderFromDatabase(order_id)

            if success:
                main_geo = self.admin_home.geometry()
                popup_width = self.order_popup.width()
                popup_height = self.order_popup.height()

                center_x = main_geo.x() + (main_geo.width() - popup_width) // 2
                center_y = main_geo.y() + (main_geo.height() - popup_height) // 2

                self.order_popup.move(center_x, center_y)
                self.order_popup.show()
                self.order_popup.raise_()
                self.order_popup.activateWindow()
                print(f"✅ Reports: Showing order details for OrderID: {order_id}")
            else:
                QMessageBox.warning(self.admin_home, "Error", "Could not load order details.")

        except ImportError as e:
            print(f"❌ Reports: Error importing OrderDetailsPopup: {e}")
            QMessageBox.warning(self.admin_home, "Error", f"Order details popup not available: {e}")
        except Exception as e:
            print(f"❌ Reports: Error showing order details: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self.admin_home, "Error", f"Error showing order details: {e}")

    def on_history_table_double_click(self, row, column):
        """Handle double-click on history table"""
        if not self.is_destroyed:
            self.view_order_details()

    def edit_order(self):
        """Edit order"""
        if self.is_destroyed:
            return

        if not hasattr(self.admin_home, "tableWidget_4"):
            return

        selected_items = self.admin_home.tableWidget_4.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.admin_home, "No Selection", "Please select an order to edit.")
            return

        print("Reports: Edit order - TODO: Implement order edit")

    def delete_order(self):
        """Delete order from history"""
        if self.is_destroyed:
            return

        if not hasattr(self.admin_home, "tableWidget_4"):
            QMessageBox.warning(self.admin_home, "Error", "History table not found.")
            return

        selected_items = self.admin_home.tableWidget_4.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.admin_home, "No Selection", "Please select an order to delete.")
            return

        selected_row = selected_items[0].row()
        order_id_display = self.admin_home.tableWidget_4.item(selected_row, 1).text()
        order_id_item = self.admin_home.tableWidget_4.item(selected_row, 5)

        if not order_id_item:
            QMessageBox.warning(self.admin_home, "Error", "Could not get order ID.")
            return

        order_id = order_id_item.data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(
            self.admin_home,
            "Confirm Delete",
            f"Are you sure you want to delete Order {order_id_display}?\n\nThis will permanently remove all order data.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.model.delete_order(order_id)
                if success:
                    self.admin_home.tableWidget_4.removeRow(selected_row)
                    print(f"✓ Reports: Deleted order: {order_id_display}")

                    self.last_order_count -= 1

                    QMessageBox.information(self.admin_home, "Success", "Order deleted successfully!")
                else:
                    QMessageBox.warning(self.admin_home, "Error", "Failed to delete order.")
            except Exception as e:
                print(f"✗ Reports: Error deleting order: {e}")
                QMessageBox.critical(self.admin_home, "Error", f"Error deleting order: {e}")

    def generate_report(self):
        """Generate annual PDF report with year selection"""
        if self.is_destroyed:
            return

        try:
            # Ask user for the year
            current_year = datetime.now().year
            year, ok = QInputDialog.getInt(
                self.admin_home,
                "Generate Annual Report",
                "Enter the year for the report:",
                current_year,
                2020,
                2050,
                1
            )

            if not ok:
                print("Reports: Annual report generation cancelled")
                return

            # Import the report generator
            try:
                from Model.Anual_Report import WashyAnnualReportGenerator
            except ImportError:
                QMessageBox.critical(
                    self.admin_home,
                    "Error",
                    "Annual report generator not found. Please ensure Anual_Report.py is available."
                )
                return

            # Get database configuration from model
            db_config = {
                'host': self.model.host if hasattr(self.model, 'host') else 'localhost',
                'user': self.model.user if hasattr(self.model, 'user') else 'root',
                'password': self.model.password if hasattr(self.model, 'password') else '',
                'database': self.model.database if hasattr(self.model, 'database') else 'washy'
            }

            # Create report generator
            report_gen = WashyAnnualReportGenerator(db_config)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Washy_Annual_Report_{year}_{timestamp}.pdf"

            # Create reports directory if it doesn't exist
            reports_dir = "reports"
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)

            filepath = os.path.join(reports_dir, filename)

            # Show progress message
            QMessageBox.information(
                self.admin_home,
                "Generating Report",
                f"Generating annual report for {year}...\nThis may take a moment."
            )

            # Generate the report
            success = report_gen.generate_annual_report(year, filepath)

            if success:
                reply = QMessageBox.question(
                    self.admin_home,
                    "Report Generated",
                    f"Annual report for {year} has been generated successfully!\n\n"
                    f"File: {filepath}\n\n"
                    f"Would you like to open the report?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    # Open the PDF file with default system viewer
                    import subprocess
                    import platform

                    try:
                        if platform.system() == 'Windows':
                            os.startfile(filepath)
                        elif platform.system() == 'Darwin':  # macOS
                            subprocess.call(['open', filepath])
                        else:  # Linux
                            subprocess.call(['xdg-open', filepath])

                        print(f"✓ Reports: Opened annual report: {filepath}")
                    except Exception as e:
                        print(f"✗ Reports: Could not open PDF: {e}")
                        QMessageBox.information(
                            self.admin_home,
                            "Report Saved",
                            f"Report saved to: {filepath}\n\nPlease open it manually."
                        )
                else:
                    print(f"✓ Reports: Annual report saved: {filepath}")
            else:
                QMessageBox.critical(
                    self.admin_home,
                    "Error",
                    f"Failed to generate annual report for {year}.\nPlease check the console for details."
                )

        except Exception as e:
            print(f"✗ Reports: Error generating annual report: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.admin_home,
                "Error",
                f"Error generating annual report: {str(e)}"
            )

    # ==================== NAVIGATION METHODS ====================

    def go_to_home(self):
        if self.is_destroyed:
            return
        print("Reports: Navigating to Home")
        try:
            self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.home_page_index)
        except Exception as e:
            print(f"✗ Error navigating to home: {e}")

    def go_to_dashboard(self):
        if self.is_destroyed:
            return
        print("Reports: Navigating to Dashboard")
        try:
            self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.dashboard_page_index)
        except Exception as e:
            print(f"✗ Error navigating to dashboard: {e}")

    def go_to_users(self):
        if self.is_destroyed:
            return
        print("Reports: Navigating to Users")
        try:
            self.manager.show()
        except Exception as e:
            print(f"✗ Error navigating to users: {e}")

    def go_to_orders(self):
        if self.is_destroyed:
            return
        print("Reports: Navigating to Orders")
        try:
            self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.order_page_index)
        except Exception as e:
            print(f"✗ Error navigating to orders: {e}")

    def go_to_reports(self):
        if self.is_destroyed:
            return
        print("Reports: Navigating to Reports")
        try:
            self.load_history_data()
            self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.report_page_index)
        except Exception as e:
            print(f"✗ Error navigating to reports: {e}")

    def go_to_logout(self):
        if self.is_destroyed:
            return

        # ✅ CRITICAL FIX: Close popup BEFORE showing confirmation
        # Changed from self.popup to self.order_popup
        if self.order_popup:  # <-- FIXED: Was checking self.popup (doesn't exist!)
            try:
                self.order_popup.hide()
                self.order_popup.close()
                self.order_popup.deleteLater()
                self.order_popup = None
                print("✓ Reports: Closed order popup before logout confirmation")
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
            print("Reports: Logging out...")

            # Call cleanup() first
            try:
                self.cleanup()
            except Exception as e:
                print(f"Warning: Error during cleanup: {e}")

            self.admin_home.close()
            self.login_view.username.clear()
            self.login_view.password.clear()
            self.login_view.show()
            self.login_view.username.setFocus()
        else:
            print("Reports: Logout cancelled")
