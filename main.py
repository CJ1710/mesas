#!/usr/bin/env python3
"""
MESAS - Medicine Expiry and Stock Alert System
Main Application File
"""

import os
import sys
import datetime
from modules.auth import AuthSystem
from modules.database import Database
from modules.medicine_manager import MedicineManager
from modules.reports import ReportGenerator

class MESAS:
    def __init__(self):
        self.db = Database()
        self.auth = AuthSystem(self.db)
        self.medicine_manager = MedicineManager(self.db)
        self.report_generator = ReportGenerator(self.db, self.medicine_manager)
        self.running = True
    
    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """Display application header"""
        print("=" * 60)
        print("MEDICINE EXPIRY AND STOCK ALERT SYSTEM (MESAS)")
        print("=" * 60)
        if self.auth.current_user:
            user = self.auth.get_current_user()
            print(f"User: {user['username']} | Role: {user['role']}")
        print()
    
    def main_menu(self):
        """Display main menu"""
        while self.running:
            self.clear_screen()
            self.display_header()
            
            # Check for alerts automatically
            if self.auth.is_authenticated():
                self.medicine_manager.check_expiry_alerts()
                self.medicine_manager.check_stock_alerts()
                all_alerts = self.medicine_manager.get_all_alerts()
                
                if all_alerts:
                    print("⚠️  ACTIVE ALERTS:")
                    for alert in all_alerts[:5]:
                        print(f"  • {alert}")
                    if len(all_alerts) > 5:
                        print(f"  ... and {len(all_alerts) - 5} more alerts")
                    print()
            
            if not self.auth.is_authenticated():
                print("1. Login")
                print("2. Sign Up")
                print("3. Exit")
                print("-" * 40)
                
                choice = input("Enter your choice (1-3): ").strip()
                
                if choice == "1":
                    self.login_menu()
                elif choice == "2":
                    self.signup_menu()
                elif choice == "3":
                    print("\nThank you for using MESAS. Goodbye!")
                    self.running = False
                else:
                    print("\nInvalid choice. Please try again.")
                    input("Press Enter to continue...")
            else:
                print("MAIN MENU:")
                print("1. Medicine Management")
                print("2. View Alerts")
                print("3. Generate Reports")
                print("4. View All Medicines")
                print("5. Search Medicine")
                if self.auth.is_admin():
                    print("6. System Administration")
                print("7. Logout")
                print("8. Exit")
                print("-" * 40)
                
                choice = input("Enter your choice: ").strip()
                
                if choice == "1":
                    self.medicine_management_menu()
                elif choice == "2":
                    self.view_alerts_menu()
                elif choice == "3":
                    self.reports_menu()
                elif choice == "4":
                    self.view_all_medicines()
                elif choice == "5":
                    self.search_medicine_menu()
                elif choice == "6" and self.auth.is_admin():
                    self.admin_menu()
                elif choice == "7":
                    self.auth.logout()
                    print("\nLogged out successfully!")
                    input("Press Enter to continue...")
                elif choice == "8":
                    print("\nThank you for using MESAS. Goodbye!")
                    self.running = False
                else:
                    print("\nInvalid choice. Please try again.")
                    input("Press Enter to continue...")
    
    def login_menu(self):
        """Handle login"""
        self.clear_screen()
        self.display_header()
        print("LOGIN")
        print("-" * 40)
        
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        success, message = self.auth.login(username, password)
        print(f"\n{message}")
        
        if success:
            if len(self.db.get_all_medicines()) == 0:
                self.add_sample_data()
        
        input("\nPress Enter to continue...")
    
    def signup_menu(self):
        """Handle user registration"""
        self.clear_screen()
        self.display_header()
        print("SIGN UP")
        print("-" * 40)
        
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        email = input("Email (optional): ").strip()
        
        success, message = self.auth.signup(username, password, email)
        print(f"\n{message}")
        
        if success:
            print("Please login with your new credentials.")
        
        input("\nPress Enter to continue...")
    
    def add_sample_data(self):
        """Add sample medicine data for new users"""
        sample_medicines = [
            ("Paracetamol", "Tablet", 100, 5.50, "2024-12-31"),
            ("Amoxicillin", "Capsule", 50, 12.75, "2025-06-30"),
            ("Cetirizine", "Tablet", 30, 8.25, "2025-03-15"),
            ("Ibuprofen", "Tablet", 25, 7.80, "2024-11-30"),
            ("Vitamin C", "Tablet", 200, 3.25, "2026-01-31"),
            ("Aspirin", "Tablet", 10, 4.50, "2024-10-15"),
            ("Omeprazole", "Capsule", 40, 15.20, "2025-08-31"),
            ("Metformin", "Tablet", 60, 9.75, "2025-05-31"),
            ("Atorvastatin", "Tablet", 35, 18.50, "2025-09-30"),
            ("Salbutamol", "Inhaler", 15, 45.00, "2025-02-28")
        ]
        
        user_id = self.auth.get_current_user()["id"]
        for name, category, stock, price, expiry in sample_medicines:
            self.medicine_manager.add_medicine(name, category, stock, price, expiry, user_id)
        
        print("\nSample medicine data has been added to your inventory.")
    
    def medicine_management_menu(self):
        """Medicine management submenu"""
        while True:
            self.clear_screen()
            self.display_header()
            print("MEDICINE MANAGEMENT")
            print("-" * 40)
            print("1. Add New Medicine")
            print("2. Update Medicine Stock")
            print("3. Update Medicine Expiry Date")
            print("4. Delete Medicine")
            print("5. Back to Main Menu")
            print("-" * 40)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.add_medicine_menu()
            elif choice == "2":
                self.update_stock_menu()
            elif choice == "3":
                self.update_expiry_menu()
            elif choice == "4":
                self.delete_medicine_menu()
            elif choice == "5":
                break
            else:
                print("\nInvalid choice. Please try again.")
                input("Press Enter to continue...")
    
    def add_medicine_menu(self):
        """Add new medicine"""
        self.clear_screen()
        self.display_header()
        print("ADD NEW MEDICINE")
        print("-" * 40)
        
        name = input("Medicine Name: ").strip()
        category = input("Category (e.g., Tablet, Capsule, Syrup): ").strip()
        
        try:
            stock = int(input("Stock Quantity: ").strip())
            price = float(input("Price per unit: ").strip())
        except ValueError:
            print("\nInvalid input! Stock must be integer and price must be number.")
            input("Press Enter to continue...")
            return
        
        expiry_date = input("Expiry Date (YYYY-MM-DD): ").strip()
        user_id = self.auth.get_current_user()["id"]
        
        success, message = self.medicine_manager.add_medicine(
            name, category, stock, price, expiry_date, user_id
        )
        
        print(f"\n{message}")
        input("\nPress Enter to continue...")
    
    def update_stock_menu(self):
        """Update medicine stock"""
        self.clear_screen()
        self.display_header()
        print("UPDATE MEDICINE STOCK")
        print("-" * 40)
        
        try:
            medicine_id = int(input("Medicine ID to update: ").strip())
            new_stock = int(input("New Stock Quantity: ").strip())
        except ValueError:
            print("\nInvalid input! ID and stock must be numbers.")
            input("Press Enter to continue...")
            return
        
        success, message = self.medicine_manager.update_stock(medicine_id, new_stock)
        print(f"\n{message}")
        input("\nPress Enter to continue...")
    
    def update_expiry_menu(self):
        """Update medicine expiry date"""
        self.clear_screen()
        self.display_header()
        print("UPDATE EXPIRY DATE")
        print("-" * 40)
        
        try:
            medicine_id = int(input("Medicine ID to update: ").strip())
        except ValueError:
            print("\nInvalid input! ID must be a number.")
            input("Press Enter to continue...")
            return
        
        new_expiry = input("New Expiry Date (YYYY-MM-DD): ").strip()
        
        success, message = self.medicine_manager.update_expiry(medicine_id, new_expiry)
        print(f"\n{message}")
        input("\nPress Enter to continue...")
    
    def delete_medicine_menu(self):
        """Delete medicine"""
        self.clear_screen()
        self.display_header()
        print("DELETE MEDICINE")
        print("-" * 40)
        
        try:
            medicine_id = int(input("Medicine ID to delete: ").strip())
        except ValueError:
            print("\nInvalid input! ID must be a number.")
            input("Press Enter to continue...")
            return
        
        medicine = self.db.get_medicine_by_id(medicine_id)
        if medicine:
            print(f"\nMedicine to delete: {medicine['name']} (ID: {medicine_id})")
            confirm = input("Are you sure? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                success, message = self.medicine_manager.delete_medicine(medicine_id)
                print(f"\n{message}")
            else:
                print("\nDeletion cancelled.")
        else:
            print("\nMedicine not found.")
        
        input("\nPress Enter to continue...")
    
    def view_alerts_menu(self):
        """View all alerts"""
        self.clear_screen()
        self.display_header()
        print("ACTIVE ALERTS")
        print("-" * 60)
        
        self.medicine_manager.check_expiry_alerts()
        self.medicine_manager.check_stock_alerts()
        all_alerts = self.medicine_manager.get_all_alerts()
        
        if not all_alerts:
            print("No active alerts at the moment.")
            print("✓ All medicines are properly stocked and not expiring soon.")
        else:
            print(f"Total Alerts: {len(all_alerts)}")
            print("=" * 60)
            
            expiry_count = 0
            stock_count = 0
            
            for i, alert in enumerate(all_alerts, 1):
                if "EXPIRY" in alert:
                    expiry_count += 1
                    print(f"{i}. ⚠️  {alert}")
                else:
                    stock_count += 1
                    print(f"{i}. 📉 {alert}")
            
            print("=" * 60)
            print(f"Summary: {expiry_count} expiry alerts, {stock_count} stock alerts")
        
        print("\n" + "-" * 60)
        input("\nPress Enter to return to main menu...")
    
    def reports_menu(self):
        """Generate reports"""
        while True:
            self.clear_screen()
            self.display_header()
            print("REPORTS")
            print("-" * 40)
            print("1. Generate Inventory Report")
            print("2. Generate Expiry Report")
            print("3. Generate Stock Report")
            print("4. View Report History")
            print("5. Back to Main Menu")
            print("-" * 40)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.generate_inventory_report()
            elif choice == "2":
                self.generate_expiry_report()
            elif choice == "3":
                self.generate_stock_report()
            elif choice == "4":
                self.view_report_history()
            elif choice == "5":
                break
            else:
                print("\nInvalid choice. Please try again.")
                input("Press Enter to continue...")
    
    def generate_inventory_report(self):
        """Generate and display inventory report"""
        self.clear_screen()
        self.display_header()
        print("INVENTORY REPORT")
        print("=" * 60)
        
        user_id = self.auth.get_current_user()["id"]
        report = self.report_generator.generate_inventory_report(user_id)
        
        print(f"Report ID: {report['report_id']}")
        print(f"Generated on: {report['generation_date']}")
        print("-" * 60)
        print(f"Total Medicines: {report['total_medicines']}")
        print(f"Expired Medicines: {report['expired_count']}")
        print(f"Medicines Expiring Soon (30 days): {report['near_expiry_count']}")
        print(f"Low Stock Medicines: {report['low_stock_count']}")
        print(f"Total Stock Value: ₹{report['total_stock_value']:.2f}")
        print("=" * 60)
        
        input("\nPress Enter to continue...")
    
    def generate_expiry_report(self):
        """Generate and display expiry report"""
        self.clear_screen()
        self.display_header()
        print("EXPIRY REPORT")
        print("=" * 60)
        
        report = self.report_generator.generate_expiry_report()
        
        print(f"Total Expired: {report['total_expired']}")
        print(f"Expiring Soon (30 days): {report['total_expiring_soon']}")
        print("-" * 60)
        
        if report['expired_medicines']:
            print("\n❌ EXPIRED MEDICINES:")
            for med in report['expired_medicines'][:10]:
                print(f"  • {med['name']} (ID: {med['id']}) - Expired on {med['expiry_date']}")
            if len(report['expired_medicines']) > 10:
                print(f"  ... and {len(report['expired_medicines']) - 10} more")
        
        if report['expiring_soon']:
            print("\n⚠️  EXPIRING SOON (within 30 days):")
            for item in report['expiring_soon'][:10]:
                print(f"  • {item['name']} (ID: {item['id']}) - Expires in {item['days_until_expiry']} days")
            if len(report['expiring_soon']) > 10:
                print(f"  ... and {len(report['expiring_soon']) - 10} more")
        
        print("=" * 60)
        input("\nPress Enter to continue...")
    
    def generate_stock_report(self):
        """Generate and display stock report"""
        self.clear_screen()
        self.display_header()
        print("STOCK REPORT")
        print("=" * 60)
        
        report = self.report_generator.generate_stock_report()
        
        print(f"Out of Stock: {report['total_out_of_stock']}")
        print(f"Low Stock (≤5 units): {report['total_low_stock']}")
        print(f"Adequate Stock: {report['total_healthy_stock']}")
        print("-" * 60)
        
        if report['out_of_stock']:
            print("\n❌ OUT OF STOCK:")
            for med in report['out_of_stock'][:10]:
                print(f"  • {med['name']} (ID: {med['id']}) - {med['category']}")
        
        if report['low_stock']:
            print("\n⚠️  LOW STOCK (≤5 units):")
            for med in report['low_stock'][:10]:
                print(f"  • {med['name']} (ID: {med['id']}) - {med['stock']} units left")
        
        print("=" * 60)
        input("\nPress Enter to continue...")
    
    def view_report_history(self):
        """View previous reports"""
        self.clear_screen()
        self.display_header()
        print("REPORT HISTORY")
        print("=" * 80)
        
        reports = self.db.data["reports"]
        
        if not reports:
            print("No reports generated yet.")
        else:
            print(f"{'ID':<5} {'Date':<20} {'Total Meds':<12} {'Expired':<10} {'Low Stock':<10} {'Total Value':<15}")
            print("-" * 80)
            
            for report in reports[-10:]:
                date_str = datetime.datetime.fromisoformat(report['report_date']).strftime("%Y-%m-%d %H:%M")
                print(f"{report['id']:<5} {date_str:<20} {report['total_medicines']:<12} "
                      f"{report['expired_count']:<10} {report['low_stock_count']:<10} "
                      f"₹{report['total_stock_value']:<12.2f}")
        
        print("=" * 80)
        input("\nPress Enter to continue...")
    
    def view_all_medicines(self):
        """View all medicines in inventory"""
        self.clear_screen()
        self.display_header()
        print("ALL MEDICINES IN INVENTORY")
        print("=" * 80)
        
        medicines = self.medicine_manager.get_sorted_medicines()
        
        if not medicines:
            print("No medicines in inventory.")
        else:
            print(f"{'ID':<5} {'Name':<20} {'Category':<15} {'Stock':<10} {'Price':<10} {'Expiry':<12}")
            print("-" * 80)
            
            for med in medicines:
                print(f"{med['id']:<5} {med['name']:<20} {med['category']:<15} "
                      f"{med['stock']:<10} ₹{med['price']:<8.2f} {med['expiry_date']:<12}")
            
            print("=" * 80)
            print(f"Total Medicines: {len(medicines)}")
        
        input("\nPress Enter to continue...")
    
    def search_medicine_menu(self):
        """Search medicine"""
        self.clear_screen()
        self.display_header()
        print("SEARCH MEDICINE")
        print("-" * 40)
        
        keyword = input("Enter medicine name or category: ").strip()
        
        results = self.medicine_manager.search_medicine(keyword)
        
        if not results:
            print(f"\nNo medicines found for '{keyword}'")
        else:
            print(f"\nFound {len(results)} medicines:")
            print("-" * 60)
            for med in results:
                print(f"ID: {med['id']}, Name: {med['name']}, Category: {med['category']}, "
                      f"Stock: {med['stock']}, Price: ₹{med['price']:.2f}, "
                      f"Expiry: {med['expiry_date']}")
        
        input("\nPress Enter to continue...")
    
    def admin_menu(self):
        """Admin functions"""
        self.clear_screen()
        self.display_header()
        print("ADMIN PANEL")
        print("-" * 40)
        print("1. View All Users")
        print("2. System Statistics")
        print("3. Back to Main Menu")
        print("-" * 40)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            self.view_all_users()
        elif choice == "2":
            self.system_statistics()
        elif choice == "3":
            return
        else:
            print("\nInvalid choice.")
        
        input("\nPress Enter to continue...")
    
    def view_all_users(self):
        """View all users (admin only)"""
        self.clear_screen()
        self.display_header()
        print("ALL USERS")
        print("=" * 60)
        
        users = self.db.data["users"]
        
        print(f"{'ID':<5} {'Username':<15} {'Role':<10} {'Email':<20} {'Last Login':<20}")
        print("-" * 60)
        
        for user in users:
            last_login = user.get('last_login', 'Never')
            if last_login != 'Never':
                try:
                    last_login = datetime.datetime.fromisoformat(last_login).strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            print(f"{user['id']:<5} {user['username']:<15} {user['role']:<10} "
                  f"{user.get('email', ''):<20} {last_login:<20}")
        
        print("=" * 60)
    
    def system_statistics(self):
        """Display system statistics"""
        self.clear_screen()
        self.display_header()
        print("SYSTEM STATISTICS")
        print("=" * 60)
        
        users = len(self.db.data["users"])
        medicines = len(self.db.data["medicines"])
        alerts = len(self.db.data["alerts"])
        reports = len(self.db.data["reports"])
        
        print(f"Total Users: {users}")
        print(f"Total Medicines: {medicines}")
        print(f"Total Alerts Generated: {alerts}")
        print(f"Total Reports Generated: {reports}")
        print("-" * 60)
        
        total_value = sum(m["price"] * m["stock"] for m in self.db.data["medicines"])
        print(f"Total Inventory Value: ₹{total_value:.2f}")
        print("=" * 60)

def main():
    """Main application entry point"""
    try:
        app = MESAS()
        app.main_menu()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()