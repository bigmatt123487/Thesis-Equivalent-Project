import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import filedialog  # Added for file dialog
import pandas as pd  

years = []
grades = []
descriptions = []
modality = []  
classtype = []
imported = False
# filters

OnlineClassFil = True 
InPersonClassFil = True 
appFil = True
theoryFil = True

def toggle_online_class():
    global OnlineClassFil
    OnlineClassFil = not OnlineClassFil
    plot_graph()
def toggle_inperson_class():
    global InPersonClassFil
    InPersonClassFil = not InPersonClassFil
    plot_graph()
    
def toggle_app():
    global appFil
    appFil = not appFil
    plot_graph()
def toggle_theory():
    global theoryFil
    theoryFil = not theoryFil
    plot_graph()
    
def update_graph():
    global imported 
    if not imported:
        year = int(year_var.get())
        grade = float(grade_entry.get())
        description = description_entry.get()
        class_mod = class_type_var.get()
        class_type = class_type_var1.get()
    
        if year and grade:
            years.append(year)
            grades.append(grade)
            descriptions.append(description)
            modality.append(class_mod)
            classtype.append(class_type)
            ax.clear()
            plot_graph()
    else:
        plot_graph()

def plot_graph():
        # Separate data points into online and in-person classes
        
        yearsTemp = years.copy()
        gradesTemp = grades.copy()
        descriptionsTemp = descriptions.copy()
        modalityTemp = modality.copy()
        classtypeTemp = classtype.copy()
        
        
        print("temp")
        print(yearsTemp)
        print(gradesTemp)
        print(descriptionsTemp)
        print(modalityTemp)
        print(classtypeTemp)
        if not OnlineClassFil:
            for i in range(len(modalityTemp) - 1, -1, -1):
                if modalityTemp[i] == 1:
                    # Remove the elements at index i from all arrays
                    del yearsTemp[i]
                    del gradesTemp[i]
                    del descriptionsTemp[i]
                    del modalityTemp[i]
                    del classtypeTemp[i]
        if not InPersonClassFil:
            for i in range(len(modalityTemp) - 1, -1, -1):
                if modalityTemp[i] == 0:
                    # Remove the elements at index i from all arrays
                    del yearsTemp[i]
                    del gradesTemp[i]
                    del descriptionsTemp[i]
                    del modalityTemp[i]
                    del classtypeTemp[i]
        if not appFil:
            for i in range(len(classtypeTemp) - 1, -1, -1):
                if classtypeTemp[i] == 1:
                    # Remove the elements at index i from all arrays
                    del yearsTemp[i]
                    del gradesTemp[i]
                    del descriptionsTemp[i]
                    del modalityTemp[i]
                    del classtypeTemp[i]
        if not theoryFil:
            for i in range(len(classtypeTemp) - 1, -1, -1):
                if classtypeTemp[i] == 0:
                    # Remove the elements at index i from all arrays
                    del yearsTemp[i]
                    del gradesTemp[i]
                    del descriptionsTemp[i]
                    del modalityTemp[i]
                    del classtypeTemp[i]

        onlineClass = [yearsTemp[i] for i in range(len(yearsTemp)) if modalityTemp[i] == 1]
        onlineGrade = [gradesTemp[i] for i in range(len(yearsTemp)) if modalityTemp[i] == 1]
        inPerson = [yearsTemp[i] for i in range(len(yearsTemp)) if modalityTemp[i] == 0]
        inPersonGrade = [gradesTemp[i] for i in range(len(yearsTemp)) if modalityTemp[i] == 0]
        print("plot info")
        print(onlineClass)
        print(inPerson)
        # Plot online and in-person classes as orange and blue dots respectively
        ax.clear()
        ax.scatter(onlineClass, onlineGrade, marker='o', s=100, label='Online Class', color='orange')
        ax.scatter(inPerson, inPersonGrade, marker='o', s=100, label='In-Person Class', color='blue')

        # Calculate and plot the best-fit lines based on class modality
        if len(onlineClass) > 1:
            online_coefficients = np.polyfit(onlineClass, onlineGrade, 1)
            online_best_fit_line = np.poly1d(online_coefficients)
            ax.plot(onlineClass, online_best_fit_line(onlineClass), color='orange', linestyle='--', label='Online Class Best Fit')

        if len(inPerson) > 1:
            in_person_coefficients = np.polyfit(inPerson, inPersonGrade, 1)
            in_person_best_fit_line = np.poly1d(in_person_coefficients)
            ax.plot(inPerson, in_person_best_fit_line(inPerson), color='blue', linestyle='--', label='In-Person Class Best Fit')
        
        combYears = yearsTemp
        combGrades = gradesTemp
        if len(combYears) > 1:
            combined_coefficients = np.polyfit(combYears, combGrades, 1)
            combined_best_fit_line = np.poly1d(combined_coefficients)
            ax.plot(combYears, combined_best_fit_line(combYears), color='green', linestyle='--', label='Combined Best Fit')

        # Annotate points with descriptions
        for x, y, desc in zip(yearsTemp, gradesTemp, descriptionsTemp):
            ax.annotate(desc, (x, y), fontsize=12, ha='center', va='bottom')

        ax.set_title("Class Percentage Grades Over the Years")
        ax.set_xlabel("Year")
        ax.set_ylabel("Percentage Grade")
        ax.grid(True)
        ax.legend()

        ax.set_xlim(2005, 2024)
        ax.set_ylim(50, 105)
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

        # Redraw the canvas
        canvas.draw()
    
