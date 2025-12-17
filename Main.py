
import warnings

from View.StaffHomeView import StaffHome

warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys

from PyQt6.QtWidgets import QApplication, QWidget
from Model.Model import Model
from View.LoginView import LoginView
from Control.LoginControl import LoginController
from View.AdminHomeView import AdminHome


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize model
        self.model = Model()

        # Initialize views
        self.login_view = LoginView()
        self.admin_home = AdminHome()
        self.staff_home = StaffHome()

        # Initialize controller (this creates dashboard, maneger, and all sub-controllers)
        self.controller = LoginController(self.login_view, self.model, self.admin_home,self.staff_home)

        # Setup and show login view
        self.login_view.resize(1000, 600)
        self.login_view.setFixedSize(1000, 600)
        self.login_view.show()


# Entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create main window (initializes everything)
    main_window = MainWindow()

    # Start event loop
    sys.exit(app.exec())