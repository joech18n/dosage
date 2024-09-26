#joe Chan - Dosage Application (Supplement Tracker App) - Version 3

#-------------------------------------------------------------------------------------------------------------------------------- #
#                                                         IMPORTS                                                                 #
#-------------------------------------------------------------------------------------------------------------------------------- #
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
from PIL import Image, ImageTk
from tkcalendar import Calendar
from tkcalendar import DateEntry
import json
from win10toast import ToastNotifier
import time
import threading
from datetime import datetime
import re
import os
from cryptography.fernet import Fernet

#-------------------------------------------------------------------------------------------------------------------------------- #
#                                               FUNCTIONS AND INITIALISATION                                                      #
#-------------------------------------------------------------------------------------------------------------------------------- #


#COLOURS
PINK = "#E96E7E"
NAVCOLOUR = "#D8CFC4"

#set user variable as empty string to be altered in check_credentials() function
USER = ""

#set minimum and maximum character length for new usernames and passwords
MIN_CHAR_LENGTH = 8
MAX_CHAR_LENGTH = 15

#initialising toplevelwindow variable which checks if there is an existing top level widget to avoid duplication
toplevelwindow = False

#DATA ENCRYPTION
with open('config/mykey.key','rb') as mykey: #retrieves key
    key = mykey.read()

f = Fernet(key) #initialise key 

#function will update encrypted file after updated decrypted file
def encrypt_files():
    #encrypting user csv file
    with open('data/dec_users.csv', 'rb') as decrypted_file: #open decrypted csv file
        file_data = decrypted_file.read() #storing decrypted content
        encrypted_data = f.encrypt(file_data) #encrypting content
    with open('data/enc_users.csv', 'wb') as encrypted_file: #opening existing encrypted file
        encrypted_file.write(encrypted_data) #rewriting encrypted data

    #encrypting user data json file
    with open('data/dec_user_data.json', 'rb') as decrypted_file: #open decrypted json file
        file_data = decrypted_file.read() #storing decrypted content
        encrypted_data = f.encrypt(file_data) #encypting content
    with open('data/enc_user_data.json', 'wb') as encrypted_file: #opening existing encrypted json file
        encrypted_file.write(encrypted_data) #rewriting encrypted data

#function decrypts encrypted files
def decrypt_files():
    #decrypting the users CSV file
    with open('data/enc_users.csv', 'rb') as encrypted_file:  #open encrypted csv file
        encrypted = encrypted_file.read()  #storing encrypted content

    decrypted = f.decrypt(encrypted)  #decrypt content using fernet

    #writing decrypted content to new file
    with open('data/dec_users.csv', 'wb') as decrypted_file:  #open new decrypted csv file
        decrypted_file.write(decrypted)  # write the decrypted content to the file

    # Decrypting the user data JSON file
    with open('data/enc_user_data.json', 'rb') as encrypted_file:  #open encrypted json file
        encrypted = encrypted_file.read()  #storing encrypted content

    decrypted = f.decrypt(encrypted)  #decrypt the content using fernet

    # Write the decrypted content to a new file
    with open('data/dec_user_data.json', 'wb') as decrypted_file:  #open a new decrypted json file
        decrypted_file.write(decrypted)  #write the decrypted content to the file

decrypt_files()  #calling the function here for simplicity


#function to read text file and return a list of lines
def read_file(filename):
    try:
        #open the file and read non-empty lines
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip()] #strip whitespace and ignore empty lines
        if not lines:
            print(f"Warning: The file {filename} is empty or contains only empty lines.") #warn if no lines are found
        return lines
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.") #error if file does not exist
        return [] #return an empty list on error
    
#load external data about vitamins and minerals from text files
VITAMINS = read_file('data/vitamins.txt')
MINERALS = read_file('data/minerals.txt')


#function to validate that input is an integer
def validate_integer_input(value):
    if value.isdigit(): #if integer
        return True
    elif value == "":  #aallow clearing the field
        return True
    else:
        return False

#function for creating sign in window
def sign_in(): 
    global toplevelwindow

    #checks if a top-level window is already open
    if toplevelwindow == False:
        sign_in_window = tk.Toplevel(root)  #creates a new top-level window
        toplevelwindow = True  #sets the global flag to True to prevent multiple windows

        sign_in_window.title("Sign In")  #sets the title of the sign-in window
        sign_in_window.geometry("230x150")  #defines the size of the window
        sign_in_window.resizable(False, False)

        #function to handle the event when the user clicks the 'x' button to close the window
        def on_close():
            global toplevelwindow
            toplevelwindow = False  #resets the flag to allow future windows
            sign_in_window.destroy()  #properly closes the sign-in window

        #binds the 'x' button click event to the on_close function
        sign_in_window.protocol("WM_DELETE_WINDOW", on_close)

        #label and entry widget for username
        tk.Label(sign_in_window, text="Username:").grid(row=0, column=0, pady=10, padx=10)  #adds a label for the username
        username_entry = tk.Entry(sign_in_window)  #creates an entry widget for input
        username_entry.grid(row=0, column=1, pady=10, padx=10)  #positions the entry field on the grid

        #label and entry widget for password
        tk.Label(sign_in_window, text="Password:").grid(row=1, column=0, pady=10, padx=10)  #adds a label for the password
        password_entry = tk.Entry(sign_in_window, show="*")  #creates an entry field that hides input with asterisks
        password_entry.grid(row=1, column=1, pady=10, padx=10)  #positions the entry field on the grid

        #function to check the entered credentials against the stored CSV file
        def check_credentials():
            global USER, toplevelwindow
            username = username_entry.get()  #retrieves the username from the entry widget
            password = password_entry.get()  #retrieves the password from the entry widget

            #opens the CSV file and reads through it to verify credentials
            with open("data/dec_users.csv", mode='r') as file:
                reader = csv.reader(file)  #creates a CSV reader object
                for row in reader:
                    #if the username and password match a row in the CSV file, log the user in
                    if row == [username, password]:
                        messagebox.showinfo("Success", "Login successful!")  #shows success message
                        USER = username_entry.get() 
                        sign_in_window.destroy()  #closes the sign-in window
                        toplevelwindow = False  #resets the flag to allow future windows
                        root.withdraw()  #hides the main application window
                        app = Application()  #initializes the main application
                        app.mainloop()  #starts the main application loop
                        return  #exits the function after successful login
                messagebox.showerror("Error", "Invalid username or password")  #shows error if no match is found
                sign_in_window.lift() #raises the sign in window back up
                toplevelwindow = False 

        #creates a sign-in button and assigns the check_credentials function to it
        tk.Button(sign_in_window, text="Sign In", command=check_credentials).grid(row=2, column=0, columnspan=2, pady=20)  #places the button at the bottom

