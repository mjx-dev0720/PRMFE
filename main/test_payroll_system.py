import unittest
import os
import shutil
from unittest.mock import MagicMock

# Import components directly from your module files
from dsa_algo import Node, SalaryRecord, PayrollQueue, PayrollAlgo
from payroll_sys import Employee, FullTimeEmployee, PartTimeEmployee, PayrollSystemManager
from db_handling import PayrollDataFileHandling


class TestDSADataStructures(unittest.TestCase):
    """
    Unit tests targeting custom data structures and algorithms (dsa_algo.py).
    """

    def setUp(self):
        self.salary_history = SalaryRecord()
        self.payroll_queue = PayrollQueue()
        self.sorter = PayrollAlgo()

    def test_linked_list_append_and_iteration(self):
        """Verify SalaryRecord custom linked list appends elements using its tail pointer."""
        self.salary_history.add_record("EMP001", "Alice", 50000.00)
        self.salary_history.add_record("EMP002", "Bob", 35000.50)
        
        logs = self.salary_history.display_all()
        self.assertEqual(len(logs), 2)
        self.assertIn("EMP001", logs[0])
        self.assertIn("Alice", logs[0])
        self.assertIn("₱50,000.00", logs[0])
        self.assertIn("EMP002", logs[1])

    def test_queue_fifo_mechanics(self):
        """Verify PayrollQueue maintains strict First-In-First-Out ordering sequences."""
        self.assertTrue(self.payroll_queue.is_empty())
        
        self.payroll_queue.enqueue("Task A")
        self.payroll_queue.enqueue("Task B")
        self.assertFalse(self.payroll_queue.is_empty())
        
        self.assertEqual(self.payroll_queue.dequeue(), "Task A")
        self.assertEqual(self.payroll_queue.dequeue(), "Task B")
        self.assertTrue(self.payroll_queue.is_empty())

    def test_merge_sort_alphabetical(self):
        """Verify PayrollAlgo correctly sorts real employee objects alphabetically (A-Z)."""
        emp1 = FullTimeEmployee("1", "Zackary", "Male", "HR", "Manager", "2026", 50000.00, "z@corp.com", "111")
        emp2 = FullTimeEmployee("2", "Alex", "Male", "IT", "Dev", "2026", 60000.00, "a@corp.com", "222")
        
        sorted_list = self.sorter.merge_sort([emp1, emp2], criteria="alphabetical", reverse=False)
        self.assertEqual(sorted_list[0].name, "Alex")
        self.assertEqual(sorted_list[1].name, "Zackary")

    def test_merge_sort_salary_bounds(self):
        """Verify Merge Sort processes real numeric salary balances."""
        emp1 = FullTimeEmployee("1", "John", "Male", "IT", "Dev", "2026", 20000.00, "j@corp.com", "111")
        emp2 = FullTimeEmployee("2", "Jane", "Female", "IT", "Lead", "2026", 80000.00, "j2@corp.com", "222")
        
        # Test Ascending
        asc_sorted = self.sorter.merge_sort([emp1, emp2], criteria="salary", reverse=False)
        self.assertEqual(asc_sorted[0].get_salary(), 20000.00)
        
        # Test Descending
        desc_sorted = self.sorter.merge_sort([emp1, emp2], criteria="salary", reverse=True)
        self.assertEqual(desc_sorted[0].get_salary(), 80000.00)


class TestPayrollBusinessLogic(unittest.TestCase):
    """
    Unit tests verifying structural inheritance definitions and accounting breakdowns.
    """

    def test_fulltime_employee_deductions_and_net(self):
        """Verify statutory percentages and daily calculation rates for Full-Time staff."""
        ft_emp = FullTimeEmployee("FT01", "Jane Doe", "Female", "IT", "Engineer", "2026-01-01", 60000.00, "jane@corp.com", "123")
        
        breakdown = ft_emp.calculate_payroll_breakdown(absences_count=0)
        self.assertEqual(breakdown['gross'], 60000.00)
        self.assertEqual(breakdown['vat'], 60000.00 * 0.12)
        self.assertEqual(breakdown['absent'], 0.00)
        
        deductions = breakdown['vat'] + breakdown['ph'] + breakdown['sss'] + breakdown['pag'] + breakdown['absent']
        self.assertAlmostEqual(breakdown['net'], 60000.00 - deductions, places=2)

    def test_fulltime_employee_absence_deduction(self):
        """Verify absence count maps to financial deduction rates based on a 22-day model."""
        ft_emp = FullTimeEmployee("FT01", "Jane Doe", "Female", "IT", "Engineer", "2026-01-01", 44000.00, "jane@corp.com", "123")
        
        breakdown = ft_emp.calculate_payroll_breakdown(absences_count=2)
        self.assertAlmostEqual(breakdown['absent'], 4000.00, places=2)

    def test_parttime_employee_overtime_multiplier(self):
        """Verify hourly wage calculation increments with your verified 1.5x overtime multiplier."""
        pt_emp = PartTimeEmployee("PT01", "Bob V", "Male", "Sales", "Rep", "2026-01-01", 45.00, 1000.00, "bob@corp.com", "456")
        
        breakdown = pt_emp.calculate_payroll_breakdown(hours_override=45.00)
        expected_reg = 40 * 1000.00
        expected_ot = 5 * (1000.00 * 1.5)  # Matches your system's 1.5x Phil Labor standard
        expected_gross = expected_reg + expected_ot
        
        self.assertEqual(breakdown['reg_pay'], expected_reg)
        self.assertEqual(breakdown['ot_pay'], expected_ot)
        self.assertEqual(breakdown['gross'], expected_gross)


