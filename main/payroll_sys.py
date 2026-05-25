from db_handling import PayrollDataFileHandling

class Employee:
    def __init__(self, id, name, gender, department, position, hire_date, email, bank_account, emp_type):
        self.id = id
        self.name = name
        self.gender = gender
        self.department = department
        self.position = position
        self.hire_date = hire_date
        self._salary = 0.0
        self.email = email
        self.bank_account = bank_account
        self.emp_type = emp_type


    def __repr__(self):
        return f"{self.id} : {self.name}"

    def set_salary(self, amount):
        if amount > 0:
            self._salary = float(amount)
        else:
            pass

    def get_salary(self):
        return self._salary
    
    def calculate_payroll_breakdown(self, hours_override=None, absences_count=0, ot_hours=0):
        """
        Calculates itemized financial breakdowns. 
        Returns a structured dictionary of figures rounded to 2 decimal places.
        This isolates business math entirely from UI layers!
        """
        num_absences = float(absences_count) if absences_count else 0.0
        if self.emp_type == "Full-Time":
            base_salary = float(self.get_salary())
            reg_pay = base_salary
            total_monthly_hours = 22.0 * 8.0
            hourly_rate = base_salary / total_monthly_hours

            ot_pay = ot_hours * (hourly_rate * 1.5)

            daily_rate = base_salary / 22.0
            attendance_deduction = round(num_absences * daily_rate, 2)
        else:
            if hours_override is not None:
                hours_worked = float(hours_override)
            else:
                hours_worked = 160.0
            rate = float(getattr(self, 'hourly_rate', 100.0))
            
            reg_hours = min(hours_worked, 160.0)
            ot_hours = max(0.0, hours_worked - 160.0)
            
            reg_pay = reg_hours * rate
            ot_pay = ot_hours * (rate * 1.5)

            attendance_deduction = round(num_absences * rate, 2)

        gross = reg_pay + ot_pay

        # Deductions
        vat = round(reg_pay * 0.12, 2)
        ph = round(reg_pay * 0.025, 2)
        sss = 1750.00 if gross >= 35000.00 else round(reg_pay * 0.045, 2)
        pag = 200.00

        total_deductions = vat + ph + sss + pag + attendance_deduction
        net = round(gross - total_deductions, 2)

        return {
            "reg_pay": round(reg_pay, 2),
            "ot_pay": round(ot_pay, 2),
            "gross": round(gross, 2),
            "vat": vat,
            "ph": ph,
            "sss": sss,
            "pag": pag,
            "absent": attendance_deduction,
            "net": net
        }
    
class PartTimeEmployee(Employee):
    def __init__(self, id, name, gender, department, position, hire_date , hours_worked, hourly_rate, email, bank_account):
        super().__init__(id, name, gender, department, position, hire_date, email, bank_account, "Part-Time")
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate 
        
    def get_salary(self):
        return round(self.hours_worked * self.hourly_rate, 2)

class FullTimeEmployee(Employee):
    def __init__(self, id, name, gender, department, position, hire_date, monthly_salary, email, bank_account):
        super().__init__(id, name, gender, department, position, hire_date, email, bank_account, "Full-Time")
        self.set_salary(monthly_salary)

