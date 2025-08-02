#!/usr/bin/env python3
"""
Comprehensive Examples: Binary Files, CSV Files, and Stack Data Structure
This module demonstrates practical applications combining all three topics.
"""

import csv
import pickle
import os
from pathlib import Path

class StudentRecord:
    """Student record class for demonstration"""
    
    def __init__(self, student_id, name, grades, subjects):
        self.student_id = student_id
        self.name = name
        self.grades = grades
        self.subjects = subjects
        self.gpa = sum(grades) / len(grades) if grades else 0.0
    
    def __str__(self):
        return f"Student({self.student_id}, {self.name}, GPA: {self.gpa:.2f})"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        """Convert to dictionary for CSV export"""
        return {
            'ID': self.student_id,
            'Name': self.name,
            'Grades': ','.join(map(str, self.grades)),
            'Subjects': ','.join(self.subjects),
            'GPA': round(self.gpa, 2)
        }

class Stack:
    """Simple stack implementation for undo operations"""
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)

class StudentManagementSystem:
    """Student Management System using binary files, CSV, and stack for undo"""
    
    def __init__(self, data_dir='sample_files'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.binary_file = self.data_dir / 'students.pkl'
        self.csv_file = self.data_dir / 'students.csv'
        self.backup_file = self.data_dir / 'students_backup.pkl'
        
        self.students = []
        self.undo_stack = Stack()
        
        print("🎓 Student Management System initialized")
        print(f"📁 Data directory: {self.data_dir}")
    
    def add_student(self, student_id, name, grades, subjects):
        """Add a new student"""
        # Save current state for undo
        self._save_state_for_undo('add_student', None)
        
        student = StudentRecord(student_id, name, grades, subjects)
        self.students.append(student)
        
        print(f"✅ Added student: {student}")
        return student
    
    def remove_student(self, student_id):
        """Remove a student by ID"""
        for i, student in enumerate(self.students):
            if student.student_id == student_id:
                # Save current state for undo
                self._save_state_for_undo('remove_student', student)
                
                removed_student = self.students.pop(i)
                print(f"🗑️ Removed student: {removed_student}")
                return removed_student
        
        print(f"❌ Student with ID {student_id} not found")
        return None
    
    def update_student_grades(self, student_id, new_grades):
        """Update a student's grades"""
        for student in self.students:
            if student.student_id == student_id:
                # Save current state for undo
                old_grades = student.grades.copy()
                self._save_state_for_undo('update_grades', (student, old_grades))
                
                student.grades = new_grades
                student.gpa = sum(new_grades) / len(new_grades) if new_grades else 0.0
                
                print(f"📝 Updated grades for {student.name}: {new_grades} (GPA: {student.gpa:.2f})\")\n                return student\n        \n        print(f\"❌ Student with ID {student_id} not found\")\n        return None\n    \n    def _save_state_for_undo(self, operation, data):\n        \"\"\"Save current state to undo stack\"\"\"\n        state = {\n            'operation': operation,\n            'data': data,\n            'students_backup': [self._copy_student(s) for s in self.students]\n        }\n        self.undo_stack.push(state)\n        \n        # Limit undo history to prevent memory issues\n        if self.undo_stack.size() > 10:\n            # Remove oldest state\n            temp_stack = Stack()\n            for _ in range(9):\n                if not self.undo_stack.is_empty():\n                    temp_stack.push(self.undo_stack.pop())\n            \n            self.undo_stack = Stack()\n            while not temp_stack.is_empty():\n                self.undo_stack.push(temp_stack.pop())\n    \n    def _copy_student(self, student):\n        \"\"\"Create a deep copy of a student\"\"\"\n        return StudentRecord(\n            student.student_id,\n            student.name,\n            student.grades.copy(),\n            student.subjects.copy()\n        )\n    \n    def undo_last_operation(self):\n        \"\"\"Undo the last operation\"\"\"\n        if self.undo_stack.is_empty():\n            print(\"❌ Nothing to undo!\")\n            return False\n        \n        state = self.undo_stack.pop()\n        operation = state['operation']\n        \n        # Restore previous state\n        self.students = state['students_backup']\n        \n        print(f\"↩️ Undid operation: {operation}\")\n        return True\n    \n    def save_to_binary(self):\n        \"\"\"Save students to binary file using pickle\"\"\"\n        try:\n            with open(self.binary_file, 'wb') as f:\n                pickle.dump(self.students, f)\n            \n            file_size = os.path.getsize(self.binary_file)\n            print(f\"💾 Saved {len(self.students)} students to binary file ({file_size} bytes)\")\n            return True\n        except Exception as e:\n            print(f\"❌ Error saving to binary file: {e}\")\n            return False\n    \n    def load_from_binary(self):\n        \"\"\"Load students from binary file\"\"\"\n        try:\n            if not self.binary_file.exists():\n                print(\"📄 No binary file found, starting with empty database\")\n                return True\n            \n            with open(self.binary_file, 'rb') as f:\n                self.students = pickle.load(f)\n            \n            print(f\"📖 Loaded {len(self.students)} students from binary file\")\n            return True\n        except Exception as e:\n            print(f\"❌ Error loading from binary file: {e}\")\n            return False\n    \n    def export_to_csv(self):\n        \"\"\"Export students to CSV file\"\"\"\n        try:\n            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:\n                if not self.students:\n                    print(\"📄 No students to export\")\n                    return True\n                \n                fieldnames = ['ID', 'Name', 'Grades', 'Subjects', 'GPA']\n                writer = csv.DictWriter(f, fieldnames=fieldnames)\n                \n                writer.writeheader()\n                for student in self.students:\n                    writer.writerow(student.to_dict())\n            \n            file_size = os.path.getsize(self.csv_file)\n            print(f\"📊 Exported {len(self.students)} students to CSV file ({file_size} bytes)\")\n            return True\n        except Exception as e:\n            print(f\"❌ Error exporting to CSV: {e}\")\n            return False\n    \n    def import_from_csv(self):\n        \"\"\"Import students from CSV file\"\"\"\n        try:\n            if not self.csv_file.exists():\n                print(\"📄 No CSV file found\")\n                return False\n            \n            imported_students = []\n            with open(self.csv_file, 'r', encoding='utf-8') as f:\n                reader = csv.DictReader(f)\n                \n                for row in reader:\n                    try:\n                        student_id = int(row['ID'])\n                        name = row['Name']\n                        grades = [int(g.strip()) for g in row['Grades'].split(',') if g.strip()]\n                        subjects = [s.strip() for s in row['Subjects'].split(',') if s.strip()]\n                        \n                        student = StudentRecord(student_id, name, grades, subjects)\n                        imported_students.append(student)\n                    except (ValueError, KeyError) as e:\n                        print(f\"⚠️ Skipping invalid row: {row} - Error: {e}\")\n            \n            # Save current state for undo\n            self._save_state_for_undo('import_csv', None)\n            self.students = imported_students\n            \n            print(f\"📥 Imported {len(self.students)} students from CSV file\")\n            return True\n        except Exception as e:\n            print(f\"❌ Error importing from CSV: {e}\")\n            return False\n    \n    def search_students(self, **criteria):\n        \"\"\"Search students by various criteria\"\"\"\n        results = []\n        \n        for student in self.students:\n            match = True\n            \n            if 'min_gpa' in criteria and student.gpa < criteria['min_gpa']:\n                match = False\n            if 'max_gpa' in criteria and student.gpa > criteria['max_gpa']:\n                match = False\n            if 'name_contains' in criteria and criteria['name_contains'].lower() not in student.name.lower():\n                match = False\n            if 'subject' in criteria and criteria['subject'] not in student.subjects:\n                match = False\n            \n            if match:\n                results.append(student)\n        \n        return results\n    \n    def generate_statistics(self):\n        \"\"\"Generate statistics about students\"\"\"\n        if not self.students:\n            print(\"📊 No students in database\")\n            return\n        \n        total_students = len(self.students)\n        gpas = [s.gpa for s in self.students]\n        avg_gpa = sum(gpas) / len(gpas)\n        min_gpa = min(gpas)\n        max_gpa = max(gpas)\n        \n        # Subject distribution\n        subject_count = {}\n        for student in self.students:\n            for subject in student.subjects:\n                subject_count[subject] = subject_count.get(subject, 0) + 1\n        \n        print(f\"\\n📊 Student Statistics:\")\n        print(f\"   Total students: {total_students}\")\n        print(f\"   Average GPA: {avg_gpa:.2f}\")\n        print(f\"   Highest GPA: {max_gpa:.2f}\")\n        print(f\"   Lowest GPA: {min_gpa:.2f}\")\n        print(f\"   Subject distribution: {dict(sorted(subject_count.items()))}\")\n    \n    def display_all_students(self):\n        \"\"\"Display all students\"\"\"\n        if not self.students:\n            print(\"📄 No students in database\")\n            return\n        \n        print(f\"\\n👥 All Students ({len(self.students)}):\")\n        print(\"-\" * 60)\n        for i, student in enumerate(self.students, 1):\n            print(f\"{i:2d}. {student}\")\n            print(f\"    Subjects: {', '.join(student.subjects)}\")\n            print(f\"    Grades: {student.grades}\")\n    \n    def create_backup(self):\n        \"\"\"Create a backup of current data\"\"\"\n        try:\n            with open(self.backup_file, 'wb') as f:\n                pickle.dump(self.students, f)\n            \n            print(f\"💾 Backup created: {self.backup_file}\")\n            return True\n        except Exception as e:\n            print(f\"❌ Error creating backup: {e}\")\n            return False\n    \n    def restore_from_backup(self):\n        \"\"\"Restore data from backup\"\"\"\n        try:\n            if not self.backup_file.exists():\n                print(\"❌ No backup file found\")\n                return False\n            \n            with open(self.backup_file, 'rb') as f:\n                backup_students = pickle.load(f)\n            \n            # Save current state for undo\n            self._save_state_for_undo('restore_backup', None)\n            self.students = backup_students\n            \n            print(f\"📥 Restored {len(self.students)} students from backup\")\n            return True\n        except Exception as e:\n            print(f\"❌ Error restoring from backup: {e}\")\n            return False\n\ndef demonstrate_student_management_system():\n    \"\"\"Comprehensive demonstration of the student management system\"\"\"\n    print(\"🎓 Student Management System Demonstration\")\n    print(\"=\" * 55)\n    \n    # Initialize system\n    sms = StudentManagementSystem()\n    \n    # Add some sample students\n    print(\"\\n--- Adding Students ---\")\n    sms.add_student(101, \"Alice Johnson\", [85, 92, 78, 96], [\"Math\", \"Physics\", \"Chemistry\"])\n    sms.add_student(102, \"Bob Smith\", [78, 85, 90, 82], [\"Math\", \"Biology\", \"English\"])\n    sms.add_student(103, \"Charlie Brown\", [92, 88, 95, 91], [\"Physics\", \"Chemistry\", \"Math\"])\n    sms.add_student(104, \"Diana Prince\", [96, 94, 98, 93], [\"Biology\", \"Chemistry\", \"Physics\"])\n    \n    # Display all students\n    sms.display_all_students()\n    \n    # Generate statistics\n    sms.generate_statistics()\n    \n    # Save to binary file\n    print(\"\\n--- Saving to Binary File ---\")\n    sms.save_to_binary()\n    \n    # Export to CSV\n    print(\"\\n--- Exporting to CSV ---\")\n    sms.export_to_csv()\n    \n    # Create backup\n    print(\"\\n--- Creating Backup ---\")\n    sms.create_backup()\n    \n    # Demonstrate undo functionality\n    print(\"\\n--- Testing Undo Functionality ---\")\n    print(f\"Undo stack size: {sms.undo_stack.size()}\")\n    \n    # Make some changes\n    sms.update_student_grades(101, [90, 95, 85, 98])\n    sms.remove_student(102)\n    \n    sms.display_all_students()\n    \n    # Undo changes\n    print(\"\\n--- Undoing Changes ---\")\n    sms.undo_last_operation()  # Undo remove\n    sms.undo_last_operation()  # Undo grade update\n    \n    sms.display_all_students()\n    \n    # Search functionality\n    print(\"\\n--- Search Functionality ---\")\n    high_performers = sms.search_students(min_gpa=90.0)\n    print(f\"High performers (GPA >= 90.0): {len(high_performers)}\")\n    for student in high_performers:\n        print(f\"   {student}\")\n    \n    math_students = sms.search_students(subject=\"Math\")\n    print(f\"\\nMath students: {len(math_students)}\")\n    for student in math_students:\n        print(f\"   {student}\")\n    \n    # Test loading from binary file\n    print(\"\\n--- Testing Load from Binary ---\")\n    sms2 = StudentManagementSystem()\n    sms2.load_from_binary()\n    print(f\"Loaded system has {len(sms2.students)} students\")\n    \n    # Test CSV import\n    print(\"\\n--- Testing CSV Import ---\")\n    sms3 = StudentManagementSystem()\n    sms3.import_from_csv()\n    print(f\"Imported system has {len(sms3.students)} students\")\n    \n    print(\"\\n✅ Demonstration completed!\")\n\ndef demonstrate_file_format_comparison():\n    \"\"\"Compare binary vs CSV file formats\"\"\"\n    print(\"\\n📊 File Format Comparison\")\n    print(\"=\" * 35)\n    \n    # Create test data\n    students = [\n        StudentRecord(i, f\"Student_{i:03d}\", \n                     [85 + (i % 15), 90 - (i % 10), 88 + (i % 12)],\n                     [\"Math\", \"Science\", \"English\"])\n        for i in range(1, 101)  # 100 students\n    ]\n    \n    data_dir = Path('sample_files')\n    binary_file = data_dir / 'comparison_test.pkl'\n    csv_file = data_dir / 'comparison_test.csv'\n    \n    # Save as binary\n    import time\n    start_time = time.time()\n    with open(binary_file, 'wb') as f:\n        pickle.dump(students, f)\n    binary_write_time = time.time() - start_time\n    \n    # Save as CSV\n    start_time = time.time()\n    with open(csv_file, 'w', newline='', encoding='utf-8') as f:\n        fieldnames = ['ID', 'Name', 'Grades', 'Subjects', 'GPA']\n        writer = csv.DictWriter(f, fieldnames=fieldnames)\n        writer.writeheader()\n        for student in students:\n            writer.writerow(student.to_dict())\n    csv_write_time = time.time() - start_time\n    \n    # Load from binary\n    start_time = time.time()\n    with open(binary_file, 'rb') as f:\n        binary_loaded = pickle.load(f)\n    binary_read_time = time.time() - start_time\n    \n    # Load from CSV\n    start_time = time.time()\n    csv_loaded = []\n    with open(csv_file, 'r', encoding='utf-8') as f:\n        reader = csv.DictReader(f)\n        for row in reader:\n            student_id = int(row['ID'])\n            name = row['Name']\n            grades = [int(g.strip()) for g in row['Grades'].split(',')]\n            subjects = [s.strip() for s in row['Subjects'].split(',')]\n            csv_loaded.append(StudentRecord(student_id, name, grades, subjects))\n    csv_read_time = time.time() - start_time\n    \n    # Get file sizes\n    binary_size = os.path.getsize(binary_file)\n    csv_size = os.path.getsize(csv_file)\n    \n    # Display comparison\n    print(f\"\\n📈 Performance Results (100 students):\")\n    print(f\"   Binary write: {binary_write_time:.4f}s\")\n    print(f\"   CSV write:    {csv_write_time:.4f}s\")\n    print(f\"   Binary read:  {binary_read_time:.4f}s\")\n    print(f\"   CSV read:     {csv_read_time:.4f}s\")\n    \n    print(f\"\\n💾 File Size Comparison:\")\n    print(f\"   Binary file: {binary_size:,} bytes\")\n    print(f\"   CSV file:    {csv_size:,} bytes\")\n    print(f\"   Size ratio:  {csv_size/binary_size:.2f}x (CSV vs Binary)\")\n    \n    print(f\"\\n🚀 Speed Comparison:\")\n    print(f\"   Binary is {csv_write_time/binary_write_time:.1f}x faster for writing\")\n    print(f\"   Binary is {csv_read_time/binary_read_time:.1f}x faster for reading\")\n    \n    # Data integrity check\n    print(f\"\\n🔍 Data Integrity:\")\n    print(f\"   Binary loaded: {len(binary_loaded)} students\")\n    print(f\"   CSV loaded:    {len(csv_loaded)} students\")\n    print(f\"   First student match: {binary_loaded[0].name == csv_loaded[0].name}\")\n    \n    # Clean up\n    binary_file.unlink()\n    csv_file.unlink()\n\ndef main():\n    \"\"\"Main demonstration function\"\"\"\n    print(\"🚀 Comprehensive File Programming Demonstration\")\n    print(\"=\" * 60)\n    print(\"This demo combines binary files, CSV files, and stack data structure\")\n    print(\"in a practical Student Management System.\")\n    \n    # Run demonstrations\n    demonstrate_student_management_system()\n    demonstrate_file_format_comparison()\n    \n    print(\"\\n🎯 Key Concepts Demonstrated:\")\n    print(\"   ✅ Binary file operations with pickle\")\n    print(\"   ✅ CSV file reading and writing\")\n    print(\"   ✅ Stack implementation for undo functionality\")\n    print(\"   ✅ Data persistence and retrieval\")\n    print(\"   ✅ Error handling and validation\")\n    print(\"   ✅ Performance comparison between formats\")\n    print(\"   ✅ Real-world application design\")\n\nif __name__ == \"__main__\":\n    main()"