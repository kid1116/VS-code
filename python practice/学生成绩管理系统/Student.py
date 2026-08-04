class Student:
    def __init__(self,name,Chinese,Math,English):
        self.name = name
        self.grade_Chinese = Chinese
        self.grade_Math = Math
        self.grade_English = English

    def __str__(self):
        return f"Student(Name:{self.name}, Chinese:{self.grade_Chinese}, Math:{self.grade_Math}, English:{self.grade_English}, "\
            f"Total:{self.grade_Chinese+self.grade_Math+self.grade_English})"

    def update_grade(self,grade_Chinese=None,grade_Math=None,grade_English=None):
        if grade_Chinese is not None:
            self.grade_Chinese = grade_Chinese
        if grade_Math is not None:
            self.grade_Math = grade_Math
        if grade_English is not None:
            self.grade_English = grade_English

if __name__ == "__main__":
    #测试代码
    student1 = Student("Alice",85,90,88)
    print("Initial grade:\n",student1)
    student1.update_grade(grade_Chinese=90,grade_English=92)
    print("After update:\n",student1)