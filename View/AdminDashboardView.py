from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt, QTimer
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta


class ADashboard:
    """Admin Dashboard view logic - works with the ADB page in stackedWidget"""

    def __init__(self, main_window, model):
        self.main_window = main_window
        self.model = model

        # Get reference to the dashboard page (ADB) in the stacked widget
        self.dashboard_widget = self.main_window.stackedWidget.widget(
            self.main_window.dashboard_page_index
        )

        self.setup_dashboard_ui()
        self.setup_weekly_orders_graph()
        self.setup_live_order_feed()
        self.load_dashboard_data()

        # Setup auto-refresh timer (refresh every 30 seconds)
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_dashboard_data)
        self.refresh_timer.start(30000)

    def setup_dashboard_ui(self):
        """Setup dashboard UI elements and fonts"""

        # Add "Dashboard" title label with custom font
        font_id = QFontDatabase.addApplicationFont("C:/Users/NITRO/PycharmProjects/Washyy/fonts/Fredoka-SemiBold.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            if hasattr(self.main_window, "title"):
                title = getattr(self.main_window, "title")
                title.setFont(QFont(family, 30))
                title.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup fonts for dashboard buttons
        dashboard_buttons = ["Homebut", "Userbut", "Dashbut", "Orderbut",
                             "Reportbut", "Settbut"]
        for name in dashboard_buttons:
            if hasattr(self.main_window, name):
                btn = getattr(self.main_window, name)
                btn.setFont(QFont("Arial", 15))
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Setup fonts for labels
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            label_names = ["l1", "l2", "ordereview", "liveorder"]
            for label_name in label_names:
                if hasattr(self.main_window, label_name):
                    lab = getattr(self.main_window, label_name)
                    lab.setFont(QFont(family, 13))
                    lab.setFocusPolicy(Qt.FocusPolicy.NoFocus)



    def setup_weekly_orders_graph(self):
        """Setup the weekly orders line graph below Order Review"""
        try:
            # Create a container widget for the graph
            self.graph_widget = QWidget(self.dashboard_widget)
            self.graph_widget.setGeometry(320, 370, 420, 150)

            # Create layout for the graph widget
            layout = QVBoxLayout(self.graph_widget)
            layout.setContentsMargins(0, 0, 0, 0)

            # Create matplotlib figure
            self.figure = Figure(figsize=(5, 2), dpi=80)
            self.figure.patch.set_facecolor('#f0f0f0')
            self.canvas = FigureCanvas(self.figure)

            # Add canvas to layout
            layout.addWidget(self.canvas)

            # Show the widget
            self.graph_widget.show()

            print("✓ Admin: Weekly orders graph widget created")

        except Exception as e:
            print(f"✗ Admin: Error setting up weekly orders graph: {e}")
            import traceback
            traceback.print_exc()

    def setup_live_order_feed(self):
        """Setup the live order feed widget using existing UI labels"""
        try:
            # Use the existing live_feed labels from the UI file
            if hasattr(self.main_window, 'live_feed'):
                self.feed_label_1 = self.main_window.live_feed
                self.feed_label_1.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.feed_label_1.setStyleSheet("color: #333333; font-size: 10px; padding: 5px;")
                self.feed_label_1.setWordWrap(True)

            if hasattr(self.main_window, 'live_feed_2'):
                self.feed_label_2 = self.main_window.live_feed_2
                self.feed_label_2.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.feed_label_2.setStyleSheet("color: #333333; font-size: 10px; padding: 5px;")
                self.feed_label_2.setWordWrap(True)

            if hasattr(self.main_window, 'live_feed_3'):
                self.feed_label_3 = self.main_window.live_feed_3
                self.feed_label_3.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.feed_label_3.setStyleSheet("color: #333333; font-size: 10px; padding: 5px;")
                self.feed_label_3.setWordWrap(True)

            print("✓ Admin: Live order feed widget configured")

        except Exception as e:
            print(f"✗ Admin: Error setting up live order feed: {e}")
            import traceback
            traceback.print_exc()

    def update_live_feed(self):
        """Update the live order feed with recent activities"""
        try:
            # Get recent activities
            activities = self.model.get_recent_activities(limit=3)

            # Update the 3 labels
            labels = [self.feed_label_1, self.feed_label_2, self.feed_label_3]

            for i, label in enumerate(labels):
                if i < len(activities):
                    activity = activities[i]
                    activity_text = self.format_simple_activity(activity)
                    label.setText(activity_text)
                else:
                    label.setText("No activity")

            print(f"✓ Admin: Live feed updated with {len(activities)} activities")

        except Exception as e:
            print(f"✗ Admin: Error updating live feed: {e}")
            import traceback
            traceback.print_exc()

    def format_simple_activity(self, activity):
        """Format activity as simple text"""
        activity_type = self.format_activity_type(activity['ActivityType'])
        details = self.format_activity_details(activity)
        time_str = self.format_time_ago(activity['ActivityTime'])

        if details:
            return f"{activity_type} - {details} ({time_str})"
        return f"{activity_type} ({time_str})"

    def format_activity_type(self, activity_type):
        """Convert activity type to readable format"""
        formats = {
            'CREATE_ORDER': '📋 Order Created',
            'EDIT_ORDER': '✏️ Order Updated',
            'CREATE_CUSTOMER': '👤 New Customer',
            'EDIT_CUSTOMER': '✏️ Customer Updated',
            'PICKUP_ORDER': '📦 Order Picked Up',
            'DELIVER_ORDER': '🚚 Order Delivered',
            'COMPLETE_TRANSACTION': '💰 Payment Received'
        }
        return formats.get(activity_type, activity_type)

    def format_activity_details(self, activity):
        """Format activity details based on type"""
        if activity['OrderID']:
            order_str = f"WSHY#{activity['OrderID']:03d}"
            if activity['customer_name']:
                return f"{order_str} - {activity['customer_name']}"
            return order_str
        elif activity['customer_name']:
            return activity['customer_name']
        return None

    def format_time_ago(self, dt):
        """Format datetime as time ago"""
        if not dt:
            return "Unknown"

        now = datetime.now()
        if isinstance(dt, str):
            try:
                dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            except:
                return "Unknown"

        diff = now - dt

        if diff.days > 0:
            return f"{diff.days}d ago" if diff.days > 1 else "1d ago"

        hours = diff.seconds // 3600
        if hours > 0:
            return f"{hours}h ago" if hours > 1 else "1h ago"

        minutes = diff.seconds // 60
        if minutes > 0:
            return f"{minutes}m ago" if minutes > 1 else "1m ago"

        return "Just now"

    def get_weekly_orders_data(self):
        """Get orders data grouped by week for the last 8 weeks"""
        try:
            all_orders = self.model.get_all_orders()

            if not all_orders:
                print("⚠️ No orders found")
                return pd.DataFrame(columns=['week', 'orders'])

            df = pd.DataFrame(all_orders)
            df['OrderDate'] = pd.to_datetime(df['OrderDate'])

            end_date = datetime.now()
            start_date = end_date - timedelta(weeks=8)
            df = df[df['OrderDate'] >= start_date]

            df['week'] = df['OrderDate'].dt.to_period('W')
            weekly_orders = df.groupby('week').size().reset_index(name='orders')
            weekly_orders['week'] = weekly_orders['week'].astype(str)

            all_weeks = pd.period_range(start=start_date, end=end_date, freq='W')
            full_df = pd.DataFrame({'week': all_weeks.astype(str)})
            full_df = full_df.merge(weekly_orders, on='week', how='left')
            full_df['orders'] = full_df['orders'].fillna(0).astype(int)

            return full_df

        except Exception as e:
            print(f"✗ Admin: Error getting weekly orders data: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame(columns=['week', 'orders'])

    def update_weekly_orders_graph(self):
        """Update the weekly orders line graph"""
        try:
            df = self.get_weekly_orders_data()

            if df.empty:
                print("⚠️ No data to plot")
                return

            self.figure.clear()
            ax = self.figure.add_subplot(111)

            ax.plot(range(len(df)), df['orders'],
                    color='#3855DB', linewidth=2, marker='o',
                    markersize=6, markerfacecolor='#3855DB')

            ax.set_facecolor('#ffffff')
            ax.set_title('Orders Per Week (Last 8 Weeks)',
                         fontsize=12, fontweight='bold', color='#333333', pad=10)
            ax.set_xlabel('Week', fontsize=9, color='#666666')
            ax.set_ylabel('Orders', fontsize=9, color='#666666')

            week_labels = [f"W{i + 1}" for i in range(len(df))]
            ax.set_xticks(range(len(df)))
            ax.set_xticklabels(week_labels, rotation=45, ha='right', fontsize=8)

            ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
            ax.tick_params(axis='y', labelsize=8)

            ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

            for i, value in enumerate(df['orders']):
                ax.text(i, value, str(int(value)),
                        ha='center', va='bottom', fontsize=8, color='#3855DB')

            self.figure.tight_layout()
            self.canvas.draw()

            print(f"✓ Admin: Weekly orders graph updated with {len(df)} weeks of data")

        except Exception as e:
            print(f"✗ Admin: Error updating weekly orders graph: {e}")
            import traceback
            traceback.print_exc()

    def get_order_statistics(self):
        """Get order statistics for the dashboard - SAME AS AdminHomeView"""
        print("🔵 ADMIN DASHBOARD get_order_statistics() CALLED!")
        try:
            if not self.model:
                print("✗ Model not available for statistics")
                return {
                    'completed_today': 0,
                    'pending_issues': 0,
                    'pending_delivery': 0,
                    'pending_pickup': 0
                }

            # Get today's date
            today = datetime.now().strftime("%Y-%m-%d")

            cursor = self.model.conn.cursor(dictionary=True)

            # 1. Get orders completed today
            cursor.execute("""
                           SELECT COUNT(*) as completed_today
                           FROM Orders
                           WHERE DATE(DateDelivered) = %s AND Status = 'Completed'
                           """, (today,))
            result = cursor.fetchone()
            completed_today = result['completed_today'] if result else 0

            # 2. Get pending issues (orders not completed AND not cancelled)
            cursor.execute("""
                           SELECT COUNT(*) as pending_issues
                           FROM Orders
                           WHERE Status NOT IN ('Completed', 'Cancelled')
                           """)
            result = cursor.fetchone()
            pending_issues = result['pending_issues'] if result else 0

            # 3. Get pending delivery orders (exclude cancelled)
            cursor.execute("""
                           SELECT COUNT(*) as pending_delivery
                           FROM Orders
                           WHERE (Status = 'Ready for Delivery' OR Status = 'Processing')
                             AND Status != 'Cancelled'
                           """)
            result = cursor.fetchone()
            pending_delivery = result['pending_delivery'] if result else 0

            # 4. Get pending pickup orders (exclude cancelled)
            cursor.execute("""
                           SELECT COUNT(*) as pending_pickup
                           FROM Orders
                           WHERE Status = 'Pending'
                           """)
            result = cursor.fetchone()
            pending_pickup = result['pending_pickup'] if result else 0

            cursor.close()

            print(f"✓ Dashboard stats: Today={completed_today}, Issues={pending_issues}, "
                  f"Delivery={pending_delivery}, Pickup={pending_pickup}")

            return {
                'completed_today': completed_today,
                'pending_issues': pending_issues,
                'pending_delivery': pending_delivery,
                'pending_pickup': pending_pickup
            }

        except Exception as e:
            import traceback
            print(f"✗ Error getting dashboard order statistics: {e}")
            traceback.print_exc()
            return {
                'completed_today': 0,
                'pending_issues': 0,
                'pending_delivery': 0,
                'pending_pickup': 0
            }

    def load_pending_statistics(self):
        """Load pending pickup and delivery statistics for dashboard"""
        try:
            # Get order statistics using the same method as home view
            stats = self.get_order_statistics()

            if stats:
                # Update pending delivery in dashboard
                if hasattr(self.main_window, "pendingdel_value_2"):  # Pending Delivery in dashboard
                    self.main_window.pendingdel_value_2.setText(str(stats.get('pending_delivery', 0)))
                    print(f"✓ Dashboard updated pending delivery: {stats.get('pending_delivery', 0)}")
                elif hasattr(self.main_window, "pendingdel_value_2"):  # Alternative widget name
                    self.main_window.pendingdel_value_2.setText(str(stats.get('pending_delivery', 0)))
                    print(f"✓ Dashboard updated pending delivery (alt): {stats.get('pending_delivery', 0)}")
                else:
                    print("⚠️ Dashboard: No pending delivery widget found")

                # Update pending pickup in dashboard
                if hasattr(self.main_window, "pendingpick_value_2"):  # Pending Pickup in dashboard
                    self.main_window.pendingpick_value_2.setText(str(stats.get('pending_pickup', 0)))
                    print(f"✓ Dashboard updated pending pickup: {stats.get('pending_pickup', 0)}")
                elif hasattr(self.main_window, "pendingpick_value_2"):  # Alternative widget name
                    self.main_window.pendingpick_value_2.setText(str(stats.get('pending_pickup', 0)))
                    print(f"✓ Dashboard updated pending pickup (alt): {stats.get('pending_pickup', 0)}")
                else:
                    print("⚠️ Dashboard: No pending pickup widget found")

        except Exception as e:
            print(f"✗ Dashboard: Error loading pending statistics: {e}")
            import traceback
            traceback.print_exc()

    def load_dashboard_data(self):
        """Load all dashboard statistics from database"""
        if not self.model:
            print("✗ No database model available")
            return

        try:
            # Get order statistics
            order_stats = self.model.get_order_statistics()
            if order_stats:
                # Update Total Orders This Month
                total_orders = order_stats.get('total_orders', 0)
                if hasattr(self.main_window, 'totalorder_value'):
                    self.main_window.totalorder_value.setText(str(total_orders))
                    self.main_window.totalorder_value.setStyleSheet(
                        "font-size: 24px; font-weight: bold; color: #3855DB;")

                # Update Monthly Revenue
                completed_revenue = self.get_completed_orders_revenue()
                if hasattr(self.main_window, 'monthlyrevenue_value'):
                    revenue_text = f"<span style='font-size:18px; font-weight:bold; color:#3855DB;'>₱{completed_revenue:,.2f}</span>"
                    self.main_window.monthlyrevenue_value.setText(revenue_text)

            # Load pending pickup and deliveries statistics
            self.load_pending_statistics()

            # Update weekly orders graph
            self.update_weekly_orders_graph()

            # Update live feed
            self.update_live_feed()

            print("✓ Admin: Dashboard data loaded successfully with pending statistics")

        except Exception as e:
            print(f"✗ Admin: Error loading dashboard data: {e}")
            import traceback
            traceback.print_exc()

    def get_completed_orders_revenue(self):
        """Get total revenue from completed orders only for current month"""
        try:
            completed_orders = self.model.get_orders_by_status('Completed')

            if not completed_orders:
                print("⚠️ No completed orders found")
                return 0.0

            current_month = datetime.now().month
            current_year = datetime.now().year

            total_revenue = 0.0
            for order in completed_orders:
                try:
                    order_date = order.get('OrderDate')
                    if isinstance(order_date, str):
                        order_date = datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S')
                    elif not isinstance(order_date, datetime):
                        continue

                    if order_date.month == current_month and order_date.year == current_year:
                        total_amount = order.get('TotalAmount', 0)
                        if total_amount:
                            total_revenue += float(total_amount)
                except Exception as e:
                    print(f"⚠️ Error processing order {order.get('OrderID')}: {e}")
                    continue

            print(f"✓ Admin: Total revenue from completed orders: ₱{total_revenue:,.2f}")
            return total_revenue

        except Exception as e:
            print(f"✗ Admin: Error calculating revenue: {e}")
            import traceback
            traceback.print_exc()
            return 0.0

    def refresh_dashboard_data(self):
        """Refresh dashboard data (called by timer)"""
        print("🔄 Admin: Refreshing dashboard data...")
        self.load_dashboard_data()

    def show(self):
        """Show the dashboard page and load data"""
        self.main_window.stackedWidget.setCurrentIndex(
            self.main_window.dashboard_page_index
        )
        self.load_dashboard_data()
        print("✓ Admin: Dashboard shown with pending statistics")