#function for creating Register window
def register():
    global toplevelwindow

    #checks if a top-level window is already open
    if toplevelwindow == False:
        register_window = tk.Toplevel(root)  #creates a new window
        toplevelwindow = True  #sets the global flag to True to prevent multiple windows
        register_window.resizable(False, False)

        register_window.title("Register")  #sets the title of the window
        register_window.geometry("230x150")  #defines the size of the register window

        #function to handle the event when the user clicks the 'x' button to close the window
        def on_close():
            global toplevelwindow
            toplevelwindow = False  #resets the flag to allow future windows
            register_window.destroy()  #properly closes the register window

        #binds the 'x' button click event to the on_close function
        register_window.protocol("WM_DELETE_WINDOW", on_close)

        #label and entry widget for username
        tk.Label(register_window, text="Username:").grid(row=0, column=0, pady=10, padx=10)  #adds a label for the username
        username_entry = tk.Entry(register_window)  #creates an entry widget for input
        username_entry.grid(row=0, column=1, pady=10, padx=10)  #positions the entry field on the grid

        #label and entry widget for password
        tk.Label(register_window, text="Password:").grid(row=1, column=0, pady=10, padx=10)  #adds a label for the password
        password_entry = tk.Entry(register_window, show="*")  #creates an entry field that hides input with asterisks
        password_entry.grid(row=1, column=1, pady=10, padx=10)  #positions the entry field on the grid

        #function to save the credentials entered by the user
    def save_credentials():
        global toplevelwindow
        username = username_entry.get()  # retrieves the username from the entry widget
        password = password_entry.get()  # retrieves the password from the entry widget

        # Check username length
        if len(username) < MIN_CHAR_LENGTH or len(username) > MAX_CHAR_LENGTH:
            messagebox.showerror("Error", f"Username must be between {MIN_CHAR_LENGTH} and {MAX_CHAR_LENGTH} characters.")
            register_window.lift()
            return  # exits the function if there is an error

        # Check password length and requirements
        if len(password) < MIN_CHAR_LENGTH or len(password) > MAX_CHAR_LENGTH:
            messagebox.showerror("Error", f"Password must be between {MIN_CHAR_LENGTH} and {MAX_CHAR_LENGTH} characters.")
            register_window.lift()
            return  # exits the function if there is an error

        # Use regex to check for at least one uppercase letter, one number, and one symbol
        if not re.search(r"[A-Z]", password):
            messagebox.showerror("Error", "Password must contain at least one uppercase letter.")
            register_window.lift()
            return

        if not re.search(r"[0-9]", password):
            messagebox.showerror("Error", "Password must contain at least one number.")
            register_window.lift()
            return

        if not re.search(r"[_!@#$%^&*(),.?\":{}|<>]", password):  # adjust symbols as needed
            register_window.lift()
            messagebox.showerror("Error", "Password must contain at least one symbol.")
            return

        # Check if either the username or password field is empty
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")  # shows error if fields are empty
            toplevelwindow = False
            return  # exits the function if there is an error

        # Check if username already exists in CSV file
        try:
            with open('data/dec_users.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == username:  # Check if the username already exists
                        messagebox.showerror("Error", "Username already exists. Please choose another.")
                        register_window.lift()
                        return  # exits if username is already taken
        except FileNotFoundError:
            pass  # If the file doesn't exist, proceed to create it

        # If username is unique, add it to the CSV file
        with open('data/dec_users.csv', mode='a', newline='') as file:
            writer = csv.writer(file)  # creates a CSV writer object
            writer.writerow([username, password])  # writes the credentials to the CSV file

        messagebox.showinfo("Success", "Registration successful! Please sign in. ")  # displays success message
        register_window.destroy()  # closes the registration window after successful registration
        toplevelwindow = False  # resets the flag to allow future windows

                 
    #creates a register button and assigns the save_credentials function to it
    tk.Button(register_window, text="Register", command=save_credentials).grid(row=2, column=0, columnspan=2, pady=20)  #places the button at the bottom

#function for loading the external data from json file specifically for notification
def load_user_data():
    #attempt to open the user_data.json file in read mode
    try:
        with open('data/dec_user_data.json', 'r') as file:
            #load and return the user data from the JSON file
            return json.load(file)
    except FileNotFoundError:
        #if the file is not found, return an empty dictionary
        return {}

#simple function that creates the wnitoast notification 
def send_notification(supplement_name, time):
    #create an instance of ToastNotifier to show notifications
    toaster = ToastNotifier()
    #show a toast notification with the supplement name and current time
    toaster.show_toast("Supplement Reminder", 
                        f"it's {time}! Time to take {supplement_name}!",
                        duration=10)  #notification lasts for 10 seconds

#every 60 seconds (as stated where mainloop is initiated), 
#this function will iterate over the external data from json file to see if the 
#current time and date matches with a time and date specified by user
def check_notifications():
    #print a message indicating that notifications are being refreshed
    print("refreshing...")

    #load user data from the JSON file
    user_data = load_user_data()
    #get the current user ID from the USER variable
    user_id = USER  
    #get the current time in HH:MM format
    current_time = datetime.now().strftime("%H:%M")  
    #get the current date
    current_date = datetime.now().date()  

    #check if the user ID exists in the user data
    if user_id in user_data:
        #iterate through each entry associated with the current user ID
        for entry in user_data[user_id]:
            #extract the selected time for the supplement from the entry
            selected_time = entry['selected_time']
            #parse the selected date from the entry to a date object
            selected_date = datetime.strptime(entry['selected_date'], "%Y-%m-%d").date()  
            #convert the frequency value from the entry to an integer
            frequency = int(entry['frequency'])  

            #calculate the difference in days between the current date and selected date
            days_since_selected = (current_date - selected_date).days
            
            #check if the current time matches the selected time
            #and if the current date is a valid notification date based on frequency
            if selected_time == current_time and days_since_selected % frequency == 0:
                #send a notification for the supplement
                send_notification(entry['supplement_name'], selected_time)

    print("refreshing...")

    user_data = load_user_data()
    user_id = USER  #assuming USER variable holds the current user ID
    current_time = datetime.now().strftime("%H:%M")  #Get current time in HH:MM format
    current_date = datetime.now().date()  #Get current date

    if user_id in user_data:
        for entry in user_data[user_id]:
            selected_time = entry['selected_time']
            selected_date = datetime.strptime(entry['selected_date'], "%Y-%m-%d").date()  #Parse selected date
            frequency = int(entry['frequency'])  #convert frequency to an integer

            #calculate the difference in days
            days_since_selected = (current_date - selected_date).days
            
            #check if the current time matches and if the current date is a valid notification date
            if selected_time == current_time and days_since_selected % frequency == 0:
                send_notification(entry['supplement_name'], selected_time)

#function that acts as continuous loop every 60s to call check notifications function
def notification_thread():
    while True:
        check_notifications()
        time.sleep(60)  #Check every minute


#-------------------------------------------------------------------------------------------------------------------------------- #
#                                                        MAIN MENU                                                                #
#-------------------------------------------------------------------------------------------------------------------------------- #
root = tk.Tk() #create the main window
root.title("Dosage") #set the window title
root.geometry("300x200") #set the window size
root.configure(bg='#e96E7E') #set the background color pink
root.resizable(width=False, height=False) #make the window size fix

#load and display the image using Pillow
logo_image = Image.open("assets/logo.png") #opens the image file named 'logo.png'
logo_image = logo_image.resize((450, 75), Image.LANCZOS) #resizes the image to 450x75 using high-quality LANCZOS filter
logo_photo = ImageTk.PhotoImage(logo_image) #converts the image to a PhotoImage object for Tkinter

#creates a label to display the logo image
logo_label = tk.Label(root, image=logo_photo) #assigns the PhotoImage object to a label
logo_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10) #places the label on the grid, spanning 3 columns, with padding

