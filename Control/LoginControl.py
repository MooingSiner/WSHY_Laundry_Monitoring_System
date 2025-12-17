from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

from Control.AdminDashboardControl import ADashBControl
from View.AdminDashboardView import ADashboard
from Control.AdminHomeControl import AHControl
from View.AdminUserManagerView import AManager
from View.AdminCostumerManagerView import AManagerC
from Control.AdminUserManagerControl import AManagerControl
from Control.AdminCostumerManagerControl import AManagerControlC
from Control.AdminOrderManagementControl import AOrderControl
from View.AdminOrderManagementView import AOrders
from Control.AdminReportsControl import AReportControl
from View.AdminReportsView import AReport
from Control.AdminCreateCustomerControl import CreateCustomerControl
from View.AdminCreateCustomerView import CreateCustomer
from View.AdminCreateStaffView import CreateStaff
from Control.AdminCreateStaffControl import Createstaffcontrol
from View.AdminEditCustomerView import EditCustomer
from Control.AdminEditCustomerControl import EditCustomerControl
from View.AdminEditStaffView import EditStaff
from View.FinalizeOrderPopup import FinalizeOrderPopup
from View.StaffCreateCustomerView import SCreateCustomer
from Control.StaffCreateCustomerControl import SCreateCustomerControl
from View.StaffCreateOrderView import CreateOrderManager
from Control.StaffCreateOrderControl import CreateOrderControl
from Control.StaffDashboardControl import SDashBControl
from View.StaffDashboardView import SDashboard
from View.StaffEditCustomerView import SEditCustomer
from Control.StaffEditCustomerControl import SEditCustomerControl
from Control.StaffHomeControl import SHControl
from View.StaffCustomerManagerView import SManagerC
from Control.AdminEditStaffControl import Editstaffcontrol
from Control.StaffCustomerManagerControl import SManagerCControl
from View.StaffOrderManagementView import SOrders
from Control.StaffOrderController import SOControl
from Control.StaffReportControl import SReportControl
from View.StaffDeliveryView import SDelivery
from View.StaffReportsView import SReports
from Control.StaffDeliveryControl import SDeliveryControl
from View.StaffEditOrderView import SEditOrder
from Control.StaffEditOrderControl import SEditOrderControl


