from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem


class AManagerControl:
    """Controller for User Manager page navigation"""

    def __init__(self, admin_home, dashboard, manager, managerc, cstaff, order, report, model, editstaff,
                 editstaff_control,login_view):
        self.admin_home = admin_home
        self.dashboard = dashboard
        self.manager = manager
        self.managerc = managerc
        self.cstaff = cstaff
        self.order = order
        self.report = report
        self.model = model
        self.editstaff = editstaff  # This is the VIEW (window)
        self.editstaff_control = editstaff_control  # This is the CONTROLLER
        self.login_view = login_view
        self.sort_ascending = True
        self.staff_popup = None

        self.selected_staff_id = None

        # CRITICAL: Set bidirectional reference
        self.editstaff_control.manager_control = self

        self.connect_manager_buttons()
        self.configure_table_settings()
        QTimer.singleShot(100, self.load_staff_data)

    def connect_manager_buttons(self):
        """Connect navigation buttons on the User Manager page"""

        if hasattr(self.admin_home, "gotc"):
            self.admin_home.gotc.clicked.connect(self.go_to_managerc)

        # Sidebar buttons
        if hasattr(self.admin_home, "Homebut_5"):
            self.admin_home.Homebut_5.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "Dashbut_5"):
            self.admin_home.Dashbut_5.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "Userbut_5"):
            self.admin_home.Userbut_5.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "Orderbut_5"):
            self.admin_home.Orderbut_5.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "Reportbut_5"):
            self.admin_home.Reportbut_5.clicked.connect(self.go_to_reports)

        if hasattr(self.admin_home, "Settbut_5"):
            self.admin_home.Settbut_5.clicked.connect(self.go_to_logout)

        # Icon buttons
        if hasattr(self.admin_home, "h2_3"):
            self.admin_home.h2_3.clicked.connect(self.go_to_home)

        if hasattr(self.admin_home, "db2_3"):
            self.admin_home.db2_3.clicked.connect(self.go_to_dashboard)

        if hasattr(self.admin_home, "u2_3"):
            self.admin_home.u2_3.clicked.connect(self.go_to_users)

        if hasattr(self.admin_home, "s2_3"):
            self.admin_home.s2_3.clicked.connect(self.go_to_logout)

        if hasattr(self.admin_home, "o2_3"):
            self.admin_home.o2_3.clicked.connect(self.go_to_orders)

        if hasattr(self.admin_home, "r2_3"):
            self.admin_home.r2_3.clicked.connect(self.go_to_reports)

        # Action buttons
        if hasattr(self.admin_home, "nwbut"):
            self.admin_home.nwbut.clicked.connect(self.go_to_createstaff)

        if hasattr(self.admin_home, "nwbut_2"):
            self.admin_home.nwbut_2.clicked.connect(self.show_staff_details)

        if hasattr(self.admin_home, "nwbut_3"):
            self.admin_home.nwbut_3.clicked.connect(self.edit_staff)

        if hasattr(self.admin_home, "nwbut_4"):
            self.admin_home.nwbut_4.clicked.connect(self.delete_staff)

        # Sort button
        if hasattr(self.admin_home, "name_srt_btn"):
            self.admin_home.name_srt_btn.clicked.connect(self.sort_by_name)

        # Search functionality
        if hasattr(self.admin_home, "line"):
            self.admin_home.line.textChanged.connect(self.search_staff)
            self.admin_home.line.returnPressed.connect(self.search_staff)

        # Table double-click
        if hasattr(self.admin_home, "tw"):
            self.admin_home.tw.cellDoubleClicked.connect(self.on_table_double_click)

            # Get headers
            h_header = self.admin_home.tw.horizontalHeader()
            v_header = self.admin_home.tw.verticalHeader()

            # Prevent column/row reordering
            h_header.setSectionsMovable(False)
            v_header.setSectionsMovable(False)
            h_header.setHighlightSections(False)
            v_header.setHighlightSections(False)

            # Disable drag and drop
            self.admin_home.tw.setDragEnabled(False)
            self.admin_home.tw.setDragDropMode(self.admin_home.tw.DragDropMode.NoDragDrop)
            self.admin_home.tw.setSelectionMode(self.admin_home.tw.SelectionMode.SingleSelection)


    def configure_table_settings(self):
        """Force configure table to be non-draggable"""
        if not hasattr(self.admin_home, "tw"):
            return

        table = self.admin_home.tw
        h_header = table.horizontalHeader()
        v_header = table.verticalHeader()

        h_header.setSectionsMovable(False)
        v_header.setSectionsMovable(False)
        h_header.setSectionsClickable(True)
        v_header.setSectionsClickable(True)
        h_header.setHighlightSections(False)
        v_header.setHighlightSections(False)

        table.setDragEnabled(False)
        table.setAcceptDrops(False)
        table.setDragDropMode(table.DragDropMode.NoDragDrop)
        table.setDragDropOverwriteMode(False)
        h_header.setSectionResizeMode(h_header.ResizeMode.Interactive)

        print("✓ Forced table drag protection")

    def load_staff_data(self):
        """Load all staff data into the table"""
        if not hasattr(self.admin_home, "tw"):
            print("Error: tw (table widget) not found")
            return

        table = self.admin_home.tw

        # CRITICAL: Block signals during table rebuild
        table.blockSignals(True)

        try:
            staff_list = self.model.get_all_staff()

            # Clear table completely
            table.clearContents()
            table.setRowCount(0)

            # Get header ONCE
            header = table.horizontalHeader()

            # Only set structure if needed
            if table.columnCount() != 5:
                table.setColumnCount(5)
                table.setHorizontalHeaderLabels([
                    "Name", "Email", "Date Applied", "Last Active", "StaffID"
                ])
                table.setColumnHidden(4, True)

                # Set resize modes - Interactive for all (user can resize manually)
                for col in range(4):
                    header.setSectionResizeMode(col, header.ResizeMode.Interactive)

            # Add staff data
            for row_num, staff in enumerate(staff_list):
                table.insertRow(row_num)

                full_name = f"{staff['EFName']} {staff['EMName'] or ''} {staff['ELName']}".strip()
                table.setItem(row_num, 0, QTableWidgetItem(full_name))
                table.setItem(row_num, 1, QTableWidgetItem(staff['EEmail'] or ''))

                date_applied = staff['SDateApplied'].strftime('%Y-%m-%d') if staff['SDateApplied'] else ''
                table.setItem(row_num, 2, QTableWidgetItem(date_applied))

                last_active = staff['LastActiveAt'].strftime('%Y-%m-%d %H:%M') if staff['LastActiveAt'] else 'Never'
                table.setItem(row_num, 3, QTableWidgetItem(last_active))

                staff_id_item = QTableWidgetItem()
                staff_id_item.setData(Qt.ItemDataRole.UserRole, staff['StaffID'])
                staff_id_item.setText(str(staff['StaffID']))
                table.setItem(row_num, 4, staff_id_item)

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.admin_home,
                "Error",
                f"Failed to load staff data: {str(e)}"
            )
        finally:
            # CRITICAL: Always unblock signals
            table.blockSignals(False)

    def search_staff(self):
        """Search staff and stretch first column only during search"""
        if not hasattr(self.admin_home, "line") or not hasattr(self.admin_home, "tw"):
            return

        search_term = self.admin_home.line.text().strip()
        table = self.admin_home.tw

        if not search_term:
            # Simply reload data
            self.load_staff_data()
            return

        # CRITICAL: Block signals during table rebuild
        table.blockSignals(True)

        try:
            staff_list = self.model.search_staff(search_term)

            # Clear table completely
            table.clearContents()
            table.setRowCount(0)

            # Get header ONCE
            header = table.horizontalHeader()

            # Only set structure if needed
            if table.columnCount() != 5:
                table.setColumnCount(5)
                table.setHorizontalHeaderLabels([
                    "Name", "Email", "Date Applied", "Last Active", "StaffID"
                ])
                table.setColumnHidden(4, True)

            # Set resize modes for search (stretch name column)
            header.setSectionResizeMode(0, header.ResizeMode.Stretch)
            header.setSectionResizeMode(1, header.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(2, header.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(3, header.ResizeMode.ResizeToContents)

            # Add search results
            for row_num, staff in enumerate(staff_list):
                table.insertRow(row_num)

                full_name = f"{staff['EFName']} {staff['EMName'] or ''} {staff['ELName']}".strip()
                table.setItem(row_num, 0, QTableWidgetItem(full_name))
                table.setItem(row_num, 1, QTableWidgetItem(staff['EEmail'] or ''))

                date_applied = staff['SDateApplied'].strftime('%Y-%m-%d') if staff['SDateApplied'] else ''
                table.setItem(row_num, 2, QTableWidgetItem(date_applied))

                last_active = staff['LastActiveAt'].strftime('%Y-%m-%d %H:%M') if staff['LastActiveAt'] else 'Never'
                table.setItem(row_num, 3, QTableWidgetItem(last_active))

                staff_id_item = QTableWidgetItem()
                staff_id_item.setData(Qt.ItemDataRole.UserRole, staff['StaffID'])
                staff_id_item.setText(str(staff['StaffID']))
                table.setItem(row_num, 4, staff_id_item)

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.admin_home,
                "Error",
                f"Failed to search staff: {str(e)}"
            )
        finally:
            # CRITICAL: Always unblock signals
            table.blockSignals(False)

    def show_staff_details(self):
        """Show staff details popup when View button is clicked"""
        if not hasattr(self.admin_home, "tw"):
            return

        selected_items = self.admin_home.tw.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self.admin_home,
                "No Selection",
                "Please select a staff member first."
            )
            return

        selected_row = selected_items[0].row()
        staff_id_item = self.admin_home.tw.item(selected_row, 4)  # Column 4 has StaffID

        if not staff_id_item:
            QMessageBox.warning(
                self.admin_home,
                "Error",
                "Could not retrieve staff ID."
            )
            return

        staff_id = staff_id_item.data(Qt.ItemDataRole.UserRole)

        # Create popup with model if it doesn't exist
        if self.staff_popup is None:
            # Import the new StaffDetailsPopup instead of DraggablePopup
            from View.StaffDetailsPopup import StaffDetailsPopup
            self.staff_popup = StaffDetailsPopup(parent=self.admin_home, model=self.model)

        # Load data directly from database using the staff ID
        success = self.staff_popup.loadStaffFromDatabase(staff_id)

        if not success:
            QMessageBox.warning(self.admin_home, "Error", "Could not load staff details.")
            return

        self.center_popup(self.staff_popup)
        self.staff_popup.show()
        self.staff_popup.raise_()
        self.staff_popup.activateWindow()



    def on_table_double_click(self, row, column):
        """Handle double-click on staff table row"""
        self.show_staff_details()

    def center_popup(self, popup):
        """Center the popup on the main window"""
        main_geometry = self.admin_home.frameGeometry()
        main_center = main_geometry.center()
        popup_x = main_center.x() - popup.width() // 2
        popup_y = main_center.y() - popup.height() // 2
        popup.move(popup_x, popup_y)

    def edit_staff(self):
        """Edit selected staff member - FIXED VERSION"""
        if not hasattr(self.admin_home, "tw"):
            print("Error: Table widget not found")
            return

        selected_items = self.admin_home.tw.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self.admin_home,
                "No Selection",
                "Please select a staff member to edit."
            )
            return

        try:
            selected_row = selected_items[0].row()
            staff_name = self.admin_home.tw.item(selected_row, 0).text()

            # Get StaffID from column 4
            staff_id_item = self.admin_home.tw.item(selected_row, 4)
            if not staff_id_item:
                QMessageBox.warning(
                    self.admin_home,
                    "Error",
                    "Could not retrieve staff ID from table."
                )
                return

            staff_id = staff_id_item.data(Qt.ItemDataRole.UserRole)


            # STORE the selected staff_id
            self.selected_staff_id = staff_id

            # Get full staff information including EmployeeID
            staff_info = self.model.get_staff_by_id(staff_id)

            if not staff_info:
                QMessageBox.warning(
                    self.admin_home,
                    "Error",
                    "Could not load staff information from database."
                )
                return

            employee_id = staff_info.get('EmployeeID')

            if not employee_id:
                QMessageBox.warning(
                    self.admin_home,
                    "Error",
                    "Staff member has no associated Employee ID."
                )
                return



            # CRITICAL FIX: Load data FIRST, then show the page
            success = self.editstaff_control.load_employee_data(employee_id, staff_id)

            if success:


                # Show edit page using stackedWidget instead of separate window
                self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.EditStaff_page_index)


            else:
                QMessageBox.warning(
                    self.admin_home,
                    "Error",
                    "Failed to load employee data for editing."
                )

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.admin_home,
                "Error",
                f"An error occurred while preparing to edit:\n{str(e)}"
            )
    def delete_staff(self):
        """Delete selected staff member"""
        if not hasattr(self.admin_home, "tw"):
            return

        selected_items = self.admin_home.tw.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self.admin_home,
                "No Selection",
                "Please select a staff member to delete."
            )
            return

        selected_row = selected_items[0].row()
        staff_name = self.admin_home.tw.item(selected_row, 0).text()

        staff_id_item = self.admin_home.tw.item(selected_row, 4)
        staff_id = staff_id_item.data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(
            self.admin_home,
            "Confirm Delete",
            f"Are you sure you want to delete {staff_name}?\n\nThis will also delete their login credentials.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.model.delete_staff(staff_id):
                    self.admin_home.tw.removeRow(selected_row)
                    QMessageBox.information(
                        self.admin_home,
                        "Success",
                        f"{staff_name} has been deleted successfully."
                    )
                else:
                    QMessageBox.critical(
                        self.admin_home,
                        "Error",
                        f"Failed to delete {staff_name}."
                    )
            except Exception as e:

                import traceback
                traceback.print_exc()
                QMessageBox.critical(
                    self.admin_home,
                    "Error",
                    f"An error occurred while deleting {staff_name}:\n{str(e)}"
                )

    def sort_by_name(self):
        """Sort table by Name column"""
        if not hasattr(self.admin_home, "tw"):
            return

        if self.sort_ascending:
            self.admin_home.tw.sortItems(0, Qt.SortOrder.AscendingOrder)
            if hasattr(self.admin_home, "name_srt_btn"):
                self.admin_home.name_srt_btn.setText("Name ▲")
        else:
            self.admin_home.tw.sortItems(0, Qt.SortOrder.DescendingOrder)
            if hasattr(self.admin_home, "name_srt_btn"):
                self.admin_home.name_srt_btn.setText("Name ▼")

        self.sort_ascending = not self.sort_ascending

    def go_to_home(self):
        print("Navigating to Home")
        self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.home_page_index)

    def go_to_dashboard(self):
        print("Navigating to Dashboard")
        self.dashboard.show()

    def go_to_users(self):
        print("Navigating to Users")
        self.manager.show()
        self.load_staff_data()

    def go_to_orders(self):
        print("Navigating to Orders")
        self.order.show()

    def go_to_reports(self):
        print("Navigating to Reports")
        self.report.show()

    def go_to_logout(self):
        from PyQt6.QtWidgets import QMessageBox

        # ✅ CRITICAL FIX: Close all popups FIRST, before showing confirmation
        if self.staff_popup:
            try:
                self.staff_popup.hide()
                self.staff_popup.close()
                self.staff_popup.deleteLater()
                self.staff_popup = None
                print("✓ Closed staff popup before logout confirmation")
            except Exception as e:
                print(f"Warning: Error closing staff popup: {e}")

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

    def go_to_managerc(self):
        self.managerc.show()

    def go_to_createstaff(self):
        self.cstaff.show()