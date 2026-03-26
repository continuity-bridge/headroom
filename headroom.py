#!/usr/bin/env python3
"""
headroom - System tray Claude usage monitor (GTK3 version)

Shows real-time Claude usage limits in your system tray.
Part of the Continuity Bridge ecosystem.

Author: Uncle Tallest & Vector
Created: 2026-03-25
GTK3 Port: 2026-03-26
"""

import os
import sys
import json
import signal
from pathlib import Path
from datetime import datetime, timedelta

import gi
import warnings
import os

# Suppress GLib deprecation warnings from libayatana-appindicator
os.environ['PYTHONWARNINGS'] = 'ignore'
warnings.filterwarnings('ignore')

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk, Gio

# Suppress GLib warnings about deprecated libraries
import logging
logging.getLogger('libayatana-appindicator').setLevel(logging.CRITICAL)

# Try to import AppIndicator for system tray
# Try AyatanaAppIndicator first (modern), then AppIndicator3 (legacy)
HAS_APPINDICATOR = False
APPINDICATOR_LIBRARY = None
APPINDICATOR_ERROR = None
try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator
    HAS_APPINDICATOR = True
    APPINDICATOR_LIBRARY = 'AyatanaAppIndicator3'
except (ValueError, ImportError) as e:
    APPINDICATOR_ERROR = f"Ayatana: {e}"
    try:
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import AppIndicator3 as AppIndicator
        HAS_APPINDICATOR = True
        APPINDICATOR_LIBRARY = 'AppIndicator3'
    except (ValueError, ImportError) as e2:
        HAS_APPINDICATOR = False
        APPINDICATOR_LIBRARY = None
        APPINDICATOR_ERROR = f"Ayatana: {e}, AppIndicator3: {e2}"


def detect_instance_home():
    """Detect INSTANCE_HOME directory"""
    # Try INSTANCE_HOME first (new), fall back to CLAUDE_HOME (old)
    if env_home := os.getenv('INSTANCE_HOME'):
        return Path(env_home)
    if env_home := os.getenv('CLAUDE_HOME'):
        return Path(env_home)
    
    # Default to ~/.claude if no environment variable
    return Path.home() / '.claude'


