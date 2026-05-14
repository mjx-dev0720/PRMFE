import os


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
                    return int(content) if content else 1001
                except ValueError:
                    return 1001
        return 1001

    def save_config(self):
        """Saves the current counter state to config.txt."""
        with open(self.config_filename, "w") as f:
            f.write(str(self.next_id_counter))
    
    def get_next_id(self):
        return self.next_id_counter
    
    def commit_next_id(self):
        new_id = self.next_id_counter
        self.next_id_counter += 1
        self.save_config()
        return new_id
        
    def save_salary_slip_record(self, emp_id, name, dept, pos, emp_type, reg_pay, ot_pay, gross, vat, ph, sss, pag, absent, net, date):
        """
        Saves a highly explicit, breakdown itemized payroll slip snapshot into the ledger file.
        This guarantees data consistency even if rates change in the future.
        """
        try:
            line = (
                f"{date}|{emp_id}|{name}|{dept}|{pos}|{emp_type}|"
                f"{reg_pay:.2f}|{ot_pay:.2f}|{gross:.2f}|"
                f"{vat:.2f}|{ph:.2f}|{sss:.2f}|{pag:.2f}|{absent:.2f}|{net:.2f}\n"
            )
            with open(self.history_filename, "a", encoding="utf-8") as f:
                f.write(line)
            return True
        except Exception as e:
            print(f"[Database Error] Failed to persist salary slip transaction record: {e}")
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
                    if len(tokens) >= 15:
                        emp_id = tokens[1]
                        if emp_id not in slips_collection:
                            slips_collection[emp_id] = []
                        
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
                            "net": float(tokens[14])
                        })
            return slips_collection
        except Exception as e:
            print(f"[Database Error] Failed to compile historical salary slips tracking array: {e}")
            return slips_collection