import customtkinter as ctk
from tkinter import messagebox, ttk
from payroll_sys import *
from db_handling import PayrollDataFileHandling
import datetime
from dsa_algo import *

#Admin Login Frame
class AdminLoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success,  width=800, height=500, fg_color="#e0e0e0", border_color="black", border_width=1, corner_radius=0):
        super().__init__(master, width=width, height=height, fg_color=fg_color, 
                        border_color=border_color, border_width=border_width, 
                        corner_radius=corner_radius)
        
        self.master.bind('<Return>', lambda event: self.login_action())
        
        self.on_login_success = on_login_success
        self.primary_font = ctk.CTkFont(family="Helvetica", size=18)

        ctk.CTkLabel(self,
                    text="Admin Login", 
                    font=("Helvetica", 48), 
                    text_color="black"
                    ).place(relx=0.5, rely=0.25, anchor="center")

        ctk.CTkLabel(self, 
                    text="Username", 
                    font=self.primary_font, 
                    text_color="black"
                    ).place(relx=0.35, rely=0.45, anchor="e")

        self.username_entry = ctk.CTkEntry(self, 
                                            width=220, 
                                            height=40, 
                                            fg_color="white", 
                                            border_color="black", 
                                            text_color="black", 
                                            corner_radius=10,
                                            font=self.primary_font
                                            )
        self.username_entry.place(relx=0.42, rely=0.45, anchor="w")

        ctk.CTkLabel(self, 
                    text="Password", 
                    font=self.primary_font, 
                    text_color="black"
                    ).place(relx=0.35, rely=0.55, anchor="e")

        self.password_entry = ctk.CTkEntry(self, 
                                            width=220, 
                                            height=40, 
                                            fg_color="white", 
                                            border_color="black", 
                                            text_color="black", 
                                            show="*", 
                                            corner_radius=10,
                                            font=self.primary_font
                                            )
        self.password_entry.place(relx=0.42, rely=0.55, anchor="w")

        self.show_pass_var = ctk.StringVar(value="off")
        self.show_pass = ctk.CTkCheckBox(self, 
                                        text="Show Password", 
                                        fg_color="#93d97d", 
                                        text_color="black", 
                                        hover_color="green" ,  
                                        variable=self.show_pass_var, 
                                        onvalue="on", offvalue="off", 
                                        command=self.toggle_show_password,
                                        font=self.primary_font
                                        )
        self.show_pass.place(relx=0.62, rely=0.65, anchor="e")

        self.login_button = ctk.CTkButton(self, 
                                        text="Login", 
                                        font=("Helvetica", 20, "bold"), 
                                        fg_color="#93d97d", 
                                        hover_color="#7cb368", 
                                        text_color="white", 
                                        width=120, 
                                        height=45, 
                                        corner_radius=8, 
                                        command=self.login_action,
                                        )
        self.login_button.place(relx=0.56, rely=0.75, anchor="center")

    def toggle_show_password(self):
        if self.show_pass_var.get() == "on":
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.master.file_handler.read_admin_data(username, password):
            self.master.unbind('<Return>')
            messagebox.showinfo("Success!", "Welcome Back {}".format(username))
            self.on_login_success(username)
        else:
            messagebox.showerror("Error", "Invalid Credentials")

