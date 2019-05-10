from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window
from kivy.base import runTouchApp
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from datetime import time, date, datetime, timedelta
import MySQLdb
import time


#Login Screen when program is started
class LoginPage(Screen):


    def __init__(self, **kwargs):

        super(LoginPage, self).__init__(**kwargs)

        Window.size = (600, 300)

        #Establish MySQL connection and cursor
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='password')
        self.cursor = self.conn.cursor()
        self.cursor.execute('USE Gradebook')

        #Query the database and obtain all the users
        self.cursor.execute('SELECT username, user_password, IDNum FROM Students')
        self.students = self.cursor.fetchall()

        print self.students

        self.cursor.execute('SELECT username, user_password, IDNum FROM Instructors')
        self.instructors = self.cursor.fetchall()

        print self.instructors

        #Close connection when this is done
        self.cursor.close()
        self.conn.close()

    def verify_student(self):
        for row in self.students:
            if self.ids.login_name.text == row[0] and self.ids.login_pass.text == row[1]:
                self.manager.signin_name = row[0]
                self.manager.signin_ID = row[2]
                self.manager.current = "student_selection_page"
                break

    def verify_instructor(self):
        for row in self.instructors:
            if self.ids.login_name.text == row[0] and self.ids.login_pass.text == row[1]:
                self.manager.signin_name = row[0]
                self.manager.signin_ID = row[2]
                self.manager.current = "instructor_selection_page"
                break



    def on_pre_enter(self):
        Window.size = (600, 300)

    def on_pre_leave(self):
        self.ids.login_name.text = ""
        self.ids.login_pass.text = ""

    pass


class StudentSelectionPage(Screen):

    #Declare list that will store buttons
    classButtons = {}

    #Labels for class info (Instructors)
    classInstructorLabels = {}

    #Labels for class times
    classTimes = {}

    #Variable that will store the class info for the student
    classesInfo = {}

    #Variable that stores class days
    classDays = {}

    #Initialize class members
    def __init__(self, **kwargs):

        super(StudentSelectionPage, self).__init__(**kwargs)

        #Establish MySQL connection and cursor
        # self.conn = MySQLdb.connect(host='localhost',user='root',passwd='password')
        # self.cursor = self.conn.cursor()
        # self.cursor.execute('USE Gradebook')

        #Query the database and obtain all the users


        #Close connection when this is done
        #self.cursor.close()
        #self.conn.close()

    def class_button_press(self, instance):

        #Obtain user class choice code
        self.manager.class_choice = instance.text

        self.cursor.execute('SELECT Classes.classNum FROM Classes WHERE Classes.classCode = \''+self.manager.class_choice+'\'')
        classID = self.cursor.fetchall()
        for row in classID:
            self.manager.classNum_choice = row[0]

        print 'After obtaining ClassNum'
        print self.manager.classNum_choice

        #Use code to find class number
        print(self.manager.class_choice)
        self.manager.current = 'student_page'


    def on_pre_enter(self):
        #Resize the screen
        Window.size = (800, 400)

        #Reset the class choice
        self.manager.class_choice = {}

        #Establish connection to MySQL database
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='password')
        self.cursor = self.conn.cursor()
        self.cursor.execute('USE Gradebook')
        #print self.manager.signin_name
        #print self.manager.signin_ID

        #Query the database and store results in list
        self.cursor.execute('SELECT Instructors.firstName, Instructors.lastName, \
                             Classes.classCode, Classes.classTime , Classes.days FROM Student_has_Classes \
                             INNER JOIN Instructors ON Instructors.IDNum = Student_has_Classes.instructorNum \
                             INNER JOIN Classes ON Classes.classNum = Student_has_Classes.classNum \
                             INNER JOIN Students ON Students.IDNum = Student_has_Classes.studentNum \
                             WHERE '+ str(self.manager.signin_ID) +' = Student_has_Classes.studentNum')

        self.classesInfo = self.cursor.fetchall()

        #Add buttons to screen for each class
        classCount = 0
        for row in self.classesInfo:
            self.classButtons[classCount] = Button(text = row[2])
            self.classButtons[classCount].bind(on_press=self.class_button_press)
            self.classInstructorLabels[classCount] = Label(text = 'Professor ' + row[0] + ' ' + row[1])
            self.classTimes[classCount] = Label(text = str(row[3]))
            self.classDays[classCount] = Label(text = row[4])
            self.ids.stud_sel_grid.add_widget(self.classButtons[classCount])
            self.ids.stud_sel_grid.add_widget(self.classInstructorLabels[classCount])
            self.ids.stud_sel_grid.add_widget(self.classTimes[classCount])
            self.ids.stud_sel_grid.add_widget(self.classDays[classCount])
            classCount = classCount + 1
        print self.classesInfo

    def on_leave(self):
        #Remove buttons from student selection page
        classCount = 0
        for row in self.classesInfo:
            self.ids.stud_sel_grid.remove_widget(self.classButtons[classCount])
            self.ids.stud_sel_grid.remove_widget(self.classInstructorLabels[classCount])
            self.ids.stud_sel_grid.remove_widget(self.classTimes[classCount])
            self.ids.stud_sel_grid.remove_widget(self.classDays[classCount])
            classCount = classCount + 1

        #Close MySQL connection
        self.cursor.close()
        self.conn.close()




    pass






