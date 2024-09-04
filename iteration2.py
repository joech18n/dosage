#Joe Chan - Dosage Application (Supplement Tracker App) - Version 2

#importing libraries and modules
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
from PIL import Image, ImageTk
from tkcalendar import Calendar
from tkcalendar import DateEntry
import datetime
import json


#set user variable as empty string to be altered in check_credentials() function
USER = ""

#----------------------------------Main menu window initialization--------------------------------------

root = tk.Tk() # create the main window
root.title("Dosage") # set the window title
root.geometry("300x200") # set the window size
root.configure(bg='#E96E7E') # set the background color
root.resizable(width=False, height=False) # make the window size fixed

#Function to read text file and return a list of lines
def read_file(filename):
    try:
        # open the file and read non-empty lines
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip()] # strip whitespace and ignore empty lines
        if not lines:
            print(f"Warning: The file {filename} is empty or contains only empty lines.") # warn if no lines are found
        return lines
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.") # error if file does not exist
        return [] # return an empty list on error

    
#Load external data about vitamins and minerals from text files
VITAMINS = read_file('vitamins.txt')
MINERALS = read_file('minerals.txt')

#Function for creating sign in window
def sign_in():
    sign_in_window = tk.Toplevel(root)
    sign_in_window.title("Sign In")
    sign_in_window.geometry("250x150")

    tk.Label(sign_in_window, text="Username:").grid(row=0, column=0, pady=10, padx=10)
    username_entry = tk.Entry(sign_in_window)
    username_entry.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(sign_in_window, text="Password:").grid(row=1, column=0, pady=10, padx=10)
    password_entry = tk.Entry(sign_in_window, show="*")
    password_entry.grid(row=1, column=1, pady=10, padx=10)

    #nested function within signin function for checking user input with credentials in external csv file
    def check_credentials():
        global USER #accesses the USER variable defined at the beginning
        username = username_entry.get()
        password = password_entry.get()

        # open the csv file and read the stored credentials
        with open("users.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # check if the entered username and password match a row in the file
                if row == [username, password]:
                    messagebox.showinfo("Success", "Login successful!") # show success message
                    USER = username_entry.get() # set the global USER variable to the logged-in username
                    sign_in_window.destroy() # close the sign-in window
                    root.withdraw() # hide the root window
                    app = Application() # create the main application instance
                    app.mainloop() # start the application loop
                    return # exit the function after a successful login
            messagebox.showerror("Error", "Invalid username or password") # error if no match found 

    # sign in button that triggers the check_credentials function
    tk.Button(sign_in_window, text="Sign In", command=check_credentials).grid(row=2, column=0, columnspan=2, pady=20)


#function for popping up the registration window
def register():
    register_window = tk.Toplevel(root) # creates a new window on top of the main one
    register_window.title("Register") # sets the window title
    register_window.geometry("250x150") # sets the window size

    #label and entry for username input
    tk.Label(register_window, text="Username:").grid(row=0, column=0, pady=10, padx=10) # labels the first row for username
    username_entry = tk.Entry(register_window) # entry field for username
    username_entry.grid(row=0, column=1, pady=10, padx=10) # places the entry field next to the label

    #label and entry for password input
    tk.Label(register_window, text="Password:").grid(row=1, column=0, pady=10, padx=10) # labels the second row for password
    password_entry = tk.Entry(register_window, show="*") # entry field for password, hides input with asterisk
    password_entry.grid(row=1, column=1, pady=10, padx=10) # places the entry field next to the label

    #function defined inside register function for saving credentials to an external csv file
    def save_credentials(): 
        username = username_entry.get() # grabs the username from the entry field
        password = password_entry.get() # grabs the password from the entry field
        if not username or not password: # checks if either field is empty
            messagebox.showerror("Error", "Please enter both username and password") # error message if fields are empty
            return # exits the function early if there's an error
        with open("users.csv", mode='a', newline='') as file: # opens the csv file in append mode
            writer = csv.writer(file) # creates a csv writer object
            writer.writerow([username, password]) # writes the username and password to the file
        messagebox.showinfo("Success", "Registration successful!") # success message after saving
        register_window.destroy() # closes the registration window after successful registration

    #button to trigger the save_credentials function
    tk.Button(register_window, text="Register", command=save_credentials).grid(row=2, column=0, columnspan=2, pady=20) # creates a button to register, spanning two columns



#-----------------------------------------MAIN MENU-------------------------------------------------------------------------

#Load and display the image using Pillow
logo_image = Image.open("logo.png") # opens the image file named 'logo.png'
logo_image = logo_image.resize((450, 75), Image.LANCZOS) # resizes the image to 450x75 using high-quality LANCZOS filter
logo_photo = ImageTk.PhotoImage(logo_image) # converts the image to a PhotoImage object for Tkinter

#creates a label to display the logo image
logo_label = tk.Label(root, image=logo_photo) # assigns the PhotoImage object to a label
logo_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10) # places the label on the grid, spanning 3 columns, with padding