class TestFileDatabaseHandling(unittest.TestCase):
    """
    Integration tests focusing on file-system state serialization and saving.
    """

    def setUp(self):
        self.test_dir = "db_test_sandbox"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
            
        self.file_handler = PayrollDataFileHandling()
        self.file_handler.emp_filename = os.path.join(self.test_dir, "employees_test.txt")
        self.file_handler.history_filename = os.path.join(self.test_dir, "history_test.txt")
        self.file_handler.config_filename = os.path.join(self.test_dir, "config_test.txt")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_save_and_load_employees_integration(self):
        """Verify data saves and parses perfectly into isolated memory slots without file leakage pollution."""
        emp = FullTimeEmployee("TEST_ID_999", "Test Character", "Male", "QA", "Tester", "2026-05-14", 30000.00, "test@corp.com", "000")
        
        # Save to database file sandbox
        self.file_handler.save_employees([emp])
        
        # Explicitly clean the manager array before isolation injection
        test_manager = PayrollSystemManager()
        test_manager.employees.clear() 
        
        # Pull data directly from our testing file handle sandbox rather than production singletons
        raw_loaded_data = self.file_handler.load_employees_from_file()
        test_manager.load_system_data(raw_loaded_data)
        
        # Verify parameters match perfectly on the parsed test array bounds
        self.assertEqual(len(test_manager.employees), 1)
        self.assertEqual(test_manager.employees[0].name, "Test Character")
        self.assertEqual(test_manager.employees[0].emp_type, "Full-Time")

    def test_save_and_retrieve_salary_slips_matrix(self):
        """Verify history tracking file matrices preserve transaction logs."""
        self.file_handler.save_salary_slip_record(
            "999", "Test Character", "QA", "Tester", "Full-Time", 
            30000.00, 0.00, 30000.00, 3600.00, 500.00, 500.00, 100.00, 0.00, 25300.00, "May 14, 2026"
        )
        
        history_ledger = self.file_handler.get_all_salary_slips()
        self.assertIn("999", history_ledger)
        self.assertEqual(history_ledger["999"][0]["name"], "Test Character")
        self.assertEqual(history_ledger["999"][0]["net"], 25300.00)


class TestSystemManagerState(unittest.TestCase):
    """
    Integration tests covering operational system behaviors inside runtime memory.
    """

    def setUp(self):
        self.manager = PayrollSystemManager()
        self.manager.employees.clear()
        self.manager.file_handler = MagicMock()

    def test_add_and_search_employee_lifecycle(self):
        """Verify registration workflows and unique fuzzy text lookups."""
        unique_test_name = "XyloCompanyUniqueName"
        self.manager.add_fulltime_employee("T10", unique_test_name, "Male", "Admin", "Chief", "2026", 90000.00, "john@corp.com", "777")
        
        found_emp = self.manager.search_employee_by_id("T10")
        self.assertIsNotNone(found_emp)
        self.assertEqual(found_emp.name, unique_test_name)
        
        fuzzy_results = self.manager.search_employees_by_name("xylocompany")
        self.assertEqual(len(fuzzy_results), 1)

    def test_delete_employee_scrubbing(self):
        """Verify records are safely stripped out upon removal requests."""
        self.manager.add_fulltime_employee("T20", "Temporary Worker", "Male", "Temp", "Staff", "2026", 15000.00, "temp@corp.com", "000")
        
        success, name = self.manager.delete_employee_by_id("T20")
        self.assertTrue(success)
        self.assertEqual(name, "Temporary Worker")
        
        self.assertIsNone(self.manager.search_employee_by_id("T20"))


if __name__ == "__main__":
    unittest.main()