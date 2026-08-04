from Student import Student

class EduManagement:
    system_version = "1.0.0"
    system_name = "EduManagement"

    def __init__(self):
        self.students_list = []

    #添加成绩
    def add_student(self):
        student_name=input("Please enter the student name:")
        for s in self.students_list:
            if s.name==student_name:
                print("The student already exists.")
                return
               
        student_Chinese=int(input("Please enter the student Chinese score:"))
        student_Math=int(input("Please enter the student Math score:"))
        student_English=int(input("Please enter the student English score:"))
        if 0<=student_Chinese<=100 and 0<=student_Math<=100 and 0<=student_English<=100:
            print("The student score is valid.")
            stu=Student(student_name,student_Chinese,student_Math,student_English)
            self.students_list.append(stu)
        else:
            print("The student score is invalid.")
            return

        
    #修改成绩
    def update_student(self):
        student_name=input("Please enter the student name:")
        for s in self.students_list:
            if s.name==student_name:
                print(f"Current score: {s}")
                
                new_Chinese = int(input("Please enter the new Chinese score: "))
                new_Math = int(input("Please enter the new Math score: "))
                new_English = int(input("Please enter the new English score: "))
                if 0<=new_Chinese<=100 and 0<=new_Math<=100 and 0<=new_English<=100:
                    s.update_grade(new_Chinese,new_Math,new_English)
                    print(f"Score after update: {s}")
                    return
                else:
                    print("The student score is invalid.")
                    return 
        
        print("The student does not exist.")
               

    #删除成绩
    def delete_student(self):
        student_name=input("Please enter the student name:")
        for s in self.students_list:
            if s.name==student_name:
                self.students_list.remove(s)
                print(f"Student {student_name} has been deleted.")
                return
        
        print("The student does not exist.")

              
    #查询成绩
    def query_student(self):
        student_name=input("Please enter the student name:")
        for s in self.students_list:
            if s.name==student_name:
                print(f"Student information: {s}")
                return
        
        print("The student does not exist.")


    #显示成绩
    def list_students(self):
        for s in self.students_list:
            print(s)


    #运行系统
    def run(self):
        print(f"Welcome to {self.system_name} System (V{self.system_version})")

        while True:
            print("\nChioices:\n1. Add student")
            print("2. Update student")
            print("3. Delete student")
            print("4. Query student")
            print("5. List students")
            print("6. Exit")

            choice = input("Please enter your choice (1-6): ")
            try:
                if choice == '1':
                    self.add_student()
                elif choice == '2':
                    self.update_student()
                elif choice == '3':
                    self.delete_student()
                elif choice == '4':
                    self.query_student()
                elif choice == '5':
                    self.list_students()
                elif choice == '6':
                    print("Exiting the system.")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")
                
if __name__ == "__main__":
    new_edu=EduManagement()
    new_edu.run()


