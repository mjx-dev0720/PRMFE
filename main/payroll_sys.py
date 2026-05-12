from db_handling import PayrollDataFileHandling

class Employee:
    def __init__(self, id, name, gender, department, position, hire_date, email, bank_account, emp_type):
        self.id = id
        self.name = name
        self.gender = gender
        self.department = department
        self.position = position
        self.hire_date = hire_date
        self.__salary = 0
        self.email = email
        self.bank_account = bank_account
        self.emp_type = emp_type


    def __repr__(self):
        return f"ID:{self.id} NAME:{self.name}"

    def set_salary(self, amount):
        if amount > 0:
            self.__salary = amount
        else:
            pass

    def get_salary(self):
        return self.__salary
    
class PartTimeEmployee(Employee):
    def __init__(self, id, name, gender, department, position, hire_date , hours_worked, hourly_rate, email, bank_account):
        super().__init__(id, name, gender, department, position, hire_date, email, bank_account, "Part-Time")
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate 

        self.calculate_salary()
        
    def calculate_salary(self):
        total_salary = self.hours_worked * self.hourly_rate
        self.set_salary(total_salary)

class FullTimeEmployee(Employee):
    def __init__(self, id, name, gender, department, position, hire_date, monthly_salary, email, bank_account):
        super().__init__(id, name, gender, department, position, hire_date, email, bank_account, "Full-Time")
        self.set_salary(monthly_salary)

class PayrollSystemManager:
    def __init__(self):
        self.db = PayrollDataFileHandling()
        self.employees = []
        self.load_system_data()

    def load_system_data(self):
        """Load The Employees"""
        raw_data = self.db.load_employees_from_file()
        for data in raw_data:
            if data[8] == "Full-Time":
                emp = FullTimeEmployee(data[0], data[1], data[2], data[3], data[4], data[5], float(data[9]), data[6], data[7])
            else:
                hours = float(data[10]) if len(data) > 10 else 0
                rate = float(data[11]) if len(data) > 11 else 0
                
                emp = PartTimeEmployee(data[0], data[1], data[2], data[3], data[4], data[5], hours, rate, data[6], data[7])
            
            self.employees.append(emp)

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
        if employee_name in self.employees:
            self.employees.remove(employee_name)
            self._sync()
            return True
        return False
    
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