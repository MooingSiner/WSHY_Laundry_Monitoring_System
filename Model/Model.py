import csv
import os
from datetime import datetime

import mysql.connector
import pymysql
from PyQt6.QtWidgets import QMessageBox


class Model:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="washy"
            )
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Database Connection Failed", str(err))

    # ---------------------- LOGIN ----------------------
    def login(self, username, password):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT * FROM securstaff WHERE username=%s AND upassword=%s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Login Error", f"Error during login:\n{err}")
            return None

    def login2(self, username, password):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT * FROM securadm WHERE username=%s AND upassword=%s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Login Error", f"Error during login:\n{err}")
            return None

    # ---------------------- EMPLOYEES ----------------------
    def create_employee(self, fname, mname, lname, email, phone, user, passw, role='staff'):
        try:
            now = datetime.now()
            with self.conn.cursor() as cursor:
                sql1 = """INSERT INTO Employees (EFName, EMName, ELName, EEmail, EPhone)
                          VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql1, (fname, mname, lname, email, phone))
                employee_id = cursor.lastrowid

                if role.lower() == 'admin':
                    sql2 = "INSERT INTO Admin (EmployeeID, SDateApplied, LastActiveAt) VALUES (%s, %s, %s)"
                    cursor.execute(sql2, (employee_id, now.date(), now))
                    admin_id = cursor.lastrowid
                    sql3 = "INSERT INTO SecurAdm (Username, UPassword, AdminID) VALUES (%s, %s, %s)"
                    cursor.execute(sql3, (user, passw, admin_id))
                    self.conn.commit()
                    return {'employee_id': employee_id, 'admin_id': admin_id, 'role': 'admin'}
                else:
                    sql2 = "INSERT INTO Staff (EmployeeID, SDateApplied, LastActiveAt) VALUES (%s, %s, %s)"
                    cursor.execute(sql2, (employee_id, now.date(), now))
                    staff_id = cursor.lastrowid
                    sql3 = "INSERT INTO SecurStaff (Username, UPassword, StaffID) VALUES (%s, %s, %s)"
                    cursor.execute(sql3, (user, passw, staff_id))
                    self.conn.commit()
                    return {'employee_id': employee_id, 'staff_id': staff_id, 'role': 'staff'}

        except pymysql.IntegrityError as e:
            self.conn.rollback()
            if 'Username' in str(e):
                QMessageBox.critical(None, "Integrity Error", f"Username '{user}' already exists")
            else:
                QMessageBox.critical(None, "Database Integrity Error", str(e))
            return None
        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Creating Employee", str(e))
            return None

    def get_all_staff(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                    SELECT e.EmployeeID, e.EFName, e.EMName, e.ELName, e.EEmail, e.EPhone,
                           s.StaffID, s.SDateApplied, s.LastActiveAt, sec.Username
                    FROM Employees e
                             INNER JOIN Staff s ON e.EmployeeID = s.EmployeeID
                             LEFT JOIN SecurStaff sec ON s.StaffID = sec.StaffID
                    ORDER BY e.EFName, e.ELName
                    """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Fetching Staff", str(err))
            return []

    def get_all_admins(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                    SELECT e.EmployeeID, e.EFName, e.EMName, e.ELName, e.EEmail, e.EPhone,
                           a.AdminID, a.SDateApplied, a.LastActiveAt, sec.Username
                    FROM Employees e
                             INNER JOIN Admin a ON e.EmployeeID = a.EmployeeID
                             LEFT JOIN SecurAdm sec ON a.AdminID = sec.AdminID
                    ORDER BY e.EFName, e.ELName
                    """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Fetching Admins", str(err))
            return []

    def get_staff_by_id(self, staff_id):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                    SELECT e.*, \
                           s.*, \
                           sec.Username,
                           COUNT(DISTINCT o.OrderID)    as orders_processed,
                           COUNT(DISTINCT c.CustomerID) as customers_created,
                           COUNT(DISTINCT t.TransactID) as transactions_count,
                           COALESCE(SUM(
                                            CASE
                                                WHEN o.Status = 'Completed' THEN t.AmountPaid
                                                ELSE 0
                                                END
                                    ), 0)               as total_transactions
                    FROM Employees e
                             INNER JOIN Staff s ON e.EmployeeID = s.EmployeeID
                             LEFT JOIN SecurStaff sec ON s.StaffID = sec.StaffID
                             LEFT JOIN Orders o ON s.StaffID = o.StaffID
                             LEFT JOIN Customer c ON s.StaffID = c.StaffID
                             LEFT JOIN Transactions t ON s.StaffID = t.StaffID AND o.OrderID = t.OrderID
                    WHERE s.StaffID = %s
                    GROUP BY e.EmployeeID, s.StaffID
                    """
            cursor.execute(query, (staff_id,))
            result = cursor.fetchone()

            if result:
                # Get last 2 activities
                cursor.execute("""
                               SELECT ActivityType, ActivityTime, OrderID, CustomerID
                               FROM StaffActivityLog
                               WHERE StaffID = %s
                               ORDER BY ActivityTime DESC LIMIT 2
                               """, (staff_id,))
                activities = cursor.fetchall()

                # Format activities into readable strings
                recent_activities = []
                for act in activities:
                    activity_text = self._format_activity_text(act)
                    recent_activities.append(activity_text)

                result['recent_activities'] = recent_activities

            cursor.close()
            return result
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Fetching Staff Details", str(err))
            return None

    def get_admin_by_id(self, admin_id):
        """Get admin details by admin ID"""
        try:
            cursor = self.conn.cursor(dictionary=True)

            # Get basic admin info
            query = """
                    SELECT e.*, a.*, sec.Username
                    FROM Employees e
                             INNER JOIN Admin a ON e.EmployeeID = a.EmployeeID
                             LEFT JOIN SecurAdm sec ON a.AdminID = sec.AdminID
                    WHERE a.AdminID = %s
                    """
            cursor.execute(query, (admin_id,))
            result = cursor.fetchone()

            if result:
                # Count customers created SPECIFICALLY by this admin
                cursor.execute("""
                               SELECT COUNT(*) as count
                               FROM Customer
                               WHERE AdminID = %s
                               """, (admin_id,))
                customers = cursor.fetchone()
                result['customers_created'] = customers['count'] if customers else 0

                print(f"✓ Admin {admin_id} has created {result['customers_created']} customers")

                # Count staff in the system
                cursor.execute("SELECT COUNT(*) as count FROM Staff")
                staff = cursor.fetchone()
                result['staff_created'] = staff['count'] if staff else 0

                # Get last 2 activities (checking if admin activity log exists)
                # Note: You may need to create an AdminActivityLog table similar to StaffActivityLog
                # For now, we'll try to get customer creation activities
                cursor.execute("""
                               SELECT 'CREATE_CUSTOMER' as ActivityType,
                                      DateCreated       as ActivityTime,
                                      CustomerID,
                                      NULL              as OrderID
                               FROM Customer
                               WHERE AdminID = %s
                               ORDER BY DateCreated DESC LIMIT 2
                               """, (admin_id,))
                activities = cursor.fetchall()

                # Format activities
                recent_activities = []
                for act in activities:
                    activity_text = self._format_activity_text(act)
                    recent_activities.append(activity_text)

                result['recent_activities'] = recent_activities

            cursor.close()
            return result

        except mysql.connector.Error as err:
            print(f"✗ Database error: {err}")
            QMessageBox.critical(None, "Error Fetching Admin Details", str(err))
            return None

    def _format_activity_text(self, activity):
        """Helper method to format activity log entries into readable text"""
        activity_type = activity.get('ActivityType', '')
        activity_time = activity.get('ActivityTime', '')
        order_id = activity.get('OrderID')
        customer_id = activity.get('CustomerID')

        # Format time
        if isinstance(activity_time, str):
            try:
                time_obj = datetime.strptime(activity_time, '%Y-%m-%d %H:%M:%S')
                time_str = time_obj.strftime('%I:%M %p')
            except:
                time_str = str(activity_time)
        elif isinstance(activity_time, datetime):
            time_str = activity_time.strftime('%I:%M %p')
        else:
            time_str = "Unknown time"

        # Format activity type into readable text
        activity_map = {
            'CREATE_ORDER': f'Created order #{order_id}' if order_id else 'Created an order',
            'EDIT_ORDER': f'Edited order #{order_id}' if order_id else 'Edited an order',
            'CREATE_CUSTOMER': f'Created customer #{customer_id}' if customer_id else 'Created a customer',
            'EDIT_CUSTOMER': f'Edited customer #{customer_id}' if customer_id else 'Edited a customer',
            'PICKUP_ORDER': f'Picked up order #{order_id}' if order_id else 'Picked up an order',
            'DELIVER_ORDER': f'Delivered order #{order_id}' if order_id else 'Delivered an order',
            'COMPLETE_TRANSACTION': f'Completed transaction for order #{order_id}' if order_id else 'Completed a transaction',
        }

        activity_text = activity_map.get(activity_type, activity_type)
        return f"{activity_text} at {time_str}"
    def search_staff(self, search_term):
        try:
            cursor = self.conn.cursor(dictionary=True)
            search_pattern = f"%{search_term}%"
            query = """
                    SELECT e.EmployeeID, e.EFName, e.EMName, e.ELName, e.EEmail, e.EPhone,
                           s.StaffID, s.SDateApplied, s.LastActiveAt, sec.Username
                    FROM Employees e
                             INNER JOIN Staff s ON e.EmployeeID = s.EmployeeID
                             LEFT JOIN SecurStaff sec ON s.StaffID = sec.StaffID
                    WHERE e.EFName LIKE %s
                       OR e.ELName LIKE %s
                       OR e.EEmail LIKE %s
                       OR e.EPhone LIKE %s
                    ORDER BY e.EFName, e.ELName
                    """
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Searching Staff", str(err))
            return []

    def delete_staff(self, staff_id):
        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM Staff WHERE StaffID = %s"
            cursor.execute(query, (staff_id,))
            self.conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows > 0
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Deleting Staff", str(err))
            return False

    def update_staff(self, staff_id, fname, mname, lname, email, phone):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT EmployeeID FROM Staff WHERE StaffID = %s", (staff_id,))
            result = cursor.fetchone()
            if not result:
                QMessageBox.critical(None, "Error Updating Staff", "Staff ID not found")
                return False
            employee_id = result[0]
            query = """
                    UPDATE Employees
                    SET EFName = %s, EMName = %s, ELName = %s, EEmail = %s, EPhone = %s
                    WHERE EmployeeID = %s
                    """
            cursor.execute(query, (fname, mname, lname, email, phone, employee_id))
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Updating Staff", str(err))
            return False

    # ---------------------- CUSTOMERS ----------------------
    def get_all_customers(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                    SELECT c.CustomerID,
                           c.CFName, c.CMName, c.CLName,
                           c.CEmail, c.CPhone,
                           COUNT(DISTINCT o.OrderID) as total_orders,
                           MAX(o.OrderDate) as last_order_date
                    FROM Customer c
                             LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
                    GROUP BY c.CustomerID
                    ORDER BY c.CFName, c.CLName
                    """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Fetching Customers", str(err))
            return []

    def get_customer_by_id(self, customer_id):
        """
        Returns customer info with total orders, total spent, and last order date.
        """
        if not self.conn:
            return None

        try:
            cursor = self.conn.cursor(dictionary=True)

            # Get basic customer info
            cursor.execute("""
                SELECT CustomerID, CFName, CMName, CLName, CEmail, CPhone, DateCreated
                FROM Customer
                WHERE CustomerID = %s
            """, (customer_id,))
            customer = cursor.fetchone()
            if not customer:
                return None

            # Total orders and total spent
            cursor.execute("""
                SELECT 
                    COUNT(*) AS total_orders, 
                    IFNULL(SUM(T.AmountPaid), 0) AS total_spent,
                    MAX(O.OrderDate) AS last_order_date
                FROM Orders O
                LEFT JOIN Transactions T ON O.OrderID = T.OrderID
                WHERE O.CustomerID = %s
            """, (customer_id,))
            stats = cursor.fetchone()
            customer['total_orders'] = stats['total_orders'] or 0
            customer['total_spent'] = float(stats['total_spent'] or 0)
            customer['last_order_date'] = stats['last_order_date']

            # Completed and pending orders
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN Status='Completed' THEN 1 ELSE 0 END) AS completed_orders,
                    SUM(CASE WHEN Status!='Completed' THEN 1 ELSE 0 END) AS pending_orders
                FROM Orders
                WHERE CustomerID = %s
            """, (customer_id,))
            order_status = cursor.fetchone()
            customer['completed_orders'] = order_status['completed_orders'] or 0
            customer['pending_orders'] = order_status['pending_orders'] or 0

            return customer

        except mysql.connector.Error as e:
            QMessageBox.critical(None, "Error Getting Customer Data", str(e))
            return None

    def search_customers(self, search_term):
        try:
            cursor = self.conn.cursor(dictionary=True)
            pattern = f"%{search_term}%"
            query = """
                    SELECT c.CustomerID,
                           c.CFName, c.CMName, c.CLName,
                           c.CEmail, c.CPhone,
                           COUNT(DISTINCT o.OrderID) as total_orders,
                           MAX(o.OrderDate) as last_order_date
                    FROM Customer c
                             LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
                    WHERE c.CFName LIKE %s OR c.CLName LIKE %s OR c.CEmail LIKE %s OR c.CPhone LIKE %s
                    GROUP BY c.CustomerID
                    ORDER BY c.CFName, c.CLName
                    """
            cursor.execute(query, (pattern, pattern, pattern, pattern))
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Searching Customers", str(err))
            return []

    def delete_customer(self, customer_id):
        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM Customer WHERE CustomerID = %s"
            cursor.execute(query, (customer_id,))
            self.conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows > 0
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Deleting Customer", str(err))
            return False

    def update_customer(self, customer_id, fname, mname, lname, email, phone):
        try:
            cursor = self.conn.cursor()
            query = """
                    UPDATE Customer
                    SET CFName=%s, CMName=%s, CLName=%s, CEmail=%s, CPhone=%s
                    WHERE CustomerID=%s
                    """
            cursor.execute(query, (fname, mname, lname, email, phone, customer_id))
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Updating Customer", str(err))
            return False

    def create_customer(self, fname, mname, lname, email, phone,
                        street_add, appart_unit, city, zip_code,
                        staff_id=None, admin_id=None):
        """Insert a new customer and address, ensuring DateCreated is automatically set"""
        if not self.conn:
            QMessageBox.critical(None, "Database Error", "No database connection")
            return None

        try:
            cursor = self.conn.cursor()
            # Insert customer (do NOT include DateCreated so default CURRENT_TIMESTAMP is used)
            sql_customer = """
                           INSERT INTO Customer (CFName, CMName, CLName, CEmail, CPhone, StaffID, AdminID)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)
                           """
            cursor.execute(sql_customer, (fname, mname, lname, email, phone, staff_id, admin_id))
            customer_id = cursor.lastrowid

            # Insert address
            sql_address = """
                          INSERT INTO Address (CustomerID, StreetAdd, AppartUnit, City, ZipCode)
                          VALUES (%s, %s, %s, %s, %s)
                          """
            cursor.execute(sql_address, (customer_id, street_add, appart_unit, city, zip_code))

            self.conn.commit()
            return customer_id

        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Creating Customer", str(e))
            return None

    def add_customer_address(self, customer_id, street_add, appart_unit, city, zip_code):
        try:
            cursor = self.conn.cursor()
            query = """
                    INSERT INTO Address (CustomerID, StreetAdd, AppartUnit, City, ZipCode)
                    VALUES (%s,%s,%s,%s,%s)
                    """
            cursor.execute(query, (customer_id, street_add, appart_unit, city, zip_code))
            self.conn.commit()
            address_id = cursor.lastrowid
            cursor.close()
            return address_id
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Adding Address", str(err))
            return None

    def update_customer_address(self, address_id, street_add, appart_unit, city, zip_code):
        try:
            cursor = self.conn.cursor()
            query = """
                    UPDATE Address
                    SET StreetAdd=%s, AppartUnit=%s, City=%s, ZipCode=%s
                    WHERE AddID=%s
                    """
            cursor.execute(query, (street_add, appart_unit, city, zip_code, address_id))
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Updating Address", str(err))
            return False

    def delete_customer_address(self, address_id):
        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM Address WHERE AddID=%s"
            cursor.execute(query, (address_id,))
            self.conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows > 0
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Deleting Address", str(err))
            return False

    def get_customer_addresses(self, customer_id):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT * FROM Address WHERE CustomerID=%s"
            cursor.execute(query, (customer_id,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Fetching Customer Addresses", str(err))
            return []

    # ---------------------- ORDERS ----------------------
    def get_all_orders(self):
        """Get all orders without transaction date"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                    SELECT o.OrderID, \
                           o.CustomerID,
                           CONCAT(c.CFName, ' ', COALESCE(c.CMName, ''), ' ', c.CLName) as customer_name,
                           o.OrderDate, \
                           o.DatePicked, \
                           o.DateDelivered,
                           o.TotalAmount, \
                           o.Status, \
                           o.StaffID
                    FROM Orders o
                             LEFT JOIN Customer c ON o.CustomerID = c.CustomerID
                    ORDER BY o.OrderDate DESC
                    """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Fetching Orders", str(err))
            return []

    def get_order_by_id(self, order_id):
        """Get order details without transaction date"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                    SELECT o.*, \
                           CONCAT(c.CFName, ' ', COALESCE(c.CMName, ''), ' ', c.CLName) as customer_name,
                           c.CEmail, \
                           c.CPhone
                    FROM Orders o
                             LEFT JOIN Customer c ON o.CustomerID = c.CustomerID
                    WHERE o.OrderID = %s
                    """
            cursor.execute(query, (order_id,))
            order = cursor.fetchone()

            if order:
                cursor.execute("SELECT * FROM OrderService WHERE OrderID=%s", (order_id,))
                order['services'] = cursor.fetchall()
                cursor.execute("SELECT * FROM Transactions WHERE OrderID=%s", (order_id,))
                order['transactions'] = cursor.fetchall()

            cursor.close()
            return order
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Fetching Order Details", str(err))
            return None

    def create_order(self, customer_id, staff_id, total_amount, status='Pending'):
        """Create a new order"""
        try:
            cursor = self.conn.cursor()
            query = """
                    INSERT INTO Orders (CustomerID, StaffID, TotalAmount, Status)
                    VALUES (%s, %s, %s, %s)
                    """
            cursor.execute(query, (customer_id, staff_id, total_amount, status))
            self.conn.commit()
            order_id = cursor.lastrowid
            cursor.close()
            return order_id
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Creating Order", str(err))
            return None

    def add_order_service(self, order_id, service_name, weight_kg, price_per_kg,
                          wash_amount, fast_dry, fast_dry_amount, iron_only,
                          iron_only_amount, fold, fold_amount, total_amount):
        """Add a service to an order"""
        try:
            cursor = self.conn.cursor()
            query = """
                    INSERT INTO OrderService
                    (OrderID, ServiceName, WeightKg, PriceperKG, WashAmount,
                     FastDry, FastDryAmount, IronOnly, IronOnlyAmount,
                     Fold, FoldAmount, TotalAmount)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (order_id, service_name, weight_kg, price_per_kg,
                                   wash_amount, fast_dry, fast_dry_amount, iron_only,
                                   iron_only_amount, fold, fold_amount, total_amount))
            self.conn.commit()
            service_id = cursor.lastrowid
            cursor.close()
            return service_id
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Adding Order Service", str(err))
            return None

    def add_transaction(self, order_id, amount_paid, payment_method, staff_id=None):
        """Add a transaction for an order"""
        try:
            cursor = self.conn.cursor()
            query = """
                    INSERT INTO Transactions (OrderID, AmountPaid, PaymentMethod, StaffID)
                    VALUES (%s, %s, %s, %s)
                    """
            cursor.execute(query, (order_id, amount_paid, payment_method, staff_id))
            self.conn.commit()
            transaction_id = cursor.lastrowid
            cursor.close()
            return transaction_id
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Adding Transaction", str(err))
            return None

    def update_order_status(self, order_id, status):
        """Update order status"""
        try:
            cursor = self.conn.cursor()
            query = "UPDATE Orders SET Status=%s WHERE OrderID=%s"
            cursor.execute(query, (status, order_id))
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Updating Order Status", str(err))
            return False

    def delete_order(self, order_id):
        """Delete order (cascades to related tables)"""
        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM Orders WHERE OrderID=%s"
            cursor.execute(query, (order_id,))
            self.conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows > 0
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Deleting Order", str(err))
            return False

    def search_orders(self, search_term):
        """Search orders without transaction date"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            pattern = f"%{search_term}%"
            query = """
                    SELECT o.OrderID, \
                           o.CustomerID,
                           CONCAT(c.CFName, ' ', COALESCE(c.CMName, ''), ' ', c.CLName) as customer_name,
                           o.OrderDate, \
                           o.DatePicked, \
                           o.DateDelivered,
                           o.TotalAmount, \
                           o.Status, \
                           o.StaffID
                    FROM Orders o
                             LEFT JOIN Customer c ON o.CustomerID = c.CustomerID
                    WHERE o.OrderID LIKE %s
                       OR CONCAT(c.CFName, ' ', c.CLName) LIKE %s
                       OR o.Status LIKE %s
                    ORDER BY o.OrderDate DESC
                    """
            cursor.execute(query, (pattern, pattern, pattern))
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Searching Orders", str(err))
            return []

    def get_orders_by_status(self, status):
        """Get orders by status without transaction date"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                    SELECT o.OrderID, \
                           o.CustomerID,
                           CONCAT(c.CFName, ' ', COALESCE(c.CMName, ''), ' ', c.CLName) as customer_name,
                           o.OrderDate, \
                           o.DatePicked, \
                           o.DateDelivered,
                           o.TotalAmount, \
                           o.Status, \
                           o.StaffID
                    FROM Orders o
                             LEFT JOIN Customer c ON o.CustomerID = c.CustomerID
                    WHERE o.Status = %s
                    ORDER BY o.OrderDate DESC
                    """
            cursor.execute(query, (status,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Fetching Orders by Status", str(err))
            return []

    def get_orders_by_customer(self, customer_id):
        """Get orders for a customer without transaction date"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                    SELECT o.*, CONCAT(c.CFName, ' ', COALESCE(c.CMName, ''), ' ', c.CLName) as customer_name
                    FROM Orders o
                             LEFT JOIN Customer c ON o.CustomerID = c.CustomerID
                    WHERE o.CustomerID = %s
                    ORDER BY o.OrderDate DESC
                    """
            cursor.execute(query, (customer_id,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Fetching Orders by Customer", str(err))
            return []

    def get_order_statistics(self):
        """Get overall order statistics"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                    SELECT COUNT(*) as total_orders,
                           COUNT(CASE WHEN Status='Completed' THEN 1 END) as completed_orders,
                           COUNT(CASE WHEN Status='Pending' THEN 1 END) as pending_orders,
                           COUNT(CASE WHEN Status='Cancelled' THEN 1 END) as cancelled_orders,
                           COALESCE(SUM(TotalAmount),0) as total_revenue,
                           COALESCE(AVG(TotalAmount),0) as average_order_value
                    FROM Orders
                    """
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Fetching Order Statistics", str(err))
            return None

    def edit_employee(self, employee_id, fname, mname, lname, email, phone, username=None, password=None, role=None):
        """
        Edit employee information and optionally update credentials
        employee_id: The EmployeeID to edit
        fname, mname, lname, email, phone: Updated personal information
        username, password: Optional - update credentials if provided
        role: 'staff' or 'admin' - determines which security table to update
        """
        try:
            cursor = self.conn.cursor()

            # 1. Update Employees table
            query = """
                    UPDATE Employees
                    SET EFName = %s,
                        EMName = %s,
                        ELName = %s,
                        EEmail = %s,
                        EPhone = %s
                    WHERE EmployeeID = %s
                    """
            cursor.execute(query, (fname, mname, lname, email, phone, employee_id))

            # 2. If username/password provided, update security tables
            if username or password:
                if not role:
                    # Try to detect role from existing records
                    cursor.execute("SELECT StaffID FROM Staff WHERE EmployeeID = %s", (employee_id,))
                    if cursor.fetchone():
                        role = 'staff'
                    else:
                        cursor.execute("SELECT AdminID FROM Admin WHERE EmployeeID = %s", (employee_id,))
                        if cursor.fetchone():
                            role = 'admin'

                if role and role.lower() == 'admin':
                    # Get AdminID
                    cursor.execute("SELECT AdminID FROM Admin WHERE EmployeeID = %s", (employee_id,))
                    result = cursor.fetchone()
                    if result:
                        admin_id = result[0]

                        # Build dynamic update query for SecurAdm
                        update_parts = []
                        params = []

                        if username:
                            update_parts.append("Username = %s")
                            params.append(username)
                        if password:
                            update_parts.append("UPassword = %s")
                            params.append(password)

                        if update_parts:
                            params.append(admin_id)
                            sec_query = f"UPDATE SecurAdm SET {', '.join(update_parts)} WHERE AdminID = %s"
                            cursor.execute(sec_query, tuple(params))

                elif role and role.lower() == 'staff':
                    # Get StaffID
                    cursor.execute("SELECT StaffID FROM Staff WHERE EmployeeID = %s", (employee_id,))
                    result = cursor.fetchone()
                    if result:
                        staff_id = result[0]

                        # Build dynamic update query for SecurStaff
                        update_parts = []
                        params = []

                        if username:
                            update_parts.append("Username = %s")
                            params.append(username)
                        if password:
                            update_parts.append("UPassword = %s")
                            params.append(password)

                        if update_parts:
                            params.append(staff_id)
                            sec_query = f"UPDATE SecurStaff SET {', '.join(update_parts)} WHERE StaffID = %s"
                            cursor.execute(sec_query, tuple(params))

            self.conn.commit()
            cursor.close()

            # Return updated employee info
            return {
                'employee_id': employee_id,
                'role': role if role else 'unknown',
                'success': True
            }

        except mysql.connector.IntegrityError as e:
            self.conn.rollback()
            if 'Username' in str(e):
                QMessageBox.critical(None, "Integrity Error", f"Username '{username}' already exists")
            else:
                QMessageBox.critical(None, "Database Integrity Error", str(e))
            return None
        except mysql.connector.Error as err:
            self.conn.rollback()
            QMessageBox.critical(None, "Error Editing Employee", str(err))
            return None

    def get_employee_full_info(self, employee_id):
        """
        Get complete employee information including role and credentials
        Useful for pre-populating edit forms
        """
        try:
            cursor = self.conn.cursor(dictionary=True)

            # Get basic employee info
            query = "SELECT * FROM Employees WHERE EmployeeID = %s"
            cursor.execute(query, (employee_id,))
            employee = cursor.fetchone()

            if not employee:
                cursor.close()
                return None

            # Check if staff or admin
            cursor.execute("SELECT StaffID FROM Staff WHERE EmployeeID = %s", (employee_id,))
            staff_result = cursor.fetchone()

            if staff_result:
                employee['role'] = 'staff'
                employee['staff_id'] = staff_result['StaffID']

                # Get username
                cursor.execute("SELECT Username FROM SecurStaff WHERE StaffID = %s",
                               (staff_result['StaffID'],))
                sec_result = cursor.fetchone()
                if sec_result:
                    employee['username'] = sec_result['Username']
            else:
                cursor.execute("SELECT AdminID FROM Admin WHERE EmployeeID = %s", (employee_id,))
                admin_result = cursor.fetchone()

                if admin_result:
                    employee['role'] = 'admin'
                    employee['admin_id'] = admin_result['AdminID']

                    # Get username
                    cursor.execute("SELECT Username FROM SecurAdm WHERE AdminID = %s",
                                   (admin_result['AdminID'],))
                    sec_result = cursor.fetchone()
                    if sec_result:
                        employee['username'] = sec_result['Username']

            cursor.close()
            return employee

        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Error Fetching Employee Info", str(err))
            return None



    def update_staff_last_active(self, staff_id):
        """Update the LastActiveAt timestamp for a staff member"""
        try:
            cursor = self.conn.cursor()
            now = datetime.now()
            query = "UPDATE Staff SET LastActiveAt = %s WHERE StaffID = %s"
            cursor.execute(query, (now, staff_id))
            self.conn.commit()
            cursor.close()
            print(f"✓ Updated LastActiveAt for StaffID {staff_id} to {now}")
            return True
        except Exception as e:
            print(f"✗ Error updating LastActiveAt: {e}")
            return False

    def log_staff_activity(self, staff_id, activity_type, order_id=None, customer_id=None):
        """
        Log a staff activity to the database

        Activity Types:
        - CREATE_ORDER
        - EDIT_ORDER
        - CREATE_CUSTOMER
        - EDIT_CUSTOMER
        - PICKUP_ORDER
        - DELIVER_ORDER
        - COMPLETE_TRANSACTION
        """
        try:
            cursor = self.conn.cursor()
            query = """
                    INSERT INTO StaffActivityLog
                        (StaffID, ActivityType, OrderID, CustomerID, ActivityTime)
                    VALUES (%s, %s, %s, %s, NOW())
                    """
            cursor.execute(query, (staff_id, activity_type, order_id, customer_id))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"✗ Error logging staff activity: {e}")
            self.conn.rollback()
            return False

    def get_recent_activities(self, limit=10):
        """Get recent staff activities with staff and customer/order details"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                    SELECT sal.ActivityID, \
                           sal.ActivityType, \
                           sal.ActivityTime, \
                           sal.OrderID, \
                           sal.CustomerID, \
                           CONCAT(e.EFName, ' ', e.ELName) as staff_name, \
                           CASE \
                               WHEN sal.CustomerID IS NOT NULL THEN \
                                   CONCAT(c.CFName, ' ', c.CLName) \
                               ELSE NULL \
                               END                         as customer_name
                    FROM StaffActivityLog sal
                             INNER JOIN Staff s ON sal.StaffID = s.StaffID
                             INNER JOIN Employees e ON s.EmployeeID = e.EmployeeID
                             LEFT JOIN Customer c ON sal.CustomerID = c.CustomerID
                    ORDER BY sal.ActivityTime DESC
                        LIMIT %s
                    """
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"✗ Error fetching recent activities: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_staff_activities(self, staff_id, limit=20):
        """Get activities for a specific staff member"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                    SELECT sal.*, \
                           CONCAT(e.EFName, ' ', e.ELName) as staff_name, \
                           CASE \
                               WHEN sal.CustomerID IS NOT NULL THEN \
                                   CONCAT(c.CFName, ' ', c.CLName) \
                               ELSE NULL \
                               END                         as customer_name
                    FROM StaffActivityLog sal
                             INNER JOIN Staff s ON sal.StaffID = s.StaffID
                             INNER JOIN Employees e ON s.EmployeeID = e.EmployeeID
                             LEFT JOIN Customer c ON sal.CustomerID = c.CustomerID
                    WHERE sal.StaffID = %s
                    ORDER BY sal.ActivityTime DESC
                        LIMIT %s
                    """
            cursor.execute(query, (staff_id, limit))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"✗ Error fetching staff activities: {e}")
            return []



        except mysql.connector.Error as err:
            print(f"❌ Database error: {err}")
            QMessageBox.critical(None, "Error Fetching Admin Details", str(err))
            return None

    def get_top_services_this_week(self, limit=3):
        """Get top services used this week by count"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                    SELECT ServiceName, \
                           COUNT(*)         as service_count, \
                           SUM(TotalAmount) as total_revenue
                    FROM OrderService os
                             INNER JOIN Orders o ON os.OrderID = o.OrderID
                    WHERE YEARWEEK(o.OrderDate, 1) = YEARWEEK(CURDATE(), 1)
                    GROUP BY ServiceName
                    ORDER BY service_count DESC
                        LIMIT %s
                    """
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            print(f"✗ Error fetching top services: {err}")
            return []