#welcome text label
welcome_label = tk.Label(root, text="Welcome.", fg="white", bg='#E96E7E', font=("Arial Bold", 17)) # label with welcome text, white text on pink background, bold Arial font size 17
welcome_label.grid(row=1, column=0, rowspan=3) # places the label on the grid, spanning 3 rows vertically

#buttons for sign in and register
tk.Button(root, text="Sign In", command=sign_in, width=15).grid(row=1, column=1, padx=10, pady=10) # sign in button, placed next to welcome label with padding
tk.Button(root, text="Register", command=register, width=15).grid(row=2, column=1, padx=10, pady=10) # register button, placed below the sign-in button, also with padding

#adjusts column weights so that they expand evenly
root.grid_columnconfigure(0, weight=1) # makes the first column expand to take up available space
root.grid_columnconfigure(1, weight=1) # makes the second column do the same


#------------------------------------------APPLICATION -------------------------------------------------
class Application(tk.Toplevel): #new class made for main application
    def __init__(self): 
        super().__init__() #inheriting toplevel parent class
        self.title("Dosage") #title
        self.geometry("500x530") #setting dimensions of window
    
        self.container = tk.Frame(self) #creating  new container for information
        self.container.grid(row=0, column=0, sticky="NSEW") #placing container

        #configuring the the row and column of the the container
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {} #create dictionary for frames
        for F in (mysupplementsPage, addPage): #iterates through the pages
            page_name = F.__name__ #get the name of thee class of the window
            frame = F(parent=self.container, controller=self) #create instance of the page
            self.frames[page_name] = frame #finds frame in dictionary
            frame.grid(row=0, column=0, sticky="NSEW") #places frame to cover entire container

        self.show_frame("mysupplementsPage") #makes the mysupplements page visible

    #function for showing the frame (used for changing windows)
    def show_frame(self, page_name): 
        frame = self.frames[page_name]
        frame.tkraise()

#-----------------------------Making base page template with banner--------------------------------------

class BasePage(tk.Frame):  #define a class basepag that inherits from tk.Frame
    def __init__(self, parent, controller):  #constructor method for initializing the page
        super().__init__(parent)  #initialize the frame with the given parent 
        self.controller = controller  #storing controller for managing frames

        #create a banner frame at the top of the page for holding the logo
        banner_frame = tk.Frame(self, bg='#E96E7E')  #set background color to pink
        banner_frame.grid(row=0, column=0, columnspan=3, sticky="EW")  #position banner at the top

        #load and resize the logo image
        logo_image = Image.open("logo.png")  #open the logo image file
        logo_image = logo_image.resize((480, 80), Image.LANCZOS)  #resize image using high-quality resizing

        self.logo_photo = ImageTk.PhotoImage(logo_image)  #convert image to a format that tkinter can use
        
        #create a label widget to display the logo
        logo_label = tk.Label(banner_frame, image=self.logo_photo)  #assign logo image to label
        logo_label.grid(row=0, column=0, padx=8, pady=10)  #position label

        #create a navigation frame below the banner for holding navigation buttons
        nav_frame = tk.Frame(self, background="#4C535D")  #set background color to dark grey
        nav_frame.grid(row=1, columnspan=3, sticky="EW")  #position navigation frame below banner

        #create the "My Supplements" button within the navigation frame
        mysupplements_button = tk.Button(nav_frame, text="My Supplements", command=lambda: controller.show_frame("mysupplementsPage"))  #set button text and command to switch to mysupplementsPage
        mysupplements_button.grid(row=0, column=0, padx=5, pady=5, sticky="EW")  #position button 

        #create the "Add Supplements" button within the navigation frame
        addsupplements_button = tk.Button(nav_frame, text="Add Supplements", command=lambda: controller.show_frame("addPage"))  #set button text and command to switch toaddPage
        addsupplements_button.grid(row=0, column=2, padx=5, pady=5, sticky="EW")  #position button