def import_data():
    global imported  
    imported = True
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        # Read file and grab data
        df = pd.read_excel(file_path)
        years.extend(df['year'].tolist())
        grades.extend(df['grade'].tolist())
        descriptions.extend(df['name'].tolist())
        
        global modality 
        modality.extend(df['modality'].tolist())
        modality = [0 if mode == 'in person' else 1 for mode in modality]
        
        global classtype 
        classtype.extend(df['application'].tolist())
        classtype = [1 if type1 == 'application' else 0 for type1 in classtype]
        update_graph()

# Create the main application window
root = tk.Tk()
root.title("Class Percentage Grades Tracker")
data_frame = ttk.Frame(root)
data_frame.pack(padx=20, pady=20)

# Fields year, grade, and description
ttk.Label(data_frame, text="Year:").grid(row=0, column=0, padx=5, pady=5)
year_var = tk.StringVar()
year_entry = ttk.Entry(data_frame, textvariable=year_var)
year_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(data_frame, text="Grade:").grid(row=1, column=0, padx=5, pady=5)
grade_entries = []
grade_entry = ttk.Entry(data_frame)
grade_entry.grid(row=1, column=1, padx=5, pady=5)
grade_entries.append(grade_entry)

ttk.Label(data_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5)
description_entries = []
description_entry = ttk.Entry(data_frame)
description_entry.grid(row=2, column=1, padx=5, pady=5)
description_entries.append(description_entry)

# Class modality selection
ttk.Label(data_frame, text="Class Modality:").grid(row=3, column=0, padx=5, pady=5)
class_type_var = tk.IntVar()
class_type_var.set(0)  
online_radio = ttk.Radiobutton(data_frame, text="Online", variable=class_type_var, value=1)
online_radio.grid(row=3, column=1, padx=5, pady=5)
in_person_radio = ttk.Radiobutton(data_frame, text="In-Person", variable=class_type_var, value=0)
in_person_radio.grid(row=3, column=2, padx=5, pady=5)

# Academic / Thoery Based
ttk.Label(data_frame, text="Class Type:").grid(row=3, column=0, padx=5, pady=5)
class_type_var1 = tk.IntVar()
class_type_var1.set(0)  
online_radio = ttk.Radiobutton(data_frame, text="Application", variable=class_type_var1, value=1)
online_radio.grid(row=4, column=1, padx=5, pady=5)
in_person_radio = ttk.Radiobutton(data_frame, text="Theory", variable=class_type_var1, value=0)
in_person_radio.grid(row=4, column=2, padx=5, pady=5)

# Create a button to add data and update the graph
add_button = ttk.Button(data_frame, text="Add Data", command=update_graph)
add_button.grid(row=5, columnspan=2, padx=5, pady=10)

import_button = ttk.Button(data_frame, text="Import Data", command=import_data)
import_button.grid(row=7, columnspan=2, padx=5, pady=10)


# Create a frame for displaying the graph
graph_frame = ttk.Frame(root)
graph_frame.pack(padx=20, pady=20)


    
online_checkbox_var = tk.BooleanVar(value=OnlineClassFil)
online_checkbox = ttk.Checkbutton(data_frame, text="Online", variable=online_checkbox_var, command=toggle_online_class)
online_checkbox.grid(row=8, column=1, padx=5, pady=10)

inperson_checkbox_var = tk.BooleanVar(value=InPersonClassFil)
inperson_checkbox = ttk.Checkbutton(data_frame, text="In-Person", variable=inperson_checkbox_var, command=toggle_inperson_class)
inperson_checkbox.grid(row=8, column=2, padx=5, pady=10)

inperson_checkbox_var = tk.BooleanVar(value=InPersonClassFil)
inperson_checkbox = ttk.Checkbutton(data_frame, text="Application", variable=inperson_checkbox_var, command=toggle_app)
inperson_checkbox.grid(row=8, column=3, padx=5, pady=10)

inperson_checkbox_var = tk.BooleanVar(value=InPersonClassFil)
inperson_checkbox = ttk.Checkbutton(data_frame, text="Theory", variable=inperson_checkbox_var, command=toggle_theory)
inperson_checkbox.grid(row=8, column=5, padx=5, pady=10)

inperson_checkbox_var = tk.BooleanVar(value=InPersonClassFil)
inperson_checkbox = ttk.Checkbutton(data_frame, text="Academic Year", variable=inperson_checkbox_var, command=toggle_inperson_class)
inperson_checkbox.grid(row=8, column=6, padx=5, pady=10)

inperson_checkbox_var = tk.BooleanVar(value=InPersonClassFil)
inperson_checkbox = ttk.Checkbutton(data_frame, text="Summer", variable=inperson_checkbox_var, command=toggle_inperson_class)
inperson_checkbox.grid(row=8, column=8, padx=5, pady=10)



# Create a new 2D scatter plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title("Class Percentage Grades Over the Years")
ax.set_xlabel("Year")
ax.set_ylabel("Percentage Grade")
ax.grid(True)
ax.set_xlim(2005, 2024)
ax.set_ylim(50, 105)
# Set the x-axis to display only whole years
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack()
canvas.draw()
root.mainloop()
