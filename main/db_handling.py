import os
import datetime

class PayrollDataFileHandling:
    """All File Handling Operations"""
    def __init__(self):
        self.admin_filename = "db/admin_db.txt"
        self.emp_filename = "db/employees.txt"
        self.history_filename = "db/history.txt"
        self.config_filename = "db/config.txt"

        if not os.path.exists("db"):
            os.makedirs("db")

        self.next_id_counter = self.load_config()

    def format_id(self, numeric_id, prefix="IT"):
        """Formats a numeric integer into an alphanumeric unique ID string (e.g., IT0000126)."""
        year_str = datetime.datetime.now().strftime("%y")
        return f"{prefix}{numeric_id:05d}{year_str}"

    def read_admin_data(self, username, password):
        """Admin.txt checker"""
        if os.path.exists(self.admin_filename):
            with open(self.admin_filename, "r") as file:
                for line in file:
                    stored_username, stored_password = line.strip().split("|")
                    if username == stored_username and password == stored_password:
                        return True
                    
        else:
            return False
        
    def save_employees(self, employee_list):
        """Saves the list of employee objects to a text file."""
        if os.path.exists(self.emp_filename) and os.path.getsize(self.emp_filename) > 0:
            try:
                backup_path = self.emp_filename + ".bak"
                with open(self.emp_filename, "r") as src, open(backup_path, "w") as dest:
                    dest.write(src.read())
            except Exception as backup_error:
                print(f"[Database Warning] Error creating file checkpoint state: {backup_error}")

        try:
            with open(self.emp_filename, "w") as f:
                for emp in employee_list:
                    line = f"{emp.id}|{emp.name}|{emp.gender}|{emp.department}|{emp.position}|{emp.hire_date}|{emp.email}|{emp.bank_account}|{emp.emp_type}|{emp.get_salary()}"
                    
                    if emp.emp_type == "Part-Time":
                        line += f"|{emp.hours_worked}|{emp.hourly_rate}"
                    else:
                        line += "|0|0"
                    
                    f.write(line + "\n")
        except Exception as write_error:
            print(f"[Database Error] Fatal disruption while flashing memory matrices to disk: {write_error}")

    def load_employees_from_file(self):
        """Returns a list of raw data lines from the file."""
        if not os.path.exists(self.emp_filename):
            return []
        with open(self.emp_filename, "r") as f:
            return [line.strip().split("|") for line in f]
        
    def load_config(self):
        """Reads the last used ID from config.txt."""
        if os.path.exists(self.config_filename):
            with open(self.config_filename, "r") as f:
                try:
                    content = f.read().strip()
                    return int(content) if content else 1
                except ValueError:
                    return 1
        return 1

    def save_config(self):
        """Saves the current counter state to config.txt."""
        with open(self.config_filename, "w") as f:
            f.write(str(self.next_id_counter))
    
    def get_next_id(self):
        return self.format_id(self.next_id_counter)
    
    def commit_next_id(self):
        formatted_id = self.format_id(self.next_id_counter)
        self.next_id_counter += 1
        self.save_config()
        return formatted_id
        
    def save_salary_slip_record(self, emp_id, name, dept, pos, emp_type, reg_pay, ot_pay, gross, vat, ph, sss, pag, absent, net, date, ref_no, hours_worked=160.0):
        """
        Saves a highly explicit, breakdown itemized payroll slip snapshot into the ledger file.
        This guarantees data consistency even if rates change in the future.
        """
        try:
            line = (
                f"{date}|{emp_id}|{name}|{dept}|{pos}|{emp_type}|"
                f"{reg_pay:.2f}|{ot_pay:.2f}|{gross:.2f}|"
                f"{vat:.2f}|{ph:.2f}|{sss:.2f}|{pag:.2f}|{absent:.2f}|{net:.2f}|{ref_no}|{float(hours_worked):.2f}\n"
            )
            with open(self.history_filename, "a", encoding="utf-8") as f:
                f.write(line)
            return True
        except Exception as e:
            print(f"[Database Error] Failed to persist salary slip transaction record: {e}")
            return False
        
    def remove_salary_slip_record(self, ref_no):
        """
        Removes a specific salary slip record from history.txt matching the reference number.
        Returns True if a record was successfully removed, False otherwise.
        """
        if not os.path.exists(self.history_filename):
            return False
            
        record_removed = False
        remaining_lines = []
        
        try:
            with open(self.history_filename, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    tokens = line.strip().split("|")
                    
                    if len(tokens) >= 16 and tokens[15].strip() == str(ref_no).strip():
                        record_removed = True
                        continue 
                        
                    remaining_lines.append(line)
            
            with open(self.history_filename, "w", encoding="utf-8") as f:
                for line in remaining_lines:
                    f.write(line)
                    
            return record_removed
        except Exception as e:
            print(f"[Database Error] Failed to delete salary slip record {ref_no}: {e}")
            return False

    def get_all_salary_slips(self):
        """
        Reads and parses every generated itemized payslip from the text storage layer.
        Returns a structured dictionary matrix keyed by Employee ID for fast O(1) lookups.
        """
        slips_collection = {}
        if not os.path.exists(self.history_filename):
            return slips_collection
        try:
            with open(self.history_filename, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    tokens = line.strip().split("|")
                    if len(tokens) >= 16:
                        emp_id = tokens[1]
                        if emp_id not in slips_collection:
                            slips_collection[emp_id] = []
                        
                        hours = float(tokens[16]) if len(tokens) >= 17 else 160.0
                        
                        slips_collection[emp_id].append({
                            "date": tokens[0],
                            "name": tokens[2],
                            "dept": tokens[3],
                            "pos": tokens[4],
                            "emp_type": tokens[5],
                            "reg_pay": float(tokens[6]),
                            "ot_pay": float(tokens[7]),
                            "gross": float(tokens[8]),
                            "vat": float(tokens[9]),
                            "ph": float(tokens[10]),
                            "sss": float(tokens[11]),
                            "pag": float(tokens[12]),
                            "absent": float(tokens[13]),
                            "net": float(tokens[14]),
                            "ref_no": tokens[15],
                            "hours_worked": hours
                        })
            return slips_collection
        except Exception as e:
            print(f"[Database Error] Failed to compile historical salary slips tracking array: {e}")
            return slips_collection
        
    def is_period_already_processed(self, emp_id, target_period_str):
        """
        Checks if a duplicate record exists based on Employee ID and the exact 
        pay period string formatted as 'Month DD-DD YYYY' in history.txt.
        
        target_period_str expects format like: "May 01-31 2026"
        """
        if not os.path.exists(self.history_filename):
            return False

        try:
            with open(self.history_filename, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    tokens = line.strip().split("|")
                    if len(tokens) >= 15:
                        line_period = tokens[0].strip()
                        line_emp_id = tokens[1].strip()

                        # Secure matching against the customized monthly string format
                        if line_emp_id == str(emp_id).strip() and line_period == str(target_period_str).strip():
                            return True
            return False
        except Exception as e:
            print(f"[Database Error] Error checking custom pay period restrictions: {e}")
            return False
        
    def undo_payroll_by_ref_no(self, target_ref_no):
        """
        Searches history.txt for the given reference number, deletes that line, 
        and returns a tuple: (success_bool, message_str, affected_emp_id).
        """
        if not os.path.exists(self.history_filename):
            return False, "History log file does not exist.", None

        target_ref_no = str(target_ref_no).strip()
        remaining_lines = []
        record_found = False
        affected_emp_id = None

        try:
            with open(self.history_filename, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    tokens = line.strip().split("|")
                    
                    
                    if len(tokens) >= 16:
                        current_ref_no = tokens[15].strip()
                        if current_ref_no == target_ref_no:
                            record_found = True
                            affected_emp_id = tokens[1].strip()
                            continue
                            
                    remaining_lines.append(line)

            if not record_found:
                return False, f"No transaction found with Reference No: {target_ref_no}", None

            # Rewrite history without the deleted record
            with open(self.history_filename, "w", encoding="utf-8") as f:
                f.writelines(remaining_lines)

            return True, f"Successfully undo payroll record {target_ref_no}.", affected_emp_id

        except Exception as e:
            return False, f"[Database Error] Reversal failed: {e}", None