class mysupplementsPage(BasePage):
    def __init__(self, parent, controller): #constructor method for initializing the page
        super().__init__(parent, controller)
        supplementsframe = tk.Frame(self, bg="#4C535D") #defining a new frame
        supplementsframe.grid(columnspan=10, rowspan=10, sticky="NSEW") #placing frame

        #configuring columns of frame
        supplementsframe.columnconfigure(0, weight=1)
        supplementsframe.columnconfigure(1, weight=1)
        supplementsframe.columnconfigure(2, weight=1)

        #create and configure calendar widget
        self.home_calendar = Calendar(supplementsframe, selectmode="day", date_pattern="yyyy-mm-dd", background="#E96E7E", headersbackground="#E96E7E")
        self.home_calendar.grid(row=3, columnspan=3, pady=(20, 10))

        #create and configure label to display selected date
        self.selected_date = tk.Label(supplementsframe, text="")
        self.selected_date.grid(row=4, column=1)

        #variable to store the selected date
        self.selected_date_value = ""

        #bind calendar selection event to update_selected_date method
        self.home_calendar.bind("<<CalendarSelected>>", self.update_selected_date)

        #create and configure button to add supplements
        self.add_supplements_button = ttk.Button(supplementsframe, text="Add Supplements", command=lambda: controller.show_frame("addPage"))
        self.add_supplements_button.grid(row=4, column=1, pady=10)

        #create new frame for list of supplements
        self.listofsupplements_frame = tk.Frame(supplementsframe)
        self.listofsupplements_frame.grid(row=5, column=0, columnspan=3, sticky="NSEW")

        #initialize label for formatted date in the new frame
        self.day_label = ttk.Label(self.listofsupplements_frame, text="", font=('Verdana', 15, 'bold'))
        self.day_label.grid(row=0, column=0, padx=10, pady=5, sticky="W")

    def update_selected_date(self, event=None):
        #get the selected date from the calendar
        date_str = self.home_calendar.get_date()
        self.selected_date.config(text=date_str)
        self.selected_date_value = date_str

        try:
            #convert the date string to a datetime object
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")

            #format the date as "Day, nth of the Month"
            formatted_date = date_obj.strftime("%A, %d of %B")
            
            #update the label with the formatted date
            self.day_label.config(text=formatted_date)
        except ValueError as e:
            #handle error if date_str is not in the expected format
            print(f"Error: {e}")


