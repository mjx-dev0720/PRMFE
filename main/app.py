from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime

# Import your custom modules
from payroll_sys import PayrollSystemManager
from dsa_algo import PayrollAlgo, PayrollQueue

# Initialize the shared backend systems
manager = PayrollSystemManager()
algo = PayrollAlgo()
process_queue = PayrollQueue()

dept_pos_map = {
    "Human Resources": ["HR Manager", "Recruiter", "Training Specialist", "Compensation Analyst"],
    "Engineering & Development": ["Software Engineer", "Embedded Systems Developer", "Mobile App Developer", "DevOps Engineer", "QA Automation Engineer"],
    "Data & Security": ["AI Engineer", "Data Scientist", "Cybersecurity Analyst", "Database Administrator"],
    "Support & Operations": ["UI/UX Developer", "Technical Support Lead", "Operations Coordinator", "Project Manager"],
    "IT Infrastructure & Cloud": ["Cloud Architect", "Network Engineer", "Systems Administrator", "IT Helpdesk"]
}

salary_rates = {
    "Software Engineer": {"Full": 60000, "Part": 600}, "Embedded Systems Developer": {"Full": 65000, "Part": 650},
    "Mobile App Developer": {"Full": 55000, "Part": 550}, "DevOps Engineer": {"Full": 70000, "Part": 700},
    "QA Automation Engineer": {"Full": 50000, "Part": 500}, "AI Engineer": {"Full": 85000, "Part": 850},
    "Data Scientist": {"Full": 80000, "Part": 800}, "Cybersecurity Analyst": {"Full": 75000, "Part": 750},
    "Database Administrator": {"Full": 65000, "Part": 650}, "HR Manager": {"Full": 45000, "Part": 450},
    "Recruiter": {"Full": 35000, "Part": 350}, "Training Specialist": {"Full": 40000, "Part": 400},
    "Compensation Analyst": {"Full": 42000, "Part": 420}, "UI/UX Developer": {"Full": 50000, "Part": 500},
    "Technical Support Lead": {"Full": 35000, "Part": 350}, "Operations Coordinator": {"Full": 38000, "Part": 380},
    "Project Manager": {"Full": 65000, "Part": 650}, "Cloud Architect": {"Full": 95000, "Part": 950},
    "Network Engineer": {"Full": 55000, "Part": 550}, "Systems Administrator": {"Full": 50000, "Part": 500},
    "IT Helpdesk": {"Full": 25000, "Part": 250}
}

