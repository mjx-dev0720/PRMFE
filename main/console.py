from db_handling import *
from dsa_algo import *
from payroll_sys import *
import datetime
import os

#Console Based System

# --- INITIALIZE REAL DATA STRUCTURES FROM dsa_algo.py ---
# Instead of basic arrays, we instantiate your required tracking classes
PAYROLL_QUEUE = PayrollQueue() # True FIFO Queue from dsa_algo.py for Option [7]
PAYROLL_SYS = PayrollSystemManager()
SALARY_HISTORY = SalaryRecord() # Custom Linked List from dsa_algo.py for Option [8]
SORTER = PayrollAlgo()   # Custom Merge Sort Algorithm class from dsa_algo.py
FILE_HANDLER = PayrollDataFileHandling()
EMPLOYEES_LIST = PAYROLL_SYS.employees          # Native list holding live active Employee instances

def initialize_system_data():
    """Loads active employees and populates the historical salary linked list from the file storage layer."""
    try:
        PAYROLL_SYS.employees.clear()
        # 1. Load active employees into the manager
        raw_data = FILE_HANDLER.load_employees_from_file()
        PAYROLL_SYS.load_system_data(raw_data)
        
        # 2. Sync the file history ledger back into our SalaryRecord Linked List
        historical_slips = FILE_HANDLER.get_all_salary_slips() # Returns the dict matrix
        
        # Loop through the dictionary and insert them into the linked list
        for emp_id, slips in historical_slips.items():
            for slip in slips:
                SALARY_HISTORY.add_record(
                    employee_id=emp_id,
                    name=slip["name"],
                    salary=slip["net"]
                )
        print("[System Info] Active records and historical linked lists successfully synchronized.")
    except Exception as e:
        print(f"[Initialization Warning] Failed to sync data structures smoothly: {e}")

def print_row(emp, count=None):
    """Utility format print layout extracting attributes from an object instance with perfect tab column gaps."""
    # Using dynamic checks to safely handle any formatting if an attribute is an integer or string
    emp_id = str(emp.id)
    emp_name = str(emp.name)
    emp_dept = str(emp.department)
    emp_pos = str(emp.position)
    hire_date = str(emp.hire_date)
    emp_type = str(emp.emp_type)
    emp_base_salary = (emp.get_salary())
    
    if count is not None:
        print(f"{count:<3} | {emp_id:<8} | {emp_name:<25} | {emp_dept:<25} | {emp_pos:<25} | {hire_date:<20} | {emp_type:<12} | ₱{emp_base_salary:.2f}")
    else:
        print(f"{emp_id:<8} | {emp_name:<25} | {emp_dept:<25} | {emp_pos:<25} | {hire_date:<20} | {emp_type:<15} | ₱{emp_base_salary:.2f}")