#Home Page Frame
class HomePageFrame(ctk.CTkFrame):
    def __init__(self, master, username="admin"):
        super().__init__(master, fg_color="white")

        self.primary_font = ctk.CTkFont(family="Helvetica", size=18)

        ctk.CTkLabel(self, 
                    bg_color="#12E068", 
                    width=1280, 
                    height=50, 
                    text="Payroll Management System for Employees", 
                    text_color="black", 
                    font=("Helvetica", 20, "bold")
                    ).pack(side="top", fill="x")
        
        self.logout_btn = ctk.CTkButton(self, 
                                        text="Logout", 
                                        width=100, 
                                        height=30, 
                                        fg_color="#e74c3c",
                                        hover_color="#c0392b",
                                        text_color="white",
                                        font=("Helvetica", 12, "bold"),
                                        command=self.master.handle_logout
                                        )
        self.logout_btn.place(relx=0.98, rely=0.015, anchor="ne")
        
        ctk.CTkLabel(self, 
                    text=f"Welcome {username}!",
                    font=("Helvetica", 75, "bold"), 
                    text_color="black"
                    ).pack(pady=(75, 25))
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10, expand=True)
        
        create_btn = ctk.CTkButton(btn_frame, 
                                    text="Create", 
                                    height=65, 
                                    width=150, 
                                    fg_color="transparent", 
                                    text_color="black", 
                                    border_width=3, 
                                    border_color="black", 
                                    hover_color="#12E068", 
                                    command=self.open_create_employee_win,
                                    font=self.primary_font
                                    )
        create_btn.grid(row=1, column=0, padx=(0,20), pady=5)

        ctk.CTkLabel(btn_frame, 
                    text="Create EMPLOYEE", 
                    font=self.primary_font, 
                    text_color="black"
                    ).grid(row=1, column=1, padx=5, pady=5)

        del_btn = ctk.CTkButton(btn_frame, 
                                text="Delete", 
                                height=65, 
                                width=150, 
                                fg_color="transparent", 
                                text_color="black", 
                                border_width=3, 
                                border_color="black", 
                                hover_color="#12E068",
                                font=self.primary_font,
                                command=self.open_delete_employee_win
                                )
        del_btn.grid(row=2, column=0, padx=(0,20), pady=5)
        ctk.CTkLabel(btn_frame, 
                    text="Delete EMPLOYEE", 
                    font=self.primary_font, 
                    text_color="black"
                    ).grid(row=2, column=1, padx=5, pady=5)

        search_btn = ctk.CTkButton(btn_frame, 
                                    text="Search", 
                                    height=65, 
                                    width=150, 
                                    fg_color="transparent", 
                                    text_color="black", 
                                    border_width=3, 
                                    border_color="black", 
                                    hover_color="#12E068",
                                    font=self.primary_font,
                                    command=self.open_search_employee_win
                                    )
        search_btn.grid(row=3, column=0, padx=(0,20), pady=5)
        ctk.CTkLabel(btn_frame, 
                    text="Search EMPLOYEE", 
                    font=self.primary_font, 
                    text_color="black"
                    ).grid(row=3, column=1, padx=5, pady=5)
        
        edit_btn = ctk.CTkButton(btn_frame, 
                                    text="Edit/Update", 
                                    height=65, 
                                    width=150, 
                                    fg_color="transparent", 
                                    text_color="black", 
                                    border_width=3, 
                                    border_color="black", 
                                    hover_color="#12E068", 
                                    command=self.open_edit_employee_win,
                                    font=self.primary_font
                                    )
        edit_btn.grid(row=4, column=0, padx=(0,20), pady=(5,50))

        ctk.CTkLabel(btn_frame, 
                    text="Edit/Update EMPLOYEE", 
                    font=self.primary_font, 
                    text_color="black"
                    ).grid(row=4, column=1, padx=5, pady=(5, 50))

        process_btn = ctk.CTkButton(btn_frame, 
                                    text="Process", 
                                    height=65, 
                                    width=150, 
                                    fg_color="transparent", 
                                    text_color="black", 
                                    border_width=3, 
                                    border_color="black", 
                                    hover_color="#12E068",
                                    font=self.primary_font,
                                    command=self.master.show_process_page
                                    )
        process_btn.grid(row=5, column=0, padx=(0,20), pady=5)
        ctk.CTkLabel(btn_frame, 
                    text="Process EMPLOYEE", 
                    font=self.primary_font, 
                    text_color="black"
                    ).grid(row=5, column=1, padx=5, pady=5)

        view_all_lbl = ctk.CTkLabel(self, 
            text="View All Employees", 
            font=self.primary_font, 
            text_color="blue", 
            cursor="hand2"    
            )
        view_all_lbl.pack(side="right", padx=20)
        view_all_lbl.bind("<Button-1>", lambda e: self.master.show_view_all_page())
        view_records_lbl = ctk.CTkLabel(self, 
            text="View All Transaction History", 
            font=self.primary_font, 
            text_color="blue", 
            cursor="hand2"    
            )
        view_records_lbl.pack(side="right", padx=20)
        view_records_lbl.bind("<Button-1>", lambda e: self.master.show_salary_records_page())
    
    #Open Create Employee Window
    def open_create_employee_win(self):
        self.create_emp = ctk.CTkToplevel(self.winfo_toplevel())
        self.create_emp.title("Creating Employee")
        self.create_emp.geometry("500x700")
        self.create_emp.configure(fg_color="#e0e0e0")
        self.create_emp.deiconify()

        self.create_emp.protocol("WM_DELETE_WINDOW", self.event_exit_create_win)

        self.dept_pos_map = {
                "Human Resources": [
                    "HR Manager", "Recruiter", "Training Specialist", "Compensation Analyst"
                ],
                "Engineering & Development": [
                    "Software Engineer", "Embedded Systems Developer", "Mobile App Developer", 
                    "DevOps Engineer", "QA Automation Engineer"
                ],
                "Data & Security": [
                    "AI Engineer", "Data Scientist", "Cybersecurity Analyst", "Database Administrator"
                ],
                "Support & Operations": [
                    "UI/UX Developer", "Technical Support Lead", "Operations Coordinator", "Project Manager"
                ],
                "IT Infrastructure & Cloud": [
                    "Cloud Architect", "Network Engineer", "Systems Administrator", "IT Helpdesk"
                ]
        } 

        self.salary_rates = {
                # Engineering
                "Software Engineer": {"Full": 60000, "Part": 600},
                "Embedded Systems Developer": {"Full": 65000, "Part": 650},
                "Mobile App Developer": {"Full": 55000, "Part": 550},
                "DevOps Engineer": {"Full": 70000, "Part": 700},
                "QA Automation Engineer": {"Full": 50000, "Part": 500},
    
                # Data & Security
                "AI Engineer": {"Full": 85000, "Part": 850},
                "Data Scientist": {"Full": 80000, "Part": 800},
                "Cybersecurity Analyst": {"Full": 75000, "Part": 750},
                "Database Administrator": {"Full": 65000, "Part": 650},
    
                # HR
                "HR Manager": {"Full": 45000, "Part": 450},
                "Recruiter": {"Full": 35000, "Part": 350},
                "Training Specialist": {"Full": 40000, "Part": 400},
                "Compensation Analyst": {"Full": 42000, "Part": 420},
    
                # Support & Ops
                "UI/UX Developer": {"Full": 50000, "Part": 500},
                "Technical Support Lead": {"Full": 35000, "Part": 350},
                "Operations Coordinator": {"Full": 38000, "Part": 380},
                "Project Manager": {"Full": 65000, "Part": 650},

                # Infrastructure
                "Cloud Architect": {"Full": 95000, "Part": 950},
                "Network Engineer": {"Full": 55000, "Part": 550},
                "Systems Administrator": {"Full": 50000, "Part": 500},
                "IT Helpdesk": {"Full": 25000, "Part": 250}
        }

        ctk.CTkLabel(self.create_emp, 
                    text="Employee Information", 
                    text_color="black", 
                    font=("Helvetica", 40, "bold")
                    ).pack(padx=5, pady=15)
        
        ctk.CTkLabel(self.create_emp, 
                    text="Basic Information", 
                    text_color="black", 
                    font=self.primary_font
                    ).pack(padx=5, pady=5)

        self.field_frame = ctk.CTkFrame(self.create_emp, fg_color="#e0e0e0", width=450, height=600)
        self.field_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(self.field_frame, 
                    text="ID", 
                    text_color="black", 
                    font=self.primary_font
                    ).grid(row=0, column=0, sticky="w", padx=5, pady=10)
        
        next_id = self.master.file_handler.get_next_id() 
        self.id_entry = ctk.CTkEntry(self.field_frame, width=175, height=30, font=self.primary_font)
        self.id_entry.grid(row=0, column=1)
        self.id_entry.insert(0, str(next_id))
        self.id_entry.configure(state="readonly")


        ctk.CTkLabel(self.field_frame, 
                    text="Type", 
                    text_color="black", 
                    font=self.primary_font
                    ).grid(row=0, column=2, sticky="e", padx=5, pady=10)
        
        self.emp_dropdown = ctk.CTkComboBox(self.field_frame, 
                                            values=["Part-Time", "Full-Time"], 
                                            width=135, 
                                            state="readonly", 
                                            font=self.primary_font, 
        command=lambda status: [self.handle_emp_status(status), self.update_salary_display(self.position_dropdown.get())])
        self.emp_dropdown.grid(row=0, column=3)

        ctk.CTkLabel(self.field_frame, 
                    text="Name", 
                    text_color="black", 
                    font=self.primary_font
                    ).grid(row=1, column=0, sticky="w", padx=5, pady=10)
        self.name_entry = ctk.CTkEntry(self.field_frame, width=175, height=30, font=self.primary_font)
        self.name_entry.grid(row=1, column=1)

        ctk.CTkLabel(self.field_frame, 
                    text="Gender", 
                    text_color="black", 
                    font=self.primary_font
                    ).grid(row=1, column=2, sticky="e", padx=5, pady=10)

        gender_val = ["Male", "Female"]
        self.gender_dropdown = ctk.CTkComboBox(self.field_frame, values=gender_val, width=135, state="readonly", font=self.primary_font)
        self.gender_dropdown.grid(row=1, column=3)

        ctk.CTkLabel(self.field_frame, 
                    text="Department", 
                    text_color="black", 
                    font=self.primary_font
                    ).grid(row=2, column=0, sticky="w", padx=5, pady=10)
        
        self.department_dropdown = ctk.CTkComboBox(self.field_frame, values=list(self.dept_pos_map.keys()), width=250, state="readonly", font=self.primary_font, command=self.update_position_list)
        self.department_dropdown.grid(row=2, column=1, columnspan=2)

        ctk.CTkLabel(self.field_frame, 
                    text="Position", 
                    text_color="black", 
                    font=self.primary_font
                    ).grid(row=3, column=0, sticky="w", padx=5, pady=10)
        
        self.position_dropdown = ctk.CTkComboBox(self.field_frame, values=[], width=250, state="readonly", font=self.primary_font, command=self.update_salary_display)
        self.position_dropdown.grid(row=3, column=1, columnspan=2)

        ctk.CTkLabel(self.create_emp, 
                    text="Salary Information", 
                    text_color="black", 
                    font=self.primary_font
                    ).pack(padx=5, pady=5)
        
        self.salary_frame = ctk.CTkFrame(self.create_emp, fg_color="#e0e0e0", width=450, height=600)
        self.salary_frame.pack(fill="x", padx=5, pady=5)

        self.salary_label = ctk.CTkLabel(
                    self.salary_frame, 
                    text="Base Salary" , 
                    font=self.primary_font
                    )
        self.salary_label.grid(row=0, column=0)
        
        self.salary_entry = ctk.CTkEntry(self.salary_frame, width=100, height=30, font=self.primary_font)
        self.salary_entry.grid(row=0, column=1)
        self.salary_entry.insert(0, "₱0")
        self.salary_entry.configure(state="readonly")

        self.hours_worked_label = ctk.CTkLabel(
                    self.salary_frame, 
                    text="Hours Worked" , 
                    font=self.primary_font
                    )
        
        self.hours_worked = ctk.CTkEntry(self.salary_frame, width=100, height=30, font=self.primary_font)

        ctk.CTkLabel(self.salary_frame, 
                    text="Email", 
                    text_color="black", 
                    font=self.primary_font
                    ).grid(row=1, column=0, sticky="w", padx=5, pady=10)

        self.email_entry = ctk.CTkEntry(self.salary_frame, width=235, height=30, font=self.primary_font)
        self.email_entry.grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=10)

        ctk.CTkLabel(self.salary_frame, 
                    text="Bank Account", 
                    text_color="black", 
                    font=self.primary_font
                    ).grid(row=2, column=0, sticky="w", padx=5, pady=10)

        self.bank_entry = ctk.CTkEntry(self.salary_frame, width=235, height=30, font=self.primary_font)
        self.bank_entry.grid(row=2, column=1, columnspan=2, sticky="w", padx=5, pady=10)


        self.save_btn = ctk.CTkButton(
                                    self.create_emp, 
                                    text="Save Employee", 
                                    font=self.primary_font,
                                    fg_color="#12E068",
                                    text_color="black",
                                    command=self.handle_employee_data
                                    )
        self.save_btn.pack(pady=20)

        self.toplevelwindow = self.save_btn.winfo_toplevel()
    
    #Logic to automaticallly insert the position
    def update_position_list(self, selected_dept):
        positions = self.dept_pos_map.get(selected_dept, [])
        self.position_dropdown.configure(values=positions)
        self.position_dropdown.set("") 
    
        self.salary_entry.configure(state="normal")
        self.salary_entry.delete(0, "end")
        self.salary_entry.insert(0, "₱0")
        self.salary_entry.configure(state="readonly")

    #Logic to automatically insert the salary
    def update_salary_display(self, pos):
        is_part_time = self.emp_dropdown.get() == "Part-Time"
        rates = self.salary_rates.get(pos, {"Full": 0, "Part": 0})
        amount = rates["Part"] if is_part_time else rates["Full"]

        self.salary_entry.configure(state="normal")
        self.salary_entry.delete(0, "end")
        self.salary_entry.insert(0, f"₱{amount}")
        self.salary_entry.configure(state="readonly")

    #Logic For Employee Type Entries Showing
    def handle_emp_status(self, status):
        if status == "Part-Time":
            self.salary_label.configure(text="Hourly Rate")
            self.hours_worked_label.grid(row=0, column=2, sticky="e", padx=5, pady=10)
            self.hours_worked.grid(row=0, column=3, sticky="e", padx=5, pady=10)
        else:
            self.salary_label.configure(text="Monthly Salary")
            self.hours_worked.delete(0, "end")
            self.hours_worked_label.grid_forget()
            self.hours_worked.grid_forget()

    #Safety Net if someone accidently close the window while creating
    def event_exit_create_win(self):
        if self.name_entry.get() != "":
            if messagebox.askyesno("Exit", "You have unsaved data. Are you sure you want to close this window?"):
                self.create_emp.destroy()
            else:
                self.toplevelwindow.lift()
                self.toplevelwindow.focus_force()
        else:
            self.create_emp.destroy()
            

    #This Function Handle The Creation Of An Employee Object
    def handle_employee_data(self):
        try:
            manager = self.master.payroll_system
            
            #Get All Entries And Dropdown data
            eid = self.id_entry.get()
            name = self.name_entry.get()
            gender = self.gender_dropdown.get()
            dep = self.department_dropdown.get()
            pos = self.position_dropdown.get()
            emp_type = self.emp_dropdown.get()
            hire_date = datetime.datetime.now().strftime("%B %d, %Y")
            email = self.email_entry.get()
            bank_account = self.bank_entry.get()
            salary_val = float(self.salary_entry.get().replace("₱", ""))

            #Validation
            if eid == "" or name == "" or gender == "" or dep == "" or pos == "" or emp_type == "" or email == "" or bank_account == "":
                messagebox.showerror("Error", "Please Input All Fields.")
                self.toplevelwindow.lift()
                self.toplevelwindow.focus_force()
                return
            
            #auto incrementing id system
            emp_id = self.master.file_handler.commit_next_id()

            if emp_type == "Part-Time":
                hours = float(self.hours_worked.get())
                manager.add_parttime_employee(emp_id, name, gender, dep, pos, hire_date, hours, salary_val, email, bank_account)
            else:
                manager.add_fulltime_employee(emp_id, name, gender, dep, pos, hire_date, salary_val, email, bank_account)
            
            messagebox.showinfo("Success", f"Employee {name} ({pos}) saved!")

            self.toplevelwindow.lift()
            self.toplevelwindow.focus_force()

            #after creation logic
            self.salary_entry.configure(state="normal")
            self.salary_entry.delete(0, "end")
            self.salary_entry.insert(0, "₱0")
            self.salary_entry.configure(state="readonly")

            next_id = self.master.file_handler.get_next_id()
            self.id_entry.configure(state="normal")
            self.id_entry.delete(0, "end")
            self.id_entry.insert(0, str(next_id))
            self.id_entry.configure(state="readonly")

            self.name_entry.delete(0, "end")
            self.gender_dropdown.set("")
            self.emp_dropdown.set("")
            self.department_dropdown.set("")
            self.position_dropdown.set("")
            self.position_dropdown.configure(values=[])
            self.email_entry.delete(0, "end")
            self.bank_entry.delete(0, "end")
    
            self.hours_worked.delete(0, "end")
            self.name_entry.focus()
        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all numeric fields (Salary/Hours) are filled correctly.")
            self.toplevelwindow.lift()
            self.toplevelwindow.focus_force()

    #Open Delete Employee Window
    def open_delete_employee_win(self):
        self.del_win = ctk.CTkToplevel(self.winfo_toplevel())
        self.del_win.title("Delete Employee")
        self.del_win.geometry("400x250")
        self.del_win.attributes("-topmost", True)

        ctk.CTkLabel(self.del_win, text="Remove Employee", font=("Helvetica", 24, "bold")).pack(pady=20)
        
        ctk.CTkLabel(self.del_win, text="Enter Employee Name or ID:", font=self.primary_font).pack(pady=5)
        
        self.del_id_entry = ctk.CTkEntry(self.del_win, width=200, font=self.primary_font)
        self.del_id_entry.pack(pady=10)
        self.del_id_entry.focus()

        delete_confirm_btn = ctk.CTkButton(self.del_win, 
                                        text="Confirm Deletion", 
                                        fg_color="#e74c3c",
                                        hover_color="#c0392b",
                                        command=self.handle_delete_action)
        delete_confirm_btn.pack(pady=20)

    #This Function Handle The Deletion of Employee
    def handle_delete_action(self):
        query = self.del_id_entry.get().strip()
        manager = self.master.payroll_system

        if not query:
            messagebox.showwarning("Input Required", "Please enter a Name or ID.")
            return

        emp = manager.search_employee_by_id(query)
        if not emp:
            matches = manager.search_employees_by_name(query)
            if len(matches) == 1:
                emp = matches[0]
            elif len(matches) > 1:
                messagebox.showwarning("Ambiguous Name", "Multiple employees found with that name. Please use the specific ID.")
                self.del_win.lift()
                return

        if emp:
            if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete {emp.name} (ID: {emp.id})?"):
                manager.delete_employee_by_name(emp)
                messagebox.showinfo("Deleted", f"Employee {emp.name} has been removed.")
                self.del_win.destroy()
        else:
            messagebox.showerror("Not Found", f"No record found for '{query}'.")
            self.del_win.lift()

    #Open Search Employee Window
    def open_search_employee_win(self):
        self.search_win = ctk.CTkToplevel(self.winfo_toplevel())
        self.search_win.title("Search Employee")
        self.search_win.geometry("400x600")
        self.search_win.attributes("-topmost", True)

        ctk.CTkLabel(self.search_win, text="Employee Search", font=("Helvetica", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(self.search_win, text="Enter Employee Name or ID:", font=self.primary_font).pack(pady=5)
        
        self.search_id_entry = ctk.CTkEntry(self.search_win, width=200)
        self.search_id_entry.pack(pady=10)
        self.search_id_entry.focus()

        ctk.CTkButton(self.search_win, text="Search Now", command=self.handle_search_action).pack(pady=20)
        
        result_frame = ctk.CTkFrame(self.search_win, border_color="black", width=250, height=300)
        result_frame.pack(pady=10)
        ctk.CTkLabel(result_frame, text="Search Result", bg_color="#c2f0d1", height=40, width=300, 
                    text_color="black", font=self.primary_font).grid(row=0, column=0, columnspan=1, pady=(0,20))
        self.search_result = ctk.CTkLabel(result_frame, text="")
        self.search_result.grid(row=1, column=0, columnspan=1, pady=10)

    #This Function Handles The Searching Mechanism/Logic 
    def handle_search_action(self):
        query = self.search_id_entry.get().strip()
        manager = self.master.payroll_system
        
        if not query:
            messagebox.showwarning("Input Required", "Please enter a Name or ID.")
            return

        emp = manager.search_employee_by_id(query)
        
        if not emp:
            matches = manager.search_employees_by_name(query)
            if len(matches) == 1:
                emp = matches[0]
            elif len(matches) > 1:
                names = "\n".join([f"ID: {e.id} - {e.name}" for e in matches])
                self.search_result.configure(text=f"Found multiple employees:\n\n{names}\n\nPlease search by specific ID.")
                self.search_win.lift()
                return

        if emp:
            info = (f"ID: {emp.id}\nName: {emp.name}\nType: {emp.emp_type}\n"
                    f"Dept: {emp.department}\nPos: {emp.position}\n"
                    f"Salary: ₱{emp.get_salary():,.2f}")
            self.search_result.configure(text=f"Details\n{info}")
            self.search_win.lift()
        else:
            messagebox.showerror("Not Found", f"No employee found matching '{query}'.")
            self.search_win.lift()

    #Open Edit Employee Window
    def open_edit_employee_win(self):
        self.edit_prompt_win = ctk.CTkToplevel(self.winfo_toplevel())
        self.edit_prompt_win.title("Edit Employee Lookup")
        self.edit_prompt_win.geometry("380x180")
        self.edit_prompt_win.attributes("-topmost", True)
        self.edit_prompt_win.resizable(False, False)

        ctk.CTkLabel(self.edit_prompt_win, text="Enter Employee ID to Edit:", font=self.primary_font).pack(pady=15)
        self.edit_id_lookup_entry = ctk.CTkEntry(self.edit_prompt_win, width=200)
        self.edit_id_lookup_entry.pack(pady=5)
        self.edit_id_lookup_entry.focus()

        def submit_lookup():
            target_id = self.edit_id_lookup_entry.get().strip()
            manager = self.master.payroll_system
            employee_obj = manager.search_employee_by_id(target_id)

            if not employee_obj:
                messagebox.showerror("Not Found", f"No employee found with ID: '{target_id}'", parent=self.edit_prompt_win)
                return
            
            self.edit_prompt_win.destroy()
            self.launch_edit_form_window(employee_obj)

        ctk.CTkButton(self.edit_prompt_win, text="Proceed to Edit", fg_color="#12E068", text_color="black", command=submit_lookup).pack(pady=15)

    #Launches the identical form of creation but for editing employee
    def launch_edit_form_window(self, emp_obj):
        """Constructs an editing window looking EXACTLY like open_create_employee_win."""
        self.edit_emp_win = ctk.CTkToplevel(self.winfo_toplevel())
        self.edit_emp_win.title("Editing Employee Records")
        self.edit_emp_win.geometry("500x700")
        self.edit_emp_win.configure(fg_color="#e0e0e0")
        self.edit_emp_win.deiconify()

        self.dept_pos_map = {
                "Human Resources": ["HR Manager", "Recruiter", "Training Specialist", "Compensation Analyst"],
                "Engineering & Development": ["Software Engineer", "Embedded Systems Developer", "Mobile App Developer", "DevOps Engineer", "QA Automation Engineer"],
                "Data & Security": ["AI Engineer", "Data Scientist", "Cybersecurity Analyst", "Database Administrator"],
                "Support & Operations": ["UI/UX Developer", "Technical Support Lead", "Operations Coordinator", "Project Manager"],
                "IT Infrastructure & Cloud": ["Cloud Architect", "Network Engineer", "Systems Administrator", "IT Helpdesk"]
        }

        self.salary_rates = {
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

        ctk.CTkLabel(self.edit_emp_win, text="Modify Employee Info", text_color="black", font=("Helvetica", 40, "bold")).pack(padx=5, pady=15)
        ctk.CTkLabel(self.edit_emp_win, text="Basic Information", text_color="black", font=self.primary_font).pack(padx=5, pady=5)

        self.field_frame = ctk.CTkFrame(self.edit_emp_win, fg_color="#e0e0e0", width=450, height=600)
        self.field_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(self.field_frame, text="ID", text_color="black", font=self.primary_font).grid(row=0, column=0, sticky="w", padx=5, pady=10)
        self.id_entry = ctk.CTkEntry(self.field_frame, width=175, height=30, font=self.primary_font)
        self.id_entry.grid(row=0, column=1)
        self.id_entry.insert(0, str(emp_obj.id))
        self.id_entry.configure(state="readonly")

        ctk.CTkLabel(self.field_frame, text="Type", text_color="black", font=self.primary_font).grid(row=0, column=2, sticky="e", padx=5, pady=10)
        self.emp_dropdown = ctk.CTkComboBox(self.field_frame, values=["Part-Time", "Full-Time"], width=135, state="readonly", font=self.primary_font,
            command=lambda status: [self.handle_emp_status(status), self.update_salary_display(self.position_dropdown.get())])
        self.emp_dropdown.grid(row=0, column=3)
        self.emp_dropdown.set(emp_obj.emp_type)

        ctk.CTkLabel(self.field_frame, text="Name", text_color="black", font=self.primary_font).grid(row=1, column=0, sticky="w", padx=5, pady=10)
        self.name_entry = ctk.CTkEntry(self.field_frame, width=175, height=30, font=self.primary_font)
        self.name_entry.grid(row=1, column=1)
        self.name_entry.insert(0, emp_obj.name)

        ctk.CTkLabel(self.field_frame, text="Gender", text_color="black", font=self.primary_font).grid(row=1, column=2, sticky="e", padx=5, pady=10)
        self.gender_dropdown = ctk.CTkComboBox(self.field_frame, values=["Male", "Female"], width=135, state="readonly", font=self.primary_font)
        self.gender_dropdown.grid(row=1, column=3)
        self.gender_dropdown.set(emp_obj.gender)

        ctk.CTkLabel(self.field_frame, text="Department", text_color="black", font=self.primary_font).grid(row=2, column=0, sticky="w", padx=5, pady=10)
        self.department_dropdown = ctk.CTkComboBox(self.field_frame, values=list(self.dept_pos_map.keys()), width=250, state="readonly", font=self.primary_font, command=self.update_position_list)
        self.department_dropdown.grid(row=2, column=1, columnspan=2)
        self.department_dropdown.set(emp_obj.department)

        ctk.CTkLabel(self.field_frame, text="Position", text_color="black", font=self.primary_font).grid(row=3, column=0, sticky="w", padx=5, pady=10)
        initial_positions = self.dept_pos_map.get(emp_obj.department, [])
        self.position_dropdown = ctk.CTkComboBox(self.field_frame, values=initial_positions, width=250, state="readonly", font=self.primary_font, command=self.update_salary_display)
        self.position_dropdown.grid(row=3, column=1, columnspan=2)
        self.position_dropdown.set(emp_obj.position)

        ctk.CTkLabel(self.edit_emp_win, text="Salary Information", text_color="black", font=self.primary_font).pack(padx=5, pady=5)
        self.salary_frame = ctk.CTkFrame(self.edit_emp_win, fg_color="#e0e0e0", width=450, height=600)
        self.salary_frame.pack(fill="x", padx=5, pady=5)

        self.salary_label = ctk.CTkLabel(self.salary_frame, text="Base Salary", font=self.primary_font)
        self.salary_label.grid(row=0, column=0)
        
        self.salary_entry = ctk.CTkEntry(self.salary_frame, width=100, height=30, font=self.primary_font)
        self.salary_entry.grid(row=0, column=1)
        
        self.hours_worked_label = ctk.CTkLabel(self.salary_frame, text="Hours Worked", font=self.primary_font)
        self.hours_worked = ctk.CTkEntry(self.salary_frame, width=100, height=30, font=self.primary_font)

        if emp_obj.emp_type == "Part-Time":
            self.salary_label.configure(text="Hourly Rate")
            self.hours_worked_label.grid(row=0, column=2, sticky="e", padx=5, pady=10)
            self.hours_worked.grid(row=0, column=3, sticky="e", padx=5, pady=10)
            self.hours_worked.insert(0, str(emp_obj.hours_worked))
            self.salary_entry.insert(0, f"₱{emp_obj.hourly_rate}")
        else:
            self.salary_label.configure(text="Monthly Salary")
            self.salary_entry.insert(0, f"₱{emp_obj.get_salary()}")
        self.salary_entry.configure(state="readonly")

        ctk.CTkLabel(self.salary_frame, text="Email", text_color="black", font=self.primary_font).grid(row=1, column=0, sticky="w", padx=5, pady=10)
        self.email_entry = ctk.CTkEntry(self.salary_frame, width=235, height=30, font=self.primary_font)
        self.email_entry.grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=10)
        self.email_entry.insert(0, emp_obj.email)

        ctk.CTkLabel(self.salary_frame, text="Bank Account", text_color="black", font=self.primary_font).grid(row=2, column=0, sticky="w", padx=5, pady=10)
        self.bank_entry = ctk.CTkEntry(self.salary_frame, width=235, height=30, font=self.primary_font)
        self.bank_entry.grid(row=2, column=1, columnspan=2, sticky="w", padx=5, pady=10)
        self.bank_entry.insert(0, emp_obj.bank_account)

        self.save_btn = ctk.CTkButton(self.edit_emp_win, text="Update", font=self.primary_font, fg_color="#2196F3", text_color="white",
                                    command=self.handle_edit_employee_data)
        self.save_btn.pack(pady=20)
        self.toplevelwindow = self.save_btn.winfo_toplevel()

    #THis Function THe Editing LOgic
    def handle_edit_employee_data(self):
        try:
            manager = self.master.payroll_system
            eid = self.id_entry.get()
            name = self.name_entry.get().strip()
            gender = self.gender_dropdown.get()
            dep = self.department_dropdown.get()
            pos = self.position_dropdown.get()
            emp_type = self.emp_dropdown.get()
            email = self.email_entry.get().strip()
            bank_account = self.bank_entry.get().strip()

            original_emp = manager.search_employee_by_id(eid)
            hire_date = original_emp.hire_date if original_emp else "2026-01-01"
            
            if not all([eid, name, gender, dep, pos, emp_type, email, bank_account]):
                messagebox.showerror("Error", "Please fill in all empty fields.", parent=self.edit_emp_win)
                return

            if emp_type == "Part-Time":
                hours = float(self.hours_worked.get())
                rate = float(self.salary_entry.get().replace("₱", "").replace(",", ""))
                manager.update_parttime_employee(eid, name, gender, dep, pos, hire_date, hours, rate, email, bank_account)
            else:
                salary_val = float(self.salary_entry.get().replace("₱", "").replace(",", ""))
                manager.update_fulltime_employee(eid, name, gender, dep, pos, hire_date, salary_val, email, bank_account)

            messagebox.showinfo("Success", f"Employee {name}'s changes have been updated!", parent=self.edit_emp_win)
            self.edit_emp_win.destroy()
            self.edit_emp_win = None

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure numeric fields contain valid quantities.", parent=self.edit_emp_win)

#View EMployees Frame
class ViewEmployeesFrame(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master, fg_color="white")
        self.master = master

        ctk.CTkLabel(self, text="EMPLOYEE LIST", 
                    font=("Helvetica", 40, "bold"), 
                    text_color="black").pack(pady=20)
        
        container = ctk.CTkFrame(self, fg_color="white", border_color="black", border_width=1)
        container.pack(fill="both", expand=True, padx=40, pady=(10, 20))
        self.reverse_var = ctk.BooleanVar(value=False)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background="white", 
                        foreground="black", 
                        rowheight=35, 
                        fieldbackground="white", 
                        font=("Helvetica", 11))
        style.configure("Treeview.Heading", 
                        font=("Helvetica", 12, "bold"), 
                        background="#c2f0d1",
                        foreground="black")
        style.map("Treeview", background=[('selected', '#12E068')])

        cols = ("ID", "Name", "Gender", "Department", "Position", "Hire Date", "Type", "Salary")
        self.tree = ttk.Treeview(container, columns=cols, show="headings")

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.populate_data()

        sort_frame = ctk.CTkFrame(self, fg_color="white")
        sort_frame.pack(fill="both", expand=True, padx=40, pady=(10, 20))
        
        ctk.CTkLabel(sort_frame, text="Sort By", 
                    font=("Helvetica", 11), 
                    text_color="black").pack(side="left", padx=5)
        
        self.sort_dropdown = ctk.CTkComboBox(sort_frame, 
                                            values=["Alphabetical", "Salary", "Department"], 
                                            command=self.handle_sorting, 
                                            state="readonly", width=150)
        self.sort_dropdown.pack(side="left", padx=5)

        self.checkbox_sort = ctk.CTkCheckBox(
        sort_frame, 
        text="Reverse", 
        variable=self.reverse_var,
        command=self.handle_sorting
        )

        ctk.CTkButton(sort_frame, text="Back to Dashboard", 
                    command=on_back, 
                    width=200, height=40).pack(side="right", padx=5)

    #HAndles Sorting in Gui
    def handle_sorting(self, choice=None):
        sorter_tool = self.master.sorter
        
        if choice is None:
            choice = self.sort_dropdown.get()
            
        if choice == "Salary":
            if not self.checkbox_sort.winfo_ismapped(): 
                self.checkbox_sort.pack(side="left", padx=5)   
        else:
            if self.checkbox_sort.winfo_ismapped():
                self.checkbox_sort.pack_forget()

        is_reversed = self.reverse_var.get()

        original_list = list(self.master.payroll_system.employees)

        sorted_list = sorter_tool.merge_sort(original_list, choice, is_reversed)
        self.update_treeview(sorted_list)

    def update_treeview(self, employee_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for emp in employee_list:
            self.tree.insert("", "end", values=(
                emp.id, emp.name, emp.gender, emp.department, 
                emp.position, emp.hire_date, emp.emp_type, 
                f"₱{emp.get_salary():,.2f}"
            ))

    def populate_data(self):
        """Fetch and display all employees from the manager."""
        for emp in self.master.payroll_system.employees:
            self.tree.insert("", "end", values=(
                emp.id,
                emp.name,
                emp.gender,
                emp.department,
                emp.position,
                emp.hire_date,
                emp.emp_type,
                f"₱{emp.get_salary():,.2f}"
            ))

class ProcessEmployeeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#f0f0f0")
        self.master = master
        self.primary_font = ctk.CTkFont(family="Helvetica", size=16, weight="bold")
        
        ctk.CTkLabel(self, bg_color="#12E068", width=1280, height=50, 
                    text="Payroll Management System for Employees", 
                    text_color="black", font=("Helvetica", 20, "bold")).pack(side="top", fill="x")

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(expand=True, pady=20)

        # --- LEFT PANEL: EMPLOYEE DETAILS ---
        self.left_panel = ctk.CTkFrame(main_container, fg_color="white", border_color="black", border_width=1, width=500, height=500)
        self.left_panel.grid(row=0, column=0, padx=20, sticky="nsew")
        self.left_panel.grid_propagate(False)

        ctk.CTkLabel(self.left_panel, text="EMPLOYEE DETAILS", bg_color="#c2f0d1", height=40, width=500, 
                    text_color="black", font=self.primary_font).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        ctk.CTkLabel(self.left_panel, text="EMPLOYEE ID:", text_color="black", font=self.primary_font).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.search_id_entry = ctk.CTkEntry(self.left_panel, width=200, fg_color="#c2f0d1", border_color="black")
        self.search_id_entry.grid(row=1, column=1, padx=5)
        ctk.CTkButton(self.left_panel, text="SEARCH", width=100, fg_color="yellow", text_color="black", hover_color="#cccc00", 
                    command=self.handle_search).grid(row=1, column=2, padx=5)

        ctk.CTkLabel(self.left_panel, text="EMPLOYEE NAME:", text_color="black", font=self.primary_font).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(self.left_panel, width=300, fg_color="#c2f0d1", border_color="black", state="readonly")
        self.name_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(self.left_panel, text="GENDER:", text_color="black", font=self.primary_font).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.gender_entry = ctk.CTkEntry(self.left_panel, width=300, fg_color="#c2f0d1", border_color="black", state="readonly")
        self.gender_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(self.left_panel, text="DEPARTMENT:", text_color="black", font=self.primary_font).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.dept_entry = ctk.CTkEntry(self.left_panel, width=300, fg_color="#c2f0d1", border_color="black", state="readonly")
        self.dept_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(self.left_panel, text="POSITION:", text_color="black", font=self.primary_font).grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.pos_entry = ctk.CTkEntry(self.left_panel, width=300, fg_color="#c2f0d1", border_color="black", state="readonly")
        self.pos_entry.grid(row=5, column=1, columnspan=2, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(self.left_panel, text="TYPE:", text_color="black", font=self.primary_font).grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.emp_type_entry = ctk.CTkEntry(self.left_panel, width=300, fg_color="#c2f0d1", border_color="black", state="readonly")
        self.emp_type_entry.grid(row=6, column=1, columnspan=2, padx=5, pady=10, sticky="w")

        # --- RIGHT PANEL: SALARY DETAILS ---
        self.right_panel = ctk.CTkFrame(main_container, fg_color="white", border_color="black", border_width=1, width=550, height=500)
        self.right_panel.grid(row=0, column=1, padx=20, sticky="nsew")
        self.right_panel.grid_propagate(False)

        ctk.CTkLabel(self.right_panel, text="EMPLOYEE SALARY DETAILS", bg_color="#c2f0d1", height=40, width=550, 
                    text_color="black", font=self.primary_font).grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        ctk.CTkLabel(self.right_panel, text="Date", text_color="black", font=self.primary_font).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.date_entry = ctk.CTkEntry(self.right_panel, width=150, fg_color="#c2f0d1", border_color="black", state="readonly")
        self.date_entry.grid(row=1, column=1, padx=0, pady=0, sticky="w")

        self.monthly_salary_label = ctk.CTkLabel(self.right_panel, text="Monthly Salary:", font=self.primary_font)
        self.monthly_salary_entry = ctk.CTkEntry(self.right_panel, width=150)

        self.rate_label = ctk.CTkLabel(self.right_panel, text="Rate / Hour:", font=self.primary_font)
        self.rate_entry = ctk.CTkEntry(self.right_panel, width=150)

        self.hours_label = ctk.CTkLabel(self.right_panel, text="Total Hours:", font=self.primary_font)
        self.hours_entry = ctk.CTkEntry(self.right_panel, width=150)

        ctk.CTkLabel(self.right_panel, text="Working Days:", text_color="black", font=self.primary_font).grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.total_days_entry = ctk.CTkEntry(self.right_panel, width=150)
        self.total_days_entry.grid(row=4, column=1, sticky="w")
        self.total_days_entry.insert(0, "22")
        self.total_days_entry.configure(state="readonly")

        ctk.CTkLabel(self.right_panel, text="Absenses:", text_color="black", font=self.primary_font).grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.absent_entry = ctk.CTkEntry(self.right_panel, width=150)
        self.absent_entry.grid(row=5, column=1, sticky="w")

        self.compute_btn = ctk.CTkButton(self.right_panel, text="Generate PaySlip", height=45, width=120, fg_color="#12E068", 
                                        text_color="black", font=self.primary_font, command=self.compute_payroll)
        self.compute_btn.grid(row=6, column=0, columnspan=2, pady=30, padx=5, sticky="ew")

        self.add_queue_btn = ctk.CTkButton(
                                        self.right_panel, 
                                        text="Add to Batch Queue", 
                                        command=self.add_to_pay_queue,
                                        font=("Helvetica", 14),
                                        fg_color="#e67e22", 
                                        hover_color="#d35400"
                                    )
        self.add_queue_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        self.queue_status_label = ctk.CTkLabel(self.right_panel, text="Queue: 0 Employees", text_color="blue")
        self.queue_status_label.grid(row=7, column=3, columnspan=2, pady=5)

        self.bulk_queue_btn = ctk.CTkButton(self.right_panel, text="ENQUEUE ALL EMPLOYEES", height=45, width=120,
                                            fg_color="#3a7ebf", text_color="white", 
                                            command=self.bulk_enqueue_all)
        self.bulk_queue_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        ctk.CTkButton(self.right_panel, text="Get All Slip", command=self.process_and_display_all_queued).grid(row=8, column=3, pady=10, padx=10, sticky="ew")

        ctk.CTkButton(self, text="BACK", fg_color="red", width=100, height=40, font=self.primary_font,
                    command=lambda: self.master.show_home_page(self.master.auth_user)).pack(pady=10)
        
        
    def bulk_enqueue_all(self):
        """Loads all active employees from the system manager directly into the FIFO QUEUE"""
        manager = self.master.payroll_system
        queue = self.master.payroll_queue
        
        if not manager.employees:
            messagebox.showwarning("Warning", "No employee databases loaded to queue.")
            return
            
        counter = 0
        for emp in manager.employees:
            if emp not in queue._queue:
                queue.enqueue(emp)
                counter += 1
                
        self.queue_status_label.configure(text=f"Queue: {queue.get_size()} Employees")
        messagebox.showinfo("Success", f"Successfully loaded {counter} employees into the Pay-Run sequence!")

    def set_current_datetime(self):
        now = datetime.datetime.now().strftime("%B %d, %Y")
        
        self.date_entry.configure(state="normal")
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, now)
        self.date_entry.configure(state="readonly")

    def handle_search(self):
        """Logic to search for employee by ID and fill the fields."""
        query = self.search_id_entry.get().strip()
        emp = self.master.payroll_system.search_employee_by_id(query)
        
        if emp:
            fields_to_update = [
                (self.name_entry, emp.name),
                (self.gender_entry, emp.gender),
                (self.dept_entry, emp.department),
                (self.pos_entry, emp.position),
                (self.emp_type_entry, emp.emp_type)
            ]

            for entry, value in fields_to_update:
                entry.configure(state="normal")
                entry.delete(0, "end")
                entry.insert(0, value)
                entry.configure(state="readonly")

            self.set_current_datetime()

            if emp.emp_type == "Full-Time":
                self.rate_label.grid_remove()
                self.rate_entry.grid_remove()
                self.hours_label.grid_remove()
                self.hours_entry.grid_remove()
                
                self.monthly_salary_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
                self.monthly_salary_entry.grid(row=2, column=1, sticky="w")
                self.monthly_salary_entry.configure(state="normal") 
                self.monthly_salary_entry.delete(0, "end")
                self.monthly_salary_entry.insert(0, str(emp.get_salary()))
                self.monthly_salary_entry.configure(state="readonly") 
                
            else:
                self.monthly_salary_label.grid_remove()
                self.monthly_salary_entry.grid_remove()
                
                self.rate_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
                self.rate_entry.grid(row=2, column=1, sticky="w")
                self.hours_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
                self.hours_entry.grid(row=3, column=1, sticky="w")
                
                self.rate_entry.delete(0, "end")
                self.hours_entry.delete(0, "end")

                self.rate_entry.insert(0, str(emp.hourly_rate))
                self.hours_entry.insert(0, str(emp.hours_worked))
                self.rate_entry.configure(state="readonly")
        else:
            messagebox.showerror("Error", "Employee Not Found")

    def add_to_pay_queue(self):
        """Captures current screen state parameters, includes absences metrics, and stages the worker to the batch queue."""
        target_id = self.search_id_entry.get().strip() 
        if not target_id:
            messagebox.showwarning("Input Error", "Please provide a valid Employee ID to stage for batch processing.")
            return

        emp = self.master.payroll_system.search_employee_by_id(target_id)
        if not emp:
            messagebox.showerror("Not Found", f"No employee found with ID: {target_id}")
            return

        absences_input = 0.0
        if hasattr(self, 'absent_entry') and self.absent_entry.get().strip():
            try:
                absences_input = float(self.absent_entry.get().strip())
            except ValueError:
                messagebox.showerror("Typing Error", "Absences field must contain a valid number or remain empty.")
                return

        emp.staged_absences = absences_input

        self.master.payroll_queue.enqueue(emp)

        messagebox.showinfo("Queue Success", f"Employee {emp.name} (ID: {emp.id}) with {absences_input} absences has been staged in the batch run queue.")
        
        self.search_id_entry.delete(0, 'end')
        if hasattr(self, 'absent_entry'):
            self.absent_entry.delete(0, 'end')
            
        if hasattr(self, 'queue_status_label'):
            queue_size = self.master.payroll_queue.get_size()
            self.queue_status_label.configure(text=f"Queue: {queue_size} Employees")

        

    def compute_payroll(self):
        """Computes Singe Payroll"""
        import datetime
        try:
            target_id = self.search_id_entry.get().strip()
            if not target_id:
                messagebox.showwarning("Input Error", "Please provide a valid Employee ID to run payroll calculations.")
                return
        
            emp = self.master.payroll_system.search_employee_by_id(target_id)
            if not emp:
                messagebox.showerror("Not Found", f"No employee found with ID: {target_id}")
                return

            absences_input = 0
            if hasattr(self, 'absent_entry') and self.absent_entry.get().strip():
                try:
                    absences_input = float(self.absent_entry.get().strip())
                except ValueError:
                    messagebox.showerror("Typing Error", "Absences field must contain a valid number.")
                    return

            current_date = datetime.datetime.now().strftime("%B %d, %Y")

            hours_val = None
            if emp.emp_type == "Part-Time":
                if hasattr(self, 'hours_entry') and self.hours_entry.get().strip():
                    try:
                        hours_val = float(self.hours_entry.get().strip())
                    except ValueError:
                        messagebox.showerror("Typing Error", "Hours Worked field must contain a valid numeric number.")
                        return
                else:
                    hours_val = getattr(emp, 'hours_worked', 40.0)

            pay_data = emp.calculate_payroll_breakdown(hours_override=hours_val, absences_count=absences_input)


            self.master.file_handler.save_salary_slip_record(
            str(emp.id), emp.name, emp.department, emp.position, emp.emp_type,
            pay_data["reg_pay"], pay_data["ot_pay"], pay_data["gross"],
            pay_data["vat"], pay_data["ph"], pay_data["sss"], pay_data["pag"],
            pay_data["absent"], pay_data["net"], current_date
            )

            self.master.salary_records.add_record(str(emp.id), emp.name, pay_data["net"])
            if hasattr(self, 'gross_salary_entry'):
                self.gross_salary_entry.delete(0, 'end')
                self.gross_salary_entry.insert(0, f"{pay_data['gross']:.2f}")
            
            if hasattr(self, 'net_salary_entry'):
                self.net_salary_entry.delete(0, 'end')
                self.net_salary_entry.insert(0, f"{pay_data['net']:.2f}")


            self.display_payslip(emp, pay_data, current_date)

        except ValueError:
            messagebox.showerror("Error", "Please ensure all numeric fields are filled correctly.")

    def display_payslip(self, emp, pay_data, date_string):
        slip_toplevel = ctk.CTkToplevel(self.master)
        slip_toplevel.withdraw() 
        slip_toplevel.title(f"Official Salary Slip for {emp.name}")
        slip_toplevel.geometry("900x750")
        slip_toplevel.resizable(False, False)
        slip_toplevel.configure(fg_color="white")
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        
        banner = ctk.CTkFrame(slip_toplevel, fg_color="#c2f0d1", corner_radius=0, height=40)
        banner.pack(fill="x", side="top")
        ctk.CTkLabel(banner, text="Payroll Management System for Employees", text_color="black").pack(pady=5)

        container = ctk.CTkFrame(slip_toplevel, fg_color="white")
        container.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(container, text=f"SALARY SLIP FOR {datetime.datetime.now().strftime('%B %Y').upper()}", 
                    text_color="black", font=("Helvetica", 24, "bold")).pack()
        ctk.CTkFrame(container, height=2, fg_color="black").pack(fill="x", pady=10)

        # --- SECTION 1: TOP GRID (INFO & EARNINGS) ---
        top_grid = ctk.CTkFrame(container, fg_color="transparent")
        top_grid.pack(fill="x", pady=10)

        # Left: Info
        left_box = ctk.CTkFrame(top_grid, fg_color="transparent")
        left_box.pack(side="left", anchor="n", expand=True, fill="x", padx=(0, 20))
        ctk.CTkLabel(left_box, text="EMPLOYEE INFORMATION", text_color="black", font=("Helvetica", 14, "bold")).pack(anchor="w")
        self._create_slip_row(left_box, "EMPLOYEE NAME", emp.name)
        self._create_slip_row(left_box, "EMPLOYEE ID", emp.id)
        self._create_slip_row(left_box, "WORK POSITION", emp.position)
        self._create_slip_row(left_box, "DEPARTMENT", emp.department)

        # Right: Earnings
        right_box = ctk.CTkFrame(top_grid, fg_color="transparent")
        right_box.pack(side="right", anchor="n", expand=True, fill="x")
        ctk.CTkLabel(right_box, text="SALARY DETAILS", text_color="black", font=("Helvetica", 14, "bold")).pack(anchor="w")
        if emp.emp_type == "Part-Time":
            self._create_slip_row(right_box, "HOURLY RATE", f"Php {emp.hourly_rate:,.2f}")
            self._create_slip_row(right_box, "HOURS WORKED", f"{emp.hours_worked} hrs")
        self._create_slip_row(right_box, "REGULAR PAY", f"Php {pay_data['reg_pay']:,.2f}")
        self._create_slip_row(right_box, "OVERTIME", f"Php {pay_data['ot_pay']:,.2f}")
        self._create_slip_row(right_box, "GROSS SALARY", f"Php {pay_data['gross']:,.2f}")

        # --- SECTION 2: MID GRID (DEDUCTIONS & ADDITIONAL) ---
        mid_grid = ctk.CTkFrame(container, fg_color="transparent")
        mid_grid.pack(fill="x", pady=20)

        # Left Bottom: Deductions
        deduct_container = ctk.CTkFrame(mid_grid, fg_color="transparent")
        deduct_container.pack(side="left", anchor="n", expand=True, fill="x", padx=(0, 20))
        ctk.CTkLabel(deduct_container, text="DEDUCTIONS", text_color="black", font=("Helvetica", 14, "bold")).pack(anchor="w")
        self._create_slip_row(deduct_container, "VAT (12%)", f"Php {pay_data['vat']:,.2f}")
        self._create_slip_row(deduct_container, "PHILHEALTH (5%)", f"Php {pay_data['ph']:,.2f}")
        self._create_slip_row(deduct_container, "SSS (4%)", f"Php {pay_data['sss']:,.2f}")
        self._create_slip_row(deduct_container, "PAG-IBIG (2%)", f"Php {pay_data['pag']:,.2f}")
        self._create_slip_row(deduct_container, "ABSENCE PENALTY", f"Php {pay_data['absent']:,.2f}")
        total_ded = pay_data['vat'] + pay_data['ph'] + pay_data['sss'] + pay_data['pag'] + pay_data['absent']
        self._create_slip_row(deduct_container, "TOTAL DEDUCTIONS", f"Php {total_ded:,.2f}")

        # Right Bottom: Additional Details
        additional_container = ctk.CTkFrame(mid_grid, fg_color="transparent")
        additional_container.pack(side="right", anchor="n", expand=True, fill="x")
        ctk.CTkLabel(additional_container, text="ADDITIONAL DETAILS", text_color="black", font=("Helvetica", 14, "bold")).pack(anchor="w")
        
        end_date = datetime.datetime.now() + datetime.timedelta(days=30)
        self._create_slip_row(additional_container, "PAYMENT DATE", current_date)
        self._create_slip_row(additional_container, "PAY PERIOD", f"{current_date} - {end_date.strftime('%b %d, %Y')}")
        self._create_slip_row(additional_container, "JOIN DATE", f"{emp.hire_date}")

        # --- SECTION 3: FOOTER (NET SALARY) ---
        footer_spacer = ctk.CTkFrame(container, fg_color="transparent", height=40)
        footer_spacer.pack(fill="x")

        net_box = ctk.CTkFrame(container, fg_color="#90ee90", border_color="black", border_width=2, corner_radius=0)
        net_box.pack(side="right", pady=(20, 10))
        
        ctk.CTkLabel(net_box, text="NET SALARY RECEIVED", text_color="black", 
                    font=("Helvetica", 18, "bold"), padx=30).pack(side="left", pady=15)
        ctk.CTkLabel(net_box, text=f"Php {pay_data['net']:,.2f}", text_color="black", 
                    font=("Helvetica", 18, "bold"), padx=30).pack(side="left", pady=15)
        
        slip_toplevel.deiconify()
        slip_toplevel.attributes("-topmost", True)
        slip_toplevel.focus_force()

    def _create_slip_row(self, parent, label_text, value_text):
        """Creates a clean, explicit row with label and value aligned to ends."""
        row = ctk.CTkFrame(parent, fg_color="white", border_color="black", border_width=1, corner_radius=0)
        row.pack(fill="x")
        
        ctk.CTkLabel(row, text=label_text, text_color="black", font=("Helvetica", 11), 
                    width=140, anchor="w", padx=10).pack(side="left", pady=2)
        
        ctk.CTkLabel(row, text=value_text, text_color="black", font=("Helvetica", 11, "bold"), 
                    anchor="e", padx=10).pack(side="right", fill="x", expand=True, pady=2)
        
    def process_and_display_all_queued(self):
        """Dequeues every employee, computes salaries, saves to database, and shows an elegant batch summary window."""
        import datetime
        queue = self.master.payroll_queue

        if queue.is_empty():
            messagebox.showwarning("Empty Queue", "There are no pending employees in the pay-run queue.")
            return

        processed_slips = []
        current_date = datetime.datetime.now().strftime("%B %d, %Y")

        while not queue.is_empty():
            emp = queue.dequeue()

            absences_to_charge = getattr(emp, 'staged_absences', 0.0)
            
            hours_val = None
            if emp.emp_type == "Part-Time":
                if hasattr(self, 'hours_entry') and self.hours_entry.get().strip():
                    try:
                        hours_val = float(self.hours_entry.get().strip())
                    except ValueError:
                        messagebox.showerror("Typing Error", "Hours Worked field must contain a valid numeric number.")
                        return
                else:
                    hours_val = getattr(emp, 'hours_worked', 40.0)
            pay_data = emp.calculate_payroll_breakdown(hours_override=hours_val, absences_count=absences_to_charge)
            
            final_gross = pay_data["gross"]
            final_absent = pay_data["absent"]
            final_net = pay_data["net"]
            
            final_vat = pay_data["vat"]
            final_ph = pay_data["ph"]
            final_sss = pay_data["sss"]
            final_pag = pay_data["pag"]
            
            self.master.file_handler.save_salary_slip_record(
                str(emp.id), emp.name, emp.department, emp.position, emp.emp_type,
                pay_data["reg_pay"], pay_data["ot_pay"], final_gross,
                final_vat, final_ph, final_sss, final_pag,
                final_absent, final_net, current_date
            )

            self.master.salary_records.add_record(str(emp.id), emp.name, final_net)

            processed_slips.append({
                "date": current_date, 
                "id": str(emp.id), 
                "name": emp.name, 
                "dept": emp.department, 
                "pos": emp.position, 
                "emp_type": emp.emp_type, 
                "reg_pay": pay_data["reg_pay"], 
                "ot_pay": pay_data["ot_pay"], 
                "gross": final_gross,
                "vat": final_vat, 
                "ph": final_ph, 
                "sss": final_sss, 
                "pag": final_pag,
                "absent": final_absent, 
                "net": final_net
            })

            if hasattr(emp, 'staged_absences'):
                del emp.staged_absences

        if hasattr(self, 'queue_status_label'):
            self.queue_status_label.configure(text="Queue: 0 Employees")

        self.open_batch_summary_window(processed_slips)

    def open_batch_summary_window(self, slips_list):
        """Displays a clean window allowing users to select and inspect slips from the batch run."""
        summary_win = ctk.CTkToplevel(self.master)
        summary_win.title("Batch Payroll Execution Summary")
        summary_win.geometry("950x650")
        summary_win.resizable(False, False)
        summary_win.configure(fg_color="#f5f5f5")
        summary_win.attributes("-topmost", True)

        banner = ctk.CTkFrame(summary_win, fg_color="#c2f0d1", corner_radius=0, height=50)
        banner.pack(fill="x", side="top")
        ctk.CTkLabel(banner, text=f"Batch Run Complete: Processed {len(slips_list)} Slips Successfully", 
                    text_color="black", font=("Helvetica", 16, "bold")).pack(pady=10)

        main_body = ctk.CTkFrame(summary_win, fg_color="transparent")
        main_body.pack(fill="both", expand=True, padx=20, pady=20)

        left_pane = ctk.CTkFrame(main_body, width=300, fg_color="white", border_color="#d3d3d3", border_width=1)
        left_pane.pack(side="left", fill="both", padx=(0, 10))
        left_pane.pack_propagate(False)
        
        ctk.CTkLabel(left_pane, text="Select Employee to View Slip", font=("Helvetica", 13, "bold"), text_color="black").pack(pady=10)

        right_pane = ctk.CTkFrame(main_body, fg_color="white", border_color="#d3d3d3", border_width=1)
        right_pane.pack(side="right", fill="both", expand=True)

        def populate_slip_details(slip):
            """Clears old content from the right pane and populates the selected employee's itemized card."""
            for widget in right_pane.winfo_children():
                widget.destroy()

            ctk.CTkLabel(right_pane, text=f"OFFICIAL SALARY SLIP - {slip['date']}", font=("Helvetica", 18, "bold"), text_color="black").pack(pady=15)
            
            info_frame = ctk.CTkFrame(right_pane, fg_color="transparent")
            info_frame.pack(fill="x", padx=30, pady=5)
            
            self._create_slip_row(info_frame, "EMPLOYEE NAME:", slip['name'])
            self._create_slip_row(info_frame, "EMPLOYEE ID:", slip['id'])
            self._create_slip_row(info_frame, "DEPARTMENT:", slip['dept'])
            self._create_slip_row(info_frame, "POSITION:", slip['pos'])
            self._create_slip_row(info_frame, "EMPLOYEE TYPE:", slip['emp_type'])

            ctk.CTkFrame(right_pane, height=2, fg_color="#e0e0e0").pack(fill="x", padx=30, pady=10)

            money_frame = ctk.CTkFrame(right_pane, fg_color="transparent")
            money_frame.pack(fill="x", padx=30, pady=5)
            self._create_slip_row(money_frame, "REGULAR EARNINGS:", f"Php {slip['reg_pay']:,.2f}")
            self._create_slip_row(money_frame, "OVERTIME PAYMENTS:", f"Php {slip['ot_pay']:,.2f}")
            self._create_slip_row(money_frame, "GROSS BASE PAY:", f"Php {slip['gross']:,.2f}")
            self._create_slip_row(money_frame, "STATUTORY DEDUCTIONS:", f"Php {(slip['vat'] + slip['ph'] + slip['sss'] + slip['pag'] + slip["absent"]):,.2f}")
            
            net_box = ctk.CTkFrame(right_pane, fg_color="#90ee90", corner_radius=4)
            net_box.pack(fill="x", padx=30, pady=20, side="bottom")
            ctk.CTkLabel(net_box, text=f"NET SALARY RECEIVED: Php {slip['net']:,.2f}", 
                        text_color="black", font=("Helvetica", 16, "bold")).pack(pady=12)

        scroll_container = ctk.CTkScrollableFrame(left_pane, fg_color="transparent")
        scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        for slip in slips_list:
            btn_text = f"{slip['date']} - {slip['name']}"
            btn = ctk.CTkButton(
                scroll_container, 
                text=btn_text, 
                anchor="w", 
                fg_color="#f8f9fa", 
                text_color="black",
                hover_color="#e2e6ea",
                command=lambda s=slip: populate_slip_details(s)
            )
            btn.pack(fill="x", pady=4, padx=5)


        if slips_list:
            populate_slip_details(slips_list[0])

class ViewSalaryRecordsFrame(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master, fg_color="#f5f5f5")
        self.master = master
        self.on_back = on_back

        banner = ctk.CTkFrame(self, fg_color="#c2f0d1", height=60, corner_radius=0)
        banner.pack(fill="x", side="top")
        
        ctk.CTkLabel(banner, text="HISTORICAL SALARY TRANSACTION LEDGER", 
                    text_color="black", font=("Helvetica", 20, "bold")).pack(side="left", padx=20, pady=15)
        
        ctk.CTkButton(banner, text="Back to Dashboard", fg_color="#333333", hover_color="#555555",
                    command=self.on_back).pack(side="right", padx=20, pady=15)

        control_panel = ctk.CTkFrame(self, fg_color="white", height=60, corner_radius=4)
        control_panel.pack(fill="x", padx=20, pady=(15, 0))
        
        ctk.CTkLabel(control_panel, text="Search Employee ID:", text_color="black", 
                    font=("Helvetica", 13, "bold")).pack(side="left", padx=(15, 5), pady=15)
        
        self.search_entry = ctk.CTkEntry(control_panel, placeholder_text="e.g., 1001", width=150, text_color="black")
        self.search_entry.pack(side="left", padx=5, pady=15)
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_records_table())

        self.table_container = ctk.CTkScrollableFrame(self, fg_color="white", label_text="Issued Payslip Ledger Matrix")
        self.table_container.configure(label_text_color="black", label_font=("Helvetica", 14, "bold"))
        self.table_container.pack(fill="both", expand=True, padx=20, pady=15)

        self.load_records_table()

    def load_records_table(self):
        """Clears old rows and reads database dictionaries to populate historical listings."""
        for widget in self.table_container.winfo_children():
            widget.destroy()

        headers = ["Date", "ID", "Name", "Department", "Gross Pay", "Deductions", "Net Salary"]
        widths = [120, 80, 180, 150, 120, 120, 120]

        header_row = ctk.CTkFrame(self.table_container, fg_color="#e0e0e0", corner_radius=0)
        header_row.pack(fill="x", pady=(0, 5))

        for col_idx, (text, w) in enumerate(zip(headers, widths)):
            lbl = ctk.CTkLabel(header_row, text=text, width=w, font=("Helvetica", 12, "bold"), text_color="black", anchor="w")
            lbl.pack(side="left", padx=10, pady=8)

        all_slips = self.master.file_handler.get_all_salary_slips()
        search_filter = self.search_entry.get().strip()

        row_counter = 0

        for emp_id, slips in all_slips.items():
            if search_filter and search_filter not in str(emp_id):
                continue

            for slip in slips:
                bg_color = "#fdfdfd" if row_counter % 2 == 0 else "#f1f3f5"
                row_frame = ctk.CTkFrame(self.table_container, fg_color=bg_color, corner_radius=0)
                row_frame.pack(fill="x", pady=1)

                total_deductions = slip['vat'] + slip['ph'] + slip['sss'] + slip['pag'] + slip['absent']

                data_fields = [
                    slip['date'],
                    emp_id,
                    slip['name'],
                    slip['dept'],
                    f"Php {slip['gross']:,.2f}",
                    f"Php {total_deductions:,.2f}",
                    f"Php {slip['net']:,.2f}"
                ]

                for text, w in zip(data_fields, widths):
                    val_lbl = ctk.CTkLabel(row_frame, text=text, width=w, text_color="black", font=("Helvetica", 12), anchor="w")
                    val_lbl.pack(side="left", padx=10, pady=6)

                row_counter += 1

        if row_counter == 0:
            ctk.CTkLabel(self.table_container, text="No payroll transactions found matching criteria.", 
                        text_color="gray", font=("Helvetica", 13, "italic")).pack(pady=30)
        
class PayrollSystemApp(ctk.CTk):
    def __init__(self, screenWidth=1280, screenHeight=720):
        super().__init__()

        self.payroll_system = PayrollSystemManager()
        self.payroll_queue = PayrollQueue()
        self.sorter = PayrollAlgo()
        self.salary_records = SalaryRecord()
        self.file_handler = PayrollDataFileHandling()

        ctk.set_appearance_mode("light")

        self.title("Payroll Management System For Employees")
        self.geometry(f"{screenWidth}x{screenHeight}")
        self.resizable(False, False)
        self.primary_font = ctk.CTkFont(family="Helvetica", size=18)
        self.protocol("WM_DELETE_WINDOW", self.exit)

        self.auth_user = None
        self.current_frame = None
        print("Current Frame: ", self.current_frame)
        self.show_admin_page()

    def exit(self):
        """Triggered when the user clicks the red X button"""
        if messagebox.askokcancel("Quit", "Are you sure you want to exit the Payroll System? Any unsaved changes may be lost."):
            self.destroy()
    
    def show_admin_page(self):
        self.current_frame = AdminLoginFrame(self, self.show_home_page)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")
        print("Current Frame: ", self.current_frame)

    def show_home_page(self, username):

        self.auth_user = username

        if self.current_frame:
            self.current_frame.pack_forget()
            self.current_frame.place_forget()

        self.current_frame.place_forget()
        self.current_frame = HomePageFrame(self, username=self.auth_user)
        self.current_frame.pack(fill="both", expand=True)
        print("Current Frame: ", self.current_frame)

    def show_view_all_page(self):
        """Hides current frame and shows the Employee List."""
        if self.current_frame:
            self.current_frame.pack_forget() 
            self.current_frame.place_forget()

        self.current_frame = ViewEmployeesFrame(self, on_back=self.show_home_after_view)
        self.current_frame.pack(fill="both", expand=True)

    def show_home_after_view(self):
        """Callback to return to Home."""
        self.current_frame.pack_forget()
        self.show_home_page(username=self.auth_user) 

    def handle_logout(self):
        """Clears session data and returns to the login page."""
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.auth_user = None 
            if self.current_frame:
                self.current_frame.pack_forget()
                self.current_frame.place_forget()
            
            self.show_admin_page()
    
    def show_process_page(self):
        """Hides current frame and shows the Process Employee Page."""
        if self.current_frame:
            self.current_frame.pack_forget()
            self.current_frame.place_forget()
        
        self.current_frame = ProcessEmployeeFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_salary_records_page(self):
        """Hides current frame context and exposes the historical transactions ledger."""
        if self.current_frame:
            self.current_frame.pack_forget()
            self.current_frame.place_forget()

        # Route viewport frame execution context
        self.current_frame = ViewSalaryRecordsFrame(self, on_back=self.show_home_after_salary_records)
        self.current_frame.pack(fill="both", expand=True)

    def show_home_after_salary_records(self):
        """Callback reference clearing view stack state returning directly to user workspace dashboard."""
        self.current_frame.pack_forget()
        self.show_home_page(username=self.auth_user)


        
if __name__ == "__main__":
    app = PayrollSystemApp()
    app.mainloop()