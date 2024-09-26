import tkinter as tk
from tkinter import ttk

#Function to read text file and return a list of lines
def read_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip()] #defines a line if there is a line 
        if not lines:
            print(f"Warning: The file {filename} is empty or contains only empty lines.")
        return lines
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return []

#Function to handle confirm button click
def confirm_selection():
    selected_item = ""
    if vitamin_combobox != None:
        selected_item = vitamin_combobox.get()
    elif mineral_combobox != None:
        selected_item = mineral_combobox.get()
    
    label_name = label_entry.get("1.0", tk.END).strip()
    dosage = dosage_entry.get().strip()
    
    if selected_item and label_name and dosage:
        #Append to the list or process as needed
        result_list.insert(tk.END, f"{label_name}: {selected_item}, Dosage: {dosage}")
        
        #Clear entry fields
        label_entry.delete("1.0", tk.END)
        label_entry.insert(tk.END, placeholder_text)  #Restore placeholder text
        label_entry.config(fg='gray')  #Set text color to gray
        
        dosage_entry.delete(0, tk.END)
        dosage_entry.insert(0, dosage_placeholder)  #Restore placeholder text
        dosage_entry.config(fg='gray')  #Set text color to gray
    else:
        print("Please select a vitamin or mineral, provide a label, and enter a dosage.")

#Function to handle focus in event for label entry
def on_label_focus_in(event):
    if label_entry.get("1.0", tk.END).strip() == placeholder_text:
        label_entry.delete("1.0", tk.END)
        label_entry.config(fg='black')  #Set text color to black when typing

#Function to handle focus out event for label entry
def on_label_focus_out(event):
    if not label_entry.get("1.0", tk.END).strip():
        label_entry.insert(tk.END, placeholder_text)
        label_entry.config(fg='gray')  #Set text color to gray for placeholder

#Function to handle focus in event for dosage entry
def on_dosage_focus_in(event):
    if dosage_entry.get() == dosage_placeholder:
        dosage_entry.delete(0, tk.END)
        dosage_entry.config(fg='black')  #Set text color to black when typing

#Function to handle focus out event for dosage entry
def on_dosage_focus_out(event):
    if not dosage_entry.get():
        dosage_entry.insert(0, dosage_placeholder)
        dosage_entry.config(fg='gray')  #Set text color to gray for placeholder

#Functions to show and hide comboboxes and entry boxes based on selection
def show_vitamins():
    vitamin_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="W")
    mineral_combobox.grid_forget() #REmove mineral combobox
    label_entry.grid(row=2, column=1, padx=10, pady=5, sticky="W")
    dosage_entry.grid(row=3, column=1, padx=10, pady=5, sticky="W")
    vitamin_label.grid(row=1, column=0, padx=10, pady=5, sticky="E")
    mineral_label.grid_forget()

def show_minerals():
    mineral_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="W")
    vitamin_combobox.grid_forget() #Remove vitamin combobox
    label_entry.grid(row=2, column=1, padx=10, pady=5, sticky="W")
    dosage_entry.grid(row=3, column=1, padx=10, pady=5, sticky="W")
    mineral_label.grid(row=1, column=0, padx=10, pady=5, sticky="E")
    vitamin_label.grid_forget()

#Load data from text files
VITAMINS = read_file('vitamins.txt')
MINERALS = read_file('minerals.txt')

#Initialize the main window
root = tk.Tk()
root.title("Dosage")

#Create and place buttons
vitamin_button = tk.Button(root, text="Select Vitamin", command=show_vitamins)
vitamin_button.grid(row=0, column=0, padx=10, pady=5, sticky="EW")

mineral_button = tk.Button(root, text="Select Mineral", command=show_minerals)
mineral_button.grid(row=0, column=1, padx=10, pady=5, sticky="EW")

#Making grid columns even
root.grid_columnconfigure(0, weight=1, uniform="group1")
root.grid_columnconfigure(1, weight=1, uniform="group1")
root.grid_rowconfigure(0, weight=1)

#Create labels for comboboxes
vitamin_label = tk.Label(root, text="Vitamins")
vitamin_label.grid(row=1, column=0, padx=10, pady=5, sticky="E")

mineral_label = tk.Label(root, text="Minerals")
mineral_label.grid(row=1, column=0, padx=10, pady=5, sticky="E")
mineral_label.grid_forget()  #Hide initially

#Create comboboxes for vitamins and minerals
vitamin_combobox = ttk.Combobox(root, values=VITAMINS)
vitamin_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="W")
vitamin_combobox.grid_forget()  #Hide initially

mineral_combobox = ttk.Combobox(root, values=MINERALS)
mineral_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="W")
mineral_combobox.grid_forget()  #Hide initially

#Placeholder text for label entry
placeholder_text = "Name my supplement"
dosage_placeholder = "Dosage (e.g., 500mg)"

#Create Text widget for labeling the selection with placeholder text
label_entry = tk.Text(root, height=1, width=20, wrap=tk.WORD, fg='gray', font=('Arial', 9, 'italic'))
label_entry.grid(row=2, column=1, padx=10, pady=5, sticky="W")
label_entry.insert(tk.END, placeholder_text)  #Set placeholder text

#Create Entry widget for dosage with placeholder text
dosage_entry = tk.Entry(root, width=20, fg='gray', font=('Arial', 9, 'italic'))
dosage_entry.grid(row=3, column=1, padx=10, pady=5, sticky="W")
dosage_entry.insert(0, dosage_placeholder)  #Set placeholder text

#Bind events to entry widgets
label_entry.bind("<FocusIn>", on_label_focus_in)
label_entry.bind("<FocusOut>", on_label_focus_out)
dosage_entry.bind("<FocusIn>", on_dosage_focus_in)
dosage_entry.bind("<FocusOut>", on_dosage_focus_out)

#Confirm button
confirm_button = tk.Button(root, text="Confirm", command=confirm_selection)
confirm_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

#Listbox to display results
result_list = tk.Listbox(root, height=10)
result_list.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="EW")

#Run the main loop
root.mainloop()
