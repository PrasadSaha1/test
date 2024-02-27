#importing tkinter and the messagebox module. Everything is imported from tkinter for convenience
from tkinter import *
from tkinter import messagebox
from math import factorial
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import webbrowser
#to access docstrings, put help(FUNCTION/CLASS NAME) at the very end of the code, then exit out of the window and look at the print area

#creating the window
window = Tk()
window.geometry("700x700")
window.title("GPA Calculator")

#Setting some constants. Using these make it easier to change the entire program at once
BACKGROUND_COLOR = "#481c1c"
FONT = "Times New Roman"
TEXTCOLOR = "#66ff33"

#setting the background color for the GUI
window.config(background=BACKGROUND_COLOR)

#this variable determines what screen is being displayed
screen = "home"

first_frame_cumulative_GPA = True
first_frame_settings = True
first_frame_previous_data_classes = True
data_loaded = False
gpa_calculated = False
x_location_change = 0
time = 0

error_sign = PhotoImage(file="error.png")
error_labels = []
for label in range(1000):
    error_label = Label(window, image=error_sign, bg=BACKGROUND_COLOR)
    error_labels.append(error_label)


file_path = "data_for_calc_gpa.txt"
previous_data_all = []
previous_data_classes = []

file_append = open(file_path, 'a')
file_read = open(file_path, "r")

#if os.path.exists(file_path):
#    previous_data.append((file_read.read()))