#welcome text label
welcome_label = tk.Label(root, text="Welcome.", fg="white", bg='#e96E7E', font=("Arial Bold", 17)) #label with welcome text, white text on pink background, bold Arial font size 17
welcome_label.grid(row=1, column=0, rowspan=3) #places the label on the grid, spanning 3 rows vertically

#buttons for sign in and register
tk.Button(root, text="Sign In", command=sign_in, width=15).grid(row=1, column=1, padx=10, pady=10) #sign in button, placed next to welcome label with padding
tk.Button(root, text="Register", command=register, width=15).grid(row=2, column=1, padx=10, pady=10) #register button, placed below the sign-in button, also with padding

#adjusts column weights so that they expand evenly
root.grid_columnconfigure(0, weight=1) #makes the first column expand to take up available space
root.grid_columnconfigure(1, weight=1) #makes the second column do the same




#-------------------------------------------------------------------------------------------------------------------------------- #
#                                                 MAIN APPLICATION                                                                #
#-------------------------------------------------------------------------------------------------------------------------------- #
class Application(tk.Toplevel): #new class made for main application
    def __init__(self): 
        super().__init__()  #inheriting toplevel parent class
        self.title("Dosage")  #title

        #center the application window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (500 / 2))
        y_coordinate = int((screen_height / 2) - (585 / 2))
        self.geometry(f"500x585+{x_coordinate}+{y_coordinate}")

        self.resizable(False, False)
    
        self.container = tk.Frame(self) #creating  new container for information
        self.container.grid(row=0, column=0, sticky="NSEW") #placing container

        #configuring the the row and column of the the container
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {} #create dictionary for frames
        for F in (homePage, addPage, settingsPage): #iterates through the pages
            page_name = F.__name__ #get the name of thee class of the window
            frame = F(parent=self.container, controller=self) #create instance of the page
            self.frames[page_name] = frame #finds frame in dictionary
            frame.grid(row=0, column=0, sticky="NSEW") #places frame to cover entire container

        self.show_frame("homePage") #makes the mysupplements page visible

    #function for showing the frame (used for changing windows)
    def show_frame(self, page_name): 
        frame = self.frames[page_name]
        frame.tkraise()

#-------------------------------------------------------------------------------------------------------------------------------- #
#                                                  BANNER TEMPLATE                                                                #
#-------------------------------------------------------------------------------------------------------------------------------- #
class BasePage(tk.Frame):  #define a class basepag that inherits from tk.Frame
    def __init__(self, parent, controller):  #constructor method for initializing the page
        super().__init__(parent)  #initialize the frame with the given parent 
        self.controller = controller  #storing controller for managing frames

        #create a banner frame at the top of the page for holding the logo
        banner_frame = tk.Frame(self, bg='#e96E7E')  #set background color to pink
        banner_frame.grid(row=0, column=0, columnspan=3, sticky="EW")  #position banner at the top

        #load and resize the logo image
        logo_image = Image.open("assets/logo.png")  #open the logo image file
        logo_image = logo_image.resize((480, 80), Image.LANCZOS)  #resize image using high-quality resizing

        self.logo_photo = ImageTk.PhotoImage(logo_image)  #convert image to a format that tkinter can use
        
        #create a label widget to display the logo
        logo_label = tk.Label(banner_frame, image=self.logo_photo)  #assign logo image to label
        logo_label.grid(row=0, column=0, padx=8, pady=10)  #position label

        #create a navigation frame below the banner for holding navigation buttons
        nav_frame = tk.Frame(self, background=NAVCOLOUR)
        nav_frame.grid(row=1, columnspan=3, sticky="EW")  #position navigation frame below banner

        #create the "home" button within the navigation frame
        home_button = tk.Button(nav_frame, text="Home", command=lambda: controller.show_frame("homePage"))  #set button text and command to switch to homePage
        home_button.grid(row=0, column=0, padx=5, pady=5, sticky="EW")  #position button 

        #create the "Add Supplements" button within the navigation frame
        addsupplements_button = tk.Button(nav_frame, text="Add Supplements", command=lambda: controller.show_frame("addPage"))  #set button text and command to switch toaddPage
        addsupplements_button.grid(row=0, column=2, padx=5, pady=5, sticky="EW")  #position button

        #create the "Settings" button within the navigation frame
        settings_button = tk.Button(nav_frame, text="Settings", command=lambda: controller.show_frame("settingsPage"))  #set button text and command to switch settings page
        settings_button.grid(row=0, column=3, padx=5, pady=5, sticky="EW")  #position button

