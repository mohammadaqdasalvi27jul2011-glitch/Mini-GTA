#!/usr/bin/env python3
"""
Digital Clock - World Time Zone Display
Shows current time in multiple time zones with a beautiful interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import pytz
from tkinter import font as tkFont
import threading
import time

class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock - World Time Zones")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")
        
        # Time zones data
        self.time_zones = {
            "UTC": "UTC",
            "New York": "America/New_York",
            "Los Angeles": "America/Los_Angeles",
            "London": "Europe/London",
            "Paris": "Europe/Paris",
            "Tokyo": "Asia/Tokyo",
            "Dubai": "Asia/Dubai",
            "Sydney": "Australia/Sydney",
            "Mumbai": "Asia/Kolkata",
            "Singapore": "Asia/Singapore",
            "Hong Kong": "Asia/Hong_Kong",
            "Bangkok": "Asia/Bangkok",
            "Istanbul": "Europe/Istanbul",
            "Moscow": "Europe/Moscow",
            "São Paulo": "America/Sao_Paulo",
            "Mexico City": "America/Mexico_City",
            "Toronto": "America/Toronto",
            "Vancouver": "America/Vancouver",
            "Auckland": "Pacific/Auckland",
            "Fiji": "Pacific/Fiji",
            "Honolulu": "Pacific/Honolulu",
            "Anchorage": "America/Anchorage",
            "Berlin": "Europe/Berlin",
            "Dubai": "Asia/Dubai",
            "Bangkok": "Asia/Bangkok",
        }
        
        self.favorites = ["UTC", "New York", "London", "Tokyo", "Sydney"]
        self.all_zones = list(self.time_zones.keys())
        self.is_24h = True
        
        self.setup_ui()
        self.update_time()
    
    def setup_ui(self):
        """Setup the user interface"""
        
        # Title
        title_font = tkFont.Font(family="Arial", size=24, weight="bold")
        title = tk.Label(
            self.root,
            text="🌍 WORLD DIGITAL CLOCK",
            font=title_font,
            fg="#00d4ff",
            bg="#1a1a2e"
        )
        title.pack(pady=20)
        
        # Settings Frame
        settings_frame = tk.Frame(self.root, bg="#16213e", height=60)
        settings_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Format toggle
        format_font = tkFont.Font(family="Arial", size=10)
        self.format_var = tk.BooleanVar(value=True)
        format_check = tk.Checkbutton(
            settings_frame,
            text="24-Hour Format",
            variable=self.format_var,
            command=self.toggle_format,
            font=format_font,
            bg="#16213e",
            fg="#00d4ff",
            selectcolor="#0f3460"
        )
        format_check.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Search
        search_label = tk.Label(
            settings_frame,
            text="Search Zone:",
            font=format_font,
            bg="#16213e",
            fg="#00d4ff"
        )
        search_label.pack(side=tk.LEFT, padx=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        search_entry = tk.Entry(
            settings_frame,
            textvariable=self.search_var,
            font=format_font,
            width=20,
            bg="#0f3460",
            fg="#00d4ff"
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Main clock display (System time)
        clock_frame = tk.Frame(self.root, bg="#0f3460", height=120)
        clock_frame.pack(fill=tk.X, padx=20, pady=20)
        
        system_label = tk.Label(
            clock_frame,
            text="SYSTEM TIME",
            font=("Arial", 12, "bold"),
            bg="#0f3460",
            fg="#00d4ff"
        )
        system_label.pack(pady=5)
        
        self.system_time_label = tk.Label(
            clock_frame,
            text="00:00:00",
            font=("Digital-7", 60, "bold"),
            bg="#0f3460",
            fg="#00ff00",
            family="monospace"
        )
        self.system_time_label.pack(pady=10)
        
        self.system_date_label = tk.Label(
            clock_frame,
            text="Loading...",
            font=("Arial", 14),
            bg="#0f3460",
            fg="#00d4ff"
        )
        self.system_date_label.pack(pady=5)
        
        # Tabs for Favorites and All Zones
        tab_control = ttk.Notebook(self.root)
        tab_control.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Style for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background="#1a1a2e", borderwidth=0)
        style.configure('TNotebook.Tab', background="#16213e", foreground="#00d4ff", padding=[20, 10])
        style.map('TNotebook.Tab', background=[("selected", "#0f3460")])
        
        # Favorites tab
        favorites_frame = ttk.Frame(tab_control)
        tab_control.add(favorites_frame, text="⭐ Favorites")
        self.favorites_container = tk.Frame(favorites_frame, bg="#1a1a2e")
        self.favorites_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # All zones tab
        all_zones_frame = ttk.Frame(tab_control)
        tab_control.add(all_zones_frame, text="🌐 All Time Zones")
        self.all_zones_container = tk.Frame(all_zones_frame, bg="#1a1a2e")
        self.all_zones_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrollable areas
        self.setup_scrollable_area(self.favorites_container, is_favorites=True)
        self.setup_scrollable_area(self.all_zones_container, is_favorites=False)
    
    def setup_scrollable_area(self, parent, is_favorites=False):
        """Setup scrollable clock area"""
        canvas = tk.Canvas(parent, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        if is_favorites:
            self.favorites_scroll_frame = scrollable_frame
        else:
            self.all_zones_scroll_frame = scrollable_frame
    
    def toggle_format(self):
        """Toggle between 12-hour and 24-hour format"""
        self.is_24h = self.format_var.get()
    
    def on_search_change(self, *args):
        """Handle search input"""
        search_term = self.search_var.get().lower()
        
        # Clear all zones container
        for widget in self.all_zones_scroll_frame.winfo_children():
            widget.destroy()
        
        # Filter zones
        if search_term:
            filtered_zones = [z for z in self.all_zones if search_term in z.lower()]
        else:
            filtered_zones = self.all_zones
        
        # Display filtered zones
        for zone in filtered_zones:
            self.create_clock_widget(self.all_zones_scroll_frame, zone, can_remove=False)
    
    def create_clock_widget(self, parent, zone_name, can_remove=False):
        """Create a clock widget for a time zone"""
        frame = tk.Frame(parent, bg="#16213e", highlightthickness=1, highlightbackground="#0f3460")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Zone name
        name_label = tk.Label(
            frame,
            text=zone_name,
            font=("Arial", 12, "bold"),
            bg="#16213e",
            fg="#00d4ff",
            width=20,
            anchor="w"
        )
        name_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Time display
        time_label = tk.Label(
            frame,
            text="00:00:00",
            font=("Digital-7", 20, "bold"),
            bg="#16213e",
            fg="#00ff00",
            width=15,
            anchor="center",
            family="monospace"
        )
        time_label.pack(side=tk.LEFT, padx=10)
        
        # Date display
        date_label = tk.Label(
            frame,
            text="MMM DD, YYYY",
            font=("Arial", 10),
            bg="#16213e",
            fg="#888888"
        )
        date_label.pack(side=tk.LEFT, padx=10)
        
        # Remove button (for favorites)
        if can_remove:
            remove_btn = tk.Button(
                frame,
                text="✕",
                command=lambda: self.remove_favorite(zone_name),
                bg="#e74c3c",
                fg="white",
                font=("Arial", 10, "bold"),
                width=2,
                border=0
            )
            remove_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Store references for updating
        frame.zone_name = zone_name
        frame.time_label = time_label
        frame.date_label = date_label
        
        return frame
    
    def remove_favorite(self, zone_name):
        """Remove a zone from favorites"""
        if zone_name in self.favorites:
            self.favorites.remove(zone_name)
            self.refresh_favorites()
    
    def add_to_favorites(self, zone_name):
        """Add a zone to favorites"""
        if zone_name not in self.favorites:
            self.favorites.append(zone_name)
            self.refresh_favorites()
    
    def refresh_favorites(self):
        """Refresh the favorites display"""
        for widget in self.favorites_scroll_frame.winfo_children():
            widget.destroy()
        
        for zone in self.favorites:
            if zone in self.time_zones:
                self.create_clock_widget(self.favorites_scroll_frame, zone, can_remove=True)
    
    def format_time(self, dt, is_24h=True):
        """Format time based on 12/24 hour preference"""
        if is_24h:
            return dt.strftime("%H:%M:%S")
        else:
            return dt.strftime("%I:%M:%S %p")
    
    def update_time(self):
        """Update all clock displays"""
        # Update system time
        now = datetime.now()
        self.system_time_label.config(text=self.format_time(now, self.is_24h))
        self.system_date_label.config(text=now.strftime("%A, %B %d, %Y"))
        
        # Update favorites
        for widget in self.favorites_scroll_frame.winfo_children():
            if hasattr(widget, 'zone_name'):
                self.update_zone_time(widget)
        
        # Update all zones (visible ones)
        for widget in self.all_zones_scroll_frame.winfo_children():
            if hasattr(widget, 'zone_name'):
                self.update_zone_time(widget)
        
        # Schedule next update
        self.root.after(1000, self.update_time)
    
    def update_zone_time(self, widget):
        """Update time for a specific zone widget"""
        zone_name = widget.zone_name
        tz = pytz.timezone(self.time_zones[zone_name])
        zone_time = datetime.now(tz)
        
        widget.time_label.config(text=self.format_time(zone_time, self.is_24h))
        widget.date_label.config(text=zone_time.strftime("%b %d, %Y"))


def main():
    print("🕐 Digital Clock - World Time Zones")
    print("=" * 50)
    print("Starting application...")
    
    root = tk.Tk()
    app = DigitalClock(root)
    
    print("✅ Application ready!")
    print("🌍 Showing time zones: UTC, New York, London, Tokyo, Sydney")
    print("=" * 50)
    
    root.mainloop()


if __name__ == "__main__":
    main()
