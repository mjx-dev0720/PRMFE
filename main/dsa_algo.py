from collections import deque
class Node:
    """Represents a single record in the payroll system structures."""
    def __init__(self, employee_id, name, salary):
        self.employee_id = employee_id
        self.name = name
        self.salary = round(float(salary), 2)
        self.next = None

class SalaryRecord():
    """This is an Linked List that stores salary records of employees with a tail pointer"""
    def __init__(self):
        self.head = None
        self.tail = None

    def add_record(self, employee_id, name, salary):
        """Adds a salary record to the end of the history."""
        new_node = Node(employee_id, name, salary)
        
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def display_all(self):
        """Iterates through records for reporting."""
        current = self.head
        records = []
        while current:
            records.append(f"{current.employee_id:<8} {current.name:<30} ₱{current.salary:<12,.2f}")
            current = current.next
        return records
    

class PayrollQueue:
    """This is an Queue for payroll handling using FIFO principle"""
    def __init__(self):
        self._queue = deque()

    def is_empty(self):
        """Checks if the queue is empty."""
        return len(self._queue) == 0

    def enqueue(self, obj):
        """Adds an employee to the end of the line."""
        self._queue.append(obj)

    def dequeue(self):
        """Removes and returns the first employee in line."""
        if self.is_empty():
            return None
        return self._queue.popleft()

    def get_size(self):
        """Returns the number of pending items."""
        return len(self._queue)

class PayrollAlgo:
    """class for algorithm"""

    def merge_sort(self, data, criteria, reverse=True):
        if len(data) <= 1:
            return data
        
        mid = len(data) // 2
        left = self.merge_sort(data[:mid], criteria, reverse)
        right = self.merge_sort(data[mid:], criteria, reverse)

        return self._merge(left, right, criteria, reverse)
    
    def _merge(self, left, right, criteria, reverse):
        result = []

        attr = criteria.lower()
        if attr == "alphabetical":
            attr = "name"

        while len(left) > 0 and len(right) > 0:
            # CRITICAL FIX: Route salary sorting requests dynamically through the custom getter methods
            if attr == "salary":
                val1 = left[0].get_salary()
                val2 = right[0].get_salary()
            else:
                # Use standard object checks fallback mappings to grab public attributes safely without breaching private bounds
                val1 = getattr(left[0], attr) if hasattr(left[0], attr) else ""
                val2 = getattr(right[0], attr) if hasattr(right[0], attr) else ""

            # Standardize structural evaluations against mixed case variations
            v1 = val1.lower() if isinstance(val1, str) else val1
            v2 = val2.lower() if isinstance(val2, str) else val2

            if not reverse:
                is_correct_order = (v1 <= v2)
            else:
                is_correct_order = (v1 >= v2)

            if is_correct_order:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))

        # Pull remaining elements out from processing sequences
        while len(left) > 0:
            result.append(left.pop(0))
        while len(right) > 0:
            result.append(right.pop(0))

        return result