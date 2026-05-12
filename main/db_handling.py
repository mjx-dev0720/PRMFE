import os



class PayrollDataFileHandling:
    """All File Handling Operations"""
    def __init__(self):
        self.admin_filename = "db/admin_db.txt"
        self.emp_filename = "db/employees.txt"
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
        with open(self.emp_filename, "w") as f:
            for emp in employee_list:
                line = (f"{emp.id}|{emp.name}|{emp.gender}|{emp.department}|"
                        f"{emp.position}|{emp.hire_date}|{emp.email}|"
                        f"{emp.bank_account}|{emp.emp_type}|{emp.get_salary()}")
                
                if emp.emp_type == "Part-Time":
                    line += f"|{emp.hours_worked}|{emp.hourly_rate}"
                else:
                    line += "|0|0"
                
                f.write(line + "\n")
                
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