#Handles Screen Transition
class ScreenManagement(ScreenManager):

    #This variable will hold the user's sign in name
    signin_name = ""
    signin_ID = ""
    class_choice = ""
    classNum_choice = ""

    pass

#Handles Student Page
class StudentPage(Screen):

    #Labels to be dynamically created
    assignmentGradeLabels = {}
    assignmentNameLabels = {}
    assignmentTypeLabels = {}
    assignmentDateLabels = {}

    #Assignment Info
    assignmentsInfo = {}


    def __init__(self, **kwargs):
        super(StudentPage, self).__init__(**kwargs)

    #Upon switching to this screen, we will call these functions
    #They will be used to populate tables and create buttons


    #Functions will be called here
    def on_pre_enter(self):
        Window.size = (960, 1080)
        print self.manager.signin_ID
        print self.manager.signin_name

        #Connect to database
        #Establish connection to MySQL database
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='password')
        self.cursor = self.conn.cursor()
        self.cursor.execute('USE Gradebook')
        #Query the database
        print 'Before Assignment Query'
        print self.manager.classNum_choice
        print self.manager.classNum_choice
        self.cursor.execute('SELECT Assignments.assignmentName, Student_has_Assignments.grade, \
                            Student_has_Assignments.studentID, Assignments.assignmentType, \
                            Student_has_Assignments.classNum, Assignments.dueDate FROM Student_has_Assignments \
                            INNER JOIN Assignments ON Assignments.assignmentName = Student_has_Assignments.assignmentName \
                            AND Assignments.classNum = Student_has_Assignments.classNum \
                            WHERE Student_has_Assignments.classNum ='+str(self.manager.classNum_choice)+' AND Student_has_Assignments.studentID = '+str(self.manager.signin_ID))

        self.assignmentsInfo = self.cursor.fetchall()
        print self.assignmentsInfo

        #Add label for each Assignment
        assignmentCount = 0
        for row in self.assignmentsInfo:
            self.assignmentNameLabels[assignmentCount] = Label(text = row[0])
            self.assignmentGradeLabels[assignmentCount] = Label(text = str(int(row[1])))
            self.assignmentDateLabels[assignmentCount] = Label(text = str(row[5]))
            self.assignmentTypeLabels[assignmentCount] = Label(text = row[3])
            self.ids.view_assignment_table.add_widget(self.assignmentNameLabels[assignmentCount])
            self.ids.view_assignment_table.add_widget(self.assignmentTypeLabels[assignmentCount])
            self.ids.view_assignment_table.add_widget(self.assignmentDateLabels[assignmentCount])
            self.ids.view_assignment_table.add_widget(self.assignmentGradeLabels[assignmentCount])
            assignmentCount = assignmentCount + 1

    def on_leave(self):
        assignmentCount = 0
        for row in self.assignmentsInfo:
            self.ids.view_assignment_table.remove_widget(self.assignmentNameLabels[assignmentCount])
            self.ids.view_assignment_table.remove_widget(self.assignmentTypeLabels[assignmentCount])
            self.ids.view_assignment_table.remove_widget(self.assignmentDateLabels[assignmentCount])
            self.ids.view_assignment_table.remove_widget(self.assignmentGradeLabels[assignmentCount])
            assignmentCount = assignmentCount + 1




    pass

