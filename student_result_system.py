import json
import os

class Student:
    def __init__(self, student_id, name, age, gender):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.marks = {}  # Subject -> Marks
    
    def add_marks(self, subject, marks):
        """Add marks for a subject with validation"""
        if not isinstance(marks, (int, float)) or marks < 0 or marks > 100:
            raise ValueError("Marks must be between 0 and 100")
        self.marks[subject] = marks
    
    def get_total_marks(self):
        return sum(self.marks.values())
    
    def get_average_marks(self):
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)
    
    def get_grade(self):
        """Calculate grade based on average marks"""
        avg = self.get_average_marks()
        if avg >= 90:
            return 'A+'
        elif avg >= 80:
            return 'A'
        elif avg >= 70:
            return 'B+'
        elif avg >= 60:
            return 'B'
        elif avg >= 50:
            return 'C'
        elif avg >= 40:
            return 'D'
        else:
            return 'F'
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'marks': self.marks
        }
    
    @classmethod
    def from_dict(cls, data):
        student = cls(data['student_id'], data['name'], data['age'], data['gender'])
        student.marks = data.get('marks', {})
        return student
    
    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Gender: {self.gender}"


class Result:
    def __init__(self, student):
        self.student = student
        self.grade = student.get_grade()
        self.total_marks = student.get_total_marks()
        self.average_marks = student.get_average_marks()
    
    def display_result(self):
        print(f"\n{'='*50}")
        print(f"RESULT CARD")
        print(f"{'='*50}")
        print(f"Student ID: {self.student.student_id}")
        print(f"Name: {self.student.name}")
        print(f"Age: {self.student.age}")
        print(f"Gender: {self.student.gender}")
        print(f"{'='*50}")
        print("MARKS:")
        for subject, marks in self.student.marks.items():
            print(f"  {subject}: {marks}")
        print(f"{'='*50}")
        print(f"Total Marks: {self.total_marks}")
        print(f"Average Marks: {self.average_marks:.2f}")
        print(f"Grade: {self.grade}")
        status = "PASS" if self.grade != 'F' else "FAIL"
        print(f"Status: {status}")
        print(f"{'='*50}\n")
    
    def to_dict(self):
        return {
            'student': self.student.to_dict(),
            'grade': self.grade,
            'total_marks': self.total_marks,
            'average_marks': self.average_marks
        }


class ResultManagementSystem:
    def __init__(self, filename="students_data.json"):
        self.filename = filename
        self.students = {}  # student_id -> Student object
        self.load_data()
    
    def add_student(self, student_id, name, age, gender):
        if student_id in self.students:
            raise ValueError(f"Student with ID {student_id} already exists")
        student = Student(student_id, name, age, gender)
        self.students[student_id] = student
        print(f"Student '{name}' added successfully!")
    
    def add_marks(self, student_id, subject, marks):
        if student_id not in self.students:
            raise ValueError(f"Student with ID {student_id} not found")
        self.students[student_id].add_marks(subject, marks)
        print(f"Marks added for {subject}: {marks}")
    
    def search_student_by_name(self, name):
        """Search students by name using list comprehension"""
        results = [student for student in self.students.values() 
                  if name.lower() in student.name.lower()]
        return results
    
    def delete_student(self, student_id):
        if student_id not in self.students:
            raise ValueError(f"Student with ID {student_id} not found")
        del self.students[student_id]
        print(f"Student with ID {student_id} deleted successfully!")
    
    def display_all_students(self):
        if not self.students:
            print("No students found!")
            return
        print(f"\n{'='*60}")
        print(f"TOTAL STUDENTS: {len(self.students)}")
        print(f"{'='*60}")
        for student in self.students.values():
            print(f"ID: {student.student_id} | Name: {student.name} | Age: {student.age} | Grade: {student.get_grade()}")
        print(f"{'='*60}\n")
    
    def get_top_performers(self, n=5):
        """Get top n performers using list comprehension"""
        students_with_marks = [student for student in self.students.values() 
                              if student.marks]
        if not students_with_marks:
            return []
        sorted_students = sorted(students_with_marks, 
                                key=lambda s: s.get_average_marks(), 
                                reverse=True)
        return sorted_students[:n]
    
    def display_top_performers(self, n=5):
        top_performers = self.get_top_performers(n)
        if not top_performers:
            print("No students with marks found!")
            return
        
        print(f"\n{'='*60}")
        print(f"TOP {min(n, len(top_performers))} PERFORMERS")
        print(f"{'='*60}")
        for i, student in enumerate(top_performers, 1):
            print(f"{i}. {student.name} - Average: {student.get_average_marks():.2f} - Grade: {student.get_grade()}")
        print(f"{'='*60}\n")
    
    def save_data(self):
        """Save data to JSON file"""
        data = {sid: student.to_dict() for sid, student in self.students.items()}
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {self.filename}")
    
    def load_data(self):
        """Load data from JSON file"""
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                for sid, student_data in data.items():
                    self.students[sid] = Student.from_dict(student_data)
            print(f"Data loaded from {self.filename}")
        except json.JSONDecodeError:
            print("Warning: Corrupt data file. Starting fresh.")
            self.students = {}
        except Exception as e:
            print(f"Error loading data: {e}")