#this program uses classes to help organize the code
class HomeScreen:
    '''The HomeScreen class controls the elements that appear when the user starts the program'''
    def __init__(self):
        '''This function makes the widgets that will appear on the home screen. It also creates the universal back button'''
        self.intro_text = Label(window, text="Welcome to the GPA Calculator!", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 30))
        self.calc_my_gpa = Button(window, text="Calculate my GPA", command=self.calc_my_gpa_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                  activeforeground=TEXTCOLOR)
        self.help = Button(window, text="Help", command=self.help_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                  activeforeground=TEXTCOLOR)
        self.data_information = Button(window, text="Data Information", command=self.data_information_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                  activeforeground=TEXTCOLOR)

        #universal back button
        self.universal_back_button = Button(window, text="Back", command=self.universal_back_button_func,
                                            font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

    def calc_my_gpa_func(self):
        '''When the button is pressed, the screen will change to the GPA home screen'''
        global screen, file_append
        if os.path.getsize("data_for_calc_gpa.txt") and not data_loaded:
            answer = messagebox.askyesno("Data not loaded",
                                         "There is data that can be imported by going to the Data Information screen. Click Yes for an oppurtunity to load that data, click No to continue and lose that data")
            if answer:
                pass
            else:
                file_append.truncate(0)
                screen = "GPA_home"
        else:
            screen = "GPA_home"

    def help_func(self):
        '''When the button is pressed, the screen will change to the help menu'''
        global screen, file_append
        if os.path.getsize("data_for_calc_gpa.txt") and not data_loaded:
            answer = messagebox.askyesno("Data not loaded",
                                         "There is data that can be imported by going to the Data Information screen. If you click no, that data will be lost.")
            if answer:
                pass
            else:
                file_append.truncate(0)
                screen = "help_menu"
        else:
            screen = "help_menu"

    def data_information_func(self):
        '''When the button is pressed, the screen will change to the data menu'''
        global screen
        screen = "data_menu"

    def universal_back_button_func(self):
        '''When the back button is pressed, the user will be brought to the previous screen'''
        global screen
        if screen in ["GPA_home", "help_menu", "data_menu"]:
            screen = "home" #at the first screen after the home menu, if back is pressed, the user will go back to the home menu
        if screen in ["instructions_1", "instructions_2", "settings"]:
            screen = "help_menu" #within the screens of the help menu, the user will be brought to the help menu hold back if the back button is pressed
        if screen in ["quarterly_grades", "cumulative_grades"]:
            screen = "GPA_home" #within the screens of the GPA menu, the user will go back to the GPA home page
        if screen == "class_term_grades_chooser":
            screen = "cumulative_grades"

class GPACalculator:
    '''The GPACalculator class controls the elements after the user hits Calculate my GPA from the home screen'''
    def __init__(self):
        '''This defines all the widgets for the GPA home screen'''
        self.gpa_text = Label(window, text="Choose scope of GPA", font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.quarterly_button = Button(window, text="Quarterly", command=self.quarterly_button_func, font=(FONT, 30),
                               bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                               activeforeground=TEXTCOLOR)
        self.cumulative_button = Button(window, text="Annual/Cumulative", command=self.cumulative_button_func, font=(FONT, 30),
                          bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                          activeforeground=TEXTCOLOR)

        #define numbers
        self.y_var = 150
        self.year_8_classes_y_var = 149
        self.year_9_classes_y_var = 149
        self.year_10_classes_y_var = 329
        self.year_11_classes_y_var = 329
        self.year_12_classes_y_var = 509
        self.gpa_scale = 100.0

        self.honors_scale_100 = 1.03
        self.AP_scale_100 = 1.05
        self.honors_scale_4 = 1.125
        self.AP_scale_4 = 1.25

        self.default_Q1 = 21.25
        self.default_Q2 = 21.25
        self.default_Q3 = 21.25
        self.default_Q4 = 21.25
        self.default_E2 = 5
        self.default_E4 = 10

        self.honors_scale = self.honors_scale_100
        self.AP_scale = self.AP_scale_100
        self.unweighted_gpa = ''
        self.weighted_gpa = ''

        #these store the data for each of the user's class
        self.class_data_quarterly = []
        self.class_data_cumulative = []
        self.for_export = []
        self.data2 = []
        self.classes_on_screen = []
        self.term_info_widgets = []

        self.term_grade_label = Label()
        self.term_weight_label = Label()

        #this stores the grades for the 4.0 scale
        self.grades_4 = {"A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
                         "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "F": 0.0}
        # Converts numerical grades to letter grades
        self.grade_ranges_4 = {"A+": range(97, factorial(999)), "A": range(93, 97), "A-": range(90, 93), "B+": range(87, 90),
                               "B": range(83, 87), "B-": range(80, 83), "C+": range(77, 80), "C": range(73, 77),
                               "C-": range(70, 73), "D+": range(67, 70), "D": range(65, 67), "F": range(0, 65)}

        #this the text at the top of the window
        self.GPA_home_text = Label(window, text="Fill in the information requested\n Add new classes as neccesary\nHit Calculate my GPA for your weighted and unweighted GPA", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))

        #this is determine if the GPA is on the 100.0 or 4.0 scale
        self.GPA_type_label = Label(window, text="Scale:", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.current_scale = Label(window, text=self.gpa_scale, bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.change_scale = Button(window, text="Change Scale", command=self.change_scale_func, font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #this is the text above the entry area
        self.class_name_label = Label(window, text="Class Name", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.grade_label = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weight_label = Label(window, text="Weight", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.credit_label = Label(window, text="Credit", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        #self.year_label = Label(window, text="Year", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #these are to scroll through the classes once there are more than 9
        self.next_page_classes = Button(window, text="Next Page", command=self.next_page_classes_func, font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.previous_page_classes = Button(window, text="Previous Page", command=self.previous_page_classes_func, font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #these are the buttons at the bottom of the window
        self.add_new_class = Button(window, text="Add New Class", command=self.add_new_class_func, font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_class = Button(window, text="Delete Class", command=self.delete_class_func, font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.whats_my_gpa = Button(window, text="Calculate my GPA", command=self.whats_my_gpa_func, font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #this is where the gpa is displayed
        self.unweighted_gpa_label = Label(window, text=f"Unweighted GPA: {self.unweighted_gpa}", font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weighted_gpa_label = Label(window, text=f"Weighted GPA: {self.weighted_gpa}", font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #defines the widgets for Cumulative GPA screen
        self.Cumulative_GPA_text = Label(window, text="Fill in the information requested\n Add new classes and years as neccesary\nHit Calculate my GPA for your cumulative weighted and unweighted GPA", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))

        #year 8 widgets
        self.year_8_label = Label(window, text="8th Grade", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.class_name_label_8 = Label(window, text="Class Name", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.grade_label_8 = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weight_label_8 = Label(window, text="Weight", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.credit_label_8 = Label(window, text="Credit", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        #self.year_label_8 = Label(window, text="Year", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.add_class_8 = Button(window, text="Add Class", command=lambda: self.add_class_cumulative_func(year=8), font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_class_8 = Button(window, text="Delete Class", command=lambda: self.delete_class_cumulative_func(year=8), font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #year 9 widgets
        self.year_9_label = Label(window, text="9th Grade", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.class_name_label_9 = Label(window, text="Class Name", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.grade_label_9 = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weight_label_9 = Label(window, text="Weight", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.credit_label_9 = Label(window, text="Credit", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
       # self.year_label_9 = Label(window, text="Year", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.add_class_9 = Button(window, text="Add Class", command=lambda: self.add_class_cumulative_func(year=9), font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_class_9 = Button(window, text="Delete Class", command=lambda: self.delete_class_cumulative_func(year=9), font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #10th grade widgets
        self.year_10_label = Label(window, text="10th Grade", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.class_name_label_10 = Label(window, text="Class Name", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.grade_label_10 = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weight_label_10 = Label(window, text="Weight", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.credit_label_10 = Label(window, text="Credit", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        #self.year_label_10 = Label(window, text="Year", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.add_class_10 = Button(window, text="Add Class", command=lambda: self.add_class_cumulative_func(year=10), font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_class_10 = Button(window, text="Delete Class", command=lambda: self.delete_class_cumulative_func(year=10), font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #widgets for 11th grade
        self.year_11_label = Label(window, text="11th Grade", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.class_name_label_11 = Label(window, text="Class Name", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.grade_label_11 = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weight_label_11 = Label(window, text="Weight", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.credit_label_11 = Label(window, text="Credit", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        #self.year_label_11 = Label(window, text="Year", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.add_class_11 = Button(window, text="Add Class", command=lambda: self.add_class_cumulative_func(year=11), font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_class_11 = Button(window, text="Delete Class", command=lambda: self.delete_class_cumulative_func(year=11), font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #year 12 widgets
        self.year_12_label = Label(window, text="12th Grade", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.class_name_label_12 = Label(window, text="Class Name", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.grade_label_12 = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weight_label_12 = Label(window, text="Weight", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.credit_label_12 = Label(window, text="Credit", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        #self.year_label_12 = Label(window, text="Year", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.add_class_12 = Button(window, text="Add Class", command=lambda: self.add_class_cumulative_func(year=12), font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_class_12 = Button(window, text="Delete Class", command=lambda: self.delete_class_cumulative_func(year=12), font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

    def quarterly_button_func(self):
        global screen
        screen = "quarterly_grades"
        #this resets the GPA
        self.unweighted_gpa = ""
        self.weighted_gpa = ""
        #self.class_data.clear()

    def cumulative_button_func(self):
        global screen
        screen = "cumulative_grades"
        #this resets the GPA
        self.unweighted_gpa = ""
        self.weighted_gpa = ""
        #self.class_data.clear()

    def change_scale_func(self):
        if self.gpa_scale == 100.0:
            self.gpa_scale = 4.0
            self.honors_scale = self.honors_scale_4
            self.AP_scale = self.AP_scale_4
        elif self.gpa_scale == 4.0:
            self.gpa_scale = 100.0
            self.honors_scale = self.honors_scale_100
            self.AP_scale = self.AP_scale_100
        self.current_scale.config(text=self.gpa_scale)

    def choose_scale_100_func(self):
        '''This sets the GPA scale to 100.0 when the 100.0 button is pressed'''
        self.gpa_scale = 100

    def choose_scale_4_func(self):
        '''This sets the GPA to 4.0 when the 4.0 button is pressed'''
        self.gpa_scale = 4

    def add_new_class_func(self):
        '''This function adds a new row of entry boxes (a new class for the user) when they press the add new class button'''
        #These are the entry boxes, similar to the ones in the __init__ function
        class_entry = Entry(window, width=15, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        grade_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)

        var = StringVar(window)
        weight_menu = OptionMenu(window, var, "R", "H", "AP")
        weight_menu.config(bg=BACKGROUND_COLOR, fg=TEXTCOLOR, highlightthickness=0, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR, width=5, font=(FONT, 10)) #change the location of credit entry maybe

        credit_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        #year_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)

        #this appends the information about the class to class_data
        #no x_location_change
        self.class_data_quarterly.append([[class_entry, 100, self.y_var],
                                          [grade_entry, 254, self.y_var],
                                          [weight_menu, 308, self.y_var],
                                          [credit_entry, 382, self.y_var],
                                          ])

        #this places the new entry boxes
      #  if len(self.class_data) <= 8:
       # class_entry.place(x=100 + x_location_change, y=self.y_var)
       # grade_entry.place(x=254 + x_location_change, y=self.y_var)
       # weight_menu.place(x=308 + x_location_change, y=self.y_var)
       # credit_entry.place(x=382 + x_location_change, y=self.y_var)
            #year_entry.place(x=436 + x_location_change, y=self.y_var)
      #      self.classes_on_screen.append((class_entry, grade_entry, weight_menu, credit_entry, year_entry))

        # this makes the row of entry boxes move down every time the user adds a new class
        self.y_var += 26

    def delete_class_func(self):
        """This deletes the most recent class when called"""
        if len(self.class_data_quarterly) >= 1:  # confirms there is more than one class
            for widget in self.class_data_quarterly[-1]:
                widget[0].place_forget()  # this loop removes the widgets for the deleted class from the window
            self.class_data_quarterly.pop()  # this removes the user's class from class_data
            self.y_var -= 26  # this confirms that the next class added is below the previous class

    def add_class_cumulative_func(self, year):
        small_class_entry = Entry(window, width=10, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                insertbackground=TEXTCOLOR)
        grade_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                insertbackground=TEXTCOLOR)

        var = StringVar(window)
        weight_menu = OptionMenu(window, var, "R", "H", "AP") #REMOVE THE BLACK BAR
        weight_menu.config(bg=BACKGROUND_COLOR, fg=TEXTCOLOR, highlightthickness=0, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR, width=3, font=(FONT, 10)) #change the location of credit entry maybe

        credit_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                 insertbackground=TEXTCOLOR)
        more_info = Button(window, text="More", command= lambda: self.more_info_func(Class=small_class_entry.get()), font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        x_var_cumulative = 0
        y_var_cumulative = 0

        if year == 8:
            self.year_8_classes_y_var += 26
            y_var_cumulative = self.year_8_classes_y_var
            x_var_cumulative = 22
        elif year == 9:
            self.year_9_classes_y_var += 26
            y_var_cumulative = self.year_9_classes_y_var
            x_var_cumulative = 337
        elif year == 10:
            self.year_10_classes_y_var += 26
            y_var_cumulative = self.year_10_classes_y_var
            x_var_cumulative = 22
        elif year == 11:
            self.year_11_classes_y_var += 26
            y_var_cumulative = self.year_11_classes_y_var
            x_var_cumulative = 337
        elif year == 12:
            self.year_12_classes_y_var += 26
            y_var_cumulative = self.year_12_classes_y_var
            x_var_cumulative = 22

        #this places the entry boxes
        #small_class_entry.place(x=x_var_cumulative + x_location_change, y=y_var_cumulative)
        #grade_entry.place(x=x_var_cumulative + 104 + x_location_change, y=y_var_cumulative)
        #weight_menu.place(x=x_var_cumulative + 158 + x_location_change, y=y_var_cumulative)
        #credit_entry.place(x=x_var_cumulative + 212 + x_location_change, y=y_var_cumulative)
        #more_info.place(x=x_var_cumulative + 266 + x_location_change, y=y_var_cumulative)
        #no x location change
        self.class_data_cumulative.append([(small_class_entry, x_var_cumulative, y_var_cumulative),
                                (grade_entry, x_var_cumulative + 104, y_var_cumulative),
                               (weight_menu, x_var_cumulative + 158, y_var_cumulative),
                                (credit_entry, x_var_cumulative + 212, y_var_cumulative),
                               (more_info, x_var_cumulative + 266, y_var_cumulative),
                                year, ["", str(self.default_Q1)], ["", str(self.default_Q2)], ["", str(self.default_E2)], ["", str(self.default_Q3)], ["", str(self.default_Q4)], ["", str(self.default_E4)], ""])
        self.for_export.append([["", x_var_cumulative, y_var_cumulative],
                                           ["", x_var_cumulative + 104, y_var_cumulative],
                                           ["", x_var_cumulative + 158, y_var_cumulative],
                                           ["", x_var_cumulative + 212, y_var_cumulative],
                                           ["", x_var_cumulative + 266, y_var_cumulative],
                                           year, ["", str(self.default_Q1)], ["", str(self.default_Q2)],
                                           ["", str(self.default_E2)], ["", str(self.default_Q3)],
                                           ["", str(self.default_Q4)], ["", str(self.default_E4)], ""])

    def delete_class_cumulative_func(self, year):
        classes = 0
        classes_of_year = []
        for Class in self.class_data_cumulative:
            if Class[5] == year:
                classes += 1
                classes_of_year.append(Class)
        if classes:
            if classes_of_year[-1][0][0].get() == "":
                messagebox.showerror("Remove Class Error", "Please enter a name for the class before removing it")
            else:
                self.class_data_cumulative.remove(classes_of_year[-1])
                for index, Class in enumerate(self.for_export):
                    if classes_of_year[-1][0][0].get() == Class[index][0]:
                        self.for_export.remove(Class)
                for widget in classes_of_year[-1][0:5]:
                    widget[0].place_forget()
                if year == 8:
                    self.year_8_classes_y_var -= 26
                elif year == 9:
                    self.year_9_classes_y_var -= 26
                elif year == 10:
                    self.year_10_classes_y_var -= 26
                elif year == 11:
                    self.year_11_classes_y_var -= 26
                elif year == 12:
                    self.year_12_classes_y_var -= 26

    def more_info_func(self, Class):
        global screen
        weight = credit = 0
        if Class == "":
            messagebox.showerror("Calc GPA Error", "Please enter in a class name first")
        else:
            for users_class in self.class_data_cumulative:
                if users_class[0][0].get() == Class:
                    weight = users_class[2][0]["text"]
                    credit = users_class[3][0].get()

                    current_Q1_grade = users_class[6][0]
                    current_Q2_grade = users_class[7][0]
                    current_E2_grade = users_class[8][0]
                    current_Q3_grade = users_class[9][0]
                    current_Q4_grade = users_class[10][0]
                    current_E4_grade = users_class[11][0]

                    current_Q1_weight = users_class[6][1]
                    current_Q2_weight = users_class[7][1]
                    current_E2_weight = users_class[8][1]
                    current_Q3_weight = users_class[9][1]
                    current_Q4_weight = users_class[10][1]
                    current_E4_weight = users_class[11][1]

            screen = "class_term_grades_chooser"
            self.term_grade_class_name = Label(window, text=f"Class Name: {Class}", font=(FONT, 20),
                                               bg=BACKGROUND_COLOR,
                                               fg=TEXTCOLOR)
            self.term_grade_weight = Label(window, text=f"Type: {weight}", font=(FONT, 20), bg=BACKGROUND_COLOR,
                                           fg=TEXTCOLOR)
            self.term_grade_credit = Label(window, text=f"Credit: {credit}", font=(FONT, 20), bg=BACKGROUND_COLOR,
                                           fg=TEXTCOLOR)
            self.terms_text = Label(window, text="Terms", font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.term_grade_label = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.term_weight_label = Label(window, text="%", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

            self.Q1 = Label(window, text="Q1:", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.Q2 = Label(window, text="Q2:", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.E2 = Label(window, text="E2:", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.Q3 = Label(window, text="Q3:", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.Q4 = Label(window, text="Q4:", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.E4 = Label(window, text="E4:", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

            self.Q1_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                  insertbackground=TEXTCOLOR)
            self.Q2_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                  insertbackground=TEXTCOLOR)
            self.E2_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                  insertbackground=TEXTCOLOR)
            self.Q3_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                  insertbackground=TEXTCOLOR)
            self.Q4_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                  insertbackground=TEXTCOLOR)
            self.E4_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                  insertbackground=TEXTCOLOR)

            self.Q1_weight = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                   insertbackground=TEXTCOLOR)
            self.Q2_weight = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                   insertbackground=TEXTCOLOR)
            self.E2_weight = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                   insertbackground=TEXTCOLOR)
            self.Q3_weight = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                   insertbackground=TEXTCOLOR)
            self.Q4_weight = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                   insertbackground=TEXTCOLOR)
            self.E4_weight = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                   insertbackground=TEXTCOLOR)

            self.save_button = Button(window, text="Save", command= lambda: self.save_button_func(Class=Class), font=(FONT, 20),
                                      bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                      activeforeground=TEXTCOLOR)

            self.term_grade_class_name.place(x=173 + x_location_change, y=20)
            self.term_grade_weight.place(x=263 + x_location_change, y=60)
            self.term_grade_credit.place(x=257 + x_location_change, y=100)

            self.terms_text.place(x=263 + x_location_change, y=150)
            self.term_grade_label.place(x=262 + x_location_change, y=193)
            self.term_weight_label.place(x=331 + x_location_change, y=193)

            self.Q1.place(x=224 + x_location_change, y=220)
            self.Q1_entry.place(x=256 + x_location_change, y=220)
            self.Q1_weight.place(x=313 + x_location_change, y=220)

            self.Q2.place(x=224 + x_location_change, y=250)
            self.Q2_entry.place(x=256 + x_location_change, y=250)
            self.Q2_weight.place(x=313 + x_location_change, y=250)

            self.E2.place(x=224 + x_location_change, y=280)
            self.E2_entry.place(x=256 + x_location_change, y=280)
            self.E2_weight.place(x=313 + x_location_change, y=280)

            self.Q3.place(x=224 + x_location_change, y=310)
            self.Q3_entry.place(x=256 + x_location_change, y=310)
            self.Q3_weight.place(x=313 + x_location_change, y=310)

            self.Q4.place(x=224 + x_location_change, y=340)
            self.Q4_entry.place(x=256 + x_location_change, y=340)
            self.Q4_weight.place(x=313 + x_location_change, y=340)

            self.E4.place(x=224 + x_location_change, y=370)
            self.E4_entry.place(x=256 + x_location_change, y=370)
            self.E4_weight.place(x=313 + x_location_change, y=370)

            self.Q1_entry.insert(0, current_Q1_grade)
            self.Q2_entry.insert(0, current_Q2_grade)
            self.E2_entry.insert(0, current_E2_grade)
            self.Q3_entry.insert(0, current_Q3_grade)
            self.Q4_entry.insert(0, current_Q4_grade)
            self.E4_entry.insert(0, current_E4_grade)

            self.Q1_weight.insert(0, current_Q1_weight)
            self.Q2_weight.insert(0, current_Q2_weight)
            self.E2_weight.insert(0, current_E2_weight)
            self.Q3_weight.insert(0, current_Q3_weight)
            self.Q4_weight.insert(0, current_Q4_weight)
            self.E4_weight.insert(0, current_E4_weight)

            self.save_button.place(x=263 + x_location_change, y=400)

            for label in [self.term_grade_label, self.term_weight_label,
                          self.Q1, self.Q2, self.E2, self.Q3, self.Q4, self.E4]:
                label.bind("<Enter>", start_hover)
                label.bind("<Leave>", end_hover)

            self.term_info_widgets.append(
                [self.term_grade_class_name, self.term_grade_weight, self.term_grade_credit, self.terms_text,
                 self.term_grade_label, self.term_weight_label, self.Q1, self.Q1_entry,
                 self.Q1_weight, self.Q2, self.Q2_entry, self.Q2_weight, self.E2,
                 self.E2_entry, self.E2_weight, self.Q3, self.Q3_entry,
                 self.Q3_weight, self.Q4, self.Q4_entry, self.Q4_weight,
                 self.E4, self.E4_entry, self.E4_weight, self.save_button])

    def save_button_func(self, Class):
        entries = [self.Q1_entry.get(), self.Q2_entry.get(), self.E2_entry.get(), self.Q3_entry.get(), self.Q4_entry.get(), self.E4_entry.get()]
        weights = [self.Q1_weight.get(), self.Q2_weight.get(), self.E2_weight.get(), self.Q3_weight.get(), self.Q4_weight.get(), self.E4_weight.get()]
        entry_weight = list(zip(entries, weights))
        for term in entry_weight:
            if term[0] != "" and term[1] == "":
                messagebox.showerror("Making Class Error", "Please have a % for each term that has a grade")
                break
            try:
                if term[0] != "" and term[1] != "":
                    float(term[0])
                    float(term[1])
            except ValueError:
                messagebox.showerror("Making Class Error", "Terms and percents must be numbers, with no % sign")
                break
        else:
            for users_class in self.class_data_cumulative:
                if users_class[0][0].get() == Class:
                    users_class[6] = entry_weight[0]
                    users_class[7] = entry_weight[1]
                    users_class[8] = entry_weight[2]
                    users_class[9] = entry_weight[3]
                    users_class[10] = entry_weight[4]
                    users_class[11] = entry_weight[5]
            for users_class in self.for_export:
                if users_class[0][0] == Class:
                    users_class[6] = entry_weight[0]
                    users_class[7] = entry_weight[1]
                    users_class[8] = entry_weight[2]
                    users_class[9] = entry_weight[3]
                    users_class[10] = entry_weight[4]
                    users_class[11] = entry_weight[5]

            grades = []
            weights = []
            for term in entry_weight:
                if term[0] != "":
                    grades.append(float(term[0]) * float(term[1]))
                    weights.append(float(term[1]))
            try:
                for users_class in self.class_data_cumulative:
                    if users_class[0][0].get() == Class:
                        users_class[12] = str(sum(grades) / sum(weights))
                        messagebox.showinfo("Making Class", "Class saved successfully")
                for users_class in self.for_export:
                    if users_class[0][0] == Class:
                        users_class[12] = str(sum(grades) / sum(weights))
            except ZeroDivisionError:
                messagebox.showerror("Making Class Error", "Please enter the grade for at least one term")

    def next_page_classes_func(self):
        pass

    def previous_page_classes_func(self):
        pass

    def get_class_data(self):
        '''This function takes the users inputs and stores them in data2'''
        self.data2.clear() #data2 is cleared every frame to prevent unintended duplicates
        for index, Class in enumerate(previous_data_classes):
            if first_frame_previous_data_classes: #this will only early in the program
                new_class = []
                new_class.append(Class[0][0])
                if Class[12]:
                    new_class.append(Class[12])
                else:
                    new_class.append(Class[1][0])
                if Class[2][0]:
                    new_class.append(Class[2][0])
                else:
                    new_class.append("")
                new_class.append(Class[3][0])
                new_class.append(Class[5])
                self.data2.append(new_class)
        if screen != "quarterly_grades": #prevents data for quarterly grades entering when on cumulative screen
            for index, Class in enumerate(self.class_data_cumulative): #this loop puts data about each class into data2
                new_class = [] #a list is made for each calss in class_data
                new_class.append(Class[0][0].get()) #name of class
                self.for_export[index][0][0] = Class[0][0].get()
                if Class[12]:
                    new_class.append(Class[12])
                    self.for_export[index][1][0] = Class[12]
                else:
                    new_class.append(Class[1][0].get()) #grade user recieved
                    self.for_export[index][1][0] = Class[1][0].get()
                if Class[2][0]["text"] == "R":
                    new_class.append(1)
                    self.for_export[index][2][0] = 1
                elif Class[2][0]["text"] == "H":
                    new_class.append(self.honors_scale)
                    self.for_export[index][2][0] = self.honors_scale
                elif Class[2][0]["text"] == "AP":
                    new_class.append(self.AP_scale)
                    self.for_export[index][2][0] = self.AP_scale
                else:
                    new_class.append("")
                new_class.append(Class[3][0].get()) #credit for class (usually based on how often it met)
                self.for_export[index][3][0] = Class[3][0].get()
                #if isinstance(self.class_data[index][4], int):
                new_class.append(Class[5]) #grade level the class was taken in (8-12)
                self.for_export[index][5] = Class[5]
                self.data2.append(new_class) #appends the temporary new_class list, which contains all the above information, into the data2 list
        if screen != "cumulative_grades":
            for index, Class in enumerate(self.class_data_quarterly): #quarterly GPA
                new_class = []
                new_class.append(Class[0][0].get()) #name of class
                new_class.append(Class[1][0].get()) #grade user recieved
                if Class[2][0]["text"] == "R":
                    new_class.append(1)
                elif Class[2][0]["text"] == "H":
                    new_class.append(self.honors_scale)
                elif Class[2][0]["text"] == "AP":
                    new_class.append(self.AP_scale)
                else:
                    new_class.append("")
                new_class.append(Class[3][0].get()) #credit for class (usually based on how often it met)
                self.data2.append(new_class) #appends the temporary new_class list, which contains all the above information, into the data2 list

    def whats_my_gpa_func(self):
        '''This function calculates the user's GPA when Calculate my GPA is pressed on the GPA page'''
        global gpa_calculated
        if self.class_data_quarterly or self.class_data_cumulative:
            if self.gpa_scale == 100:
                try:
                    #unweighted_total_grade_list makes a list of every grade the user has (stored in self.data2), multipled by the amount of credit for the class.
                    unweighted_total_grade_list_100 = list(map(lambda Class: float(Class[1]) * float(Class[3]), self.data2))
                    #weighted is similar but also includes the weight of the class
                    weighted_total_grade_list_100 = list(map(lambda Class: float(Class[1]) * float(Class[2]) * float(Class[3]), self.data2))
                    #this is a list of the total points available in every class (100) * the credit for the class
                    total_points_available_list_100 = list(map(lambda Class: 100 * float(Class[3]), self.data2))
                    #this replaces the already defines weighted and unweighted GPA widgets. It adds up the elements in the respective lists and divides it by the total points.
                    #the GPA is rounded to 4 decmial places, with zeroes shown.
                    self.unweighted_gpa = "{:.4f}".format(sum(unweighted_total_grade_list_100) / sum(total_points_available_list_100) * 100)
                    self.weighted_gpa = "{:.4f}".format(sum(weighted_total_grade_list_100) / sum(total_points_available_list_100) * 100)
                    gpa_calculated = True
                except ValueError:
                    for Class in self.data2:
                        if Class[1] in self.grades_4:
                            messagebox.showerror("Calc GPA Error", "100.0 Scale does not support letter grades")
                            break
                    else: #if the user did not fill out all the required fields, an error message will appear
                        messagebox.showerror("Calc GPA Error", "Please fill out all fields correctly")
                except ZeroDivisionError:
                    messagebox.showerror("Calc GPA Error", "Weight and Credit can not be zero")
            elif self.gpa_scale == 4: #MAKE SURE TO DOCUMENT THIS
                try:
                    unweighted_total_grade_list_4 = []
                    weighted_total_grade_list_4 = []
                    total_points_available_list_4 = []
                    for Class in self.data2:
                        if Class[1] in self.grades_4:
                            unweighted_total_grade_list_4.append(self.grades_4[Class[1]] * float(Class[3]))
                            weighted_total_grade_list_4.append(self.grades_4[Class[1]] * float(Class[3]) * float(Class[2]))
                            total_points_available_list_4.append(float(4) * float(Class[3]))
                        elif float(Class[1]) or float(Class[1]) == 0.0:
                            for key, value in self.grade_ranges_4.items():
                                if round(float(Class[1])) in value:
                                    unweighted_total_grade_list_4.append(float(self.grades_4[key]) * float(Class[3]))
                                    weighted_total_grade_list_4.append(float(self.grades_4[key]) * float(Class[3]) * float(Class[2]))
                                    total_points_available_list_4.append(float(4) * float(Class[3]))
                    self.unweighted_gpa = "{:.1f}".format(sum(unweighted_total_grade_list_4) / sum(total_points_available_list_4) * 4)
                    self.weighted_gpa = "{:.1f}".format(sum(weighted_total_grade_list_4) / sum(total_points_available_list_4) * 4)
                    gpa_calculated = True
                except ValueError:
                    messagebox.showerror("Calc GPA Error", "Please fill out all fields")

            #this updates the labels for the GPA
            self.unweighted_gpa_label.config(text=f"Unweighted GPA: {self.unweighted_gpa}")
            self.weighted_gpa_label.config(text=f"Weighted GPA: {self.weighted_gpa}")
        else:
            messagebox.showerror("Calc GPA Error", "Please enter at least one class")

    def run_functions(self):
        """This function makes it easy to run other functions in the class"""
        self.get_class_data()

class HelpMenu:
    """The HelpMenu class controls the elements pressed after the user presses Help on the home screen"""
    def __init__(self):
        '''This function creates the buttons and label on the help menu home screen'''
        #widgets for help menu home screen
        self.instructions = Button(window, text="Instructions", command=self.instructions_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                  activeforeground=TEXTCOLOR)
        self.settings = Button(window, text="Settings", command=self.settings_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                  activeforeground=TEXTCOLOR)
        self.help_menu_label = Label(window, text="Help Menu", font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #widgets for instructions page 1
        self.instructions_top = Label(window, text="Instructions",
                                        font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.intro_instructions = Label(window, text="This calculator allows students of Monroe-Woodbury High School \n to calculate their quarterly and cumulative GPA.",
                                        font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.quarterly_GPA_instructions = Label(window, text="For a simple, quarterly GPA, click Calculate My GPA, and then click Quarterly \n Fill in all the instructions, adding classes as you need to, and then hit calculate my GPA \n Because this is meant to be a simple experience, data for quarterly GPA is not stored.",
                                        font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.cumulative_GPA_instructions = Label(window, text="For a more comprehensive GPA, hit Annual/Cumulative. \n Here, you can recieve your cumulative GPA for all the classes you took in High School \n If you in the middle of a year, update the credit for each class \n For example, if 3 quarters have passed, full year courses get .75 credit \n Data is stored and can be loaded in \n More information about loading in data can be found on the Load Data page.",
                                        font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.QA_top = Label(window, text="Questions and Answers",
                                        font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.Q1 = Label(window, text="Question: What is GPA and how is it calculated? "
                                     "\n\nAnswer: GPA is the grade point average for all the classes for a given period. \nIt is calculated based on the grade the student received, \nthe credit (usually proportional to length) of the course, and for weighted GPA, weight",
                                    font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")
        self.Q2 = Label(window, text="Question: What is the difference between weighted and unweighted GPA? \n\nAnswer: Unweighted GPA is without giving extra points for Honors and AP classes\nWeighted GPA accounts for Honors and AP classes\nWeighted GPA is more common and Monroe-Woodbury",
                                        font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")

        #widgets for instructions page 2
        self.next_page = Button(window, text="Next Page", command=self.change_page_func, font=(FONT, 20),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                  activeforeground=TEXTCOLOR)
        self.Q3 = Label(window, text="Question: What is the difference between weighted and unweighted GPA?"
                                    "\n\nAnswer: Regular classes get 1.0 weight, Honors classes get 1.03 (1.125 on 4.0 scale), \nand AP classes get 1.05 (1.25 on 4.0 scale). \nThis is done automatically and get be adjusted in the settings"
                                    "\nFor specific classes - "
                                    "\n            Pre-AP World History gets Honors credit"
                                    "\n            Dual Enrollment (college) classes that are not AP classes get regular credit (fact check this)"
                                    "\n            Any more that come up",
                                    font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")
        self.Q4 = Label(window, text="Question: What is the difference between 100.0 and 4.0 GPA? \n\nAnswer: Monroe-Woodbury uses 100.0 GPA, but many other schools use 4.0 GPA\nBoth are provided so M-W students can easily compare GPAs to students at other schools.",
                         font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")
        self.Q5 = Label(window, text="Question: What 8th-grade classes count for High School GPA? \nAnswer: Only enter in Algebra I, Biology, and World Language for 8th Grade",
                         font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")
        self.Q6 = Label(window, text="Question: Where can I access the grades for classes I took in previous years? \nAnswer: Click Grade History in PowerSchool and click Grade History",
                         font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")
        self.Q7 = Label(window, text="Question: How can I report a bug for this program? \nAnswer: All bugs can be reported to prasadsaha11@gmail.com",
                         font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")
        self.previous_page = Button(window, text="Previous Page", command=self.change_page_func, font=(FONT, 20),
                                bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                activeforeground=TEXTCOLOR)

        #widgets for the settings screen
        self.settings_top = Label(window, text="Settings",
                                        font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_honors_weight_100 = Label(window, text="Honors Weight (100.0):",
                                        font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_AP_weight_100 = Label(window, text="AP Weight (100.0)",
                                              font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_honors_weight_4 = Label(window, text="Honors Weight (4.0):",
                                              font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_AP_weight_4 = Label(window, text="AP Weight (4.0):",
                                              font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_honors_weight_100_entry = Entry(window, width=5, font=(FONT, 15),
                                              bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        self.change_AP_weight_100_entry = Entry(window, width=5, font=(FONT, 15),
                                              bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        self.change_honors_weight_4_entry = Entry(window, width=5, font=(FONT, 15),
                                              bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        self.change_AP_weight_4_entry = Entry(window, width=5, font=(FONT, 15),
                                              bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        self.confirm_settings_button = Button(window, text="Confirm New Settings", command=self.confirm_settings_button_func, font=(FONT, 15),
                                              bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

    def instructions_func(self):
        '''This function changes the screen to the instructions screen'''
        global screen
        screen = "instructions_1"

    def settings_func(self):
        '''This function changes the screen to the settings screen'''
        global screen
        screen = "settings"

    def change_page_func(self):
        global screen
        if screen == "instructions_1":
            screen = "instructions_2"
        elif screen == "instructions_2":
            screen = "instructions_1"

    def confirm_settings_button_func(self):
        '''This function updates the weights of Honors and AP Classes based on the new settings'''
        try:
            gpa_calculator.honors_scale_100 = float(help_menu.change_honors_weight_100_entry.get())
            gpa_calculator.AP_scale_100 = float(help_menu.change_AP_weight_100_entry.get())
            gpa_calculator.honors_scale_4 = float(help_menu.change_honors_weight_4_entry.get())
            gpa_calculator.AP_scale_4 = float(help_menu.change_AP_weight_4_entry.get())

            if gpa_calculator.gpa_scale == 100.0:
                gpa_calculator.honors_scale = gpa_calculator.honors_scale_100
                gpa_calculator.AP_scale = gpa_calculator.AP_scale_100
            elif gpa_calculator.gpa_scale == 4.0:
                gpa_calculator.honors_scale = gpa_calculator.honors_scale_4
                gpa_calculator.AP_scale = gpa_calculator.AP_scale_4

            messagebox.showinfo("Changed Settings", "Settings changed successfully")
        except ValueError:
            messagebox.showerror("Change Settings Error", "Please enter numbers for all fields")

class LoadingData:
    """This class controls the elements for the loading data screen"""
    def __init__(self):
        self.data_info_top = Label(window, text="Data Information",
                              font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.load_data_button = Button(window, text="Load Data", command=self.load_data_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_data_button = Button(window, text="Delete Data", command=self.delete_data_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.save_data_button = Button(window, text="Save Data as PDF", command=self.save_data_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)


    def load_data_func(self):
        global previous_data_all, previous_data_classes, data_loaded
        if os.path.getsize("data_for_calc_gpa.txt") and not data_loaded:
            previous_data_all.append(file_read.read())

            try: #this can be any type of wrong data, such as NameError
                previous_data_all = eval(previous_data_all[0]) #if data is invalid, it won't be imported
                data_loaded = True

                gpa_calculator.gpa_scale = previous_data_all[-1][0]
                gpa_calculator.current_scale.config(text=gpa_calculator.gpa_scale)
                gpa_calculator.honors_scale_100 = previous_data_all[-1][1]
                gpa_calculator.AP_scale_100 = previous_data_all[-1][2]
                gpa_calculator.honors_scale_4 = previous_data_all[-1][3]
                gpa_calculator.AP_scale_4 = previous_data_all[-1][4]

                if gpa_calculator.gpa_scale == 4.0:
                    gpa_calculator.honors_scale = gpa_calculator.honors_scale_4
                    gpa_calculator.AP_scale = gpa_calculator.AP_scale_4

                gpa_calculator.year_8_classes_y_var = previous_data_all[-1][5]
                gpa_calculator.year_9_classes_y_var = previous_data_all[-1][6]
                gpa_calculator.year_10_classes_y_var = previous_data_all[-1][7]
                gpa_calculator.year_11_classes_y_var = previous_data_all[-1][8]
                gpa_calculator.year_12_classes_y_var = previous_data_all[-1][9]

                previous_data_classes = previous_data_all[:-1]

                for index, Class in enumerate(previous_data_classes):
                    small_class_entry = Entry(window, width=10, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                              insertbackground=TEXTCOLOR)
                    grade_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                        insertbackground=TEXTCOLOR)
                    var = StringVar(window)
                    weight_menu = OptionMenu(window, var, "R", "H", "AP")  # REMOVE THE BLACK BAR
                    weight_menu.config(bg=BACKGROUND_COLOR, fg=TEXTCOLOR, highlightthickness=0,
                                       activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR, width=3,
                                       font=(FONT, 10))  # change the location of credit entry maybe
                    credit_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                         insertbackground=TEXTCOLOR)
                    more_info = Button(window, text="More", command=lambda: gpa_calculator.more_info_func(Class=small_class_entry.get()),
                                       font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                       activeforeground=TEXTCOLOR)
                    gpa_calculator.class_data_cumulative.append([(small_class_entry, previous_data_classes[index][0][1], previous_data_classes[index][0][2]),
                                                       (grade_entry, previous_data_classes[index][1][1], previous_data_classes[index][1][2]),
                                                     (weight_menu, previous_data_classes[index][2][1], previous_data_classes[index][2][2]),
                                                       (credit_entry, previous_data_classes[index][3][1], previous_data_classes[index][3][2]),
                                                       (more_info, previous_data_classes[index][4][1], previous_data_classes[index][4][2]),
                                                       previous_data_classes[index][5], [previous_data_classes[index][6][0], previous_data_classes[index][6][1]], [previous_data_classes[index][7][0], previous_data_classes[index][7][1]],
                                                       [previous_data_classes[index][8][0], previous_data_classes[index][8][1]], [previous_data_classes[index][9][0], previous_data_classes[index][9][1]],
                                                       [previous_data_classes[index][10][0], previous_data_classes[index][10][1]], [previous_data_classes[index][11][0], previous_data_classes[index][11][1]], previous_data_classes[index][12]])
                    gpa_calculator.for_export.append([[previous_data_classes[index][0][0], previous_data_classes[index][0][1], previous_data_classes[index][0][2]],
                                                       [previous_data_classes[index][1][0], previous_data_classes[index][1][1], previous_data_classes[index][1][2]],
                                                     [previous_data_classes[index][2][0], previous_data_classes[index][2][1], previous_data_classes[index][2][2]],
                                                       [previous_data_classes[index][3][0], previous_data_classes[index][3][1], previous_data_classes[index][3][2]],
                                                       ["", previous_data_classes[index][4][1], previous_data_classes[index][4][2]],
                                                       previous_data_classes[index][5], [previous_data_classes[index][6][0], previous_data_classes[index][6][1]], [previous_data_classes[index][7][0], previous_data_classes[index][7][1]],
                                                       [previous_data_classes[index][8][0], previous_data_classes[index][8][1]], [previous_data_classes[index][9][0], previous_data_classes[index][9][1]],
                                                       [previous_data_classes[index][10][0], previous_data_classes[index][10][1]], [previous_data_classes[index][11][0], previous_data_classes[index][11][1]], ""])
                messagebox.showinfo("Loading in Data", "Data loaded in successfully")
            except:
                messagebox.showerror("Load Data Error", "Data was invalid and could not be loaded in")
                file_append.truncate(0)
        else:
            if data_loaded:
                messagebox.showerror("Load Data Error", "Data already loaded in")
            else:
                messagebox.showerror("Load Data Error", "No data to load in")

    def delete_data_func(self):
        answer = messagebox.askyesno("Delete Saved Data", "Are you sure you would like to delete saved data?")
        if not answer:
            pass
        if answer:
            file_append.truncate(0)
            messagebox.showinfo("Data Deleted", "Saved data has been deleted. This action did not delete any data within the program. To achieve that, reopen the program and do not load your data.")

    def save_data_func(self):
        pass
        '''
        file = "GPA.pdf"
        if not gpa_calculated:
            messagebox.showerror("Save GPA Error", "Please hit calculate GPA once on the cumulative screen before exporting your data")
        else: #check for errors
            gpa_calculator.whats_my_gpa_func()
            print(gpa_calculator.weighted_gpa)
            c = canvas.Canvas(file, pagesize=letter)
            c.drawString(100, 750, "Hello, World!")
            c.save()
            webbrowser.open(file)
            '''

def update_ui():
    """This function updates the UI everytime the user enters a new screen"""
    global first_frame_settings, first_frame_cumulative_GPA, first_frame_previous_data_classes
    if screen == "home": #this will be seen whenever the user goes home or at the start of the program
        home_screen.universal_back_button.place_forget() #the back button is forgotten here rather than elsewhere as multiple screens use it
        home_screen.intro_text.place(x=35 + x_location_change, y=30)
        home_screen.calc_my_gpa.place(x=135 + x_location_change, y=100)
        home_screen.help.place(x=245 + x_location_change, y=190)
        home_screen.data_information.place(x=147 + x_location_change, y=280)
    else:
        #when the screen is changed, every widget on the home screen will be forgotten
        for widget in [home_screen.intro_text, home_screen.calc_my_gpa, home_screen.help, home_screen.data_information]:
            widget.place_forget()

    if screen == "GPA_home":
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        gpa_calculator.gpa_text.place(x=123 + x_location_change, y=30)
        gpa_calculator.quarterly_button.place(x=209 + x_location_change, y=90)
        gpa_calculator.cumulative_button.place(x=127 + x_location_change, y=180)
    else:
        for widget in [gpa_calculator.gpa_text, gpa_calculator.quarterly_button, gpa_calculator.cumulative_button]:
            widget.place_forget()

    if screen == "quarterly_grades":
        # this configures the GPA
        gpa_calculator.unweighted_gpa_label.config(text=f"Unweighted GPA: {gpa_calculator.unweighted_gpa}")
        gpa_calculator.weighted_gpa_label.config(text=f"Weighted GPA: {gpa_calculator.weighted_gpa}")

        #this is the text at the top and the back button
        gpa_calculator.GPA_home_text.place(x=108 + x_location_change, y=20)
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)

        #these are the widgets for determing the scale
        gpa_calculator.GPA_type_label.place(x=200 + x_location_change, y=95)
        gpa_calculator.current_scale.place(x=260 + x_location_change, y=95)
        gpa_calculator.change_scale.place(x=325 + x_location_change, y=90)

        #this the the text above the class entry area
        gpa_calculator.class_name_label.place(x=137 + x_location_change, y=128)
        gpa_calculator.grade_label.place(x=259 + x_location_change, y=128)
        gpa_calculator.weight_label.place(x=320 + x_location_change, y=128)
        gpa_calculator.credit_label.place(x=387 + x_location_change, y=128)
        #gpa_calculator.year_label.place(x=444 + x_location_change, y=128)

        for Class in gpa_calculator.class_data_quarterly:
            for index, part in enumerate(Class):
                Class[index][0].place(x=Class[index][1] + x_location_change, y=Class[index][2])

        #this is where the GPAs are located before the user calculates their GPA
        gpa_calculator.unweighted_gpa_label.place(x=190 + x_location_change, y=395)
        gpa_calculator.weighted_gpa_label.place(x=200 + x_location_change, y=420)

        #these are the buttons at the bottom
        gpa_calculator.add_new_class.place(x=54 + x_location_change, y=450)
        gpa_calculator.whats_my_gpa.place(x=336 + x_location_change, y=450)
        gpa_calculator.delete_class.place(x=70 + x_location_change, y=504)
    #    if len(gpa_calculator.class_data) > 8:
     #       gpa_calculator.next_page_classes.place(x=250 + x_location_change, y=365)
          #  gpa_calculator.previous_page_classes.place(x=444, y=290)
      #  else:
       #     gpa_calculator.up_class.place_forget()
        #    gpa_calculator.down_class.place_forget()
    else:
        #this forgets most of the widgets
        for widget in [gpa_calculator.GPA_home_text, gpa_calculator.class_name_label, gpa_calculator.grade_label,
                       gpa_calculator.weight_label, gpa_calculator.credit_label, #gpa_calculator.year_label,
                       gpa_calculator.add_new_class, gpa_calculator.whats_my_gpa,
                       gpa_calculator.unweighted_gpa_label, gpa_calculator.weighted_gpa_label, gpa_calculator.delete_class,
                       gpa_calculator.current_scale, gpa_calculator.change_scale, gpa_calculator.GPA_type_label]:
            widget.place_forget()
        #this forgets all of the classes (including the first)
        if screen not in ["cumulative_grades", "class_term_grades_chooser"]:
            for Class in gpa_calculator.class_data_quarterly:
                for widget in Class[0:4]:
                  widget[0].place_forget()
        gpa_calculator.y_var = 150 #this assures that in the future, when the user adds new classes, they appear in the right spot.

    if screen == "cumulative_grades":
        #this configures the GPA
        gpa_calculator.unweighted_gpa_label.config(text=f"Unweighted GPA: {gpa_calculator.unweighted_gpa}")
        gpa_calculator.weighted_gpa_label.config(text=f"Weighted GPA: {gpa_calculator.weighted_gpa}")

        #this places all the widgets that appear on the cumulative grades screen
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        gpa_calculator.Cumulative_GPA_text.place(x=75 + x_location_change, y=20)
        gpa_calculator.GPA_type_label.place(x=200 + x_location_change, y=95)
        gpa_calculator.current_scale.place(x=260 + x_location_change, y=95)
        gpa_calculator.change_scale.place(x=325 + x_location_change, y=90)

        for i, Class in enumerate(gpa_calculator.class_data_cumulative):
            first_frame_cumulative_GPA = True
            for index, part in enumerate(Class[0:5]):
                Class[index][0].place(x=Class[index][1] + x_location_change, y=Class[index][2])
                if index == 1 and Class[12] and first_frame_cumulative_GPA: #the grade entry
                    part[0].delete(0, END)
                    part[0].insert(0, str(round(float(Class[12]))))
                    first_frame_cumulative_GPA = False
                if previous_data_classes and first_frame_previous_data_classes:
                    if index == 0:
                        part[0].insert(0, previous_data_classes[i][0][0])
                    if index == 1 and not Class[12]:
                        part[0].insert(0, str(round(float(previous_data_classes[i][1][0]))))
                    if index == 2:
                        if previous_data_classes[i][2][0] == 1:
                            part[0].children['menu'].invoke(0)
                        elif previous_data_classes[i][2][0] in [gpa_calculator.honors_scale_100, gpa_calculator.honors_scale_4]:
                            part[0].children['menu'].invoke(1)
                        elif previous_data_classes[i][2][0] in [gpa_calculator.AP_scale_100, gpa_calculator.AP_scale_4]:
                            part[0].children['menu'].invoke(2)
                    if index == 3:
                        part[0].insert(0, previous_data_classes[i][3][0])
        first_frame_previous_data_classes = False

        #widgets for 8th grade
        gpa_calculator.year_8_label.place(x=117 + x_location_change, y=125)
        gpa_calculator.class_name_label_8.place(x=34 + x_location_change, y=150)
        gpa_calculator.grade_label_8.place(x=131 + x_location_change, y=150)
        gpa_calculator.weight_label_8.place(x=182 + x_location_change, y=150)
        gpa_calculator.credit_label_8.place(x=239 + x_location_change, y=150)

        gpa_calculator.add_class_8.place(x=78 + x_location_change, y=260)
        gpa_calculator.delete_class_8.place(x=150 + x_location_change, y=260)

        #widgets for 9th grade
        gpa_calculator.year_9_label.place(x=432 + x_location_change, y=125)
        gpa_calculator.class_name_label_9.place(x=358 + x_location_change, y=150)
        gpa_calculator.grade_label_9.place(x=446 + x_location_change, y=150)
        gpa_calculator.weight_label_9.place(x=497 + x_location_change, y=150)
        gpa_calculator.credit_label_9.place(x=554 + x_location_change, y=150)
        gpa_calculator.add_class_9.place(x=393 + x_location_change, y=260)
        gpa_calculator.delete_class_9.place(x=465 + x_location_change, y=260)

        #widgets for 10th grade
        gpa_calculator.year_10_label.place(x=117 + x_location_change, y=305)
        gpa_calculator.class_name_label_10.place(x=34 + x_location_change, y=330)
        gpa_calculator.grade_label_10.place(x=131 + x_location_change, y=330)
        gpa_calculator.weight_label_10.place(x=182 + x_location_change, y=330)
        gpa_calculator.credit_label_10.place(x=239 + x_location_change, y=330)

        gpa_calculator.add_class_10.place(x=78 + x_location_change, y=440)
        gpa_calculator.delete_class_10.place(x=150 + x_location_change, y=440)

        #widgets for 11th grade
        gpa_calculator.year_11_label.place(x=432 + x_location_change, y=305)
        gpa_calculator.class_name_label_11.place(x=358 + x_location_change, y=330)
        gpa_calculator.grade_label_11.place(x=446 + x_location_change, y=330)
        gpa_calculator.weight_label_11.place(x=497 + x_location_change, y=330)
        gpa_calculator.credit_label_11.place(x=554 + x_location_change, y=330)

        gpa_calculator.add_class_11.place(x=393 + x_location_change, y=440)
        gpa_calculator.delete_class_11.place(x=465 + x_location_change, y=440)

        #widgets for 12th grade
        gpa_calculator.year_12_label.place(x=117 + x_location_change, y=485)
        gpa_calculator.class_name_label_12.place(x=34 + x_location_change, y=510)
        gpa_calculator.grade_label_12.place(x=131 + x_location_change, y=510)
        gpa_calculator.weight_label_12.place(x=182 + x_location_change, y=510)
        gpa_calculator.credit_label_12.place(x=239 + x_location_change, y=510)

        gpa_calculator.add_class_12.place(x=78 + x_location_change, y=620)
        gpa_calculator.delete_class_12.place(x=150 + x_location_change, y=620)

        #widgets for calcuating the cumulative GPA
        gpa_calculator.whats_my_gpa.place(x=337 + x_location_change, y=500)
        gpa_calculator.unweighted_gpa_label.place(x=337 + x_location_change, y=560)
        gpa_calculator.weighted_gpa_label.place(x=337 + x_location_change, y=590)
    else:
        for widget in [gpa_calculator.Cumulative_GPA_text, gpa_calculator.year_8_label, gpa_calculator.delete_class_8, gpa_calculator.add_class_8,
                       gpa_calculator.class_name_label_8, gpa_calculator.grade_label_8, gpa_calculator.weight_label_8, gpa_calculator.credit_label_8,
                       gpa_calculator.year_9_label, gpa_calculator.delete_class_9, gpa_calculator.add_class_9, gpa_calculator.class_name_label_9,
                       gpa_calculator.grade_label_9, gpa_calculator.weight_label_9, gpa_calculator.credit_label_9,
                       gpa_calculator.year_10_label, gpa_calculator.delete_class_10, gpa_calculator.add_class_10, gpa_calculator.class_name_label_10,
                       gpa_calculator.grade_label_10, gpa_calculator.weight_label_10, gpa_calculator.credit_label_10,
                       gpa_calculator.year_11_label, gpa_calculator.delete_class_11, gpa_calculator.add_class_11, gpa_calculator.class_name_label_11,
                       gpa_calculator.grade_label_11, gpa_calculator.weight_label_11, gpa_calculator.credit_label_11,
                       gpa_calculator.year_12_label, gpa_calculator.delete_class_12, gpa_calculator.add_class_12, gpa_calculator.class_name_label_12,
                       gpa_calculator.grade_label_12, gpa_calculator.weight_label_12, gpa_calculator.credit_label_12]:
            widget.place_forget()
     #   if screen != "class_term_grades_chooser":
      #      gpa_calculator.year_8_classes_y_var = 149
       #     gpa_calculator.year_9_classes_y_var = 149
        #    gpa_calculator.year_10_classes_y_var = 329
         #   gpa_calculator.year_11_classes_y_var = 329
          #  gpa_calculator.year_12_classes_y_var = 509

        #this forgets all of the classes (including the first)
        for Class in gpa_calculator.class_data_cumulative:
            for widget in Class[0:5]:
                    widget[0].place_forget()

    if screen != "class_term_grades_chooser":
        if gpa_calculator.term_info_widgets:
            for widget in gpa_calculator.term_info_widgets[0]:
                widget.place_forget()
            gpa_calculator.term_info_widgets.clear()

    if screen == "help_menu":
        #this places all the widgets that appear on the home screen for the help menu
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        help_menu.help_menu_label.place(x=208 + x_location_change, y=30)
        help_menu.instructions.place(x=190 + x_location_change, y=100)
        help_menu.settings.place(x=220 + x_location_change, y=190)
    else:
        #this deletes all the widgets, except for the back button
        for widget in [help_menu.help_menu_label, help_menu.instructions, help_menu.settings]:
            widget.place_forget()

    if screen == "instructions_1":
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        help_menu.instructions_top.place(x=204 + x_location_change, y=10)
        help_menu.intro_instructions.place(x=95 + x_location_change, y=60)
        help_menu.quarterly_GPA_instructions.place(x=34 + x_location_change, y=100)
        help_menu.cumulative_GPA_instructions.place(x=33 + x_location_change, y=170)

        help_menu.QA_top.place(x=109 + x_location_change, y=300)
        help_menu.Q1.place(x=0 + x_location_change, y=360)
        help_menu.Q2.place(x=0 + x_location_change, y=490)
        help_menu.next_page.place(x=233 + x_location_change, y=595)
    else:
        if screen != "instructions_1":
            help_menu.instructions_top.place_forget()
        for widget in [help_menu.intro_instructions, help_menu.quarterly_GPA_instructions, help_menu.cumulative_GPA_instructions, #this is all for the instructions
                       help_menu.QA_top, help_menu.Q1, help_menu.Q2, help_menu.next_page]: #this is all for the Q&A
            widget.place_forget()

    if screen == "instructions_2":
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        help_menu.instructions_top.place(x=204 + x_location_change, y=10)
        help_menu.Q3.place(x=0 + x_location_change, y=60)
        help_menu.Q4.place(x=0 + x_location_change, y=260)
        help_menu.Q5.place(x=0 + x_location_change, y=370)
        help_menu.Q6.place(x=0 + x_location_change, y=430)
        help_menu.Q7.place(x=0 + x_location_change, y=490)
        help_menu.previous_page.place(x=213 + x_location_change, y=595)
    else:
        if screen != "instructions_1":
            help_menu.instructions_top.place_forget()
        for widget in [help_menu.Q3, help_menu.Q4, help_menu.Q5,
                       help_menu.Q6, help_menu.Q7, help_menu.previous_page]:
            widget.place_forget()

    if screen == "settings":
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        help_menu.settings_top.place(x=233 + x_location_change, y=30)
        help_menu.change_honors_weight_100.place(x=198 + x_location_change, y=85)
        help_menu.change_AP_weight_100.place(x=211 + x_location_change, y=115)
        help_menu.change_honors_weight_4.place(x=205 + x_location_change, y=145)
        help_menu.change_AP_weight_4.place(x=218 + x_location_change, y=175)

        if first_frame_settings:
        #if help_menu.change_honors_weight_100_entry.get() == "":
            help_menu.change_honors_weight_100_entry.insert(0, str(gpa_calculator.honors_scale_100))
        #if help_menu.change_AP_weight_100_entry.get() == "":
            help_menu.change_AP_weight_100_entry.insert(0, str(gpa_calculator.AP_scale_100))
        #if help_menu.change_honors_weight_4_entry.get() == "":
            help_menu.change_honors_weight_4_entry.insert(0, str(gpa_calculator.honors_scale_4))
        #if help_menu.change_AP_weight_4_entry.get() == "":
            help_menu.change_AP_weight_4_entry.insert(0, str(gpa_calculator.AP_scale_4))
            first_frame_settings = False

        help_menu.change_honors_weight_100_entry.place(x=352 + x_location_change, y=85)
        help_menu.change_AP_weight_100_entry.place(x=337 + x_location_change, y=115)
        help_menu.change_honors_weight_4_entry.place(x=343 + x_location_change, y=145)
        help_menu.change_AP_weight_4_entry.place(x=331 + x_location_change, y=175)
        help_menu.confirm_settings_button.place(x=204 + x_location_change, y=235)
    else:
        for widget in [help_menu.settings_top, help_menu.change_honors_weight_100, help_menu.change_honors_weight_4, help_menu.change_AP_weight_100, help_menu.change_AP_weight_4,
                       help_menu.change_honors_weight_100_entry, help_menu.change_honors_weight_4_entry, help_menu.change_AP_weight_100_entry, help_menu.change_AP_weight_4_entry, help_menu.confirm_settings_button]:
            widget.place_forget()

    if screen == "data_menu":
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        data_menu.data_info_top.place(x=160 + x_location_change, y=10)
        data_menu.load_data_button.place(x=200 + x_location_change, y=70)
        data_menu.delete_data_button.place(x=190 + x_location_change, y=160)
        data_menu.save_data_button.place(x=139 + x_location_change, y=250)
    else:
        for widget in [data_menu.data_info_top, data_menu.load_data_button, data_menu.delete_data_button, data_menu.save_data_button]:
            widget.place_forget()

def improve_entry_boxes(event):
    entry_boxes = [widget for widget in window.winfo_children() if isinstance(widget, Entry)]
    for entry in entry_boxes:
        if event.widget != entry:
            text = entry.get()
            entry.delete(0, END)
            entry.insert(0, text)

def update_frame():
    '''This updates the program once per 17 ms (about 60 fps), updating the ui and running functions for the classes'''
    global x_location_change, time
    entry_boxes = [widget for widget in window.winfo_children() if isinstance(widget, Entry)]
    option_menus = [widget for widget in window.winfo_children() if isinstance(widget, OptionMenu)]
    time += 1
    gpa_calculator.run_functions()
    update_ui()
    i = 0
    entries_term_grade_error = []
    error_labels_for_term_grades = []
    for entry in entry_boxes:
        if entry.winfo_ismapped():
            isfloat = lambda s: s.replace('.', '', 1).isdigit()
            if entry.winfo_x() == 256 + x_location_change: #grade in more info:
                if isfloat(entry.get()):
                    entries_term_grade_error.append(entry.get())
                if not entries_term_grade_error:
                    error_labels_for_term_grades.append(error_labels[i])
                    error_labels[i].place(x=entry.winfo_x() + entry.winfo_width() - error_labels[i].winfo_width() - 5, y=entry.winfo_y() + 5)
                    error_labels[i].lift()
                else:
                    error_labels[i].place_forget()
                    for label in error_labels_for_term_grades:
                        label.place_forget()
            elif entry.get() == "" or (not isfloat(entry.get()) and entry.winfo_x() not in [100 + x_location_change, 22 + x_location_change, 337 + x_location_change]): #second part checks if it's float, but only if it's not a class name entry
                error_labels[i].place(x=entry.winfo_x() + entry.winfo_width() - error_labels[i].winfo_width() - 5, y=entry.winfo_y() + 5)
                error_labels[i].lift()
            else:
                error_labels[i].place_forget()
        else:
            error_labels[i].place_forget()
        i += 1
    for option in option_menus:
        if option.winfo_ismapped():
            if option["text"] == "":
                error_labels[i].place(x=option.winfo_x(), y=option.winfo_y() + 5)
                error_labels[i].lift()
            else:
                error_labels[i].place_forget()
        else:
            error_labels[i].place_forget()
        i += 1
   # if time % 15 == 0: #once per 5 seconds, but the rate of data backup make be different depending on the computer
   #     file_append.truncate(0)
   #     file_append.write(f"{gpa_calculator.for_export}\n")
    x_location_change = (window.winfo_width() / 2) - 300 #this varaible accounts for change in the screen width and is used to centralize everything. It is located here rather than at the start as it must be updated.
    window.after(17, update_frame) #the function is recursive and will run from the start of the program to the end of it

#this creates instances of each classe
gpa_calculator = GPACalculator()
home_screen = HomeScreen()
help_menu = HelpMenu()
data_menu = LoadingData()

update_frame() #runs the function to update the program

labels_for_help_text_when_hover = [gpa_calculator.class_name_label, gpa_calculator.grade_label, gpa_calculator.weight_label, gpa_calculator.credit_label, #labels for entry boxes, quarter GPA screen
                                   gpa_calculator.GPA_type_label, gpa_calculator.current_scale, gpa_calculator.unweighted_gpa_label, gpa_calculator.weighted_gpa_label, #labels for UW vs W gpa and 100.0 vs 4.0 gpa
                                   gpa_calculator.year_8_label,  #states to only enter high school level classes for 8th Grade
                                   gpa_calculator.class_name_label_8, gpa_calculator.grade_label_8, gpa_calculator.weight_label_8, gpa_calculator.credit_label_8, #labels for entry boxes above 8th grade, cumulative GPA screen
                                   gpa_calculator.class_name_label_9, gpa_calculator.grade_label_9, gpa_calculator.weight_label_9, gpa_calculator.credit_label_9, #labels for entry boxes above 9th grade, cumulative GPA screen
                                   gpa_calculator.class_name_label_10, gpa_calculator.grade_label_10, gpa_calculator.weight_label_10, gpa_calculator.credit_label_10, #labels for entry boxes above 10th grade, cumulative GPA screen
                                   gpa_calculator.class_name_label_11, gpa_calculator.grade_label_11, gpa_calculator.weight_label_11, gpa_calculator.credit_label_11, #labels for entry boxes above 11th grade, cumulative GPA screen
                                   gpa_calculator.class_name_label_12, gpa_calculator.grade_label_12, gpa_calculator.weight_label_12, gpa_calculator.credit_label_12, #labels for entry boxes above 12th grade, cumulative GPA screen
                                   ]
widget_help_label = Label(window, bg=TEXTCOLOR, fg=BACKGROUND_COLOR)

def start_hover(event):
    """This function makes it so that when a widget is hovered over, a help text appears"""
    lines = 0
    x_change = 0
    if event.widget.winfo_ismapped():
        if event.widget in [gpa_calculator.class_name_label, gpa_calculator.class_name_label_8, gpa_calculator.class_name_label_9,
                            gpa_calculator.class_name_label_10, gpa_calculator.class_name_label_11, gpa_calculator.class_name_label_12]:
            widget_help_label.config(text="Enter the name of your class")
            lines = 1
            x_change = 155
        elif event.widget in [gpa_calculator.grade_label, gpa_calculator.grade_label_8, gpa_calculator.grade_label_9,
                              gpa_calculator.grade_label_10, gpa_calculator.grade_label_11, gpa_calculator.grade_label_12]:
            widget_help_label.config(text="Enter the grade you received in that class")
            lines = 1
            x_change = 221
        elif event.widget in [gpa_calculator.weight_label, gpa_calculator.weight_label_8, gpa_calculator.weight_label_9,
                              gpa_calculator.weight_label_10, gpa_calculator.weight_label_11, gpa_calculator.weight_label_12]:
            if gpa_calculator.gpa_scale == 100.0:
                widget_help_label.config(text=f"Select the weight of the class \n Honors get {gpa_calculator.honors_scale_100} weight and AP gets {gpa_calculator.AP_scale_100} weight \n this can be adjusted in the settings")
                lines = 3
                x_change = 263
            elif gpa_calculator.gpa_scale == 4.0:
                widget_help_label.config(text=f"Select the weight of the class \n Honors get {gpa_calculator.honors_scale_4} weight and AP gets {gpa_calculator.AP_scale_4} weight \n this can be adjusted in the settings")
                lines = 3
                x_change = 269
        elif event.widget == gpa_calculator.credit_label:
            widget_help_label.config(text="Enter the credit for the course \n Every day (A-F) courses usually get 1 credit \n Alternative Day courses usually get .5 credit") #BE SURE TO ALLOW FOR ½ and ¼
            lines = 3
            x_change = 237
        elif event.widget in [gpa_calculator.credit_label_8, gpa_calculator.credit_label_9,
                              gpa_calculator.credit_label_10, gpa_calculator.credit_label_11, gpa_calculator.credit_label_12]:
            widget_help_label.config(text="Enter the credit for the course \n Every day (A-F) Full Year courses usually get 1 credit \n Alternative Day or Semester courses usually get .5 credit \n A semester of PE gets .25 credit")
            lines = 4
            x_change = 305
        elif event.widget == gpa_calculator.GPA_type_label:
            widget_help_label.config(text="The GPA Scale could be 100.0 (what Monroe Woodbury uses) \n or 4.0 (what some other schools use)")
            lines = 2
        elif event.widget == gpa_calculator.current_scale:
            if gpa_calculator.gpa_scale == 100.0:
                widget_help_label.config(text="Honors get 1.03 weight and AP gets 1.05 weight \n this can be adjusted in the settings")
                lines = 2
            elif gpa_calculator.gpa_scale == 4.0:
                widget_help_label.config(text="Honors get 1.125 weight and AP gets 1.25 weight \n This can be adjusted in the settings")
                lines = 2
        elif event.widget == gpa_calculator.unweighted_gpa_label:
            widget_help_label.config(text="This is your GPA without giving extra points for Honors/AP Classes")
            lines = 1
            x_change = 357
        elif event.widget == gpa_calculator.weighted_gpa_label:
            widget_help_label.config(text="This is your GPA with extra points for Honors/AP Classes")
            lines = 1
            x_change = 303
        elif event.widget == gpa_calculator.year_8_label:
            widget_help_label.config(text="Only enter high school level classes (Algebra, Biology, World Langauge)")
            lines = 1
        elif event.widget == gpa_calculator.term_grade_label:
            widget_help_label.config(text="Enter the grade you received in the term")
            lines = 1
            x_change = 217
        elif event.widget == gpa_calculator.term_weight_label:
            widget_help_label.config(text="Enter the weight that the term had for your F4 grade \nIf this term did not impact your F4 grade, put 0 \nThe defaults can be changed in the settings")
            lines = 3
            x_change = 283
        elif event.widget == gpa_calculator.Q1:
            widget_help_label.config(text=f"Q1 Grade")
            lines = 1
        elif event.widget == gpa_calculator.Q2:
            widget_help_label.config(text=f"Q2 Grade")
            lines = 1
        elif event.widget == gpa_calculator.E2:
            widget_help_label.config(text=f"Midterm")
            lines = 1
        elif event.widget == gpa_calculator.Q3:
            widget_help_label.config(text=f"Q3 Grade")
            lines = 1
        elif event.widget == gpa_calculator.Q4:
            widget_help_label.config(text=f"Q4 Grade")
            lines = 1
        elif event.widget == gpa_calculator.E4:
            widget_help_label.config(text=f"Final Exam")
            lines = 1

        help_label_x = event.widget.winfo_x()
        help_label_y = event.widget.winfo_y()

        if lines == 1:
            help_label_y = event.widget.winfo_y() - 20
        elif lines == 2:
            help_label_y = event.widget.winfo_y() - 35
        elif lines == 3:
            help_label_y = event.widget.winfo_y() - 50
        elif lines == 4:
            help_label_y = event.widget.winfo_y() - 65

        if event.widget.winfo_x() > 300:
            help_label_x -= x_change - event.widget.winfo_width()

        widget_help_label.place(x=help_label_x, y=help_label_y)
        widget_help_label.lift()

def end_hover(event):
    """This function makes it so that when a widget stops being hovered over, the help text goes away"""
    widget_help_label.place_forget()
    widget_help_label.config(text="")

for label in labels_for_help_text_when_hover:
    label.bind("<Enter>", start_hover)
    label.bind("<Leave>", end_hover)

window.bind("<Button-1>", improve_entry_boxes)

window.mainloop() #this line is needed to run the GUI

file_append.truncate(0)
if len(gpa_calculator.for_export) >= 1:
    gpa_calculator.for_export.append([gpa_calculator.gpa_scale, gpa_calculator.honors_scale_100, gpa_calculator.AP_scale_100, gpa_calculator.honors_scale_4, gpa_calculator.AP_scale_4,
                                      gpa_calculator.year_8_classes_y_var, gpa_calculator.year_9_classes_y_var, gpa_calculator.year_10_classes_y_var, gpa_calculator.year_11_classes_y_var, gpa_calculator.year_12_classes_y_var,])
    file_append.write(f"{gpa_calculator.for_export}\n")
file_append.close()
file_read.close()
