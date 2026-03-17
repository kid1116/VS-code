#include <iostream>
#include <string>
using namespace std;

class GradeBook
{
public:
    string courseName;
    string instructorName;

    GradeBook(string name, string InsName)
    {
        courseName = name;
        instructorName = InsName;
    }

    void setInstructorName(string name)
    {
        instructorName = name;
    }
};

int main()
{
    string courseName;
    getline(cin, courseName);
    string instructorName;
    getline(cin, instructorName);
    string newInstructorName;
    getline(cin, newInstructorName);

    GradeBook g(courseName, instructorName);

    cout << "Welcome to the grade book for\n"
         << g.courseName << endl;
    cout << "This course is presented by: " << g.instructorName << endl;

    g.setInstructorName(newInstructorName);
    cout << "Changing instructor name to " << g.instructorName << endl;

    cout << "Welcome to the grade book for\n"
         << g.courseName << endl;
    cout << "This course is presented by: " << g.instructorName << endl;

    return 0;
}