#----------------------------------------------Adding new supplements page-------------------------------------------------
class addPage(BasePage):
    def __init__(self, parent, controller): #constructor method for initializing the page
        #initialize parent class
        super().__init__(parent, controller)

        #configure grid column weights
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        #label for the page
        label = ttk.Label(self, text="Add Supplements", font=('Verdana', 18, 'bold')) #create label
        label.grid(row=2, column=0, columnspan=3, padx=10, pady=10) #place label

        #button to select vitamins
        tk.Button(self, text="Select Vitamin", command=self.show_vitamins).grid(row=3, column=0, padx=10, pady=5, sticky="EW")
        #button to select minerals
        tk.Button(self, text="Select Mineral", command=self.show_minerals).grid(row=3, column=1, padx=10, pady=5, sticky="EW")

        #labels and comboboxes for vitamins and minerals
        self.vitamin_label = tk.Label(self, text="Vitamins") #create label
        self.mineral_label = tk.Label(self, text="Minerals") #create label
        self.vitamin_combobox = ttk.Combobox(self, values=VITAMINS) #crate combobox
        self.mineral_combobox = ttk.Combobox(self, values=MINERALS) #create combobox

        #label and entry for custom supplement name
        tk.Label(self, text="Supplement Name:").grid(row=5, column=0, padx=10, pady=5, sticky="E") #create and place label
        self.label_entry = tk.Entry(self) #create entry
        self.label_entry.grid(row=5, column=1, padx=10, pady=5, sticky="W") #place entry

        #label and scale for dosage
        tk.Label(self, text="Dosage:").grid(row=6, column=0, padx=10, pady=5, sticky="E") #place label
        self.dosage_scale = tk.Scale(self, from_=1, to=500, orient="horizontal") #create scale
        self.dosage_scale.grid(row=6, column=1, padx=10, pady=5, sticky="W") #place scale

        #label and combobox for dosage units
        tk.Label(self, text="Units:").grid(row=6, column=1, padx=10, pady=5, sticky="E") #create label
        self.units_combobox = ttk.Combobox(self, values=["mg", "g", "ml"], state="readonly", width=10) #create combobox
        self.units_combobox.grid(row=6, column=2, sticky="W") #place combobox

        #label and spinbox for tablets/pills to take
        tk.Label(self, text="Tablets/Pills to Take:").grid(row=7, column=0, padx=10, pady=5, sticky="E") #create label
        self.tablets_spinbox = tk.Spinbox(self, from_=1, to=100) #create spinbox
        self.tablets_spinbox.grid(row=7, column=1, padx=10, pady=5, sticky="W") #place spinbox

        #label and spinbox for current tablets/pills
        tk.Label(self, text="Current Tablets/Pills:").grid(row=8, column=0, padx=10, pady=5, sticky="E") #create label
        self.current_tablets_spinbox = tk.Spinbox(self, from_=1, to=1000) #create spinbox
        self.current_tablets_spinbox.grid(row=8, column=1, padx=10, pady=5, sticky="W") #place spinbox

        #label and calendar entry for selecting date
        tk.Label(self, text="Select Date:").grid(row=9, column=0, padx=10, pady=5, sticky="E") #create label
        #creat dateentry(calendar) with a bunch of cool decorations
        self.date_entry = DateEntry(self, width=12, background="#E96E7E", foreground="white", headersbackground='#4C535D', headersforeground="white", bordercolor='#4C535D', borderwidth=2)
        self.date_entry.grid(row=9, column=1, padx=10, pady=5, sticky="W") #place date entry

        #label and entry for selecting time
        tk.Label(self, text="Select Time:").grid(row=10, column=0, padx=10, pady=5, sticky="E") #create label
        self.time_entry = tk.Entry(self) #create the entry for time
        self.time_entry.grid(row=10, column=1, padx=10, pady=5, sticky="W") #place entry

        #button to confirm selection
        self.confirm_button = tk.Button(self, text="Confirm Selection", command=self.confirm_selection) #create confirm button
        self.confirm_button.grid(row=11, column=0, columnspan=3, padx=10, pady=10) #place confirm button

    #function to show vitamin combobox and hide mineral combobox
    def show_vitamins(self):
        # show the vitamin combobox and label
        self.vitamin_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="W")
        self.vitamin_label.grid(row=4, column=0, padx=10, pady=5, sticky="E")
        # hide the mineral combobox and label
        self.mineral_combobox.grid_forget()
        self.mineral_label.grid_forget()

    #function to show mineral combobox and hide vitamin combobox
    def show_minerals(self):
        # show the mineral combobox and label
        self.mineral_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="W")
        self.mineral_label.grid(row=4, column=0, padx=10, pady=5, sticky="E")
        # hide the vitamin combobox and label
        self.vitamin_combobox.grid_forget()
        self.vitamin_label.grid_forget()

    #function to confirm selection and save data
    def confirm_selection(self):
        # retrieve user inputs from various widgets
        supplement_name = self.label_entry.get() # gets the supplement name from the entry field
        dosage = self.dosage_scale.get() # gets the dosage from the scale widget
        unit = self.units_combobox.get() # gets the selected unit (mg, g, ml) from the combobox
        tablets = self.tablets_spinbox.get() # gets the number of tablets from the spinbox
        current_tablets = self.current_tablets_spinbox.get() # gets the current number of tablets from the spinbox
        selected_date = self.date_entry.get_date() # gets the selected date from the date picker
        selected_time = self.time_entry.get() # gets the time from the time entry field

        # validate inputs to ensure necessary fields are filled
        if not supplement_name: 
            messagebox.showerror("Error", "Please enter or select a supplement name") # error if supplement name is missing
        elif not unit:
            messagebox.showerror("Error", "Please select a unit for dosage") # error if unit is not selected
        elif not selected_time:
            messagebox.showerror("Error", "Please enter the time you want to take the supplement") # error if time is not entered
        else:
            # show confirmation message with all the details
            messagebox.showinfo("Confirmation", 
                                f"Supplement '{supplement_name}' scheduled for {selected_date} at {selected_time}. "
                                f"Dosage: {dosage} {unit}, Tablets: {tablets}, Current Tablets: {current_tablets}") 

        #prepare data for saving
        user_data = {
            "supplement_name": supplement_name,
            "dosage": dosage,
            "unit": unit,
            "tablets": tablets,
            "current_tablets": current_tablets,
            "selected_date": str(selected_date),
            "selected_time": selected_time
        }

        #save data to JSON file
        self.save_data_to_json(user_data)

#function to save user data to JSON file
    def save_data_to_json(self, user_data):
        try:
            # attempt to load existing data from the file if it exists
            try:
                with open('user_data.json', 'r') as file:
                    data = json.load(file) # load JSON data
            except FileNotFoundError:
                data = {} # if file not found, start with an empty dictionary

            # add or update user data using a unique identifier
            user_id = USER
            data[user_id] = user_data

            # write the updated data back to the JSON file
            with open('user_data.json', 'w') as file:
                json.dump(data, file, indent=4) # save data with indentation for readability
        except Exception as e:
            # display an error message if saving fails
            messagebox.showerror("Error", f"An error occurred while saving data: {e}")

if __name__ == "__main__": #checks if python script is being run directly or imported as a module into another script
    root.mainloop() #start event loop