class UsageData:
    """Parse and calculate usage from state file"""
    
    def __init__(self, state_file: Path):
        self.state_file = state_file
    
    def load(self):
        """Load current usage status"""
        if not self.state_file.exists():
            return None
        
        try:
            with open(self.state_file) as f:
                state = json.load(f)
        except Exception:
            return None
        
        # Plan limits
        limits = {
            'pro': 45,
            'max_5x': 225,
            'max_20x': 900
        }
        
        plan = state.get('plan', 'pro')
        window_hours = state.get('window_hours', 5)
        limit = limits.get(plan, 45)
        
        # Filter events in current window
        cutoff = datetime.now() - timedelta(hours=window_hours)
        events = []
        
        for event in state.get('events', []):
            event_time = datetime.fromisoformat(event['timestamp'])
            if event_time >= cutoff:
                events.append(event)
        
        # Calculate usage
        total_weight = sum(e['weight'] for e in events)
        
        # Breakdown by product
        by_product = {}
        for product in ['chat', 'code', 'cowork']:
            product_events = [e for e in events if e['product'] == product]
            by_product[product] = {
                'count': len(product_events),
                'weight': sum(e['weight'] for e in product_events)
            }
        
        # Next reset
        if events:
            oldest = min(datetime.fromisoformat(e['timestamp']) for e in events)
            next_reset = oldest + timedelta(hours=window_hours)
            time_to_reset = next_reset - datetime.now()
        else:
            time_to_reset = timedelta(0)
        
        remaining = max(0, limit - total_weight)
        percent = (total_weight / limit) * 100 if limit > 0 else 0
        
        # Get weekly usage and session reset if available
        weekly_usage = state.get('weekly_usage')
        session_reset = state.get('session_reset')
        
        return {
            'plan': plan,
            'limit': limit,
            'used': total_weight,
            'remaining': remaining,
            'percent': percent,
            'by_product': by_product,
            'time_to_reset': {
                'hours': int(time_to_reset.total_seconds() // 3600),
                'minutes': int((time_to_reset.total_seconds() % 3600) // 60)
            },
            'event_count': len(events),
            'color': self._get_color(percent),
            'weekly_usage': weekly_usage,
            'session_reset': session_reset
        }
    
    @staticmethod
    def _get_color(percent):
        """Get status color based on percentage"""
        if percent >= 95:
            return 'red'
        elif percent >= 90:
            return 'orange'
        elif percent >= 80:
            return 'yellow'
        else:
            return 'green'


class HeadroomWindow(Gtk.ApplicationWindow):
    """Popup window showing detailed usage"""
    
    def __init__(self, app, usage_data):
        super().__init__(application=app)
        self.usage_data = usage_data
        
        self.set_title("Claude Usage - headroom")
        self.set_default_size(400, 300)
        self.set_resizable(False)
        self.set_keep_above(True)  # Keep window on top
        
        # Build UI
        self.build_ui()
        
        # Update timer
        GLib.timeout_add_seconds(5, self.update_display)
    
    def build_ui(self):
        """Build the window UI"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        
        # Header
        header = Gtk.Label()
        header.set_markup("<span size='large' weight='bold'>Claude Usage Monitor</span>")
        box.pack_start(header, False, False, 0)
        
        # Usage bar and percentage
        self.percent_label = Gtk.Label()
        box.pack_start(self.percent_label, False, False, 0)
        
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_show_text(False)
        box.pack_start(self.progress_bar, False, False, 0)
        
        # Breakdown
        breakdown_label = Gtk.Label()
        breakdown_label.set_markup("<span weight='bold'>Breakdown:</span>")
        breakdown_label.set_xalign(0)
        box.pack_start(breakdown_label, False, False, 0)
        
        self.breakdown_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.pack_start(self.breakdown_box, False, False, 0)
        
        # Reset time
        self.reset_label = Gtk.Label()
        self.reset_label.set_xalign(0)
        box.pack_start(self.reset_label, False, False, 0)
        
        # Weekly usage
        self.weekly_label = Gtk.Label()
        self.weekly_label.set_xalign(0)
        box.pack_start(self.weekly_label, False, False, 0)
        
        # Status message
        self.status_label = Gtk.Label()
        self.status_label.set_line_wrap(True)
        self.status_label.set_xalign(0)
        box.pack_start(self.status_label, False, False, 0)
        
        self.add(box)
        self.update_display()
    
    def update_display(self):
        """Update all display elements"""
        status = self.usage_data.load()
        
        if not status:
            self.percent_label.set_text("No usage data available")
            return True
        
        # Update percentage and bar
        self.percent_label.set_markup(
            f"<span size='x-large'>{status['used']:.1f}/{status['limit']} units "
            f"({status['percent']:.0f}%)</span>"
        )
        
        self.progress_bar.set_fraction(status['percent'] / 100)
        
        # Color-code the progress bar with inline CSS
        style_context = self.progress_bar.get_style_context()
        css_provider = Gtk.CssProvider()
        
        if status['color'] == 'red':
            css_data = b"progressbar progress { background-color: #e74c3c; }"
        elif status['color'] == 'orange':
            css_data = b"progressbar progress { background-color: #e67e22; }"
        elif status['color'] == 'yellow':
            css_data = b"progressbar progress { background-color: #f39c12; }"
        else:
            css_data = b"progressbar progress { background-color: #27ae60; }"
        
        css_provider.load_from_data(css_data)
        style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        # Update breakdown - clear old labels
        for child in self.breakdown_box.get_children():
            self.breakdown_box.remove(child)
        
        # Add new breakdown
        for product in ['chat', 'code', 'cowork']:
            data = status['by_product'][product]
            if data['count'] > 0:
                label = Gtk.Label()
                label.set_markup(
                    f"  <tt>{product.capitalize():8}</tt> {data['count']:3} events  "
                    f"({data['weight']:.1f} units)"
                )
                label.set_xalign(0)
                self.breakdown_box.pack_start(label, False, False, 0)
                label.show()
        
        # Update reset time
        if status.get('session_reset'):
            # Use actual reset time from Claude Desktop
            self.reset_label.set_markup(
                f"<b>Session resets in:</b> {status['session_reset']}"
            )
        else:
            # Fall back to calculated time
            reset = status['time_to_reset']
            self.reset_label.set_markup(
                f"<b>Next reset:</b> {reset['hours']}h {reset['minutes']}m"
            )
        
        # Update weekly usage if available
        if status.get('weekly_usage'):
            weekly = status['weekly_usage']
            usage_text = f"<b>Weekly usage:</b> {weekly['percent']}%"
            if weekly.get('reset_time'):
                usage_text += f" (resets {weekly['reset_time']})"
            self.weekly_label.set_markup(usage_text)
        else:
            self.weekly_label.set_text("")
        
        # Update status message
        if status['percent'] >= 95:
            self.status_label.set_markup(
                "<span foreground='red' weight='bold'>⚠ CRITICAL: Near usage limit!</span>"
            )
        elif status['percent'] >= 90:
            self.status_label.set_markup(
                "<span foreground='orange' weight='bold'>⚠ WARNING: Usage high</span>"
            )
        elif status['percent'] >= 80:
            self.status_label.set_markup(
                "<span foreground='#CCCC00'>ℹ Usage elevated - monitor carefully</span>"
            )
        else:
            self.status_label.set_text("")
        
        return True


class HeadroomApp(Gtk.Application):
    """Main application"""
    
    def __init__(self):
        super().__init__(application_id='com.continuitybridge.headroom')
        
        # Detect INSTANCE_HOME (or use default ~/.claude)
        self.instance_home = detect_instance_home()
        
        self.state_file = self.instance_home / '.claude' / 'logs' / 'limit-tracker-state.json'
        self.usage_data = UsageData(self.state_file)
        
        self.window = None
        self.indicator = None
        self.last_notified_level = None  # Track last notification to avoid spam
    
    def do_activate(self):
        """Application activation"""
        if not self.window:
            self.window = HeadroomWindow(self, self.usage_data)
        
        # Create system tray indicator
        if HAS_APPINDICATOR and not self.indicator:
            print(f"✓ Using {APPINDICATOR_LIBRARY} for system tray")
            self.setup_indicator()
        elif not HAS_APPINDICATOR:
            print("Note: System tray not available on this desktop environment.")
            print(f"Debug: {APPINDICATOR_ERROR}")
            print("Running in window-only mode. Keep this window open to monitor usage.")
        
        # Show window on first activation
        self.window.show_all()
        
        # Update indicator regularly
        GLib.timeout_add_seconds(5, self.update_indicator)
    
    def setup_indicator(self):
        """Setup system tray indicator"""
        # Create indicator
        self.indicator = AppIndicator.Indicator.new(
            "headroom",
            "utilities-system-monitor",
            AppIndicator.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        
        # Create menu
        menu = Gtk.Menu()
        
        # Show window item
        show_item = Gtk.MenuItem(label="Show Usage")
        show_item.connect("activate", self.on_show_window)
        menu.append(show_item)
        
        # Quick Sync item
        sync_item = Gtk.MenuItem(label="Sync Now")
        sync_item.connect("activate", self.on_quick_sync)
        menu.append(sync_item)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Quit item
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.on_quit)
        menu.append(quit_item)
        
        menu.show_all()
        self.indicator.set_menu(menu)
        
        # Set initial label
        self.update_indicator()
    
    def update_indicator(self):
        """Update indicator label and check for notifications"""
        if not self.indicator:
            return True
        
        status = self.usage_data.load()
        if status:
            label = f"{status['percent']:.0f}%"
            self.indicator.set_label(label, "")
            
            # Check if we should send a notification
            self.check_usage_notification(status)
        
        return True
    
    def check_usage_notification(self, status):
        """Send desktop notification at usage thresholds"""
        percent = status['percent']
        
        # Define notification levels
        if percent >= 95 and self.last_notified_level != 95:
            self.send_notification(
                "Claude Usage Critical!",
                f"You've used {percent:.0f}% of your limit. Almost at capacity!",
                Gio.NotificationPriority.URGENT
            )
            self.last_notified_level = 95
        elif percent >= 90 and self.last_notified_level != 90:
            self.send_notification(
                "Claude Usage High",
                f"You've used {percent:.0f}% of your limit. Approaching capacity.",
                Gio.NotificationPriority.HIGH
            )
            self.last_notified_level = 90
        elif percent >= 80 and self.last_notified_level != 80:
            self.send_notification(
                "Claude Usage Warning",
                f"You've used {percent:.0f}% of your limit. Monitor carefully.",
                Gio.NotificationPriority.NORMAL
            )
            self.last_notified_level = 80
        elif percent < 80:
            # Reset notification state when usage drops
            self.last_notified_level = None
    
    def send_notification(self, title, body, priority=Gio.NotificationPriority.NORMAL):
        """Send desktop notification"""
        notification = Gio.Notification.new(title)
        notification.set_body(body)
        notification.set_priority(priority)
        # Fixed: use proper notification ID (avoid recursion)
        super().send_notification(f"usage-alert", notification)
    
    def on_show_window(self, _widget):
        """Show the main window"""
        if self.window:
            self.window.show_all()
    
    def on_quick_sync(self, _widget):
        """Run claude-auto-sync"""
        import subprocess
        
        script_dir = Path(__file__).parent
        auto_sync = script_dir / 'claude-auto-sync'
        
        if auto_sync.exists():
            try:
                # Run sync in background
                subprocess.Popen([str(auto_sync)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Show quick notification using parent class method
                notification = Gio.Notification.new("Syncing Usage")
                notification.set_body("Fetching latest usage from Claude...")
                super().send_notification("sync", notification)
                
                # Update display after a delay
                GLib.timeout_add_seconds(2, self.update_indicator)
            except Exception as e:
                print(f"Sync failed: {e}", file=sys.stderr)
    
    def on_quit(self, _widget):
        """Quit application"""
        self.quit()


def main():
    """Main entry point"""
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    app = HeadroomApp()
    return app.run(sys.argv)


if __name__ == '__main__':
    sys.exit(main())
