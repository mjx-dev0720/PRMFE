import unittest
import os
import shutil
from unittest.mock import MagicMock, patch
import customtkinter as ctk

# Import your GUI and system components
from payroll_gui import ProcessEmployeeFrame 
from payroll_sys import PayrollSystemManager, PartTimeEmployee, FullTimeEmployee


class TestPayrollGUIInteractions(unittest.TestCase):
    """
    Automated integration tests validating CustomTkinter frame inputs, 
    value capture mechanics, and window rendering behaviors.
    """

    def setUp(self):
        # Initialize a top-level window acting as our test root anchor
        self.root = ctk.CTk()
        self.root.withdraw()  # Keeps the window invisible during the test run

        # Set up mock structures inside our root application frame context
        self.root.payroll_system = PayrollSystemManager()
        self.root.payroll_system.employees.clear()
        
        # Create a real mock file handler to capture incoming save data streams
        self.root.file_handler = MagicMock()
        self.root.salary_records = MagicMock()

        # Create a mock Part-Time employee and inject them into memory
        self.mock_pt_emp = PartTimeEmployee(
            id="PT-99", name="Marc Jay", gender="Male", department="Engineering", 
            position="Developer", hire_date="2026-01-01", hours_worked=40.0, 
            hourly_rate=1000.0, email="marc@corp.com", bank_account="987654"
        )
        self.root.payroll_system.employees.append(self.mock_pt_emp)

        # Build a safe stub function on the root mock to catch window popup requests safely
        if not hasattr(self.root, 'open_payslip_window'):
            self.root.open_payslip_window = MagicMock()

        # Instantiate the frame we want to test
        self.frame = ProcessEmployeeFrame(self.root)
        self.frame.pack()
        self.root.update_idletasks()  # Forces Tkinter to build layout geometries

    def tearDown(self):
        # Prevent "after script" memory thread leakage from CustomTkinter loops
        try:
            self.root.quit()
        except:
            pass
        self.frame.destroy()
        self.root.destroy()

    def test_overtime_entry_override_flow(self):
        """Verify that typing 70 hours into the GUI dynamically overrides baseline hours."""
        
        # Simulate typing an ID into the search box
        self.frame.search_id_entry.delete(0, 'end')
        self.frame.search_id_entry.insert(0, "PT-99")
        
        # Set up hours entry frame field parameters
        if hasattr(self.frame, 'hours_entry'):
            self.frame.hours_entry.configure(state="normal")
            self.frame.hours_entry.delete(0, 'end')
            self.frame.hours_entry.insert(0, "70")
        
        # Patch out the popup window layer to ensure headless execution runs smoothly
        with patch.object(self.frame, 'open_payslip_window', create=True) as mock_local_popup, \
             patch.object(self.root, 'open_payslip_window', create=True) as mock_root_popup:
            
            # Execute your compute button callback sequence
            self.frame.compute_payroll()
            
            # Verify the file system layer was signaled to save the calculated breakdown parameters
            self.root.file_handler.save_salary_slip_record.assert_called_once()
            
            # Extract the raw positional parameters passed into your file handling layer!
            called_args = self.root.file_handler.save_salary_slip_record.call_args[0]
            
            # mapping parameters matching save_salary_slip_record structure:
            # args: (id, name, dept, pos, type, reg_pay, ot_pay, gross, vat, ph, sss, pag, absent, net, date)
            saved_reg_pay = called_args[5]
            saved_ot_pay = called_args[6]
            saved_gross_pay = called_args[7]
            
            # Assert that the overtime math calculated 70 hours instead of 40!
            # Regular Pay: 40 hours * 1000 = 40,000
            # Overtime Pay: 30 hours * (1000 * 1.5 multiplier) = 45,000
            # Gross Pay: 40,000 + 45,000 = 85,000
            self.assertEqual(saved_reg_pay, 40000.0)
            self.assertEqual(saved_ot_pay, 45000.0)
            self.assertEqual(saved_gross_pay, 85000.0)

    def test_invalid_hours_input_error_handling(self):
        """Verify that typing letters into the numeric entry fields triggers an alert pop-up."""
        self.frame.search_id_entry.insert(0, "PT-99")
        if hasattr(self.frame, 'hours_entry'):
            self.frame.hours_entry.configure(state="normal")
            self.frame.hours_entry.delete(0, 'end')
            self.frame.hours_entry.insert(0, "INVALID_STRING_TEXT")

        # Intercept Tkinter's alert box message stream
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.frame.compute_payroll()
            
            # Verify that an error popup caught the mistake and alerted the user
            mock_error.assert_called_once()


if __name__ == "__main__":
    unittest.main()