#Handles Instructor Page
class InstructorPage(Screen):

    #Store the Assignment Table Info
    assign_table_info = {}

    #Labels and buttons
    studentNameLabels = {}
    studentGradeLabels = {}
    studentAssignmentLabels = {}
    studentGradeInputs = {}
    studentUpdateButtons = {}

    #List of Assignments
    assignmentsList = {}

    #List of students
    studentsList = {}

    #Student ID list
    studentIDList = {}

    #Drop down buttons
    buttonsList = {}
    studButtonsList = {}

    #Error popup window
    errorPop = 0
    errorBtn = 0
    errorLayout = 0
    errorLabel = 0

    #Student add popup window
    studErrorPop = 0
    studErrorBtn = 0
    studErrorLayout = 0
    studErrorLabel = 0

    #update popup window
    upErrorPop = 0
    upErrorBtn = 0
    upErrorLayout = 0
    upErrorLabel = 0


    def __init__(self, **kwargs):

        super(InstructorPage, self).__init__(**kwargs)

    def create_assignment_table(self):

        #Query the database and obtain all the students, assignments, and grades
        self.cursor.execute('SELECT DISTINCT Student_has_Assignments.grade, Student_has_Assignments.classNum, \
                             Students.firstName, Students.lastName, Assignments.assignmentName , Student_has_Assignments.studentID FROM Student_has_Assignments \
                             INNER JOIN Students ON Students.IDNum = Student_has_Assignments.studentID \
                             INNER JOIN Assignments ON Assignments.assignmentName = Student_has_Assignments.assignmentName \
                             WHERE Student_has_Assignments.classNum = '+ str(self.manager.classNum_choice))

        self.assign_table_info = self.cursor.fetchall()
        print self.assign_table_info

        #Each widget must have a unique id
        #ID System:
        #Grade Inputs = assignmentCount
        #Update Buttons = assignmentCount*2
        #This will be used to get the index of the list corresponding to the proper label
        assignmentCount = 0
        for row in self.assign_table_info:

            #Create widgets
            self.studentNameLabels[assignmentCount] = Label(text = row[2] + ' ' +row[3], size = (280, 50))
            self.studentAssignmentLabels[assignmentCount] = Label(text = row[4], size = (280, 50))
            self.studentGradeLabels[assignmentCount] = Label(text = str(row[0]), size = (280, 50))
            self.studentGradeInputs[assignmentCount] = TextInput(multiline = False)
            self.studentUpdateButtons[assignmentCount] = Button(text = "Update", id = str(assignmentCount))
            self.studentIDList[assignmentCount] = row[5]

            #Bind Buttons
            self.studentUpdateButtons[assignmentCount].bind(on_release = self.update_grade)

            #Place Widgets
            self.ids.instructor_assignment_table.add_widget(self.studentNameLabels[assignmentCount])
            self.ids.instructor_assignment_table.add_widget(self.studentAssignmentLabels[assignmentCount])
            self.ids.instructor_assignment_table.add_widget(self.studentGradeLabels[assignmentCount])
            self.ids.instructor_assignment_table.add_widget(self.studentGradeInputs[assignmentCount])
            self.ids.instructor_assignment_table.add_widget(self.studentUpdateButtons[assignmentCount])

            assignmentCount = assignmentCount + 1

    def update_table(self):

        #Obtain number of entries in table
        num_entries = len(self.studentAssignmentLabels)

        #Remove all the widgets within the table
        c = 0
        while c < num_entries:
            self.ids.instructor_assignment_table.remove_widget(self.studentNameLabels[c])
            self.ids.instructor_assignment_table.remove_widget(self.studentAssignmentLabels[c])
            self.ids.instructor_assignment_table.remove_widget(self.studentGradeLabels[c])
            self.ids.instructor_assignment_table.remove_widget(self.studentGradeInputs[c])
            self.ids.instructor_assignment_table.remove_widget(self.studentUpdateButtons[c])
            self.studentIDList[c] = ""
            c = c + 1

        #Query database for newly updated table and place new entries
        self.cursor.execute('SELECT DISTINCT Student_has_Assignments.grade, Student_has_Assignments.classNum, \
                             Students.firstName, Students.lastName, Assignments.assignmentName , Student_has_Assignments.studentID FROM Student_has_Assignments \
                             INNER JOIN Students ON Students.IDNum = Student_has_Assignments.studentID \
                             INNER JOIN Assignments ON Assignments.assignmentName = Student_has_Assignments.assignmentName \
                             WHERE Student_has_Assignments.classNum = '+ str(self.manager.classNum_choice))
        self.assign_table_info = self.cursor.fetchall()

        assignmentCount = 0
        for row in self.assign_table_info:

            #Create widgets
            self.studentNameLabels[assignmentCount] = Label(text = row[2] + ' ' +row[3], size = (280, 50))
            self.studentAssignmentLabels[assignmentCount] = Label(text = row[4], size = (280, 50))
            self.studentGradeLabels[assignmentCount] = Label(text = str(row[0]), size = (280, 50))
            self.studentGradeInputs[assignmentCount] = TextInput(multiline = False)
            self.studentUpdateButtons[assignmentCount] = Button(text = "Update", id = str(assignmentCount))
            self.studentIDList[assignmentCount] = row[5]

            #Bind Buttons
            self.studentUpdateButtons[assignmentCount].bind(on_release = self.update_grade)

            #Place Widgets
            self.ids.instructor_assignment_table.add_widget(self.studentNameLabels[assignmentCount])
            self.ids.instructor_assignment_table.add_widget(self.studentAssignmentLabels[assignmentCount])
            self.ids.instructor_assignment_table.add_widget(self.studentGradeLabels[assignmentCount])
            self.ids.instructor_assignment_table.add_widget(self.studentGradeInputs[assignmentCount])
            self.ids.instructor_assignment_table.add_widget(self.studentUpdateButtons[assignmentCount])

            assignmentCount = assignmentCount + 1

    def update_grade(self, instance):

        #Obtain the ID of the button which will correspond to the info of the first row
        index = int(instance.id)
        print self.studentIDList[index]

        #Obtain the text from the corresponding text input and clear it
        new_grade = self.studentGradeInputs[index].text
        print new_grade
        self.studentGradeInputs[index].text = ""

        #Create error popup
        self.upErrorLayout = RelativeLayout(rows = 2, cols = 1, size_hint = (None, None), size = (380, 380))
        self.upErrorLabel = Label(text = 'Could not update grade. Try Again', size_hint = (None, None), size = (180,180), pos = (110, 100))
        self.upErrorBtn = Button(text = 'Close Window', size_hint = (None, None), size = (180,100), pos = (110, 0))
        self.upErrorLayout.add_widget(self.upErrorLabel)
        self.upErrorLayout.add_widget(self.upErrorBtn)

        self.upErrorPop = Popup(title='Error', content=self.upErrorLayout, auto_dismiss=False, size_hint = (None, None), size = (400, 400))
        self.upErrorBtn.bind(on_press=self.upErrorPop.dismiss)

        try:

            self.cursor.execute('UPDATE Student_has_Assignments SET grade = '+ str(new_grade)+ ' WHERE assignmentName = \''+ str(self.studentAssignmentLabels[index].text)
                                + '\' AND classNum = '+ str(self.manager.classNum_choice)+ ' AND studentID = '+ str(self.studentIDList[index]))
            self.conn.commit()
        except MySQLdb.Error as e:
            self.conn.rollback()              #rollback transaction here
            self.upErrorPop.open()

        self.update_table()






    def create_dropdown(self):

        #Get list of assignments for this class
        self.cursor.execute('SELECT assignmentName FROM Assignments \
                             WHERE classNum = '+ str(self.manager.classNum_choice))

        self.assignmentsList = self.cursor.fetchall()
        print self.assignmentsList


        self.assignmentDropdown = DropDown()
        numbtns = 0
        for row in self.assignmentsList:
            self.buttonsList[numbtns] = Button(text = row[0], size_hint = (None, None), size = (230, 40))
            self.buttonsList[numbtns].bind(on_release = self.dropdownBtnChoice)
            self.assignmentDropdown.add_widget(self.buttonsList[numbtns])
            numbtns = numbtns + 1

        self.mainDropBtn = Button(text = 'Delete Assignment',size_hint = (None, None), size = (230, 40))
        self.mainDropBtn.bind(on_release = self.assignmentDropdown.open)

        self.ids.add_del_assignment.add_widget(self.mainDropBtn)

    def create_stud_dropdown(self):

        #Get list of students and their IDs
        self.cursor.execute('SELECT DISTINCT Students.firstName, Students.lastName, Student_has_Classes.studentNum FROM Students \
                             INNER JOIN Student_has_Classes ON Students.IDNum = Student_has_Classes.studentNum WHERE \
                             Student_has_Classes.classNum = '+ str(self.manager.classNum_choice))
        self.studentsList = self.cursor.fetchall()

        self.studentDropdown = DropDown()
        numbtns = 0
        for row in self.studentsList:
            self.studButtonsList[numbtns] = Button(text = row[0] +' '+row[1] + ', '+ 'ID: '+ str(row[2]), size_hint = (None, None), size = (230, 40))
            self.studButtonsList[numbtns].bind(on_release = self.studDropdownBtnChoice)
            self.studentDropdown.add_widget(self.studButtonsList[numbtns])
            numbtns = numbtns + 1

        self.studMainDropBtn = Button(text = 'Remove Student',size_hint = (None, None), size = (230, 40))
        self.studMainDropBtn.bind(on_release = self.studentDropdown.open)

        self.ids.add_del_stud.add_widget(self.studMainDropBtn)

    def update_stud_dropdown(self):
        btnindex = 0
        btns = len(self.studButtonsList)
        while btnindex < btns:
            self.studentDropdown.remove_widget(self.studButtonsList[btnindex])
            btnindex = btnindex + 1

        #Remake buttons and bind them again
        self.studButtonsList = {}
        self.cursor.execute('SELECT DISTINCT Students.firstName, Students.lastName, Student_has_Classes.studentNum FROM Students \
                             INNER JOIN Student_has_Classes ON Students.IDNum = Student_has_Classes.studentNum WHERE \
                             Student_has_Classes.classNum = '+ str(self.manager.classNum_choice))
        self.studentsList = self.cursor.fetchall()

        #Loop through updated list
        numbtns = 0
        for row in self.studentsList:
            self.studButtonsList[numbtns] = Button(text = row[0] +' '+row[1] + ', '+ 'ID: '+ str(row[2]), size_hint = (None, None), size = (230, 40))
            self.studButtonsList[numbtns].bind(on_release = self.studDropdownBtnChoice)
            self.studentDropdown.add_widget(self.studButtonsList[numbtns])
            numbtns = numbtns + 1



    def update_dropdown(self):

        #Loop through the buttons list, removing each one and then query and reupdate it
        btnindex = 0
        btns = len(self.buttonsList)
        while btnindex < btns:
            self.assignmentDropdown.remove_widget(self.buttonsList[btnindex])
            btnindex = btnindex + 1

        #Remake buttons and bind them again
        self.buttonsList = {}
        self.cursor.execute('SELECT assignmentName FROM Assignments \
                             WHERE classNum = '+ str(self.manager.classNum_choice))
        self.assignmentsList = self.cursor.fetchall()

        #Loop through updated list
        numbtns = 0
        for row in self.assignmentsList:
            self.buttonsList[numbtns] = Button(text = row[0], size_hint = (None, None), size = (230, 40))
            self.buttonsList[numbtns].bind(on_release = self.dropdownBtnChoice)
            self.assignmentDropdown.add_widget(self.buttonsList[numbtns])
            numbtns = numbtns + 1


    def studDropdownBtnChoice(self, instance):
        print instance.text
        stud_remove = instance.text
        #Split the string to obtain the ID num
        split_string = stud_remove.split()
        stud_remove_ID = split_string[3]
        print stud_remove_ID

        #Remove the selected student
        self.cursor.execute('USE Gradebook')
        self.cursor.execute('DELETE FROM Student_has_Classes WHERE studentNum = '+ stud_remove_ID
                             + ' AND classNum = '+ str(self.manager.classNum_choice))

        self.conn.commit()

        #Update table and drop down
        self.update_stud_dropdown()
        self.update_table()


    def dropdownBtnChoice(self, instance):

        print instance.text

        #Delete the assignment selected
        self.cursor.execute('USE Gradebook')
        #print 'DELETE FROM Assignments WHERE assignmentName = \''+ instance.text +'\' AND classNum = '+ str(self.manager.classNum_choice)
        self.cursor.execute('DELETE FROM Assignments WHERE assignmentName = \''+ instance.text +'\' AND classNum = '+ str(self.manager.classNum_choice))
        self.conn.commit()

        #Update table and drop down
        self.update_dropdown()
        self.update_table()

    def add_student(self):

        print self.ids.student_ID_input.text

        #Capture text input from text box
        new_stud_ID = self.ids.student_ID_input.text

        #Clear the text box
        self.ids.student_ID_input.text = ""

        print new_stud_ID

        #Create popup Window
        self.studErrorLayout = RelativeLayout(rows = 2, cols = 1, size_hint = (None, None), size = (380, 380))
        self.studErrorLabel = Label(text = 'Could not add student. Try Again', size_hint = (None, None), size = (180,180), pos = (110, 100))
        self.studErrorBtn = Button(text = 'Close Window', size_hint = (None, None), size = (180,100), pos = (110, 0))
        self.studErrorLayout.add_widget(self.studErrorLabel)
        self.studErrorLayout.add_widget(self.studErrorBtn)

        self.studErrorPop = Popup(title='Error', content=self.studErrorLayout, auto_dismiss=False, size_hint = (None, None), size = (400, 400))
        self.studErrorBtn.bind(on_press=self.studErrorPop.dismiss)

        #Try to Add student to the class
        try:
            self.cursor.execute('INSERT INTO Student_has_Classes (classNum, studentNum, instructorNum) \
                                 VALUES (' + str(self.manager.classNum_choice)+ ', '+ str(new_stud_ID)+ ', '
                                 + str(self.manager.signin_ID)+ ')')
            self.conn.commit()
        except MySQLdb.Error as e:
            self.studErrorLabel.text = 'Could not add student. Try Again'
            self.conn.rollback()              #rollback transaction here
            self.studErrorPop.open()

        #Obtain assignments from the current class in order to assign them to new students
        self.cursor.execute('SELECT assignmentName FROM Assignments WHERE classNum = '+ str(self.manager.classNum_choice))
        toAssign = self.cursor.fetchall()



        #Try to assign existing assignments to student
        try:
            for row in toAssign:
                self.cursor.execute('INSERT INTO Student_has_Assignments (classNum, assignmentName, studentID, grade) \
                                     VALUES (' +str(self.manager.classNum_choice)+ ', \''+ row[0]+ '\', '+ str(new_stud_ID)+ ', 0)')
                self.conn.commit()
        except MySQLdb.Error as e:
            self.studErrorLabel.text = 'Trouble assigning assignments. Try Again'
            self.conn.rollback()              #rollback transaction here
            self.studErrorPop.open()

        self.update_stud_dropdown()
        self.update_table()


    def create_assignment(self):

        #Take the text from the text boxes and store them in variables
        assign_name = self.ids.assign_name_input.text
        assign_type = self.ids.assign_type_input.text
        assign_date = self.ids.assign_date_input.text

        #Clear the text box
        self.ids.assign_name_input.text = ""
        self.ids.assign_type_input.text = ""
        self.ids.assign_date_input.text = ""

        #Create popup Window
        self.errorLayout = RelativeLayout(rows = 2, cols = 1, size_hint = (None, None), size = (380, 380))
        self.errorLabel = Label(size_hint = (None, None), size = (180,180), pos = (110, 100))
        self.errorBtn = Button(text = 'Close Window', size_hint = (None, None), size = (180,100), pos = (110, 0))
        self.errorLayout.add_widget(self.errorLabel)
        self.errorLayout.add_widget(self.errorBtn)

        self.errorPop = Popup(title='Error', content=self.errorLayout, auto_dismiss=False, size_hint = (None, None), size = (400, 400))
        self.errorBtn.bind(on_press=self.errorPop.dismiss)

        #Try to add the assignment to the database
        try:
            self.errorLabel.text = 'Could not create assignment. Try Again'
            self.cursor.execute('INSERT INTO Assignments (assignmentName, assignmentType, dueDate, classNum, instructorID) \
                                 VALUES (\'' +assign_name+ '\', \'' +assign_type+ '\', \'' +assign_date+ '\', ' +str(self.manager.classNum_choice)+ ', ' +str(self.manager.signin_ID)+ ')')
            self.conn.commit()
        except MySQLdb.Error as e:
            self.conn.rollback()              #rollback transaction here
            self.errorPop.open()

        #Obtain the list of students in the class and assign the assignment to each one
        self.cursor.execute('SELECT studentNum FROM Student_has_Classes WHERE classNum = '+ str(self.manager.classNum_choice))
        list_of_studs = self.cursor.fetchall()
        time.sleep(.1)

        #Try to assign existing assignments to student
        try:
            for row in list_of_studs:
                print 'INSERT INTO Student_has_Assignments (classNum, assignmentName, studentID, grade) \
                                     VALUES (' +str(self.manager.classNum_choice)+ ', \''+assign_name+ '\', '+ str(row[0])+ ', 0)'
                self.cursor.execute('INSERT INTO Student_has_Assignments (classNum, assignmentName, studentID, grade) \
                                     VALUES (' +str(self.manager.classNum_choice)+ ', \''+assign_name+ '\', '+ str(row[0])+ ', 0)')
                self.conn.commit()
        except MySQLdb.Error as e:
            self.errorLabel.text = 'Trouble assigning assignments. Try Again'
            self.conn.rollback()              #rollback transaction here
            self.errorPop.open()

        self.update_dropdown()
        self.update_table()


    def on_pre_enter(self):
        Window.size = (1400, 1080)
        print self.manager.signin_ID
        print self.manager.signin_name
        print self.manager.classNum_choice

        #Establish SQL connection and choose database
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='password')
        self.cursor = self.conn.cursor()
        self.cursor.execute('USE Gradebook')
        #Function calls that will be called upon entering
        self.create_dropdown()
        self.create_stud_dropdown()
        self.create_assignment_table()

    def on_leave(self):
        #Remove table and dropdown
        num_entries = len(self.studentAssignmentLabels)

        #Remove all the widgets within the table
        c = 0
        while c < num_entries:
            self.ids.instructor_assignment_table.remove_widget(self.studentNameLabels[c])
            self.ids.instructor_assignment_table.remove_widget(self.studentAssignmentLabels[c])
            self.ids.instructor_assignment_table.remove_widget(self.studentGradeLabels[c])
            self.ids.instructor_assignment_table.remove_widget(self.studentGradeInputs[c])
            self.ids.instructor_assignment_table.remove_widget(self.studentUpdateButtons[c])
            self.studentIDList[c] = ""
            c = c + 1

        self.ids.add_del_assignment.remove_widget(self.mainDropBtn)

        btnindex = 0
        btns = len(self.buttonsList)
        while btnindex < btns:
            self.assignmentDropdown.remove_widget(self.buttonsList[btnindex])
            btnindex = btnindex + 1

        self.ids.add_del_stud.remove_widget(self.studMainDropBtn)
        btnindex = 0
        btns = len(self.studButtonsList)
        while btnindex < btns:
            self.studentDropdown.remove_widget(self.studButtonsList[btnindex])
            btnindex = btnindex + 1

        self.cursor.close()
        self.conn.close()