class PayrollSystemManager:
    def __init__(self):
        self.db = PayrollDataFileHandling()
        self.employees = []

        raw_data = self.db.load_employees_from_file()
        self.load_system_data(raw_data)

    def load_system_data(self, raw_data_list):
        """Load The Employees"""
        for data in raw_data_list:
            if not data or len(data) < 9:
                continue
            try:
                eid, name, gender, dept, pos, h_date, email, bank, e_type = data[:9]
                if e_type == "Part-Time":
                    hours = float(data[10]) if len(data) > 10 else 0.0
                    rate = float(data[11]) if len(data) > 11 else 0.0
                    emp = PartTimeEmployee(eid, name, gender, dept, pos, h_date, hours, rate, email, bank)
                else:
                    salary = float(data[9]) if len(data) > 9 else 0.0
                    emp = FullTimeEmployee(eid, name, gender, dept, pos, h_date, salary, email, bank)
            
                self.employees.append(emp)
            except (ValueError, IndexError) as e:
                print(f"[Warning] Skipping corrupted line entries in data ledger: {data}. Error: {e}")

    def _sync(self):
        """Internal helper to save data to disk."""
        self.db.save_employees(self.employees)

    def add_fulltime_employee(self, id, name, gender, department, position, hire_date, monthly_salary, email, bank_account):
        """Add an FullTime Employee to the list"""
        fulltime_employee = FullTimeEmployee(id, name, gender, department, position, hire_date, monthly_salary, email, bank_account)
        self.employees.append(fulltime_employee)
        self._sync()
        return fulltime_employee
    
    def add_parttime_employee(self, id, name, gender,  department, position, hire_date, hours_worked, hourly_rate, email, bank_account):
        """Add an PartTime Employee to the list"""
        parttime_employee = PartTimeEmployee(id, name, gender, department, position, hire_date, hours_worked, hourly_rate, email, bank_account)
        self.employees.append(parttime_employee)
        self._sync()
        return parttime_employee
    
    def delete_employee_by_id(self, employee_id):
        """Removes a specific employee object by ID"""
        target_id = str(employee_id)
        for emp in self.employees:
            if str(emp.id) == target_id:
                self.employees.remove(emp)
                self._sync()
                return True, emp.name
        return False, None
    
    def delete_employee_by_name(self, employee_name):
        """Removes a specific employee object by Name."""
        target_name = str(employee_name).strip()
        for emp in self.employees:
            cur_emp = str(emp.name).strip()
            if target_name in cur_emp:
                self.employees.remove(employee_name)
                self._sync()
                return True, emp.name
        return False, None
    
    def search_employee_by_id(self, eid):
        """Returns the employee object if found, otherwise None."""
        for emp in self.employees:
            if str(emp.id) == str(eid):
                return emp
        return None
    
    def search_employees_by_name(self, name):
        """Returns a list of employee objects that match the name (case-insensitive)."""
        matches = [emp for emp in self.employees if name.lower() in emp.name.lower()]
        return matches
    
    def update_fulltime_employee(self, id, name, gender, department, position, hire_date, salary, email, bank_account):
        """Updates an existing Full-Time Employee's records."""
        emp = self.search_employee_by_id(id)
        if emp:
            if emp.emp_type != "Full-Time":
                new_emp = FullTimeEmployee(id, name, gender, department, position, hire_date, float(salary), email, bank_account)
            
                idx = self.employees.index(emp)
                self.employees[idx] = new_emp
            else:
                emp.name = name
                emp.gender = gender
                emp.department = department
                emp.position = position
                emp.hire_date = hire_date
                emp.set_salary(float(salary))
                emp.email = email
                emp.bank_account = bank_account
                
            self._sync()
            return True
        return False
    
    def update_parttime_employee(self, id, name, gender, department, position, hire_date, hours_worked, hourly_rate, email, bank_account):
        """Updates an existing Part-Time Employee's records."""
        emp = self.search_employee_by_id(id)
        if emp:
            if emp.emp_type != "Part-Time":
                new_emp = PartTimeEmployee(id, name, gender, department, position, hire_date, float(hours_worked), float(hourly_rate), email, bank_account)
                
                idx = self.employees.index(emp)
                self.employees[idx] = new_emp
            else:
                emp.name = name
                emp.gender = gender
                emp.department = department
                emp.position = position
                emp.hire_date = hire_date
                emp.hours_worked = float(hours_worked)
                emp.hourly_rate = float(hourly_rate)
                
            self._sync()
            return True
        return False
    
    def undo_employee_payroll(self, ref_no):
        """Undo a pay record"""
        success, message, emp_id = self.db.undo_payroll_by_ref_no(ref_no)
        
        if success and emp_id:
            emp = self.search_employee_by_id(emp_id)
            if emp and emp.emp_type == "Part-Time":
                emp.hours_worked = 160.0
                self._sync()
                
        return success, message