#-------------------------------------------------------------------------------------------------------------------------------- #
#                                                     HOME PAGE                                                                   #
#-------------------------------------------------------------------------------------------------------------------------------- #
class homePage(BasePage):
    def __init__(self, parent, controller):  #this method is basically a constructor, it sets up the page when an instance is created
        super().__init__(parent, controller)  #calling the parent class's init method to ensure everything is set up properly
        supplementsframe = tk.Frame(self, bg=NAVCOLOUR) 
        supplementsframe.grid(columnspan=10, rowspan=10, sticky="NSEW")  #grid configuration with column span and row span set to 10, ensuring it takes up space

        #configuring columns of the frame so that everything looks neat
        supplementsframe.columnconfigure(0, weight=1)  #making sure column 0 takes up equal space
        supplementsframe.columnconfigure(1, weight=1)  #same thing for column 1
        supplementsframe.columnconfigure(2, weight=1)  #and column 2, all equally balanced

        #so this gets today's date in 'yyyy-mm-dd' format and assigns it to 'self.today'
        self.today = datetime.now().strftime("%Y-%m-%d")


        #calendar fancy pinkish background colour
        self.home_calendar = Calendar(supplementsframe, selectmode="day", date_pattern="yyyy-mm-dd", width=12,
            background="#e96E7E", #pink
            foreground="white",
            headersforeground="white",
            bordercolor='#4C535D', #grey
            borderwidth=2, headersbackground="#4c535d") #grey
        self.home_calendar.grid(row=3, columnspan=3, pady=(10, 10))  #positioning the calendar and giving it some padding

        #setting today's date to be the default selection when the calendar first loads
        self.home_calendar.selection_set(self.today)

        #this label is going to display whatever date the user selects
        self.selected_date = tk.Label(supplementsframe, text="")
        self.selected_date.grid(row=4, column=1)

        #initializing the variable that will store the selected date, and we set it to today’s date by default
        self.selected_date_value = self.today  

        #where the selected date gets formatted into a more human-readable format (eg."monday, 22 of September")
        date_obj = datetime.strptime(self.today, "%Y-%m-%d")
        self.formatted_date = date_obj.strftime("%A, %d of %B")  #fancy formatting here
        self.selected_date.config(text=self.today)  #updating the label with today's date

        #binding the calendar widget to the 'update_selected_date' method  when the user clicks on a date, it updates the selected date
        self.home_calendar.bind("<<CalendarSelected>>", self.update_selected_date)

        #button that will redirect users to the 'addPage' to add new supplements, pretty self-explanatory
        self.add_supplements_button = tk.Button(supplementsframe, text="Add Supplements", command=lambda: controller.show_frame("addPage"))
        self.add_supplements_button.grid(row=4, column=1, pady=(2,7))

        #frame for holding the list of supplements,  this is where the table will go later
        self.listofsupplements_frame = tk.Frame(supplementsframe)
        self.listofsupplements_frame.grid(row=5, column=0, columnspan=3, pady=5, sticky="NSEW")  #positioning this frame nicely below everything else

        #initializing the label inside this frame to show the current day in a big, bold font
        self.day_label = ttk.Label(self.listofsupplements_frame, text="", font=('Verdana', 15, 'bold'))
        self.day_label.grid(row=0, column=0, padx=10, pady=5, sticky="W")

        #updating the day label to show the formatted version of today's date
        self.day_label.config(text=self.formatted_date)

        #calling a method that will create the table where supplements will be displayed
        self.create_supplements_table()

        #this method loads supplements for today's date as soon as the page loads
        self.load_supplements_for_date(self.today)

    def update_selected_date(self, event=None):
        #getting the date selected from the calendar and updating the label with it
        date_str = self.home_calendar.get_date()
        self.selected_date.config(text=date_str) #configures the date into the selected date
        self.selected_date_value = date_str  #storing it in a variable as well

        #formatting the selected date to something a bit more user-friendly and updating the label
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%A, %d of %B")
        self.day_label.config(text=formatted_date)

        #loading supplements for the newly selected date
        self.load_supplements_for_date(date_str)

    #function for creating the table of the supplements 
    def create_supplements_table(self):
        #configuring the grid so the table frame stretches nicely inside the parent frame
        self.listofsupplements_frame.columnconfigure(0, weight=1)
        self.listofsupplements_frame.rowconfigure(1, weight=1)  #row 1 for the table

        #making sure the day label is placed properly above the table, just in case
        self.day_label.grid(row=0, column=0, padx=10, pady=5, sticky="EW")

        #creating a frame that will actually hold the table (treeview)
        table_frame = ttk.Frame(self.listofsupplements_frame)
        table_frame.grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)

        #creating the table with three columns: 'Name', 'Time', and 'Actions'
        self.supplement_table = ttk.Treeview(table_frame, columns=("Name", "Time", "Actions"), show="headings", height=6)
        self.supplement_table.pack(fill="both", expand=True)  #make sure the table fills the space

        #setting the column headings
        self.supplement_table.heading("Name", text="Supplement Name") #supplement name
        self.supplement_table.heading("Time", text="Time") #time
        self.supplement_table.heading("Actions", text="Actions (double click)") #actions (edit or delete)

        #specifying the widths for each column, to keep things looking tidy
        self.supplement_table.column("Name", width=150, anchor="center", minwidth=150)
        self.supplement_table.column("Time", width=100, anchor="center", minwidth=100)
        self.supplement_table.column("Actions", width=150, anchor="center", minwidth=150)

        #bind double-clicking on a row to the 'on_row_double_click' method, where edit/delete options will pop up
        self.supplement_table.bind("<Double-1>", self.on_row_double_click)

        #customizing the table header font to make it bold and stand out a bit
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

    #function for finding the supplements er user allocated to the specific date chosen by user - iterates throug json file
    def load_supplements_for_date(self, selected_date):
        #load the user data from a json file, this is where the magic happens for loading the supplements
        user_data = self.load_data_from_json()

        #first, we clear the table so we don't display old data mixed with new data
        for item in self.supplement_table.get_children():
            self.supplement_table.delete(item)

        #convert the selected date into a datetime object for comparison purposes
        selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d")

        #loop through the user's data to check if the supplement needs to appear on the selected date
        for entry in user_data:
            entry_date_obj = datetime.strptime(entry['selected_date'], "%Y-%m-%d")
            frequency = int(entry.get('frequency'))  #how often the supplement should show up

            #calculate the difference between the selected date and the supplement's starting date
            days_difference = (selected_date_obj - entry_date_obj).days

            #only add the supplement if it should appear on the selected date (based on frequency)
            if days_difference % frequency == 0 and days_difference >= 0:
                self.supplement_table.insert("", "end", values=(entry['supplement_name'], entry['selected_time'], "Edit/Delete"))  #insert into table

    #function for handling the edit option for supplements (creates new top level window for changing name and time)
    def handle_edit(self, selected_item):
        if hasattr(self, 'edit_window') and self.edit_window.winfo_exists():
            return  #do nothing if the edit window is already open
    
        #retrieve supplement data from the table row
        item_values = self.supplement_table.item(selected_item)['values']
        supplement_name = item_values[0]
        time = item_values[1]  #assuming 'time' is in the format "HH:MM"

        #open an edit window
        edit_window = tk.Toplevel(self)
        edit_window.title(f"Editing: {supplement_name}")

        #resets dialog_open flag when the dialog is closed
        edit_window.protocol("WM_DELETE_WINDOW", lambda: (edit_window.destroy(), self.reset_dialog() ))
    
        #center the edit window and set a smaller size
        dialog_width = 380 #fixed needed width
        dialog_height = 160 #fixed needed height
        screen_width = edit_window.winfo_screenwidth() #storing in variable
        screen_height = edit_window.winfo_screenheight() #storing in variable
        x_coordinate = int((screen_width / 2) - (dialog_width / 2)) #placing in the centre of the screen
        y_coordinate = int((screen_height / 2) - (dialog_height / 2)) #placing in the centre of the screen
        edit_window.geometry(f"{dialog_width}x{dialog_height}+{x_coordinate}+{y_coordinate}") ##basically figuring out new geometry 
        edit_window.resizable(0, 0)  #prevent resizing

        #create entry fields to edit the supplement name
        ttk.Label(edit_window, text="Custom Supplement Label:", font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="E")
        name_entry = ttk.Entry(edit_window, font=('Arial', 10))
        name_entry.insert(0, supplement_name)  #pre-fill the entry with the current supplement name
        name_entry.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="W")

        #label for selecting time
        ttk.Label(edit_window, text="Select Time (24 hr time):", font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=5, sticky="E")

        #create a new frame to hold the time spinboxes
        timeentry_frame = tk.Frame(edit_window)
        timeentry_frame.grid(row=1, column=1, pady=5, sticky="NSEW")

        #labels for hours and minutes within the time entry frame
        ttk.Label(timeentry_frame, text="HR:", font=('Arial', 10)).grid(row=0, column=0, padx=5, sticky="E")
        ttk.Label(timeentry_frame, text="MIN:", font=('Arial', 10)).grid(row=0, column=2, padx=5, sticky="E")

        #extract the current hours and minutes from the existing time string
        hour, minute = time.split(':')  #assuming the time format is "HH:MM"

        #create spinboxes for hour and minute selection
        hours_spinbox = tk.Spinbox(timeentry_frame, from_=0, to=23, width=5, format="%02.0f", font=('Arial', 10))
        minutes_spinbox = tk.Spinbox(timeentry_frame, from_=0, to=59, width=5, format="%02.0f", font=('Arial', 10))

        #insert the current hour and minute values into the spinboxes
        hours_spinbox.delete(0, 'end')  #clear any existing value
        hours_spinbox.insert(0, hour)  #set the spinbox to the current hour
        minutes_spinbox.delete(0, 'end')  #clear any existing value
        minutes_spinbox.insert(0, minute)  #set the spinbox to the current minute

        #place the spinboxes in the frame for time entry
        hours_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky="W") 
        minutes_spinbox.grid(row=0, column=3, padx=5, pady=5, sticky="W")

        #function saves changes on entries made in editing window
        def save_changes():
            #disables editing menu buttons
            self.edit_save_button.config(state="disabled")
            self.edit_cancel_button.config(state="disabled")

            #retrieves editted entries
            new_name = name_entry.get()
            new_hour = hours_spinbox.get()
            new_minute = minutes_spinbox.get()
            new_time = f"{new_hour}:{new_minute}"

            #load user data from JSON
            user_data = self.load_data_from_json()  #this returns the user's list of supplements

            #update the relevant entry in the current user's list
            for entry in user_data:
                if entry['supplement_name'] == supplement_name:
                    entry['supplement_name'] = new_name
                    entry['selected_time'] = new_time
                    break  #exit the loop after updating

            #load the entire data structure again to modify it
            with open('data/dec_user_data.json', 'r') as file:
                all_data = json.load(file)

            #update the correct user's list in all_data
            all_data[USER] = user_data  #replace with the updated list for the current user

            #save the updated data back to the JSON file
            with open('data/dec_user_data.json', 'w') as file:
                json.dump(all_data, file, indent=4)

            #show confirmation message
            messagebox.showinfo("Success!", "Changes have been saved successfully!")

            #update the values in the table
            self.supplement_table.item(selected_item, values=(new_name, new_time, "Edit/Delete"))

            edit_window.destroy()
            self.reset_dialog()

        #add Save button to apply the changes
        self.edit_save_button = ttk.Button(edit_window, text="Save", command=save_changes, width=10)
        self.edit_save_button.grid(row=2, column=0, columnspan=2, pady=(10, 10))

        #add a Cancel button to close the edit window
        self.edit_cancel_button = ttk.Button(edit_window, text="Cancel", command=lambda: (edit_window.destroy(), self.reset_dialog()), width=10)
        self.edit_cancel_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))

    #function for handling the delete option for supplements (with msgbox confirming deletion)
    def handle_delete(self, selected_item):
        #disabling buttons on show edit delete menu after the user clicks it once so multiple msgboxes don't appear
        self.edit_button.config(state="disabled")
        self.delete_button.config(state="disabled") 
        self.cancel_button.config(state="disabled")

        #confirm deletion
        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this supplement?")
        if confirm:
            #remove the selected item from the JSON and the table
            item_values = self.supplement_table.item(selected_item)['values']
            supplement_name = item_values[0]

            #load existing data
            with open('data/dec_user_data.json', 'r') as file:  #open in read mode first
                all_data = json.load(file)  #load existing data

            user_data = all_data.get(USER, [])  #get the user's data, or an empty list if not found
            for entry in user_data:
                if entry['supplement_name'] == supplement_name:
                    user_data.remove(entry)  #remove the supplement from the list
                    break  #exit the loop after removing

            #save the updated data back to the JSON file
            with open('data/dec_user_data.json', 'w') as file:
                all_data[USER] = user_data  #update the correct user's list
                json.dump(all_data, file)

            #remove the item from the table
            self.supplement_table.delete(selected_item)
        self.reset_dialog()


    #function for getting which button user double clicks - and also makes sure if the header is double clicked data is not taken
    def on_row_double_click(self, event):
        selected_items = self.supplement_table.selection()  #get selected rows
        if not selected_items:  #check if no row is selected
            messagebox.showwarning("No Selection", "Please select a supplement to edit or delete.")
            return  #exit the function if no selection
        selected_item = selected_items[0]  #get the first selected row
        self.show_edit_delete_menu(selected_item)

    #function for a messagebox asking is user actually wants to edit or delete, and then a top level window that lets user choose either edit or delete
    def show_edit_delete_menu(self, selected_item):
        #Check if the dialog is already open
        if hasattr(self, 'dialog_open') and self.dialog_open:
            return  #Prevent multiple dialogs

        #Set the dialog_open flag to True
        self.dialog_open = True

        action = messagebox.askyesno("Action", "Do you want to edit or delete this supplement?")
        if action:  #If user clicks "Yes"
            #Create a custom dialog for Edit or Delete
            dialog = tk.Toplevel(self)
            dialog.title("Choose an Action")
            
            #Set dialog dimensions
            dialog_width = 300  #Dialog width in pixels
            dialog_height = 150  #fixed dialog height
            screen_width = dialog.winfo_screenwidth()  #Screen width in pixels
            screen_height = dialog.winfo_screenheight()  #Screen height in pixels
            x_coordinate = int((screen_width / 2) - (dialog_width / 2))  #Center the dialog
            y_coordinate = int((screen_height / 2) - (dialog_height / 2))  #Center the dialog

            #setting dialog position and size
            dialog.geometry(f"{dialog_width}x{dialog_height}+{x_coordinate}+{y_coordinate}")
            dialog.resizable(False, False) #preventing resizing

            #heading label
            ttk.Label(dialog, text="Choose an action:", font=('Arial', 12)).pack(pady=(20, 10))

            #buttons for edit and delete
            button_frame = ttk.Frame(dialog)
            button_frame.pack(pady=10)

            #two choice buttons
            self.edit_button = ttk.Button(button_frame, text="Edit", command=lambda: self.handle_edit(selected_item) or dialog.destroy(), width=10)
            self.edit_button.pack(side="left", padx=10)
            self.delete_button = ttk.Button(button_frame, text="Delete", command=lambda: self.handle_delete(selected_item) or dialog.destroy(), width=10) #set delete button as variable so that it can be disabled in handle_delete
            self.delete_button.pack(side="right", padx=10)

            #adding a cancel button
            self.cancel_button = ttk.Button(dialog, text="Cancel",  command=lambda: (dialog.destroy(), self.reset_dialog()), width=10)
            self.cancel_button.pack(pady=(10, 20))

            dialog.transient(self)  #keepingdialog above the main window
            dialog.grab_set()       #prevent interaction with the main window until closed)

            #resetting dialog_open flag when the dialog is closed
            dialog.protocol("WM_DELETE_WINDOW", lambda: (dialog.destroy(), self.reset_dialog() ))
        else: 
            self.reset_dialog() 
        
    #function for resetting any dialog after a dialog is closed, so new dialog can open    
    def reset_dialog(self):
        #Resets the dialog_open flag to allow new dialogs to open.
        self.dialog_open = False

    #function for loading all the data that is allocated to the user which is logged in
    def load_data_from_json(self):
        #attempt to open and read the user data from a JSON file
        try:
            with open('data/dec_user_data.json', 'r') as file:
                data = json.load(file)  #load the JSON data into a variable
            
            #check if there is data available for the current user
            user_id = USER  #get the current user's ID
            if user_id in data:
                user_data = data[user_id]  #if user data exists, retrieve the list of supplements for that user
            else:
                user_data = []  #if there is no data for the user, create an empty list to return

            return user_data  #return the user's supplement data

        except Exception as e:
            print(f"Error loading data: {e}")  #print an error message if something goes wrong
            return []  #return an empty list in case of an error