def launch_app():
    root = Tk()
    root.title("Payroll Management System")
    root.geometry("1280x720")
    root.configure(bg="#f4f6f9")
    
    # Configure global styling/theme options
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=("Arial", 10))
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#e1e5eb")
    
    # Simple top-level container for tracking the currently visible screen frame
    current_frame = [None]

    # Shared UI state variables
    selected_emp_type = StringVar(value="None")
    sort_criteria = StringVar(value="Name")
    sort_order = StringVar(value="Ascending")

    # ---------------------------------------------------------
    # ROUTING & SCREEN NAVIGATION ENGINE
    # ---------------------------------------------------------
    def switch_to(page_builder_func):
        """Clears the current screen layout and swaps in a new page view."""
        if current_frame[0] is not None:
            current_frame[0].destroy()
        
        # Build the new UI screen frame context container
        new_frame = Frame(root, bg="#f4f6f9")
        new_frame.pack(fill="both", expand=True)
        current_frame[0] = new_frame
        
        # Populate the newly constructed view matrix
        page_builder_func(new_frame)

    def create_navigation_sidebar(parent, active_page=""):
        """Generates a synchronized clean left navigation control bar."""
        sidebar = Frame(parent, bg="#2c3e50", width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Title brand block
        lbl_brand = Label(sidebar, text="PAYROLL SYSTEM", font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#2c3e50", pady=20)
        lbl_brand.pack()
        
        # Helper to construct nav action triggers
        def nav_btn(text, target_func, page_name):
            is_active = (page_name == active_page)
            btn = Button(
                sidebar, text=text, font=("Arial", 10, "bold" if is_active else "normal"),
                fg="#ffffff" if is_active else "#bdc3c7",
                bg="#34495e" if is_active else "#2c3e50",
                activebackground="#34495e", activeforeground="#ffffff",
                bd=0, cursor="hand2", anchor="w", padx=20, pady=12,
                command=lambda: switch_to(target_func)
            )
            btn.pack(fill="x")

        nav_btn("🏠 Home Dashboard", build_home_page, "home")
        nav_btn("⚙️ Process Queue", build_process_page, "process")
        nav_btn("👥 View Employees", build_view_employees_page, "employees")
        nav_btn("📜 Payroll History", build_history_page, "history")
        
        # Divider split gap line
        Frame(sidebar, bg="#34495e", height=2).pack(fill="x", pady=10)
        
        # Logout trigger button control
        btn_logout = Button(
            sidebar, text="🚪 Log Out", font=("Arial", 10), fg="#e74c3c", bg="#2c3e50",
            activebackground="#c0392b", activeforeground="#ffffff", bd=0, cursor="hand2",
            anchor="w", padx=20, pady=12, command=lambda: switch_to(build_login_page)
        )
        btn_logout.pack(fill="x", side="bottom")

    # ---------------------------------------------------------
    # BEAUTIFUL TOPLEVEL PAYSLIP GENERATOR WINDOW
    # ---------------------------------------------------------
    def show_beautiful_payslip_window(emp, breakdown, date_str):
        """Generates a custom visual Toplevel window modal displaying a premium printed invoice look."""
        slip_win = Toplevel(root)
        slip_win.title(f"Payslip Record Summary - ID {emp.id}")
        slip_win.geometry("500x650")
        slip_win.configure(bg="#ffffff")
        slip_win.resizable(False, False)
        slip_win.grab_set()  # Lock focus onto this popup window context

        # Master Canvas / Container with corporate clean palette borders
        main_box = Frame(slip_win, bg="#ffffff", bd=2, relief="groove", padx=25, pady=20)
        main_box.pack(fill="both", expand=True, padx=15, pady=15)

        # Header Block
        Label(main_box, text="OFFICIAL SALARY DISBURSEMENT SLIP", font=("Arial", 13, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=(0, 2))
        Label(main_box, text=f"Processing Execution Timestamp: {date_str}", font=("Arial", 9, "italic"), bg="#ffffff", fg="#7f8c8d").pack(pady=(0, 15))

        # Structural Meta Data Frame Grid Panel
        meta_frame = Frame(main_box, bg="#f8f9fa", padx=10, pady=10, bd=1, relief="solid")
        meta_frame.pack(fill="x", pady=5)
        
        def add_meta_row(lbl1, val1, lbl2, val2, r):
            Label(meta_frame, text=lbl1, font=("Arial", 9, "bold"), bg="#f8f9fa", fg="#34495e").grid(row=r, column=0, sticky="w", pady=3)
            Label(meta_frame, text=val1, font=("Arial", 9), bg="#f8f9fa", fg="#2c3e50").grid(row=r, column=1, sticky="w", padx=(5, 20), pady=3)
            Label(meta_frame, text=lbl2, font=("Arial", 9, "bold"), bg="#f8f9fa", fg="#34495e").grid(row=r, column=2, sticky="w", pady=3)
            Label(meta_frame, text=val2, font=("Arial", 9), bg="#f8f9fa", fg="#2c3e50").grid(row=r, column=3, sticky="w", pady=3)

        add_meta_row("Employee ID:", emp.id, "Full Name:", emp.name, 0)
        add_meta_row("Department:", emp.department, "Position:", emp.position, 1)
        add_meta_row("Type:", emp.emp_type, "Bank Account:", emp.bank_account if emp.bank_account else "N/A", 2)

        # Itemized Details Headers
        Label(main_box, text="FINANCIAL BREAKDOWN DETAILS", font=("Arial", 10, "bold"), bg="#ffffff", fg="#2c3e50").pack(anchor="w", pady=(15, 5))

        ledger_frame = Frame(main_box, bg="#ffffff")
        ledger_frame.pack(fill="x", pady=5)

        def add_ledger_item(title, amount, is_deduction=False, is_bold=False):
            f_style = ("Arial", 10, "bold" if is_bold else "normal")
            color = "#c0392b" if is_deduction else ("#27ae60" if is_bold and not is_deduction else "#2c3e50")
            prefix = "-" if is_deduction and amount > 0 else ""
            
            row = Frame(ledger_frame, bg="#ffffff")
            row.pack(fill="x", pady=4)
            Label(row, text=title, font=f_style, bg="#ffffff", fg="#34495e").pack(side="left")
            Label(row, text=f"{prefix}₱{amount:,.2f}", font=f_style, bg="#ffffff", fg=color).pack(side="right")

        # Earnings Array Breakdown Elements
        add_ledger_item("Base Regular Compensation Credits", breakdown["reg_pay"])
        add_ledger_item("Supplemental Overtime Allowances", breakdown["ot_pay"])
        
        # Divider Line
        Frame(ledger_frame, bg="#bdc3c7", height=1).pack(fill="x", pady=6)
        add_ledger_item("GROSS CONSOLIDATED EARNINGS", breakdown["gross"], is_bold=True)
        Frame(ledger_frame, bg="#bdc3c7", height=1).pack(fill="x", pady=6)

        # Deductions Sections
        add_ledger_item("Withholding Tax (VAT Obligation)", breakdown["vat"], is_deduction=True)
        add_ledger_item("PhilHealth Contribution Premium", breakdown["ph"], is_deduction=True)
        add_ledger_item("SSS Insurance Contribution Premium", breakdown["sss"], is_deduction=True)
        add_ledger_item("Pag-IBIG Mutual Fund Deduction", breakdown["pag"], is_deduction=True)
        add_ledger_item("Unexcused Absences Penalty Deductions", breakdown["absent"], is_deduction=True)

        # Total Consolidated Summary Frame
        Frame(ledger_frame, bg="#2c3e50", height=2).pack(fill="x", pady=(15, 5))
        
        total_deductions = breakdown["vat"] + breakdown["ph"] + breakdown["sss"] + breakdown["pag"] + breakdown["absent"]
        add_ledger_item("TOTAL CONSOLIDATED DEDUCTIONS", total_deductions, is_deduction=True, is_bold=True)
        
        Frame(ledger_frame, bg="#2c3e50", height=1).pack(fill="x", pady=5)
        
        # Big Net Pay Banner Box Area Frame Layout Context Block
        net_box = Frame(main_box, bg="#ebf5fb", pady=10, padx=10, bd=1, relief="solid")
        net_box.pack(fill="x", pady=15)
        Label(net_box, text="NET TAKE-HOME DISBURSEMENT", font=("Arial", 11, "bold"), bg="#ebf5fb", fg="#2980b9").pack(side="left")
        Label(net_box, text=f"₱{breakdown['net']:,.2f}", font=("Arial", 13, "bold"), bg="#ebf5fb", fg="#2980b9").pack(side="right")

        Button(main_box, text="Close Invoice Sheet View", font=("Arial", 10), bg="#7f8c8d", fg="#ffffff", bd=0, padx=15, pady=6, cursor="hand2", command=slip_win.destroy).pack(side="bottom", pady=5)
    # ---------------------------------------------------------
    # PAGE 1: ADMIN LOGIN PAGE
    # ---------------------------------------------------------
    def build_login_page(container):
        # Center presentation anchoring block frame layout wrapper
        login_card = LabelFrame(container, bg="#ffffff", bd=1, relief="solid", padx=30, pady=30)
        login_card.place(relx=0.5, rely=0.5, anchor="center")
        
        lbl_title = Label(login_card, text="Admin LOGIN", font=("Arial", 16, "bold"), bg="#ffffff", fg="#2c3e50")
        lbl_title.pack(pady=(0, 20))
        
        Label(login_card, text="Username:", font=("Arial", 10), bg="#ffffff", fg="#7f8c8d").pack(anchor="w")
        ent_user = Entry(login_card, font=("Arial", 11), width=28, bd=1, relief="solid")
        ent_user.pack(pady=(5, 15))
        
        Label(login_card, text="Password:", font=("Arial", 10), bg="#ffffff", fg="#7f8c8d").pack(anchor="w")
        ent_pass = Entry(login_card, font=("Arial", 11), width=28, bd=1, relief="solid", show="*")
        ent_pass.pack(pady=(5, 20))

        def execute_login_auth():
            username = ent_user.get().strip()
            password = ent_pass.get().strip()
            # Intercept credentials against DB handling layer
            if manager.db.read_admin_data(username, password):
                switch_to(build_home_page)
            else:
                messagebox.showerror("Auth Error", "Invalid Administrative login entry keys.")

        btn_login = Button(
            login_card, text="Sign In", font=("Arial", 11, "bold"), fg="#ffffff", bg="#2980b9",
            activebackground="#3498db", activeforeground="#ffffff", bd=0, cursor="hand2",
            width=26, pady=8, command=execute_login_auth
        )
        btn_login.pack()

    # ---------------------------------------------------------
    # PAGE 2: HOME DASHBOARD PAGE (Add / Edit Form)
    # ---------------------------------------------------------
    def build_home_page(container):
        create_navigation_sidebar(container, active_page="home")
        
        # Main content body context view pane area
        content = Frame(container, bg="#f4f6f9", padx=25, pady=20)
        content.pack(side="right", fill="both", expand=True)
        
        lbl_header = Label(content, text="System Master Control Dashboard", font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#2c3e50")
        lbl_header.pack(anchor="w", pady=(0, 15))
        
        # Form Container Group Wrapper Box Layout Frame block
        form_frame = LabelFrame(content, text=" Employee Registration & Master Record Modifier ", bg="#ffffff", font=("Arial", 10, "bold"), padx=15, pady=15)
        form_frame.pack(fill="x", expand=False)

        # --- Automatic Field Generations Engine Sequences ---
        # 1. Fetch next ID tracking counter value straight from the storage layer configuration properties
        auto_generated_id = str(manager.db.next_id_counter)
        # 2. Extract localized calendar datestamp for real-time automatic injection 
        auto_current_hire_date = datetime.now().strftime("%B %d, %Y")
        
        # Layout grids mapping positioning configurator setup rows
        Label(form_frame, text="Employee ID:", font=("Arial", 10, "bold"), bg="#ffffff", fg="#7f8c8d").grid(row=0, column=0, sticky="e", padx=5, pady=6)
        id_search_frame = Frame(form_frame, bg="#ffffff")
        id_search_frame.grid(row=0, column=1, sticky="w", padx=5, pady=6)

        ent_id = Entry(id_search_frame, font=("Arial", 11, "bold"), bg="#ebf5fb", fg="#2980b9", width=16, bd=1, relief="solid")
        ent_id.pack()
        ent_id.insert(END, auto_generated_id)
        emp_search_btn = Button(id_search_frame, text="Search", font=("Arial", 10, "bold"),height=8,width=12, fg="#ffffff", bg="#fff700", bd=0, padx=20, pady=10, cursor="hand2", command="").pack(side="left", padx=5)
        emp_search_btn.pack(side="left", padx=5, pady=6)

        Label(form_frame, text="Full Name *:", font=("Arial", 10), bg="#ffffff", fg="#34495e").grid(row=0, column=2, sticky="e", padx=5, pady=6)
        ent_name = Entry(form_frame, font=("Arial", 10), width=20, bd=1, relief="solid")
        ent_name.grid(row=0, column=3, sticky="w", padx=5, pady=6)

        Label(form_frame, text="Gender:", font=("Arial", 10), bg="#ffffff", fg="#34495e").grid(row=0, column=4, sticky="e", padx=5, pady=6)
        cb_gender = ttk.Combobox(form_frame, values=["Male", "Female", "Other"], width=10, state="readonly")
        cb_gender.grid(row=0, column=5, sticky="w", padx=5, pady=6)

        # Cascading Reactive Dropdown Controls Block
        Label(form_frame, text="Department *:", font=("Arial", 10), bg="#ffffff", fg="#34495e").grid(row=1, column=0, sticky="e", padx=5, pady=6)
        cb_dept = ttk.Combobox(form_frame, values=list(dept_pos_map.keys()), width=18, state="readonly")
        cb_dept.grid(row=1, column=1, sticky="w", padx=5, pady=6)

        Label(form_frame, text="Position *:", font=("Arial", 10), bg="#ffffff", fg="#34495e").grid(row=1, column=2, sticky="e", padx=5, pady=6)
        cb_pos = ttk.Combobox(form_frame, values=[], width=22, state="readonly")
        cb_pos.grid(row=1, column=3, sticky="w", padx=5, pady=6)

        Label(form_frame, text="Hire Date:", font=("Arial", 10, "bold"), bg="#ffffff", fg="#7f8c8d").grid(row=1, column=4, sticky="e", padx=5, pady=6)
        lbl_show_date = Label(form_frame, text=auto_current_hire_date, font=("Arial", 10), bg="#f8f9fa", fg="#34495e", width=12, anchor="w", padx=5, bd=1, relief="solid")
        lbl_show_date.grid(row=1, column=5, sticky="w", padx=5, pady=6)

        Label(form_frame, text="Email Address *:", font=("Arial", 10), bg="#ffffff", fg="#34495e").grid(row=2, column=0, sticky="e", padx=5, pady=6)
        ent_email = Entry(form_frame, font=("Arial", 10), width=20, bd=1, relief="solid")
        ent_email.grid(row=2, column=1, sticky="w", padx=5, pady=6)

        Label(form_frame, text="Bank Account *:", font=("Arial", 10), bg="#ffffff", fg="#34495e").grid(row=2, column=2, sticky="e", padx=5, pady=6)
        ent_bank = Entry(form_frame, font=("Arial", 10), width=22, bd=1, relief="solid")
        ent_bank.grid(row=2, column=3, sticky="w", padx=5, pady=6)

        # Classification Type Selector Controls
        Label(form_frame, text="Employee Type:", font=("Arial", 10), bg="#ffffff", fg="#34495e").grid(row=3, column=0, sticky="e", padx=5, pady=6)
        rb_frame = Frame(form_frame, bg="#ffffff")
        rb_frame.grid(row=3, column=1, columnspan=2, sticky="w")
        
        # Dynamic Automation Configuration Trigger Methods Bound directly into form dropdown bindings
        def sync_wage_rates_to_fields(*args):
            position_selected = cb_pos.get()
            if position_selected in salary_rates:
                rates = salary_rates[position_selected]
                if selected_emp_type.get() == "Full-Time":
                    lbl_v1.config(text="Monthly Salary:", fg="#7f8c8d", font=("Arial", 10, "bold"))
                    ent_v1.delete(0, END)
                    ent_v1.insert(0, str(rates["Full"]))
                    ent_v1.config(state="readonly")
                    
                    lbl_v2.grid_remove()
                    ent_v2.grid_remove()
                else:
                    lbl_v1.config(text="Hours Worked *:", fg="#34495e", font=("Arial", 10, "normal"))
                    ent_v1.config(state="normal")
                    ent_v1.delete(0, END)
                    
                    lbl_v2.grid()
                    ent_v2.grid()
                    lbl_v2.config(text="Hourly Rate (Auto):", fg="#7f8c8d", font=("Arial", 10, "bold"))
                    ent_v2.config(state="normal")
                    ent_v2.delete(0, END)
                    ent_v2.insert(0, str(rates["Part"]))
                    ent_v2.config(state="readonly")

        def on_department_change_event(*args):
            dept_selected = cb_dept.get()
            if dept_selected in dept_pos_map:
                positions_available = dept_pos_map[dept_selected]
                cb_pos.config(values=positions_available)
                cb_pos.set(positions_available[0]) # Default cascading fallback select configuration step
                sync_wage_rates_to_fields()

        cb_dept.bind("<<ComboboxSelected>>", on_department_change_event)
        cb_pos.bind("<<ComboboxSelected>>", sync_wage_rates_to_fields)

        Radiobutton(rb_frame, text="Full-Time", variable=selected_emp_type, value="Full-Time", bg="#ffffff", command=sync_wage_rates_to_fields).pack(side="left", padx=5)
        Radiobutton(rb_frame, text="Part-Time", variable=selected_emp_type, value="Part-Time", bg="#ffffff", command=sync_wage_rates_to_fields).pack(side="left", padx=5)

        # Monetary Data Fields Area Rows
        lbl_v1 = Label(form_frame, text="Monthly Salary", font=("Arial", 10), bg="#ffffff", fg="#34495e")
        lbl_v1.grid(row=4, column=0, sticky="e", padx=5, pady=6)
        ent_v1 = Entry(form_frame, font=("Arial", 10), width=20, bd=1, relief="solid")
        ent_v1.grid(row=4, column=1, sticky="w", padx=5, pady=6)

        lbl_v2 = Label(form_frame, text="Hourly Rate", font=("Arial", 10), bg="#ffffff", fg="#34495e")
        lbl_v2.grid(row=4, column=2, sticky="e", padx=5, pady=6)
        ent_v2 = Entry(form_frame, font=("Arial", 10), width=22, bd=1, relief="solid")
        ent_v2.grid(row=4, column=3, sticky="w", padx=5, pady=6)

        # --- IMPROVED DATA VALIDATIONS ENGINE ---
        def run_validate_and_add():
            name = ent_name.get().strip()
            dept = cb_dept.get()
            pos = cb_pos.get()
            email = ent_email.get().strip()
            bank = ent_bank.get().strip()

            # Strict field completion checks
            if not name or not email or not bank:
                messagebox.showwarning("Validation Error", "All fields marked with an asterisk (*) must be fully completed.")
                return
            if len(name) < 2:
                messagebox.showerror("Validation Error", "Please parse a realistic name configuration containing at least 2 characters.")
                return
            if "@" not in email or "." not in email:
                messagebox.showerror("Validation Error", "Invalid Email formatting string parsed.")
                return
            if "-" in bank and len(bank) == 14:
                messagebox.showerror("Validation Error", "Bank Account field configuration must be purely this format (XXXX-XXXX-XXXX)")
                return

            try:
                eid = ent_id.cget("text")
                hire_dt = lbl_show_date.cget("text")

                if selected_emp_type.get() == "Full-Time":
                    salary_val = float(ent_v1.get() or 0.0)
                    manager.add_fulltime_employee(
                        eid, name, cb_gender.get(), dept, pos, hire_dt, salary_val, email, bank
                    )
                else:
                    # Capture variable user tracking entries for part time hours worked allocations
                    hours_worked_str = ent_v1.get().strip()
                    if not hours_worked_str:
                        messagebox.showwarning("Validation Error", "Please provide a numeric configuration entry tracking total hours worked details.")
                        return
                    hours_val = float(hours_worked_str or 40.0)
                    rate_val = float(ent_v2.get() or 0.0)
                    
                    if hours_val < 0 or hours_val > 744: # Check logical physical thresholds inside calendar constraints 
                        messagebox.showerror("Validation Error", "Total hours worked entry value falls outside logical operational bounds.")
                        return

                    manager.add_parttime_employee(
                        eid, name, cb_gender.get(), dept, pos, hire_dt, hours_val, rate_val, email, bank
                    )
                
                messagebox.showinfo("Success", f"Successfully recorded employee master account registry for {name} linked under Unique identifier ID: {eid}.")
                switch_to(build_home_page) # Refresh workspace frame panel block cleanly to advance automated state loops
            except ValueError:
                messagebox.showerror("Validation Error", "Numeric data conversion operations returned exceptions matching raw field text blocks.")

        # Action Buttons Dock Layout Frame
        btn_frame = Frame(content, bg="#f4f6f9")
        btn_frame.pack(fill="x", pady=15)

        def run_update():
            emp = manager.search_employee_by_id(auto_generated_id)
            if not emp:
                messagebox.showwarning("Missing key ID", "Please specify an existing unique targeting Employee ID parameter to query.")
                return
            
            if selected_emp_type.get() == "Full-Time":
                ok = manager.update_fulltime_employee(
                    emp.id, emp.name, emp.gender, emp.department,
                    emp.position, emp.hire_date, ent_v1.get() or 0,
                    emp.email, emp.bank_account
                )
            else:
                ok = manager.update_parttime_employee(
                    emp.id, emp.name, emp.gender, emp.department,
                    emp.position, emp.hire_date, ent_v1.get() or 0, ent_v2.get() or 0,
                    emp.email, emp.bank_account
                )
            
            if ok:
                messagebox.showinfo("Success", f"Successfully updated administrative system configurations data for: {emp.name}.")
            else:
                messagebox.showerror("Update Missed Error Target", f"The query tracker engine returned empty references matching ID.")

        def run_delete():
            emp = manager.search_employee_by_id(auto_generated_id)
            if not emp:
                messagebox.showwarning("Selection ID Key Error", "Please parse an Employee ID into the form target row field to locate deletion entry tracking records.")
                return
            ok, name = manager.delete_employee_by_id(emp.id)
            if ok:
                messagebox.showinfo("Record Dropped", f"Successfully expunged and wiped active working system registries for {name}.")
                run_clear()
            else:
                messagebox.showerror("Drop Fault Engine Exception", "The execution processor returned exceptions tracing targeted database reference keys.")

        def run_clear():
            
            ent_v1.delete(0, END)
            ent_v2.delete(0, END)

        Button(btn_frame, text="📥 Save New Automated Profile Record", font=("Arial", 10, "bold"), fg="#ffffff", bg="#27ae60", bd=0, padx=20, pady=10, cursor="hand2", command=run_validate_and_add).pack(side="left", padx=5)
        Button(btn_frame, text="🔄 Commit Data Update", font=("Arial", 10, "bold"), fg="#ffffff", bg="#2980b9", bd=0, padx=15, pady=8, cursor="hand2", command=run_update).pack(side="left", padx=5)
        Button(btn_frame, text="❌ Purge Record Account", font=("Arial", 10, "bold"), fg="#ffffff", bg="#c0392b", bd=0, padx=15, pady=8, cursor="hand2", command=run_delete).pack(side="left", padx=5)
        Button(btn_frame, text="🧹 Reset Working Form", font=("Arial", 10), fg="#2c3e50", bg="#bdc3c7", bd=0, padx=15, pady=8, cursor="hand2", command=run_clear).pack(side="left", padx=5)
    # ---------------------------------------------------------
    # PAGE 3: PROCESS PAGE (FIFO Pipeline Processing Engine)
    # ---------------------------------------------------------
    def build_process_page(container):
        create_navigation_sidebar(container, active_page="process")
        
        content = Frame(container, bg="#f4f6f9", padx=25, pady=20)
        content.pack(side="right", fill="both", expand=True)
        
        lbl_header = Label(content, text="FIFO Processing Pipeline Line Queue Dashboard", font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#2c3e50")
        lbl_header.pack(anchor="w", pady=(0, 15))
        
        # Side-by-side presentation view column panels frame block area
        panels = Frame(content, bg="#f4f6f9")
        panels.pack(fill="both", expand=True)
        
        left_panel = LabelFrame(panels, text=" Active System Registries Database Array Source ", bg="#ffffff", font=("Arial", 10, "bold"), padx=10, pady=10)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_panel = LabelFrame(panels, text=" FIFO Pipeline Assembly Vector Queue Line State ", bg="#ffffff", font=("Arial", 10, "bold"), padx=10, pady=10)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # LEFT TREE: Active Employees Frame Block
        cols_l = ("id", "name", "type")
        tree_l = ttk.Treeview(left_panel, columns=cols_l, show="headings", height=15)
        tree_l.heading("id", text="ID")
        tree_l.heading("name", text="Employee Name")
        tree_l.heading("type", text="Type")
        tree_l.column("id", width=60, anchor="center")
        tree_l.column("name", width=160, anchor="w")
        tree_l.column("type", width=90, anchor="center")
        tree_l.pack(fill="both", expand=True)
        
        for emp in manager.employees:
            tree_l.insert("", "end", values=(emp.id, emp.name, emp.emp_type))

        # RIGHT LISTBOX: Visual representation array tracking list elements tracking lines
        lbl_counter = Label(right_panel, text=f"Pending Pipeline Backlog Load: {process_queue.get_size()} items in line", font=("Arial", 10, "bold"), bg="#ffffff", fg="#d35400")
        lbl_counter.pack(anchor="w", pady=(0, 5))
        
        lb_q = Listbox(right_panel, font=("Courier", 10), bd=1, relief="solid")
        lb_q.pack(fill="both", expand=True)
        
        def render_current_queue_state():
            lb_q.delete(0, END)
            # Peek view into structural contents of underlying queue array tracking collections list
            for item in list(process_queue._queue):
                lb_q.insert(END, f" [{item.id}] -> {item.name} ({item.emp_type})")
            lbl_counter.config(text=f"Pending Pipeline Backlog Load: {process_queue.get_size()} items in line")

        render_current_queue_state()

        # Processing Pipeline Operations Actions Logic Functions Block
        def push_selection_to_line():
            selected = tree_l.selection()
            if not selected:
                messagebox.showwarning("Selection Missing Context", "Please select an employee tracking row entry inside the registry column module first.")
                return
            eid = tree_l.item(selected[0], "values")[0]
            emp_obj = manager.search_employee_by_id(eid)
            if emp_obj:
                process_queue.enqueue(emp_obj)
                render_current_queue_state()

        def resolve_next_in_line():
            if process_queue.is_empty():
                messagebox.showinfo("Pipeline Load Idle", "There are currently zero entries waiting computational resolution queue allocations pipeline lanes.")
                return
            
            emp = process_queue.dequeue()
            breakdown = emp.calculate_payroll_breakdown()
            today = datetime.now().strftime("%B %d, %Y")
            
            # Persist the snapshot into the ledger using DB layers directly
            manager.db.save_salary_slip_record(
                emp.id, emp.name, emp.department, emp.position, emp.emp_type,
                breakdown["reg_pay"], breakdown["ot_pay"], breakdown["gross"],
                breakdown["vat"], breakdown["ph"], breakdown["sss"], breakdown["pag"],
                breakdown["absent"], breakdown["net"], today
            )
            
            render_current_queue_state()
            
            slip_view = (
                f"=== INDIVIDUAL TRANSACTION PAYSLIP ACCOUNT RECORD MATRIX ===\n"
                f"Transaction Timestamp: {today}\n"
                f"Profile ID: {emp.id} | Account Name: {emp.name}\n"
                f"Assigned Allocation Position Status Matrix: {emp.position} ({emp.emp_type})\n"
                f"-----------------------------------------------------------\n"
                f" Gross Earnings Base Pay Allocation: ₱{breakdown['gross']:.2f}\n"
                f"    - Base Regular Compensation Core:  ₱{breakdown['reg_pay']:.2f}\n"
                f"    - Supplemental Overtime Credits:  ₱{breakdown['ot_pay']:.2f}\n"
                f" Total Consolidated Regulatory Deductions: ₱{(breakdown['vat'] + breakdown['ph'] + breakdown['sss'] + breakdown['pag'] + breakdown['absent']):.2f}\n"
                f"-----------------------------------------------------------\n"
                f" NET CALCULATED TAKE-HOME DISBURSEMENT: ₱{breakdown['net']:.2f}"
            )
            messagebox.showinfo("Pipeline Processing Resolution Success Output", slip_view)

        # Trigger Controls Bar Row Block Panel Box
        ctrl_bar = Frame(content, bg="#f4f6f9")
        ctrl_bar.pack(fill="x", pady=15)
        
        Button(ctrl_bar, text="📥 Enqueue Selected Employee", font=("Arial", 10, "bold"), fg="#ffffff", bg="#d35400", bd=0, padx=12, pady=8, cursor="hand2", command=push_selection_to_line).pack(side="left", padx=5)
        Button(ctrl_bar, text="⚙️ Process Next In Line (Dequeue)", font=("Arial", 10, "bold"), fg="#ffffff", bg="#2980b9", bd=0, padx=12, pady=8, cursor="hand2", command=resolve_next_in_line).pack(side="left", padx=5)

    # ---------------------------------------------------------
    # PAGE 4: VIEW EMPLOYEES PAGE (Sorting & Algorithmic Matrix)
    # ---------------------------------------------------------
    def build_view_employees_page(container):
        create_navigation_sidebar(container, active_page="employees")
        
        content = Frame(container, bg="#f4f6f9", padx=25, pady=20)
        content.pack(side="right", fill="both", expand=True)
        
        lbl_header = Label(content, text="System Master Employee Record Registries", font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#2c3e50")
        lbl_header.pack(anchor="w", pady=(0, 15))
        
        # Sorting Control Configuration Panel Block Frame area 
        sort_frame = LabelFrame(content, text=" Algorithmic Merge-Sort Workspace Configuration Matrix Controls ", bg="#ffffff", font=("Arial", 10, "bold"), padx=10, pady=10)
        sort_frame.pack(fill="x", pady=(0, 15))
        
        Label(sort_frame, text="Sort Evaluation Parameter Key:", font=("Arial", 10), bg="#ffffff").pack(side="left", padx=5)
        cb_crit = ttk.Combobox(sort_frame, textvariable=sort_criteria, values=["Name", "ID", "Salary"], width=10, state="readonly")
        cb_crit.pack(side="left", padx=5)
        
        Label(sort_frame, text="Vector Sequence Direction:", font=("Arial", 10), bg="#ffffff").pack(side="left", padx=5)
        cb_dir = ttk.Combobox(sort_frame, textvariable=sort_order, values=["Ascending", "Descending"], width=12, state="readonly")
        cb_dir.pack(side="left", padx=5)

        # Output Core Representation Grid Data Spreadsheet Block Area Frame
        grid_frame = Frame(content)
        grid_frame.pack(fill="both", expand=True)
        
        cols = ("id", "name", "type", "dept", "pos", "salary")
        tree = ttk.Treeview(grid_frame, columns=cols, show="headings")
        tree.heading("id", text="ID Link")
        tree.heading("name", text="Employee Profile Name")
        tree.heading("type", text="Classification")
        tree.heading("dept", text="Department Core")
        tree.heading("pos", text="Position Assigned")
        tree.heading("salary", text="Evaluated Base Salary")
        
        tree.column("id", width=70, anchor="center")
        tree.column("name", width=180, anchor="w")
        tree.column("type", width=90, anchor="center")
        tree.column("dept", width=120, anchor="center")
        tree.column("pos", width=120, anchor="center")
        tree.column("salary", width=120, anchor="e")
        
        scroller = ttk.Scrollbar(grid_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroller.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scroller.pack(side="right", fill="y")

        def evaluate_and_render_sorted_records():
            tree.delete(*tree.get_children())
            
            raw_base_array = list(manager.employees)
            
            # Map visual presentation names cleanly into string arguments used by the back-end merge-sort algorithm
            crit_mapping = {"Name": "alphabetical", "ID": "id", "Salary": "salary"}
            backend_criteria = crit_mapping.get(sort_criteria.get(), "name")
            reverse_flag = True if sort_order.get() == "Descending" else False
            
            # Fire operations matching requirements via backend algorithms
            processed_data_matrix = algo.merge_sort(raw_base_array, criteria=backend_criteria, reverse=reverse_flag)
            
            for emp in processed_data_matrix:
                tree.insert("", "end", values=(
                    emp.id, emp.name, emp.emp_type,
                    emp.department, emp.position, f"₱{emp.get_salary():,.2f}"
                ))

        Button(sort_frame, text="⚡ Re-Sort Data Array Matrix", font=("Arial", 10, "bold"), fg="#ffffff", bg="#8e44ad", bd=0, padx=12, pady=4, cursor="hand2", command=evaluate_and_render_sorted_records).pack(side="left", padx=15)
        
        # Initial compilation run on screen presentation entry sequence loading loop
        evaluate_and_render_sorted_records()

    # ---------------------------------------------------------
    # PAGE 5: VIEW PAYROLL HISTORY PAGE
    # ---------------------------------------------------------
    def build_history_page(container):
        create_navigation_sidebar(container, active_page="history")
        
        content = Frame(container, bg="#f4f6f9", padx=25, pady=20)
        content.pack(side="right", fill="both", expand=True)
        
        lbl_header = Label(content, text="Historical Payroll Ledger Transactions System Records", font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#2c3e50")
        lbl_header.pack(anchor="w", pady=(0, 15))
        
        grid_frame = Frame(content)
        grid_frame.pack(fill="both", expand=True)
        
        cols = ("date", "id", "name", "gross", "deductions", "net")
        tree = ttk.Treeview(grid_frame, columns=cols, show="headings")
        tree.heading("date", text="Process Date")
        tree.heading("id", text="ID Link")
        tree.heading("name", text="Employee Name")
        tree.heading("gross", text="Gross Total")
        tree.heading("deductions", text="Deductions")
        tree.heading("net", text="Net Take Home")
        
        tree.column("date", width=100, anchor="center")
        tree.column("id", width=70, anchor="center")
        tree.column("name", width=180, anchor="w")
        tree.column("gross", width=120, anchor="e")
        tree.column("deductions", width=120, anchor="e")
        tree.column("net", width=120, anchor="e")
        
        scroller = ttk.Scrollbar(grid_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroller.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scroller.pack(side="right", fill="y")
        
        # Pull raw item history data snapshots collection from storage via DB handling layer
        history_matrix = manager.db.get_all_salary_slips()
        
        for emp_id, slips in history_matrix.items():
            for slip in slips:
                total_deductions = slip["vat"] + slip["ph"] + slip["sss"] + slip["pag"] + slip["absent"]
                tree.insert("", "end", values=(
                    slip["date"], emp_id, slip["name"],
                    f"₱{slip['gross']:,.2f}", f"₱{total_deductions:,.2f}", f"₱{slip['net']:,.2f}"
                ))

    # ---------------------------------------------------------
    # APP MAIN ENTRY TRIGGER INITIALIZATION
    # ---------------------------------------------------------
    # Route into Auth Page view frame layout context initially
    switch_to(build_login_page)
    root.mainloop()

if __name__ == "__main__":
    launch_app()