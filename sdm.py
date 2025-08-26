import stdio

class Student:
    """
    A class representing a student with attributes for name, roll number, and marks.
    """

    def __init__(self, name, rollno, m1, m2):
        """
        Constructor to initialize a Student instance.
        :param name: Student's name (str)
        :param rollno: Student's roll number (int)
        :param m1: Marks in subject 1 (int)
        :param m2: Marks in subject 2 (int)
        """
        self.name = name
        self.rollno = rollno
        self.m1 = m1
        self.m2 = m2

    def display(self):
        """
        Displays the details of the student.
        """
        stdio.writeln(f"Name: {self.name}")
        stdio.writeln(f"RollNo: {self.rollno}")
        stdio.writeln(f"Marks1: {self.m1}")
        stdio.writeln(f"Marks2: {self.m2}")
        stdio.writeln("\n")

class StudentManager:
    """
    A class to manage a list of students.
    """
    
    def __init__(self):
        self.students = []

    def accept(self, name, rollno, marks1, marks2):
        """
        Accepts student details and adds a new student to the list.
        :param name: Student's name (str)
        :param rollno: Student's roll number (int)
        :param marks1: Marks in subject 1 (int)
        :param marks2: Marks in subject 2 (int)
        """
        student = Student(name, rollno, marks1, marks2)
        self.students.append(student)

    def display_all(self):
        """
        Displays details of all students.
        """
        stdio.writeln("\nList of Students:")
        for student in self.students:
            student.display()

    def search(self, rollno):
        """
        Searches for a student by roll number.
        :param rollno: Roll number to search for (int)
        :return: Index of the student if found, otherwise -1
        """
        for index, student in enumerate(self.students):
            if student.rollno == rollno:
                return index
        return -1

    def delete(self, rollno):
        """
        Deletes a student by roll number.
        :param rollno: Roll number of the student to delete (int)
        """
        index = self.search(rollno)
        if index != -1:
            del self.students[index]

    def update(self, rollno, new_rollno):
        """
        Updates the roll number of a student.
        :param rollno: Current roll number (int)
        :param new_rollno: New roll number (int)
        """
        index = self.search(rollno)
        if index != -1:
            self.students[index].rollno = new_rollno

if __name__ == '__main__':
    manager = StudentManager()

    stdio.writeln("\nOperations:")
    stdio.writeln("1. Accept Student details")
    stdio.writeln("2. Display Student Details")
    stdio.writeln("3. Search Details of a Student")
    stdio.writeln("4. Delete Details of Student")
    stdio.writeln("5. Update Student Details")
    stdio.writeln("6. Exit")

    # Sample data for demonstration
    manager.accept("A", 1, 100, 100)
    manager.accept("B", 2, 90, 90)
    manager.accept("C", 3, 80, 80)

    # Display all students
    manager.display_all()

    # Search for a student
    stdio.writeln("\nSearching for Student with RollNo 2:")
    index = manager.search(2)
    if index != -1:
        stdio.writeln("Student Found:")
        manager.students[index].display()
    else:
        stdio.writeln("Student Not Found.")

    # Delete a student
    manager.delete(2)
    stdio.writeln("List after deletion:")
    manager.display_all()

    # Update a student's roll number
    manager.update(3, 2)
    stdio.writeln("List after updation:")
    manager.display_all()

    stdio.writeln("Thank You!")
