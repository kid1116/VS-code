import os
os.system('cls')
class Dog():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def sit(self): #f-string表达
        print(f"{self.name} is now sitting.")

    def roll_over(self):
        print(f"{self.name} rolled over!")

my_dog = Dog('Tom', 6)
my_dog.sit()
my_dog.roll_over()
print(f"My dog is {my_dog.age} years old.")