def main():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    initialize_system_data()
    while True:
        print("--- Payroll Management System For Employees ---")
        print("[1]Add Employee")
        print("[2]View All Employees")
        print("[3]Search Employee")
        print("[4]Delete Employee")
        print("[5]Edit Employee")
        print("[6]Process Employee")
        print("[7]Process Batch Payroll")
        print("[8]View Salary History")
        print("[9]Sort Employees")
        print("[10]Exit")
        try:
            choice = int(input("Enter Choice: "))
        except ValueError:
            print("Error: Invalid choice format. Please enter an integer.")
            continue

        if choice == 1:
            subchoice = int(input("\n[1]Full-Time\n[2]Part-Time\nEnter Choice: "))

            id = FILE_HANDLER.commit_next_id()
            name = input("Enter Full Name: ").strip()
            gender = input("Enter Gender (Male/Female): ").strip()
            dept = input("Enter Department: ").strip()
            pos = input("Enter Position: ").strip()
            email = input("Enter Corporate Email: ").strip()
            bank = input("Enter Bank Account Number: ").strip()

            if not (name and gender and dept and pos and email and bank):
                print("Error: Missing parameters. All metadata inputs are mandatory.")
                continue

            if subchoice == 1:
                salary = float(input("Enter Fixed Monthly Salary (Php): "))
                PAYROLL_SYS.add_fulltime_employee(id, name, gender, dept, pos, current_date, salary, email, bank)
                print(f"[Success] FullTimeEmployee registered with ID: {id}")
            elif subchoice == 2:
                rate = float(input("Enter Hourly Rate (Php): "))
                hours = float(input("Enter Regular Clocked Hours: "))
                PAYROLL_SYS.add_parttime_employee(id, name, gender, dept, pos, current_date, hours, rate, email, bank)
                print(f"[Success] PartTimeEmployee registered with ID: {id}")
            else:
                print("ERROR: Index Error")
                    
        elif choice == 2:
            if not EMPLOYEES_LIST:
                print("\n[Notice] No active employee found.")
                continue
            print("\n" + "="* 152)
            print("\t\t\t\t\t\t\t\tCURRENT EMPLOYEE LIST")
            print("="* 152)
            print(f"{'#':<3} | {'ID':<8} | {'Employee Name':<25} | {'Department':<25} | {'Position':<25} | {'Hire Date':<20} | {'Type':<12} | {'Base Salary'}")
            print("-" * 152)
            for count, emp in enumerate(EMPLOYEES_LIST, start=1):
                print_row(emp, count=count)
            print("="* 152)

        elif choice == 3:
            subchoice = int(input("\n[1]ID\n[2]Name\nSearch By: "))
            found = False
            if subchoice == 1:
                search_id = input("Enter target employee ID to lookup: ").strip()
                result = PAYROLL_SYS.search_employee_by_id(search_id)
                print("\n\t\t\t\t\t\t\t\t--- ID Search Result ---")
                print(f"{'ID':<8} | {'Employee Name':<25} | {'Department':<25} | {'Position':<25} | {'Hire Date':<20} | {'Type':<12} | {'Base Salary'}")
                print("-" * 152)
                print_row(result)
                found = True
                print("\n")
                continue
                    
            elif subchoice == 2:
                search_name = input("Enter query name string: ").strip()
                result = PAYROLL_SYS.search_employees_by_name(search_name)
                print("\n\t\t\t\t\t\t\t--- Matching Search Results ---")
                print(f"{'ID':<8} | {'Employee Name':<25} | {'Department':<25} | {'Position':<25} | {'Hire Date':<20} | {'Type':<12} | {'Base Salary'}")
                print("-" * 152)
                for emp in result:
                    print_row(emp)
                    found = True

                print("\n")
            else:
                print("Error: Index Error")
                continue

            if not found:
                    print("Notice: No matching names found.")
                    
        elif choice == 4:
            removed = False
            del_id = input("Enter unique target ID to delete: ").strip()
            result, rname = PAYROLL_SYS.delete_employee_by_id(del_id)
                    
            if result:
                print(f"Successfully Deleted {rname}")
                removed = True
                continue
                
            if not removed:
                print("Notice: No matching names found.")

        elif choice == 5:
            print("\n--- Edit Employee Details ---")
            search_id = input("Enter Employee ID to edit/update: ").strip()

            target_emp = PAYROLL_SYS.search_employee_by_id(search_id)

            if not target_emp:
                print("Error: Employee not found.")
                continue

            print(f"\nModifying details for {target_emp.name} ({target_emp.emp_type})")
            print("--- Press [Enter] to keep the current value ---")

            new_name = input(f"New Name [{target_emp.name}]: ").strip()
            new_gender = input(f"New Gender [{target_emp.gender}]: ").strip()
            new_dept = input(f"New Department [{target_emp.department}]: ").strip()
            new_pos = input(f"New Position [{target_emp.position}]: ").strip()
            new_email = input(f"New Email [{target_emp.email}]: ").strip()
            new_bank = input(f"New Bank Account [{target_emp.bank_account}]: ").strip()

            if new_name: target_emp.name = new_name
            if new_gender: target_emp.gender = new_gender
            if new_dept: target_emp.department = new_dept
            if new_pos: target_emp.position = new_pos
            if new_email: target_emp.email = new_email
            if new_bank: target_emp.bank_account = new_bank

            print(f"\nSelect target employment model for this employee:")
            print(f"[1] Full-Time")
            print(f"[2] Part-Time")
            try:
                type_choice = int(input("Enter Target Type Choice: "))
            except ValueError:
                print("Error: Invalid entry format. Aborting operational changes.")
                continue
                
            success = False

            if type_choice == 1:
                current_salary = target_emp.get_salary() if target_emp.emp_type == "Full-Time" else 0.00
                raw_sal = input(f"Enter Fixed Monthly Salary (Php) [{current_salary}]: ").strip()
                salary = float(raw_sal) if raw_sal else current_salary

                success = PAYROLL_SYS.update_fulltime_employee(
                search_id, new_name, new_gender, new_dept, new_pos, current_date, salary, new_email, new_bank
            )
            elif type_choice == 2:
                current_hours = getattr(target_emp, 'hours_worked', 0.0) if target_emp.emp_type == "Part-Time" else 0.0
                current_rate = getattr(target_emp, 'hourly_rate', 0.0) if target_emp.emp_type == "Part-Time" else 0.0

                raw_hours = input(f"Enter Regular Logged Hours [{current_hours}]: ").strip()
                hours_worked = float(raw_hours) if raw_hours else current_hours

                raw_rate = input(f"Enter Base Hourly Rate (Php) [{current_rate}]: ").strip()
                hourly_rate = float(raw_rate) if raw_rate else current_rate

                success = PAYROLL_SYS.update_parttime_employee(
                search_id, new_name, new_gender, new_dept, new_pos, current_date, hours_worked, hourly_rate, new_email, new_bank
                )
            else:
                print("Error: Index Error. Invalid category configuration type.")
                continue

            if success:
                print(f"\n[Success] Records for ID {search_id} cleanly committed and synchronized.")
                continue

        elif choice == 6:
            print("\n--- Process Individual Employee Payroll ---")
            proc_id = input("Enter Employee ID to calculate payroll: ").strip()

            target_emp = PAYROLL_SYS.search_employee_by_id(proc_id)

            if not target_emp:
                print("Error: Employee object instance could not be located.")
                continue
                
            print(f"\nProcessing payroll execution track for: {target_emp.name} ({target_emp.emp_type})")

            try:
                abs_input = input("Enter number of unpaid absences [Press Enter for 0]: ").strip()
                absences = float(abs_input) if abs_input else 0.0
            except ValueError:
                print("Error: Invalid numeric input format for absences. Operation cancelled.")
                continue

            hours_val = getattr(target_emp, 'hours_worked', None) if target_emp.emp_type == "Part-Time" else None

            pay = target_emp.calculate_payroll_breakdown(hours_override=hours_val, absences_count=absences)

            gross = float(pay.get('gross', 0.0))
            vat = float(pay.get('vat', 0.0))
            ph = float(pay.get('ph', 0.0))
            sss = float(pay.get('sss', 0.0))
            pag = float(pay.get('pag', 0.0))
            absent_deduction = float(pay.get('absent', 0.0))
            net = float(pay.get('net', 0.0))
            reg_pay = float(pay.get('reg_pay', gross))
            ot_pay = float(pay.get('ot_pay', 0.0))

            print("\n" + "="*50)
            print("          OFFICIAL INDIVIDUAL PAYSLIP             ")
            print("="*50)
            print(f" Pay Date: {current_date:<15} | Employee ID: {target_emp.id}")
            print(f" Name: {target_emp.name:<19} | Type: {target_emp.emp_type}")
            print(f" Dept: {target_emp.department}")
            print(f" Position: {target_emp.position}")
            print("-"*50)
            print(f" [+] Gross Base Earnings:        Php {gross:>14,.2f}")
            if 'reg_pay' in pay and pay['reg_pay'] > 0:
                print(f"     Regular Pay Component:      Php {reg_pay:>14,.2f}")
            if 'ot_pay' in pay and pay['ot_pay'] > 0:
                print(f"     Overtime Earnings:          Php {ot_pay:>14,.2f}")
            print("-"*50)
            print(f" [-] Statutory Taxes (VAT/WHT):  Php {vat:>14,.2f}")
            print(f" [-] PhilHealth Contribution:    Php {ph:>14,.2f}")
            print(f" [-] SSS Premium Contribution:   Php {sss:>14,.2f}")
            print(f" [-] Pag-IBIG Fund Core:         Php {pag:>14,.2f}")
            print(f" [-] Absence Penalties Check:    Php {absent_deduction:>14,.2f}")
            print("="*50)
            print(f" [*] TOTAL NET TAKE-HOME PAY:    Php {net:>14,.2f}")
            print("="*50)
            print("\n")

            if hasattr(SALARY_HISTORY, 'add_record'):
                SALARY_HISTORY.add_record(str(target_emp.id), target_emp.name, net)
            elif hasattr(SALARY_HISTORY, 'insert'):
                SALARY_HISTORY.insert(str(target_emp.id), target_emp.name, net)

            try:
                FILE_HANDLER.save_salary_slip_record(
                    str(target_emp.id), target_emp.name, target_emp.department, target_emp.position, 
                    target_emp.emp_type, reg_pay, ot_pay, gross, vat, ph, sss, pag, absent_deduction, net, current_date
                )
            except Exception as db_err:
                print(f"[File Engine Warning] Could not backup slip to database log files: {db_err}")
                    
            continue
            
        elif choice == 7:
            print("\n" + "="*50)
            print("             PROCESS BATCH PAYROLL            ")
            print("="*50)

            if not EMPLOYEES_LIST:
                print("[Notice] No active employees found to process.")
                continue

            while hasattr(PAYROLL_QUEUE, 'is_empty') and not PAYROLL_QUEUE.is_empty():
                    PAYROLL_QUEUE.dequeue()

            for emp in EMPLOYEES_LIST:
                    if hasattr(PAYROLL_QUEUE, 'enqueue'):
                        PAYROLL_QUEUE.enqueue(emp)

            print(f"Successfully queued {len(EMPLOYEES_LIST)} employees for batch processing.")
            confirm = input("Begin automated calculation processing? (Y/N): ").strip().upper()

            if confirm != 'Y':
                print("Batch processing aborted.")
                continue

            processed_count = 0

            while True:
                if hasattr(PAYROLL_QUEUE, 'is_empty') and PAYROLL_QUEUE.is_empty():
                    break
                    
                emp = None
                if hasattr(PAYROLL_QUEUE, 'dequeue'):
                    emp = PAYROLL_QUEUE.dequeue()
                elif hasattr(PAYROLL_QUEUE, 'pop'):
                    emp = PAYROLL_QUEUE.pop()
                        
                if emp is None:
                    break  # Guard rail for queue structures returning None when exhausted
                    
                    # 3. Calculate payroll automatically (Assuming 0 absences for batch runs)
                hours_val = getattr(emp, 'hours_worked', None) if emp.emp_type == "Part-Time" else None
                pay = emp.calculate_payroll_breakdown(hours_override=hours_val, absences_count=0.0)

                gross = float(pay.get('gross', 0.0))
                vat = float(pay.get('vat', 0.0))
                ph = float(pay.get('ph', 0.0))
                sss = float(pay.get('sss', 0.0))
                pag = float(pay.get('pag', 0.0))
                absent_deduction = float(pay.get('absent', 0.0))
                net = float(pay.get('net', 0.0))
                reg_pay = float(pay.get('reg_pay', gross))
                ot_pay = float(pay.get('ot_pay', 0.0))

                    # 4. Commit to Custom Linked List History (matching Option 6 methods)
                if hasattr(SALARY_HISTORY, 'add_record'):
                    SALARY_HISTORY.add_record(str(emp.id), emp.name, net)
                elif hasattr(SALARY_HISTORY, 'insert'):
                    SALARY_HISTORY.insert(str(emp.id), emp.name, net)

                    # 5. Backup slip records to file engine logs
                try:
                    FILE_HANDLER.save_salary_slip_record(
                        str(emp.id), emp.name, emp.department, emp.position, 
                        emp.emp_type, reg_pay, ot_pay, gross, vat, ph, sss, pag, absent_deduction, net, current_date
                    )
                except Exception as db_err:
                    pass # Kept silent during massive batch processing loops to prevent logs spamming
                    
                print(f" -> Processed: ID {emp.id:<5} | {emp.name:<25} |Sending to Bank Account: {emp.bank_account} -> PAID: ₱{net:>10,.2f}")
                processed_count += 1

            print("="*50)
            print(f"[Success] Batch Run Complete! {processed_count} execution records committed.")
            print("="*50)
            print("\n")
            continue

        elif choice == 8:
            print("\n" + "="*60)
            print("                  EMPLOYEE SALARY HISTORY                  ")
            print("="*60)

        
            history_logs = SALARY_HISTORY.display_all()
            print(f"{"ID":<8} {"NAME":<30} {"PAID":<12}")

            if not history_logs:
                print("[Notice] No historical salary slip transactions found.")
            else:
                for log in history_logs:
                    print(log)
                        
            print("-" * 60)
            print(f"Total historical entries in Linked List: {len(history_logs)}")
            print("="*60 + "\n")
            continue


        elif choice == 9:
            if not EMPLOYEES_LIST:
                print("\n[Notice] No active employees available to sort.")
                continue    

            print("\n--- Sort Employees Configuration ---")
            print("[1] Alphabetically (By Name)")
            print("[2] By Department")
            print("[3] By Base Salary")

            try:
                subchoice = int(input("Enter Choice: "))
            except ValueError:
                print("Error: Invalid entry format. Aborting sort.")
                continue
            
            sandbox_list = list(EMPLOYEES_LIST)
            sorted_list = []

            if subchoice == 1:
                print("\nSorting employees alphabetically (A-Z)...")
                # reverse=False forces ascending (A-Z) order
                sorted_list = SORTER.merge_sort(sandbox_list, criteria="alphabetical", reverse=False)
            elif subchoice == 2:
                print("\nSorting employees by department (A-Z)...")
                # reverse=False forces alphabetical order for the department names
                sorted_list = SORTER.merge_sort(sandbox_list, criteria="department", reverse=False)
            elif subchoice == 3:
                try:
                    subsubchoice = int(input("\n[1] Ascending (Low to High)\n[2] Descending (High to Low)\nEnter Choice: "))
                except ValueError:
                    print("Error: Invalid choice. Aborting sort.")
                    continue

                if subsubchoice == 1:
                    print("\nSorting employees by base salary (Ascending)...")
                    sorted_list = SORTER.merge_sort(sandbox_list, criteria="salary", reverse=False)
                else:
                    print("\nSorting employees by base salary (Descending)...")
                    sorted_list = SORTER.merge_sort(sandbox_list, criteria="salary", reverse=True)
            else:
                print("Error: Index Error. Invalid sorting criteria selected.")
                continue

            if not sorted_list:
                sorted_list = EMPLOYEES_LIST

            # --- DISPLAY THE SORTED DATA ---
            print("\n" + "="* 152)
            print("\t\t\t\t\t\t\t\tSORTED EMPLOYEE RESULTS")
            print("="* 152)
            print(f"{'#':<3} | {'ID':<8} | {'Employee Name':<25} | {'Department':<25} | {'Position':<25} | {'Hire Date':<20} | {'Type':<12} | {'Base Salary'}")
            print("-" * 152)
            for count, emp in enumerate(sorted_list, start=1):
                print_row(emp, count=count)
            print("="* 152 + "\n")

        elif choice == 10:
            print("Exiting Program")
            break
        else:
            print("Error: Index Error")

if __name__ == "__main__":
    main()