#-------------------------------------------------------------------------------------------------------------------------------- #
#                                               ADDING SUPPLEMENTS PAGE                                                           #
#-------------------------------------------------------------------------------------------------------------------------------- #
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
        label.grid(row=2, columnspan=3, padx=10, pady=10) #place label

        #making new frame to span the 2 buttons to fit the entire width
        self.selectbuttons_frame = tk.Frame(self)
        self.selectbuttons_frame.grid(row=3, columnspan=3, sticky="NSEW")
        #configuring columns sizes
        self.selectbuttons_frame.grid_columnconfigure(0, weight=1)
        self.selectbuttons_frame.grid_columnconfigure(1, weight=1)

        #button to select vitamins
        tk.Button(self.selectbuttons_frame, text="Select Vitamin", command=self.show_vitamins).grid(row=0, column=0, padx=10, pady=5, sticky="EW")
        #button to select minerals
        tk.Button(self.selectbuttons_frame, text="Select Mineral", command=self.show_minerals).grid(row=0, column=1, padx=10, pady=5, sticky="EW")

        #labels and comboboxes for vitamins and minerals
        self.vitamin_label = tk.Label(self, text="Vitamins") #create label
        self.mineral_label = tk.Label(self, text="Minerals") #create label
        self.vitamin_combobox = ttk.Combobox(self, values=VITAMINS) #create combobox
        self.mineral_combobox = ttk.Combobox(self, values=MINERALS) #create combobox

        #label and entry for custom supplement name
        sup_label = tk.Label(self, text="Custom Supplement Label:")
        sup_label.grid(row=5, column=0, padx=10, pady=5, sticky="E") #create and place label
        self.label_entry = tk.Entry(self) #create entry
        self.label_entry.grid(row=5, column=1, padx=10, pady=5, sticky="W") #place entry

        #label and spinbox for dosage
        self.dosage_label = tk.Label(self, text="*Dosage of supplement:")
        self.dosage_label.grid(row=6, column=0, padx=10, pady=5, sticky="E") #place label


        #new frame for dosage positioning
        self.dosage_frame = tk.Frame(self)
        self.dosage_frame.grid(row=6, column=1, sticky="NSEW")

        self.dosage_spinbox = tk.Spinbox(self.dosage_frame, from_=1, to=500, width=10) #create spinbox
        self.dosage_spinbox.grid(row=0, column=0, padx=10, pady=5, sticky="W") #place spinbox

        #label and combobox for dosage units
        self.units_label = tk.Label(self.dosage_frame, text="Units:")
        self.units_label.grid(row=0, column=1, padx=10, pady=5, sticky="E") #create label
        self.units_combobox = ttk.Combobox(self.dosage_frame, values=["mg", "g", "ml"], state="readonly", width=3) #create combobox
        self.units_combobox.grid(row=0, column=2, pady=5, sticky="W") #place combobox

        #label and spinbox for tablets/pills to take
        self.tablets_label =tk.Label(self, text="*Number of Tablets/Pills per dose:")
        self.tablets_label.grid(row=7, column=0, padx=10, pady=5, sticky="E") #create label
        self.tablets_spinbox = tk.Spinbox(self, from_=1, to=100) #create spinbox
        self.tablets_spinbox.grid(row=7, column=1, padx=10, pady=5, sticky="W") #place spinbox

        #label and scale for current tablets/pills
        self.current_tabletlabel = tk.Label(self, text="*Your current number of Tablets/Pills:")
        self.current_tabletlabel.grid(row=8, column=0, padx=10, pady=5, sticky="E") #create label
        self.current_tablets_scale = tk.Scale(self, from_=1, to=1000, orient="horizontal", length=200) #create scale
        self.current_tablets_scale.grid(row=8, column=1, padx=10, pady=5, sticky="W") #place scale

        #accounts for if settings page has not yet been opened by user(created in controller)
        if "settingsPage" not in self.controller.frames:
            checked_count = 3
        else: #if user has opened settings/changed settings
            settings_page = self.controller.frames["settingsPage"] #retrieves the page
            checked_count = settings_page.get_checked_count() #counts the number of checked boxes on the page

        #creates and place widgets in their right spots
        self.show_other_widgets(checked_count)


    #function moves the other widgets up depending on how many boxes have been checked (ie. if 1 box checked, move up by 2)
    def show_other_widgets(self, checked_count):
        #label and calendar entry for selecting date
        tk.Label(self, text="Select Date:").grid(row=checked_count+6, column=0, padx=10, pady=5, sticky="E") #create label
        self.date_entry = DateEntry(
            self,
            width=12,
            background="#e96E7E", #pink
            foreground="white",
            headersbackground='#4c535d', #grey
            headersforeground="white",
            bordercolor='#4C535D', #grey
            borderwidth=2,
            date_pattern='dd/mm/yyyy'  #Set the desired date format
        )
        self.date_entry.grid(row=checked_count+6, column=1, padx=10, pady=5, sticky="W")

        #label and spinboxes for hours and minutes
        tk.Label(self, text="Select Time (24 hr time):").grid(row=checked_count+7, column=0, padx=10, pady=5, sticky="E") #create label

        #create new frame for time stuff
        self.timeentry_frame = tk.Frame(self)
        self.timeentry_frame.grid(row=checked_count+7, column=1, pady=5, sticky="NSEW")

        #labels for time entry
        tk.Label(self.timeentry_frame, text="HR:").grid(row=0, column=0, padx=10, sticky="E") #create and place label
        tk.Label(self.timeentry_frame, text="MIN:").grid(row=0, column=2, padx=10, sticky="E") #create and place label

        #time entry spinboxes
        self.hours_spinbox = tk.Spinbox(self.timeentry_frame, from_=0, to=23, width=5, format="%02.0f") #create hours spinbox
        self.minutes_spinbox = tk.Spinbox(self.timeentry_frame, from_=0, to=59, width=5, format="%02.0f") #create minutes spinbox
        self.hours_spinbox.delete(0, "end") #clear the initial value to display nothing
        self.minutes_spinbox.delete(0, "end") #clear the initial value to display nothing
        self.hours_spinbox.grid(row=0, column=1, padx=10, pady=5, sticky="W") #place hours spinbox
        self.minutes_spinbox.grid(row=0, column=3, padx=10, pady=5, sticky="W") #place minutes spinbox

        #label and combobox for dosage frequency
        tk.Label(self, text="Set reminder every:").grid(row=checked_count+8, column=0, padx=10, pady=5, sticky="E") #create label

        self.frequency_frame = tk.Frame(self)
        self.frequency_frame.grid(row=checked_count+8, column=1, sticky="NSEW")

        vcmd = (self.register(validate_integer_input), '%P') #setting validation command
        self.frequency_combobox = ttk.Combobox(self.frequency_frame, values=[1, 2, 3, 7, 14, 30], width=20, validate="key", validatecommand=vcmd)
        self.frequency_combobox.grid(row=0, column=0, padx=10, pady=5, sticky="W") #place combobox

        #label and combobox for dosage units
        self.units_label = tk.Label(self.frequency_frame, text="Days")
        self.units_label.grid(row=0, column=1, padx=10, pady=5, sticky="E") #create label

        #button to confirm selection
        self.confirm_button = tk.Button(self, text="Confirm Selection", command=self.confirm_selection, bg="green", fg="white") #create confirm button
        self.confirm_button.grid(row=checked_count+9, column=0, columnspan=4, padx=10, pady=10) #place confirm button

        bottom_label = tk.Label(self, text="*Options can be removed in settings")
        bottom_label.grid(row=checked_count+10, column=0, sticky="SW", padx=10, pady=10)

    #function to show vitamin combobox and hide mineral combobox
    def show_vitamins(self):
        #show the vitamin combobox and label
        self.vitamin_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="W")
        self.vitamin_label.grid(row=4, column=0, padx=10, pady=5, sticky="E")
        #hide the mineral combobox and label
        self.mineral_combobox.grid_forget()
        self.mineral_label.grid_forget()

    #function to show mineral combobox and hide vitamin combobox
    def show_minerals(self):
        #show the mineral combobox and label
        self.mineral_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="W")
        self.mineral_label.grid(row=4, column=0, padx=10, pady=5, sticky="E")
        #hide the vitamin combobox and label
        self.vitamin_combobox.grid_forget()
        self.vitamin_label.grid_forget()

    #function to confirm selection and save data
    def confirm_selection(self):
        supplement = ""
        #retrieve user inputs from various widgets
        if self.vitamin_combobox.get():
            supplement = self.vitamin_combobox.get()
        elif self.mineral_combobox.get():
            supplement = self.mineral_combobox.get()
        supplement_name = self.label_entry.get() #gets the supplement name from the entry field
        dosage = self.dosage_spinbox.get() #gets the dosage from the scale widget
        unit = self.units_combobox.get() #gets the selected unit (mg, g, ml) from the combobox
        tablets = self.tablets_spinbox.get() #gets the number of tablets from the spinbox
        current_tablets = self.current_tablets_scale.get() #gets the current number of tablets from the spinbox
        selected_date = self.date_entry.get_date() #gets the selected date from the date picker
        selected_hours = self.hours_spinbox.get() #gets the selected hours from the hours spinbox
        selected_minutes = self.minutes_spinbox.get() #gets the selected minutes from the minutes spinbox
        selected_time = f"{selected_hours.zfill(2)}:{selected_minutes.zfill(2)}" #format time
        frequency = self.frequency_combobox.get() #gets the selected frequency

        #validate inputs to ensure necessary fields are filled
        if not supplement: 
            messagebox.showerror("Error", "Please enter or select Vitamin or Mineral") #error if vitamin or mineral is missing
        elif not supplement_name: 
            messagebox.showerror("Error", "Please enter a custom supplement label") #error if supplement name is missing
        elif not selected_hours or not selected_minutes:
            messagebox.showerror("Error", "Please enter the time you want to take the supplement") #error if time is not entered
        elif not frequency:
            messagebox.showerror("Error", "Please select the frequency for taking the supplement") #error if frequency is not selected
        else:
            #show confirmation message with all the details
            messagebox.showinfo("Confirmation", 
                                f"{supplement}: Supplement '{supplement_name}' scheduled for {selected_date} at {selected_time}. "
                                f"Dosage: {dosage} {unit}, Tablets: {tablets}, Current Tablets: {current_tablets}, Frequency: {frequency}") 

            self.label_entry.delete(0, tk.END)  #Clear supplement name entry
            self.dosage_spinbox.delete(0, tk.END)  #Clear dosage spinbox
            self.units_combobox.set('')  #Clear units combobox selection
            self.tablets_spinbox.delete(0, tk.END)  #Clear tablets spinbox
            self.current_tablets_scale.set(0)  #Reset current tablets scale
            self.date_entry.set_date(None)  #Clear date picker
            self.hours_spinbox.delete(0, tk.END)  #Clear hours spinbox
            self.minutes_spinbox.delete(0, tk.END)  #Clear minutes spinbox
            self.frequency_combobox.set('')  #Clear frequency combobox selection
            
            if self.vitamin_combobox.get():
                self.vitamin_combobox.set('')
            elif self.mineral_combobox.get():
                self.mineral_combobox.set('')


            #prepare data for saving
            user_data = {
                "supplement": supplement,
                "supplement_name": supplement_name,
                "dosage": dosage,
                "unit": unit,
                "tablets": tablets,
                "current_tablets": current_tablets,
                "selected_date": str(selected_date),
                "selected_time": selected_time,
                "frequency": frequency
            }

            #save data to JSON file
            self.save_data_to_json(user_data)

    #function to save user data to JSON file
    def save_data_to_json(self, user_data):
        try:
            #attempt to load existing data from the file if it exists
            try:
                with open('data/dec_user_data.json', 'r') as file:
                    data = json.load(file)  #load JSON data
            except FileNotFoundError:
                data = {}  #if file not found, start with an empty dictionary

            #ensure the user's data is a list
            user_id = USER
            if user_id not in data:
                data[user_id] = []  #initialize with an empty list if user doesn't exist

            #append the new user data (supplement) to the user's list
            data[user_id].append(user_data)

            #write the updated data back to the JSON file
            with open('data/dec_user_data.json', 'w') as file:
                json.dump(data, file, indent=4)  #save data with indentation for readability
        except Exception as e:
            #display an error message if saving fails
            messagebox.showerror("Error", f"An error occurred while saving data: {e}")

