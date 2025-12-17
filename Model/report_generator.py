"""
Washy Laundry Management System - Enhanced PDF Report Generator
Generates beautiful detailed reports for Staff, Customers, and Orders
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph,
                                 Spacer, PageBreak, Image, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas
from datetime import datetime
import mysql.connector
from typing import Dict, List, Any


class WashyEnhancedReportGenerator:
    """Generate beautiful detailed PDF reports for Washy Laundry System"""

    def __init__(self, db_config: Dict[str, str]):
        """Initialize report generator with database configuration"""
        self.db_config = db_config
        self.conn = None

    def connect_db(self):
        """Establish database connection"""
        try:
            self.conn = mysql.connector.connect(
                host=self.db_config.get('host', 'localhost'),
                user=self.db_config.get('user', 'root'),
                password=self.db_config.get('password', ''),
                database=self.db_config.get('database', 'washy')
            )
            return True
        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")
            return False

    def close_db(self):
        """Close database connection"""
        if self.conn and self.conn.is_connected():
            self.conn.close()

    # ==================== STAFF REPORT ====================

    def get_staff_full_details(self, staff_id: int) -> Dict:
        """Get complete staff details with all metrics"""
        cursor = self.conn.cursor(dictionary=True)

        # Basic staff info
        cursor.execute("""
            SELECT e.*, s.*, sec.Username
            FROM employees e
            INNER JOIN staff s ON e.EmployeeID = s.EmployeeID
            LEFT JOIN securstaff sec ON s.StaffID = sec.StaffID
            WHERE s.StaffID = %s
        """, (staff_id,))
        staff_data = cursor.fetchone()

        if not staff_data:
            return None

        # Orders processed
        cursor.execute("""
            SELECT COUNT(*) as count FROM orders WHERE StaffID = %s
        """, (staff_id,))
        staff_data['orders_processed'] = cursor.fetchone()['count']

        # Customers created by this staff
        cursor.execute("""
            SELECT COUNT(*) as count FROM customer WHERE StaffID = %s
        """, (staff_id,))
        staff_data['customers_created'] = cursor.fetchone()['count']

        # Transactions made
        cursor.execute("""
            SELECT COUNT(*) as count, COALESCE(SUM(AmountPaid), 0) as total
            FROM transactions WHERE StaffID = %s
        """, (staff_id,))
        trans = cursor.fetchone()
        staff_data['transactions_count'] = trans['count']
        staff_data['total_transactions'] = float(trans['total'])

        # Recent activity
        cursor.execute("""
            SELECT ActivityType, ActivityTime, OrderID, CustomerID
            FROM staffactivitylog
            WHERE StaffID = %s
            ORDER BY ActivityTime DESC
            LIMIT 10
        """, (staff_id,))
        staff_data['recent_activities'] = cursor.fetchall()

        cursor.close()
        return staff_data

    def generate_staff_report(self, staff_id: int, filename: str = None):
        """Generate detailed staff performance report"""

        if not self.connect_db():
            print("Failed to connect to database")
            return False

        try:
            staff = self.get_staff_full_details(staff_id)
            if not staff:
                print(f"Staff ID {staff_id} not found")
                return False

            if not filename:
                staff_name = f"{staff['EFName']}_{staff['ELName']}".replace(" ", "_")
                filename = f"Staff_{staff_id}_{staff_name}.pdf"

            doc = SimpleDocTemplate(filename, pagesize=letter,
                                   rightMargin=50, leftMargin=50,
                                   topMargin=50, bottomMargin=30)

            elements = []
            styles = getSampleStyleSheet()

            # Custom styles
            title_style = ParagraphStyle(
                'Title', parent=styles['Heading1'],
                fontSize=28, textColor=colors.HexColor('#3855DB'),
                spaceAfter=8, alignment=TA_CENTER, fontName='Helvetica-Bold'
            )

            section_style = ParagraphStyle(
                'Section', parent=styles['Heading2'],
                fontSize=14, textColor=colors.white,
                backColor=colors.HexColor('#3855DB'),
                spaceAfter=10, spaceBefore=15,
                fontName='Helvetica-Bold', leftIndent=10, rightIndent=10
            )

            # Header with staff name
            full_name = f"{staff['EFName']} {staff.get('EMName', '')} {staff['ELName']}".replace("  ", " ")
            elements.append(Paragraph(full_name, title_style))
            elements.append(Paragraph("Staff Performance Report", styles['Heading3']))
            elements.append(Spacer(1, 0.2*inch))

            # Personal Info Section
            elements.append(Paragraph("Personal Info", section_style))

            personal_data = [
                ['Email:', staff.get('EEmail', 'N/A')],
                ['Phone:', staff.get('EPhone', 'N/A')],
                ['Username:', staff.get('Username', 'N/A')],
                ['Date Applied:', staff['SDateApplied'].strftime('%B %d, %Y') if staff.get('SDateApplied') else 'N/A'],
                ['Last Active:', staff['LastActiveAt'].strftime('%B %d, %Y at %I:%M %p') if staff.get('LastActiveAt') else 'Never']
            ]

            personal_table = Table(personal_data, colWidths=[2*inch, 4*inch])
            personal_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(personal_table)
            elements.append(Spacer(1, 0.2*inch))

            # Performance Metrics Section
            elements.append(Paragraph("Performance Metrics", section_style))

            metrics_data = [
                ['Orders Processed:', str(staff.get('orders_processed', 0))],
                ['Customers Created:', str(staff.get('customers_created', 0))],
                ['Transactions Made:', str(staff.get('transactions_count', 0))],
                ['Total Revenue Handled:', f"PHP {staff.get('total_transactions', 0):,.2f}"]
            ]

            metrics_table = Table(metrics_data, colWidths=[2.5*inch, 3.5*inch])
            metrics_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#3855DB')),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(metrics_table)
            elements.append(Spacer(1, 0.2*inch))

            # Recent Activity Section
            elements.append(Paragraph("Recent Activity", section_style))

            if staff.get('recent_activities'):
                activity_data = [['Time', 'Action', 'Order/Customer']]

                for activity in staff['recent_activities'][:10]:
                    time_str = activity['ActivityTime'].strftime('%b %d, %I:%M %p')
                    action = activity['ActivityType'].replace('_', ' ').title()

                    detail = ''
                    if activity.get('OrderID'):
                        detail = f"Order #{activity['OrderID']}"
                    elif activity.get('CustomerID'):
                        detail = f"Customer #{activity['CustomerID']}"

                    activity_data.append([time_str, action, detail])

                activity_table = Table(activity_data, colWidths=[1.8*inch, 2.5*inch, 1.7*inch])
                activity_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8EAF6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#3855DB')),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
                ]))
                elements.append(activity_table)
            else:
                elements.append(Paragraph("No recent activity.", styles['Normal']))

            # Footer
            elements.append(Spacer(1, 0.3*inch))
            footer_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
            elements.append(Paragraph(footer_text, styles['Normal']))

            doc.build(elements)
            print(f"✅ Staff report generated: {filename}")
            return True

        except Exception as e:
            print(f"❌ Error generating staff report: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.close_db()

    # ==================== CUSTOMER REPORT ====================

    def get_customer_full_details(self, customer_id: int) -> Dict:
        """Get complete customer details with order history"""
        cursor = self.conn.cursor(dictionary=True)

        # Basic customer info
        cursor.execute("""
            SELECT * FROM customer WHERE CustomerID = %s
        """, (customer_id,))
        customer_data = cursor.fetchone()

        if not customer_data:
            return None

        # Order statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_orders,
                SUM(CASE WHEN Status='Completed' THEN 1 ELSE 0 END) as completed_orders,
                SUM(CASE WHEN Status='Pending' THEN 1 ELSE 0 END) as pending_orders,
                SUM(CASE WHEN Status='Processing' THEN 1 ELSE 0 END) as processing_orders,
                COALESCE(SUM(CASE WHEN Status='Completed' THEN TotalAmount ELSE 0 END), 0) as total_spent,
                MAX(OrderDate) as last_order_date
            FROM orders WHERE CustomerID = %s
        """, (customer_id,))
        stats = cursor.fetchone()
        customer_data.update(stats)

        # Get addresses
        cursor.execute("""
            SELECT * FROM address WHERE CustomerID = %s
        """, (customer_id,))
        customer_data['addresses'] = cursor.fetchall()

        # Get all orders
        cursor.execute("""
            SELECT o.*, CONCAT(e.EFName, ' ', e.ELName) as staff_name
            FROM orders o
            LEFT JOIN staff s ON o.StaffID = s.StaffID
            LEFT JOIN employees e ON s.EmployeeID = e.EmployeeID
            WHERE o.CustomerID = %s
            ORDER BY o.OrderDate DESC
        """, (customer_id,))
        customer_data['orders'] = cursor.fetchall()

        cursor.close()
        return customer_data

    def generate_customer_report(self, customer_id: int, filename: str = None):
        """Generate detailed customer report"""

        if not self.connect_db():
            print("Failed to connect to database")
            return False

        try:
            customer = self.get_customer_full_details(customer_id)
            if not customer:
                print(f"Customer ID {customer_id} not found")
                return False

            if not filename:
                customer_name = f"{customer['CFName']}_{customer['CLName']}".replace(" ", "_")
                filename = f"Customer_{customer_id}_{customer_name}.pdf"

            doc = SimpleDocTemplate(filename, pagesize=letter,
                                   rightMargin=50, leftMargin=50,
                                   topMargin=50, bottomMargin=30)

            elements = []
            styles = getSampleStyleSheet()

            # Styles
            title_style = ParagraphStyle(
                'Title', parent=styles['Heading1'],
                fontSize=28, textColor=colors.HexColor('#3855DB'),
                spaceAfter=8, alignment=TA_CENTER, fontName='Helvetica-Bold'
            )

            section_style = ParagraphStyle(
                'Section', parent=styles['Heading2'],
                fontSize=14, textColor=colors.white,
                backColor=colors.HexColor('#3855DB'),
                spaceAfter=10, spaceBefore=15,
                fontName='Helvetica-Bold', leftIndent=10, rightIndent=10
            )

            # Header
            full_name = f"{customer['CFName']} {customer.get('CMName', '')} {customer['CLName']}".replace("  ", " ")
            elements.append(Paragraph(full_name, title_style))
            elements.append(Paragraph("Customer Profile Report", styles['Heading3']))
            elements.append(Spacer(1, 0.2*inch))

            # Personal Info
            elements.append(Paragraph("Personal Info", section_style))

            personal_data = [
                ['Email:', customer.get('CEmail', 'N/A')],
                ['Phone:', customer.get('CPhone', 'N/A')],
                ['Member Since:', customer['DateCreated'].strftime('%B %d, %Y') if customer.get('DateCreated') else 'N/A'],
            ]

            personal_table = Table(personal_data, colWidths=[2*inch, 4*inch])
            personal_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(personal_table)
            elements.append(Spacer(1, 0.15*inch))

            # Addresses
            if customer.get('addresses'):
                elements.append(Paragraph("Addresses:", ParagraphStyle(
                    'AddressHeader', parent=styles['Normal'],
                    fontSize=11, fontName='Helvetica-Bold',
                    textColor=colors.HexColor('#666666')
                )))

                for addr in customer['addresses']:
                    addr_parts = [addr.get('StreetAdd', ''), addr.get('AppartUnit', ''),
                                 addr.get('City', ''), addr.get('ZipCode', '')]
                    addr_str = ', '.join([str(p) for p in addr_parts if p])
                    elements.append(Paragraph(f"• {addr_str}", styles['Normal']))

                elements.append(Spacer(1, 0.15*inch))

            # Order Statistics
            elements.append(Paragraph("Order Statistics", section_style))

            stats_data = [
                ['Total Orders:', str(customer.get('total_orders', 0))],
                ['Completed:', str(customer.get('completed_orders', 0))],
                ['Pending:', str(customer.get('pending_orders', 0))],
                ['Processing:', str(customer.get('processing_orders', 0))],
                ['Total Spent:', f"PHP {float(customer.get('total_spent', 0)):,.2f}"],
                ['Last Order:', customer['last_order_date'].strftime('%B %d, %Y') if customer.get('last_order_date') else 'No orders yet']
            ]

            stats_table = Table(stats_data, colWidths=[2*inch, 4*inch])
            stats_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#3855DB')),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(stats_table)
            elements.append(Spacer(1, 0.2*inch))

            # Order History
            elements.append(Paragraph("Order History", section_style))

            if customer.get('orders'):
                order_data = [['Order ID', 'Date', 'Amount', 'Status', 'Staff']]

                for order in customer['orders']:
                    order_id = f"WSHY#{order['OrderID']:03d}"
                    date = order['OrderDate'].strftime('%b %d, %Y') if order.get('OrderDate') else 'N/A'
                    amount = f"PHP {order['TotalAmount']:,.2f}"
                    status = order['Status']
                    staff = order.get('staff_name', 'N/A')[:15]

                    order_data.append([order_id, date, amount, status, staff])

                order_table = Table(order_data, colWidths=[1*inch, 1.3*inch, 1.3*inch, 1.2*inch, 1.2*inch])
                order_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8EAF6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#3855DB')),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
                ]))
                elements.append(order_table)
            else:
                elements.append(Paragraph("No orders yet.", styles['Normal']))

            # Footer
            elements.append(Spacer(1, 0.3*inch))
            footer_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
            elements.append(Paragraph(footer_text, styles['Normal']))

            doc.build(elements)
            print(f"✅ Customer report generated: {filename}")
            return True

        except Exception as e:
            print(f"❌ Error generating customer report: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.close_db()

    # ==================== ORDER REPORT ====================

    def get_order_full_details(self, order_id: int) -> Dict:
        """Get complete order details with services"""
        cursor = self.conn.cursor(dictionary=True)

        # Basic order info
        cursor.execute("""
            SELECT o.*,
                   CONCAT(c.CFName, ' ', COALESCE(c.CMName, ''), ' ', c.CLName) as customer_name,
                   c.CPhone, c.CEmail,
                   CONCAT(e.EFName, ' ', e.ELName) as staff_name
            FROM orders o
            LEFT JOIN customer c ON o.CustomerID = c.CustomerID
            LEFT JOIN staff s ON o.StaffID = s.StaffID
            LEFT JOIN employees e ON s.EmployeeID = e.EmployeeID
            WHERE o.OrderID = %s
        """, (order_id,))
        order_data = cursor.fetchone()

        if not order_data:
            return None

        # Get services
        cursor.execute("""
            SELECT * FROM orderservice WHERE OrderID = %s
        """, (order_id,))
        order_data['services'] = cursor.fetchall()

        # Get transactions
        cursor.execute("""
            SELECT * FROM transactions WHERE OrderID = %s
        """, (order_id,))
        order_data['transactions'] = cursor.fetchall()

        # Get customer address
        cursor.execute("""
            SELECT * FROM address WHERE CustomerID = %s LIMIT 1
        """, (order_data['CustomerID'],))
        order_data['address'] = cursor.fetchone()

        cursor.close()
        return order_data

    def generate_order_report(self, order_id: int, filename: str = None):
        """Generate detailed order report"""

        if not self.connect_db():
            print("Failed to connect to database")
            return False

        try:
            order = self.get_order_full_details(order_id)
            if not order:
                print(f"Order ID {order_id} not found")
                return False

            if not filename:
                filename = f"Order_WSHY{order_id:03d}.pdf"

            doc = SimpleDocTemplate(filename, pagesize=letter,
                                   rightMargin=50, leftMargin=50,
                                   topMargin=50, bottomMargin=30)

            elements = []
            styles = getSampleStyleSheet()

            # Styles
            title_style = ParagraphStyle(
                'Title', parent=styles['Heading1'],
                fontSize=28, textColor=colors.HexColor('#3855DB'),
                spaceAfter=8, alignment=TA_CENTER, fontName='Helvetica-Bold'
            )

            section_style = ParagraphStyle(
                'Section', parent=styles['Heading2'],
                fontSize=14, textColor=colors.white,
                backColor=colors.HexColor('#3855DB'),
                spaceAfter=10, spaceBefore=15,
                fontName='Helvetica-Bold', leftIndent=10, rightIndent=10
            )

            # Header
            order_code = f"WSHY#{order['OrderID']:03d}"
            elements.append(Paragraph(f"Order Details {order_code}", title_style))
            elements.append(Spacer(1, 0.2*inch))

            # Order Info Section
            elements.append(Paragraph("Order Info", section_style))

            # Status badge color
            status = order['Status']
            status_color = {
                'Completed': colors.green,
                'Pending': colors.orange,
                'Processing': colors.blue,
                'Cancelled': colors.red
            }.get(status, colors.grey)

            order_info_data = [
                ['Payment Method:', order['transactions'][0]['PaymentMethod'] if order.get('transactions') else 'Not paid'],
                ['Status:', status],
                ['Order Created:', order['OrderDate'].strftime('%B %d, %Y at %I:%M %p') if order.get('OrderDate') else 'N/A'],
            ]

            order_info_table = Table(order_info_data, colWidths=[2*inch, 4*inch])
            order_info_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
                ('TEXTCOLOR', (1, 1), (1, 1), status_color),
                ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(order_info_table)
            elements.append(Spacer(1, 0.2*inch))

            # Process Info
            elements.append(Paragraph("Process Info", section_style))

            process_data = [
                ['Ordered By:', order.get('customer_name', 'Unknown')],
                ['Processed By:', order.get('staff_name', 'N/A')],
                ['Date Picked up:', order['DatePicked'].strftime('%B %d, %Y at %I:%M %p') if order.get('DatePicked') else 'Not picked up yet'],
                ['Date Delivered:', order['DateDelivered'].strftime('%B %d, %Y at %I:%M %p') if order.get('DateDelivered') else 'Not delivered yet'],
            ]

            if order.get('address'):
                addr = order['address']
                addr_parts = [addr.get('StreetAdd', ''), addr.get('City', ''), addr.get('ZipCode', '')]
                addr_str = ', '.join([str(p) for p in addr_parts if p])
                process_data.append(['Address:', addr_str])

            process_table = Table(process_data, colWidths=[2*inch, 4*inch])
            process_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(process_table)
            elements.append(Spacer(1, 0.2*inch))

            # Order Items
            elements.append(Paragraph("Order Items", section_style))

            if order.get('services'):
                items_data = [['Service', 'Weight', 'Price/kg', 'Amount']]

                total_wash = 0
                total_fast_dry = 0
                total_iron = 0
                total_fold = 0

                for service in order['services']:
                    weight = float(service['WeightKg'])
                    price_per_kg = float(service['PriceperKG'])

                    # WASH - Always show
                    wash_amount = float(service['WashAmount'])
                    total_wash += wash_amount
                    items_data.append([
                        'Wash',
                        f"{weight} kg",
                        f"PHP {price_per_kg:,.2f}/kg",
                        f"PHP {wash_amount:,.2f}"
                    ])

                    # FAST DRY - Always show (even if 0)
                    fast_dry_amount = float(service['FastDryAmount'])
                    total_fast_dry += fast_dry_amount
                    items_data.append([
                        'Fast Dry',
                        f"{weight} kg" if service['FastDry'] else 'Not selected',
                        'PHP 140.00/kg',
                        f"PHP {fast_dry_amount:,.2f}"
                    ])

                    # IRON ONLY - Always show (even if 0)
                    iron_amount = float(service['IronOnlyAmount'])
                    total_iron += iron_amount
                    items_data.append([
                        'Iron Only',
                        f"{weight} kg" if service['IronOnly'] else 'Not selected',
                        'PHP 50.00/kg',
                        f"PHP {iron_amount:,.2f}"
                    ])

                    # FOLD - Always show (even if 0)
                    fold_amount = float(service['FoldAmount'])
                    total_fold += fold_amount
                    items_data.append([
                        'Fold',
                        f"{weight} kg" if service['Fold'] else 'Not selected',
                        'PHP 30.00/kg',
                        f"PHP {fold_amount:,.2f}"
                    ])

                items_table = Table(items_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
                items_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8EAF6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#3855DB')),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ALIGN', (0, 0), (1, -1), 'LEFT'),
                    ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
                ]))
                elements.append(items_table)
                elements.append(Spacer(1, 0.2*inch))

                # Summary
                elements.append(Paragraph("Summary", section_style))

                total_addons = total_fast_dry + total_iron + total_fold

                summary_data = [
                    ['Wash:', f"PHP {total_wash:,.2f}"],
                    ['Fast Dry:', f"PHP {total_fast_dry:,.2f}"],
                    ['Iron Only:', f"PHP {total_iron:,.2f}"],
                    ['Fold:', f"PHP {total_fold:,.2f}"],
                    ['Total Add-ons:', f"PHP {total_addons:,.2f}"],
                ]

                summary_table = Table(summary_data, colWidths=[4*inch, 2*inch])
                summary_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(summary_table)

                # Grand Total
                grand_total_data = [['Grand Total:', f"PHP {float(order['TotalAmount']):,.2f}"]]
                grand_total_table = Table(grand_total_data, colWidths=[4*inch, 2*inch])
                grand_total_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#3855DB')),
                    ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#3855DB')),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 12),
                ]))
                elements.append(grand_total_table)
            else:
                elements.append(Paragraph("No services found.", styles['Normal']))

            # Footer
            elements.append(Spacer(1, 0.3*inch))
            footer_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
            elements.append(Paragraph(footer_text, styles['Normal']))

            doc.build(elements)
            print(f"✅ Order report generated: {filename}")
            return True

        except Exception as e:
            print(f"❌ Error generating order report: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.close_db()

    # ==================== DASHBOARD REPORT ====================

    def generate_dashboard_report(self, filename: str = "washy_dashboard_report.pdf"):
        """Generate comprehensive dashboard summary report"""

        if not self.connect_db():
            print("Failed to connect to database")
            return False

        try:
            doc = SimpleDocTemplate(filename, pagesize=letter,
                                   rightMargin=50, leftMargin=50,
                                   topMargin=50, bottomMargin=30)

            elements = []
            styles = getSampleStyleSheet()

            title_style = ParagraphStyle(
                'Title', parent=styles['Heading1'],
                fontSize=24, textColor=colors.HexColor('#3855DB'),
                spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica-Bold'
            )

            section_style = ParagraphStyle(
                'Section', parent=styles['Heading2'],
                fontSize=14, textColor=colors.white,
                backColor=colors.HexColor('#3855DB'),
                spaceAfter=10, spaceBefore=15,
                fontName='Helvetica-Bold', leftIndent=10, rightIndent=10
            )

            # Title
            elements.append(Paragraph("WASHY LAUNDRY MANAGEMENT SYSTEM", title_style))
            elements.append(Paragraph("Operational Dashboard Report", styles['Heading3']))
            elements.append(Paragraph(
                f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
                styles['Normal']
            ))
            elements.append(Spacer(1, 0.3*inch))

            # Dashboard Statistics
            cursor = self.conn.cursor(dictionary=True)

            # Staff stats
            cursor.execute("SELECT COUNT(*) as total FROM staff")
            total_staff = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as active FROM staff WHERE LastActiveAt IS NOT NULL")
            active_staff = cursor.fetchone()['active']

            # Order stats
            cursor.execute("SELECT COUNT(*) as total FROM orders")
            total_orders = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE Status='Completed'")
            completed_orders = cursor.fetchone()['count']

            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE Status='Pending'")
            pending_orders = cursor.fetchone()['count']

            cursor.execute("SELECT COALESCE(SUM(TotalAmount), 0) as revenue FROM orders WHERE Status='Completed'")
            total_revenue = float(cursor.fetchone()['revenue'])

            cursor.execute("SELECT COUNT(*) as total FROM customer")
            total_customers = cursor.fetchone()['total']

            elements.append(Paragraph("Dashboard Statistics", section_style))

            stats_data = [
                ['Metric', 'Value'],
                ['Total Staff', str(total_staff)],
                ['Active Staff', str(active_staff)],
                ['Total Orders', str(total_orders)],
                ['Completed Orders', str(completed_orders)],
                ['Pending Orders', str(pending_orders)],
                ['Total Revenue', f"PHP {total_revenue:,.2f}"],
                ['Total Customers', str(total_customers)]
            ]

            stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3855DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
            ]))
            elements.append(stats_table)

            cursor.close()
            doc.build(elements)
            print(f"✅ Dashboard report generated: {filename}")
            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.close_db()


# ===== EXAMPLE USAGE =====
if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'washy'
    }

    report_gen = WashyEnhancedReportGenerator(db_config)

    print("=== Washy Report Generator ===\n")
    print("1. Generate Staff Report")
    print("2. Generate Customer Report")
    print("3. Generate Order Report")
    print("4. Generate Dashboard Report")
    print("\nChoose option (1-4): ", end='')

    choice = input()

    if choice == '1':
        staff_id = int(input("Enter Staff ID: "))
        report_gen.generate_staff_report(staff_id)
    elif choice == '2':
        customer_id = int(input("Enter Customer ID: "))
        report_gen.generate_customer_report(customer_id)
    elif choice == '3':
        order_id = int(input("Enter Order ID: "))
        report_gen.generate_order_report(order_id)
    elif choice == '4':
        report_gen.generate_dashboard_report()
    else:
        print("Invalid choice")