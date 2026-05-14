# Payroll Management System for Employees (PRMFE)

A robust, high-performance desktop application engineered to automate enterprise employee tracking, payroll allocation matrices, and transaction history auditing. Built using **Python** and **CustomTkinter**, this system completely satisfies the requirements for Topic #22 of the Data Structures and Algorithms curriculum.

---

## 🚀 Key Features & Architectural Overview

The application is cleanly divided into a modular frontend user interface and an optimized backend data engine, fully backed by automated unit test suites.

### 1. Data Structures & Memory Management (Topic #22 Blueprint)
* **Custom FIFO Queue (`PayrollQueue`):** Manages batch payroll processing. Employees are queued and run in a strict First-In-First-Out sequence, ensuring linear, predictable execution states operating at $O(1)$ efficiency.
* **Custom Linked List (`SalaryRecord`):** Tracks historical payout transaction ledgers. It features a **Tail-Pointer Optimization**, transforming append operations from standard $O(N)$ lookup sweeps into high-speed $O(1)$ constant-time operations.
* **Dynamic Records List:** Standard employee directories are queried and maintained dynamically within system memory modules.

### 2. Algorithmic Optimization
* **Merge Sort Engine ($O(N \log N)$):** Uses a recursive divide-and-conquer strategy to sort records across multiple user-selected filters (Alphabetical sorting, Numeric Salary bounds, and Attendance counts).
* **Fuzzy Key Search Matrix:** Linear searching enhanced with case-insensitive token mapping, supporting instant identifier lookups and substring name matching.

### 3. Business Logic & Compliance Math
* **Full-Time Allocation Rules:** Automated monthly salary distributions including exact fractional day deductions for unexcused absences calculated using a standard 22-day corporate calendar template.
* **Part-Time Labor Scale:** Live hourly entry monitoring incorporating a standard **1.5x Overtime Multiplier** for hours logged beyond the standard 40-hour regular workweek boundary.
* **Statutory Contribution Matrix:** Native computation of regional withholding values, including Withholding Tax/VAT (12%), SSS, PhilHealth, and Pag-IBIG contributions.

### 4. Enterprise Interface & Database Security (Bonus +10 Points Cap)
* **Modern UI Customization (+5 Pts):** Fully implemented asynchronous user interface built completely on top of `customtkinter` elements featuring responsive frame positioning.
* **Data Persistence & Admin Security (+5 Pts):** Secure credentials verification gating system utilizing text-file streaming databases (`db/admin_db.txt`). Features dynamic state saving and automated `.bak` backup verification routines to prevent data corruption during read/write cycles.

---

## 📂 Project Repository Layout

```text
PRMFE/
├── main/
│   ├── dsa_algo.py            # Custom Data Structures (Queue, Linked List, Merge Sort)
│   ├── payroll_sys.py         # Business Engine, Employee Models, and Calculation Math
│   ├── db_handling.py         # File IO Serialization, File Handlers, and Backups
│   ├── payroll_gui.py         # CustomTkinter Graphical User Interface frames
│   ├── console.py             # Backup Command-Line Menu Application Interface
│   ├── test_payroll_system.py # 11 Automated Core Logic and Algorithm Unit Tests
│   └── test_payroll_gui.py    # 2 Automated User Input and Event Loop Integration Tests
└── db/
    ├── employees.txt          # Active Employee Database Flat File
    ├── history.txt            # Payslip Ledger Transaction Strings
    └── admin_db.txt           # Secure Application Login Access Tokens
🛠️ Installation and Setup Instructions
Prerequisites
Ensure you have Python 3.10 or higher installed on your operating system.

Step 1: Clone the Repository
Bash
git clone https://github.com/mjx-dev0720/PRMFE.git
cd PRMFE
Step 2: Install UI Dependencies
Install the required modern UI widget package:

Bash
pip install customtkinter
Step 3: Run the Application
To launch the modern desktop user interface window, run:

Bash
python main/payroll_gui.py
(Alternatively, run the text console backup application via python main/console.py)

🧪 Automated Testing Suite
This repository is backed by a multi-layered automated test matrix that validates the backend core structures, calculations, and interface tracking layers under completely isolated conditions.

Running Backend Component Tests (11 Verification Checks)
Verifies the custom FIFO queue operations, tail-pointer optimized linked lists, sorting partition boundaries, and labor tax deduction math formulas:

Bash
python -m unittest main/test_payroll_system.py
Running GUI Integration Tests (2 Verification Checks)
Verifies manual entry field value extraction, numeric typing validation catches, and data routing channels inside a virtual headless layout frame:

Bash
python -m unittest main/test_payroll_gui.py
Expected Test Suite Results:
Plaintext
Ran 11 tests in 0.006s
OK

Ran 2 tests in 0.531s
OK