class LoginController:
    def __init__(self, view, model, admin_home, staff_home):
        self.view = view
        self.model = model
        self.admin_home = admin_home
        self.staff_home = staff_home

        # Store current logged-in user info
        self.current_staff_id = None
        self.current_admin_id = None

        # Initialize views
        # AdminView
        self.dashboard = ADashboard(admin_home, model)
        self.maneger = AManager(admin_home)
        self.manegerc = AManagerC(admin_home)
        self.cstaff = CreateStaff(admin_home)
        self.order = AOrders(admin_home)
        self.report = AReport(admin_home)
        self.ccv = CreateCustomer(admin_home)
        self.editstaff = EditStaff(admin_home)
        self.editcustomer = EditCustomer(admin_home)

        # StaffView
        self.staff_db = SDashboard(staff_home, model)
        self.customer = SManagerC(staff_home)
        self.staff_ccv = SCreateCustomer(staff_home)
        self.staffeditcustomer = SEditCustomer(staff_home)
        self.stafforder = SOrders(staff_home)
        self.createorder = CreateOrderManager(staff_home)
        self.staffreport = SReports(staff_home)
        self.delivery = SDelivery(self.staff_home)
        self.editorder = SEditOrder(staff_home)

        self.finalize_popup = FinalizeOrderPopup(parent=staff_home, model=model)

        # Admin Controllers
        self.home_controller = AHControl(admin_home, self.dashboard, self.maneger, self.order, self.report, self.cstaff,self.view)
        self.dashboard_controller = ADashBControl(admin_home, self.dashboard, self.maneger, self.order, self.report,self.model, self.view)
        self.editstaff_controller = Editstaffcontrol(self.model, self.admin_home, self.dashboard, self.maneger,self.order, self.report, self.view)
        self.editcustomer_control = EditCustomerControl(self.model, self.admin_home, self.dashboard, self.maneger,self.manegerc, self.order, self.report, self.view)
        self.maneger_controller = AManagerControl(admin_home, self.dashboard, self.maneger, self.manegerc, self.cstaff,self.order, self.report, self.model, self.editstaff,self.editstaff_controller, self.view)
        self.manegerc_controller = AManagerControlC(admin_home, self.dashboard, self.maneger, self.manegerc, self.order,self.report, self.ccv, self.model, self.editcustomer,self.editcustomer_control, self.view)
        self.order_controller = AOrderControl(admin_home, self.dashboard, self.maneger, self.order, self.report,self.model, self.view)
        self.report_controller = AReportControl(admin_home, self.dashboard, self.maneger, self.order, self.report,self.model, self.view)
        self.customer_controller = CreateCustomerControl(self.model, admin_home, self.dashboard, self.maneger,self.order, self.report, self.view, self.manegerc_controller)
        self.staff_controller = Createstaffcontrol(self.model, admin_home, self.dashboard, self.maneger, self.order,self.report, self.view, self.maneger_controller)

        # Staff Controllers - Initialize in correct order
        self.staff_home_controller = SHControl(staff_home, self.staff_db, self.customer, self.stafforder, self.delivery,self.staffreport, self.view)
        self.staff_dashboard_controller = SDashBControl(staff_home, self.staff_db, self.customer, self.stafforder,self.delivery, self.staffreport, self.view)
        self.staff_editcustomer_controller = SEditCustomerControl(self.model, staff_home, self.staff_db, self.customer,self.delivery, self.stafforder, self.staffreport,self.view)

        # Initialize edit order controller FIRST (before order controller)
        self.staff_editorder_controller = SEditOrderControl(staff_home, self.staff_db, self.customer, self.stafforder,self.delivery, self.staffreport, self.model, self.view)

        # Initialize order controller WITH edit_order_control parameter
        self.staff_order_controller = SOControl(staff_home, self.staff_db, self.customer, self.stafforder,self.delivery, self.staffreport, model, self.view,edit_order_control=self.staff_editorder_controller)

        self.staff_report_controller = SReportControl(staff_home, self.staff_db, self.customer, self.stafforder,self.delivery, self.staffreport, self.model, self.view)
        self.staff_delivery_controller = SDeliveryControl(staff_home, self.staff_db, self.customer, self.stafforder,self.delivery, self.staffreport, self.model, self.view)

        self.staff_smanagerc_controller = SManagerCControl(staff_home, self.staff_db, self.customer, self.stafforder,self.delivery, self.createorder, self.staffreport,self.model, self.staffeditcustomer,self.staff_editcustomer_controller, self.view)

        # Create order controller
        self.staff_createorder_controller = CreateOrderControl(staff_home, self.staff_db, self.customer,self.stafforder, self.delivery, self.staffreport,self.model, self.view, self.staff_smanagerc_controller,self.staff_order_controller)

        # Set cross-references
        self.staff_smanagerc_controller.createorder_control = self.staff_createorder_controller
        self.staff_createcustomer_controller = SCreateCustomerControl(self.model, staff_home, self.staff_db,self.customer, self.stafforder, self.delivery,self.staffreport, self.view,self.staff_smanagerc_controller)
        self.staff_delivery_controller.order_controller = self.staff_order_controller
        # Connect login button
        self.view.login_btn.clicked.connect(self.handle_login)

    def handle_login(self):
        try:
            username = self.view.username.text().strip()
            password = self.view.password.text()

            # Validate input
            if not username or not password:
                QMessageBox.warning(
                    self.view,
                    "Input Required",
                    "Please enter both username and password."
                )
                return



            user = self.model.login2(username, password)

            if user:
                # Admin login successful
                admin_id = user.get('AdminID')

                # Store admin ID
                self.current_admin_id = admin_id
                self.current_staff_id = None

                QtWidgets.QMessageBox.information(
                    self.view,
                    "Success",
                    f"Welcome {username}!"
                )

                # CRITICAL: Set model FIRST
                self.admin_home.model = self.model

                # Set admin context in AdminHome
                self.admin_home.set_admin_context(admin_id, self.model)

                # Set admin context in home controller
                self.home_controller.set_admin_context(admin_id)

                # Set admin ID in customer controller
                if hasattr(self.customer_controller, 'set_admin_id'):
                    self.customer_controller.set_admin_id(admin_id)
                    print(f"✓ Set admin ID in CreateCustomerControl: {admin_id}")

                # Clear login view and show admin home
                self.view.close()
                self.admin_home.show()

                # IMPORTANT: Set to home page FIRST
                self.admin_home.stackedWidget.setCurrentIndex(self.admin_home.home_page_index)

                # THEN refresh the data
                print("🔵 Calling admin_home.load_home_data() after login")
                if hasattr(self.admin_home, 'load_home_data'):
                    self.admin_home.load_home_data()
                else:
                    print("⚠️ admin_home doesn't have load_home_data method!")

                print(f"✓ Admin login complete - AdminID: {admin_id}")
                return  # Exit after successful admin login

                # If admin fails, try staff login
            user = self.model.login(username, password)

            if user:
                # Staff login successful
                self.current_staff_id = user.get('StaffID')
                self.current_admin_id = None

                QtWidgets.QMessageBox.information(
                    self.view,
                    "Success",
                    f"Welcome {username}!"
                )

                # UPDATE LAST ACTIVE ON LOGIN
                self.model.update_staff_last_active(self.current_staff_id)

                # Set staff ID in StaffHome
                self.staff_home.set_staff_context(self.current_staff_id, self.model)

                # Set staff ID in SHControl (HOME CONTROLLER)
                if hasattr(self.staff_home_controller, 'set_staff_context'):
                    self.staff_home_controller.set_staff_context(self.current_staff_id)
                    print(f"✓ Set staff ID in SHControl: {self.current_staff_id}")

                # Set staff ID in ALL controllers that need it:

                # 1. Edit Customer Controller
                if hasattr(self.staff_editcustomer_controller, 'set_staff_id'):
                    self.staff_editcustomer_controller.set_staff_id(self.current_staff_id)
                    print(f"✓ Set staff ID in SEditCustomerControl: {self.current_staff_id}")

                # 2. Edit Order Controller (already has it)
                if hasattr(self.staff_editorder_controller, 'set_staff_id'):
                    self.staff_editorder_controller.set_staff_id(self.current_staff_id)
                    print(f"✓ Set staff ID in SEditOrderControl: {self.current_staff_id}")

                # 3. Create Order Controller (already has it)
                self.staff_createorder_controller.set_staff_id(self.current_staff_id)
                print(f"✓ Set staff ID in CreateOrderControl: {self.current_staff_id}")

                # 4. Create Customer Controller (already has it)
                self.staff_createcustomer_controller.set_staff_id(self.current_staff_id)
                print(f"✓ Set staff ID in CreateCustomerControl: {self.current_staff_id}")

                # 5. Delivery Controller
                self.staff_delivery_controller.set_staff_context(self.current_staff_id)
                print(f"✓ Set staff ID in DeliveryControl: {self.current_staff_id}")

                # 6. Finalize popup
                self.finalize_popup.set_staff_id(self.current_staff_id)
                print(f"✓ Set staff ID in FinalizeOrderPopup: {self.current_staff_id}")

                # 7. Customer Manager Controller (SManegerCControl)
                if hasattr(self.staff_smanagerc_controller, 'set_staff_id'):
                    self.staff_smanagerc_controller.set_staff_id(self.current_staff_id)
                    print(f"✓ Set staff ID in SManegerCControl: {self.current_staff_id}")

                # 8. Order Controller (SOControl)
                if hasattr(self.staff_order_controller, 'set_staff_id'):
                    self.staff_order_controller.set_staff_id(self.current_staff_id)
                    print(f"✓ Set staff ID in SOControl: {self.current_staff_id}")

                self.view.close()
                self.staff_home.show()
                self.staff_home.stackedWidget.setCurrentIndex(self.staff_home.home_page_index)

                # Trigger initial refresh of home page
                if hasattr(self.staff_home_controller, 'refresh_home_page'):
                    self.staff_home_controller.refresh_home_page()
                    print("✓ Initial home page refresh triggered")

            else:
                # Both failed - show error message
                QMessageBox.warning(
                    self.view,
                    "Login Failed",
                    "Invalid username or password.\nPlease check your credentials and try again."
                )
                # Clear password field for security
                self.view.password.clear()
                self.view.password.setFocus()

        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Login Error",
                f"An unexpected error occurred during login:\n{str(e)}"
            )
            print(f"Login exception: {e}")
            import traceback
            traceback.print_exc()