def get_input(prompt, input_type=str, allow_empty=False):
    """Safe input with exception handling"""
    while True:
        try:
            value = input(prompt).strip()
            if not value and not allow_empty:
                print("This field cannot be empty. Try again.")
                continue
            if not value and allow_empty:
                return None
            if input_type == int:
                return int(value)
            elif input_type == float:
                return float(value)
            return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")


def main():
    system = ResultManagementSystem()
    
    while True:
        print("\n" + "="*60)
        print("STUDENT RESULT MANAGEMENT SYSTEM")
        print("="*60)
        print("1. Add Student")
        print("2. Add Marks")
        print("3. Display Student Result")
        print("4. Search Student by Name")
        print("5. Display All Students")
        print("6. Display Top Performers")
        print("7. Delete Student")
        print("8. Save Data")
        print("9. Exit")
        print("="*60)
        
        choice = get_input("Enter your choice (1-9): ", int)
        
        try:
            if choice == 1:
                sid = get_input("Enter Student ID: ", str)
                name = get_input("Enter Name: ", str)
                age = get_input("Enter Age: ", int)
                gender = get_input("Enter Gender (M/F/O): ", str)
                system.add_student(sid, name, age, gender)
            
            elif choice == 2:
                sid = get_input("Enter Student ID: ", str)
                subject = get_input("Enter Subject: ", str)
                marks = get_input("Enter Marks (0-100): ", float)
                system.add_marks(sid, subject, marks)
            
            elif choice == 3:
                sid = get_input("Enter Student ID: ", str)
                if sid in system.students:
                    result = Result(system.students[sid])
                    result.display_result()
                else:
                    print("Student not found!")
            
            elif choice == 4:
                name = get_input("Enter Student Name to search: ", str)
                results = system.search_student_by_name(name)
                if results:
                    print(f"\nFound {len(results)} student(s):")
                    for student in results:
                        print(f"  ID: {student.student_id} | Name: {student.name} | Grade: {student.get_grade()}")
                else:
                    print("No students found with that name!")
            
            elif choice == 5:
                system.display_all_students()
            
            elif choice == 6:
                n = get_input("How many top performers to show? (default 5): ", int, allow_empty=True)
                n = n or 5
                system.display_top_performers(n)
            
            elif choice == 7:
                sid = get_input("Enter Student ID to delete: ", str)
                system.delete_student(sid)
            
            elif choice == 8:
                system.save_data()
            
            elif choice == 9:
                save = input("Save data before exiting? (y/n): ").strip().lower()
                if save == 'y':
                    system.save_data()
                print("Thank you for using Student Result Management System!")
                break
            
            else:
                print("Invalid choice! Please enter 1-9.")
        
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()