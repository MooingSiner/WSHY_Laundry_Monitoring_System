"""
Washy Laundry Management System - Annual Report Generator
Generates comprehensive PDF reports with executive summary and detailed records
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import mysql.connector
from typing import Dict, List


class WashyAnnualReportGenerator:
    """Generate annual summary reports for Washy Laundry System"""

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

    def get_annual_statistics(self, year: int) -> Dict:
        """Get comprehensive statistics for the year"""
        cursor = self.conn.cursor(dictionary=True)
        stats = {}

        # Total orders for the year
        cursor.execute("""
                       SELECT COUNT(*) as total_orders
                       FROM Orders
                       WHERE YEAR (OrderDate) = %s
                       """, (year,))
        stats['total_orders'] = cursor.fetchone()['total_orders']

        # Orders by status
        cursor.execute("""
                       SELECT SUM(CASE WHEN Status = 'Completed' THEN 1 ELSE 0 END)  as completed,
                              SUM(CASE WHEN Status = 'Pending' THEN 1 ELSE 0 END)    as pending,
                              SUM(CASE WHEN Status = 'Processing' THEN 1 ELSE 0 END) as processing,
                              SUM(CASE WHEN Status = 'Cancelled' THEN 1 ELSE 0 END)  as cancelled
                       FROM Orders
                       WHERE YEAR (OrderDate) = %s
                       """, (year,))
        status_data = cursor.fetchone()
        stats['completed'] = status_data['completed'] or 0
        stats['pending'] = status_data['pending'] or 0
        stats['processing'] = status_data['processing'] or 0
        stats['cancelled'] = status_data['cancelled'] or 0

        # Calculate completion rate
        if stats['total_orders'] > 0:
            stats['completion_rate'] = (stats['completed'] / stats['total_orders']) * 100
        else:
            stats['completion_rate'] = 0

        # Total revenue
        cursor.execute("""
                       SELECT COALESCE(SUM(TotalAmount), 0) as total_revenue
                       FROM Orders
                       WHERE YEAR (OrderDate) = %s AND Status='Completed'
                       """, (year,))
        stats['total_revenue'] = int(cursor.fetchone()['total_revenue'])

        # Total weight processed
        cursor.execute("""
                       SELECT COALESCE(SUM(os.WeightKg), 0) as total_weight
                       FROM OrderService os
                                INNER JOIN Orders o ON os.OrderID = o.OrderID
                       WHERE YEAR (o.OrderDate) = %s AND o.Status='Completed'
                       """, (year,))
        stats['total_weight'] = int(cursor.fetchone()['total_weight'])

        # Busiest staff member
        cursor.execute("""
                       SELECT CONCAT(e.EFName, ' ', e.ELName) as staff_name,
                              COUNT(o.OrderID)                as order_count
                       FROM Orders o
                                INNER JOIN Staff s ON o.StaffID = s.StaffID
                                INNER JOIN Employees e ON s.EmployeeID = e.EmployeeID
                       WHERE YEAR (o.OrderDate) = %s
                       GROUP BY s.StaffID
                       ORDER BY order_count DESC
                           LIMIT 1
                       """, (year,))
        busiest = cursor.fetchone()
        stats['busiest_staff'] = busiest['staff_name'] if busiest else 'N/A'

        # New customers this year
        cursor.execute("""
                       SELECT COUNT(*) as new_customers
                       FROM Customer
                       WHERE YEAR (DateCreated) = %s
                       """, (year,))
        stats['new_customers'] = cursor.fetchone()['new_customers']

        # Average order value
        if stats['completed'] > 0:
            stats['avg_order_value'] = stats['total_revenue'] / stats['completed']
        else:
            stats['avg_order_value'] = 0

        cursor.close()
        return stats

    def get_all_orders_for_year(self, year: int) -> List[Dict]:
        """Get all orders for the specified year"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
                       SELECT o.OrderID,
                              CONCAT(c.CFName, ' ', c.CLName) as customer_name,
                              CONCAT(e.EFName, ' ', e.ELName) as staff_name,
                              o.OrderDate,
                              o.Status,
                              o.TotalAmount,
                              o.DatePicked,
                              o.DateDelivered
                       FROM Orders o
                                LEFT JOIN Customer c ON o.CustomerID = c.CustomerID
                                LEFT JOIN Staff s ON o.StaffID = s.StaffID
                                LEFT JOIN Employees e ON s.EmployeeID = e.EmployeeID
                       WHERE YEAR (o.OrderDate) = %s
                       ORDER BY o.OrderDate DESC
                       """, (year,))
        orders = cursor.fetchall()
        cursor.close()
        return orders

        # ... (previous code remains the same)

    def generate_annual_report(self, year: int, filename: str = None):
        """Generate comprehensive annual report PDF"""

        if not self.connect_db():
            print("Failed to connect to database")
            return False

        try:
            # Get statistics
            stats = self.get_annual_statistics(year)
            orders = self.get_all_orders_for_year(year)

            if not filename:
                filename = f"washy_report_{year}.pdf"

            # Create PDF document
            doc = SimpleDocTemplate(
                filename,
                pagesize=letter,
                rightMargin=50,
                leftMargin=50,
                topMargin=50,
                bottomMargin=30
            )

            elements = []
            styles = getSampleStyleSheet()

            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#3855DB'),
                spaceAfter=6,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )

            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#2746C3'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )

            section_style = ParagraphStyle(
                'SectionHeader',
                parent=styles['Heading2'],
                fontSize=12,
                textColor=colors.HexColor('#3855DB'),
                spaceAfter=12,
                spaceBefore=20,
                fontName='Helvetica-Bold'
            )

            # ============= TITLE PAGE =============
            elements.append(Spacer(1, 1 * inch))
            elements.append(Paragraph(f"WASHY LAUNDRY REPORT - {year}", title_style))
            elements.append(Spacer(1, 0.3 * inch))
            elements.append(Paragraph("EXECUTIVE SUMMARY & INSIGHTS", subtitle_style))
            elements.append(Spacer(1, 0.5 * inch))

            # ============= EXECUTIVE SUMMARY =============
            summary_text = f"""
            In the year {year}, Washy Laundry processed a total of <b>{stats['total_orders']}</b> orders.<br/>
            The operation achieved a <b>{stats['completion_rate']:.1f}%</b> completion rate.<br/>
            """
            elements.append(Paragraph(summary_text, styles['Normal']))
            elements.append(Spacer(1, 0.2 * inch))

            # Key Metrics Box
            elements.append(Paragraph("Key Metrics:", section_style))

            metrics_data = [
                ['Metric', 'Value'],
                ['Completed Orders:', f"{stats['completed']}"],
                ['Pending Orders:', f"{stats['pending']}"],
                ['Processing Orders:', f"{stats['processing']}"],
                ['Cancelled Orders:', f"{stats['cancelled']}"],
                ['Total Revenue:', f"PHP {stats['total_revenue']:,}"],  # Changed to integer format
                ['Average Order Value:', f"PHP {stats['avg_order_value']:,.2f}"],
                ['Total Weight Processed:', f"{stats['total_weight']:,} kg"],  # Changed to integer format
                ['New Customers:', f"{stats['new_customers']}"],
                ['Busiest Staff Member:', f"{stats['busiest_staff']}"]
            ]

            metrics_table = Table(metrics_data, colWidths=[3 * inch, 3 * inch])
            metrics_table.setStyle(TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3855DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

                # Data rows
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#3855DB')),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))
            elements.append(metrics_table)
            elements.append(Spacer(1, 0.3 * inch))

            # Additional insights
            elements.append(Paragraph(
                "This report details individual order records below.",
                styles['Normal']
            ))
            elements.append(Spacer(1, 0.5 * inch))

            # ============= DETAILED ORDERS TABLE =============
            elements.append(PageBreak())
            elements.append(Paragraph("Detailed Order Records", section_style))
            elements.append(Spacer(1, 0.2 * inch))

            # Create orders table
            order_table_data = [['Order ID', 'Customer', 'Staff', 'Date', 'Status', 'Amount']]

            for order in orders:
                order_id = f"WSHY#{order['OrderID']:03d}"
                customer = order['customer_name'] if order['customer_name'] else 'Unknown'
                staff = order['staff_name'] if order['staff_name'] else 'N/A'
                order_date = order['OrderDate'].strftime('%Y-%m-%d') if order['OrderDate'] else 'N/A'
                status = order['Status']
                amount = f"PHP {order['TotalAmount']:,.2f}"

                order_table_data.append([
                    order_id,
                    customer[:20],  # Truncate long names
                    staff[:20],
                    order_date,
                    status,
                    amount
                ])

            # Split into multiple pages if needed
            rows_per_page = 35
            for i in range(0, len(order_table_data), rows_per_page):
                if i > 0:
                    elements.append(PageBreak())

                chunk = order_table_data[i:min(i + rows_per_page, len(order_table_data))]
                if i > 0:
                    # Add header row for continuation pages
                    chunk.insert(0, order_table_data[0])

                orders_table = Table(
                    chunk,
                    colWidths=[0.8 * inch, 1.4 * inch, 1.4 * inch, 1 * inch, 1 * inch, 1 * inch]
                )
                orders_table.setStyle(TableStyle([
                    # Header
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8EAF6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#3855DB')),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

                    # Data
                    ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                    ('ALIGN', (5, 1), (5, -1), 'RIGHT'),  # Amount column
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
                    ('TOPPADDING', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ]))
                elements.append(orders_table)

            # ============= FOOTER =============
            elements.append(Spacer(1, 0.5 * inch))
            footer_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
            elements.append(Paragraph(footer_text, styles['Normal']))

            # Build PDF
            doc.build(elements)
            print(f"✅ Annual report generated: {filename}")
            return True

        except Exception as e:
            print(f"❌ Error generating report: {e}")
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

    report_gen = WashyAnnualReportGenerator(db_config)

    print("=== Washy Annual Report Generator ===\n")
    year = int(input("Enter year for report (e.g., 2025): "))

    report_gen.generate_annual_report(year)