class InstructorSelectionPage(Screen):

    #Declare list that will store buttons
    instructorClassButtons = {}

    #List that will store class times
    instructorClassTimes = {}

    #List that will store class days
    instructorClassDays = {}

    #List that will store the current instructor class info
    instructorClassInfo = {}

    def __init__(self, **kwargs):

        super(InstructorSelectionPage, self).__init__(**kwargs)

    #Labels for the classes taught by instructor choice
    def on_pre_enter(self):
        Window.size = (600, 300)

        #Reset the class class choice
        self.manager.class_choice = {}

        #Establish connection to MySQL database
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='password')
        self.cursor = self.conn.cursor()
        self.cursor.execute('USE Gradebook')
        #print self.manager.signin_name
        #print self.manager.signin_ID

        #Query the database and store results in list
        self.cursor.execute('SELECT Classes.classCode, Classes.classTime, Classes.days FROM Classes \
                             WHERE '+ str(self.manager.signin_ID) +' = Classes.taughtBy')

        self.classesInfo = self.cursor.fetchall()

        print self.classesInfo

        #Add buttons to screen for each class
        classCount = 0
        for row in self.classesInfo:
            self.instructorClassButtons[classCount] = Button(text = row[0], id = str(classCount))
            self.instructorClassButtons[classCount].bind(on_press=self.instructor_class_press)
            self.instructorClassTimes[classCount] = Label(text = str(row[1]))
            self.instructorClassDays[classCount] = Label(text = row[2])
            self.ids.inst_sel_grid.add_widget(self.instructorClassButtons[classCount])
            self.ids.inst_sel_grid.add_widget(self.instructorClassTimes[classCount])
            self.ids.inst_sel_grid.add_widget(self.instructorClassDays[classCount])
            classCount = classCount + 1

    def instructor_class_press(self, instance):
        #Remember the id thing works to use in the instructor assignment page
        # buttonCount = 0
        # for button in self.instructorClassButtons:
        #     if(str(self.instructorClassButtons[buttonCount].id) == instance.id):
        #         print 'Printing ID'
        #         print instance.id
        #         print buttonCount
        #     buttonCount = buttonCount + 1


        #Obtain user class choice code
        self.manager.class_choice = instance.text

        #Obtain class classNum primary key based on button choice
        self.cursor.execute('SELECT Classes.classNum FROM Classes WHERE Classes.classCode = \''+self.manager.class_choice+'\'')
        classID = self.cursor.fetchall()
        for row in classID:
            self.manager.classNum_choice = row[0]

        print 'After obtaining ClassNum'
        print self.manager.classNum_choice

        #Use code to find class number
        print(self.manager.class_choice)
        self.manager.current = 'instructor_page'

    def on_leave(self):
        #Remove buttons from student selection page
        classCount = 0
        for row in self.classesInfo:
            self.ids.inst_sel_grid.remove_widget(self.instructorClassButtons[classCount])
            self.ids.inst_sel_grid.remove_widget(self.instructorClassTimes[classCount])
            self.ids.inst_sel_grid.remove_widget(self.instructorClassDays[classCount])
            classCount = classCount + 1

        #Close MySQL connection
        self.cursor.close()
        self.conn.close()






    pass

#Creates the App
class GradebookApp(App):
    def builder(self):
        return kv_file

if __name__ == '__main__':
    GradebookApp().run()