#-------------------------------------------------------------------------------------------------------------------------------- #
#                                                   SETTINGS PAGE                                                                 #
#-------------------------------------------------------------------------------------------------------------------------------- #
class settingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller  #this is where we're storing the reference to the controller for use elsewhere

        #setting up column weights so things align nicely in a two-column layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #creating the label for the settings page with a custom font and some padding around it
        label = ttk.Label(self, text="Settings", font=('Verdana', 18, 'bold'))
        label.grid(row=2, columnspan=2, padx=10, pady=10)

        #creating the checkbox for toggling the display of dosage
        #we start by initializing a BooleanVar that will store the state of this checkbox
        #by default, we set it to true because we want dosage to be visible initially
        self.dosage_var = tk.BooleanVar(value=True)
        dosage_checkbox = tk.Checkbutton(self, text="Show Dosage", variable=self.dosage_var, command=lambda: (self.toggle_update(), self.toggle_dosage()))
        dosage_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky="W")

        #same process as above but now for the tablets/pills to take checkbox
        self.tablets_var = tk.BooleanVar(value=True)
        tablets_checkbox = tk.Checkbutton(self, text="Show Tablets/Pills to Take", variable=self.tablets_var, command=lambda: (self.toggle_update(), self.toggle_tablets()))
        tablets_checkbox.grid(row=4, column=0, padx=10, pady=5, sticky="W")

        #another checkbox for current tablets/pills, which works similarly to the previous ones
        self.current_tablets_var = tk.BooleanVar(value=True)
        current_tablets_checkbox = tk.Checkbutton(self, text="Show Current Tablets/Pills", variable=self.current_tablets_var, command=lambda: (self.toggle_update(), self.toggle_current_tablets()))
        current_tablets_checkbox.grid(row=5, column=0, padx=10, pady=5, sticky="W")


    def toggle_update(self):
        add_page = self.controller.frames["addPage"]  # get the addPage frame from the controller

        if self.dosage_var.get():  # check if dosage checkbox is checked
            # place dosage frame and label
            add_page.dosage_frame.grid(row=6, column=1, sticky="NSEW")
            add_page.dosage_label.grid(row=6, column=0, padx=10, pady=5, sticky="E")

            if self.tablets_var.get():  # check if tablets checkbox is checked
                # place tablets spinbox and label
                add_page.tablets_spinbox.grid(row=7, column=1, padx=10, pady=5, sticky="W") 
                add_page.tablets_label.grid(row=7, column=0, padx=10, pady=5, sticky="E")

                if self.current_tablets_var.get():  # check if current tablets checkbox is checked
                    # place current tablets scale and label
                    add_page.current_tablets_scale.grid(row=8, column=1, padx=10, pady=5, sticky="W")
                    add_page.current_tabletlabel.grid(row=8, column=0, padx=10, pady=5, sticky="E")

            elif self.current_tablets_var.get():  # if only current tablets checkbox is checked
                # place current tablets scale and label at row 7
                add_page.current_tablets_scale.grid(row=7, column=1, padx=10, pady=5, sticky="W")
                add_page.current_tabletlabel.grid(row=7, column=0, padx=10, pady=5, sticky="E")

        elif self.tablets_var.get():  # if only tablets checkbox is checked
            # place tablets spinbox and label
            add_page.tablets_spinbox.grid(row=6, column=1, padx=10, pady=5, sticky="W") 
            add_page.tablets_label.grid(row=6, column=0, padx=10, pady=5, sticky="E")

            if self.current_tablets_var.get():  # check if current tablets checkbox is checked
                # place current tablets scale and label
                add_page.current_tablets_scale.grid(row=7, column=1, padx=10, pady=5, sticky="W")
                add_page.current_tabletlabel.grid(row=7, column=0, padx=10, pady=5, sticky="E")

        elif self.current_tablets_var.get():  # if only current tablets checkbox is checked
            # place current tablets scale and label at row 6
            add_page.current_tablets_scale.grid(row=6, column=1, padx=10, pady=5, sticky="W")
            add_page.current_tabletlabel.grid(row=6, column=0, padx=10, pady=5, sticky="E")

            

    # this function toggles the visibility of the dosage widgets on the addPage
    # it is called when the dosage checkbox is checked or unchecked
    def toggle_dosage(self):
        # access the addPage class using the controller to modify its widgets
        add_page = self.controller.frames["addPage"]
        # if the checkbox is unchecked, hide the dosage widgets
        if not self.dosage_var.get():  # check if the checkbox is unchecked
            add_page.dosage_frame.grid_forget()  # hide the dosage frame
            add_page.dosage_label.grid_forget()  # hide the dosage label
        # this updates the layout so that other widgets adjust their positions accordingly

    # this function toggles the visibility of the tablets/pills to take widgets
    # it is called when the tablets checkbox is checked or unchecked
    def toggle_tablets(self):
        add_page = self.controller.frames["addPage"]
        # if the checkbox is unchecked, hide the tablets widgets
        if not self.tablets_var.get():  # check if the checkbox is unchecked
            add_page.tablets_spinbox.grid_forget()  # hide the tablets spinbox
            add_page.tablets_label.grid_forget()  # hide the tablets label

    # this function toggles the visibility of the current tablets/pills widgets
    # it is called when the current tablets checkbox is checked or unchecked
    def toggle_current_tablets(self):
        add_page = self.controller.frames["addPage"]
        # if the checkbox is unchecked, hide the current tablets widgets
        if not self.current_tablets_var.get():  # check if the checkbox is unchecked
            add_page.current_tablets_scale.grid_forget()  # hide the current tablets scale
            add_page.current_tabletlabel.grid_forget()  # hide the current tablets label

        
    def get_checked_count(self):
        count = 0
        
        #check if dosage checkbox is checked
        if self.dosage_var.get() == 1:
            count += 1
        
        #check if tablets checkbox is checked
        if self.tablets_var.get() == 1:
            count += 1
        
        #check if current tablets checkbox is checked
        if self.current_tablets_var.get() == 1:
            count += 1
        return count

#-------------------------------------------------------------------------------------------------------------------------------- #
#------------------------------------------------ Start of main program --------------------------------------------------------- #
#-------------------------------------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":  #Checks if the script is being run directly
    #Start the notification checking in a separate thread
    threading.Thread(target=notification_thread, daemon=True).start()
    
    root.mainloop()  #Start the Tkinter event loop

    encrypt_files() #updating data in encrypted files
    os.remove('data/dec_user_data.json') #deleting user data json
    os.remove('data/dec_users.csv') #deleting users csv