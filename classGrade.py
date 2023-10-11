import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

years = []
grades = []
descriptions = []
modality = []  

# Function to update the graph and best-fit line
def update_graph():
    year = int(year_var.get())
    grade = float(grade_entry.get())
    description = description_entry.get()
    class_type = class_type_var.get()

    if year and grade:
        years.append(year)
        grades.append(grade)
        descriptions.append(description)
        modality.append(class_type)
        ax.clear()

        # Separate data points into online and in-person classes
        onlineClass = [years[i] for i in range(len(years)) if modality[i] == 1]
        onlineGrade = [grades[i] for i in range(len(years)) if modality[i] == 1]
        inPerson = [years[i] for i in range(len(years)) if modality[i] == 0]
        inPersonGrade = [grades[i] for i in range(len(years)) if modality[i] == 0]

        # Plot online and in-person classes as orange and blue dots respectively
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
        
        combYears = years
        combGrades = grades
        if len(combYears) > 1:
            combined_coefficients = np.polyfit(combYears, combGrades, 1)
            combined_best_fit_line = np.poly1d(combined_coefficients)
            ax.plot(combYears, combined_best_fit_line(combYears), color='green', linestyle='--', label='Combined Best Fit')

        # Annotate points with descriptions
        for x, y, desc in zip(years, grades, descriptions):
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
    print(years)
    print(descriptions)
    print(grades)
    print(modality)

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
ttk.Label(data_frame, text="Class Type:").grid(row=3, column=0, padx=5, pady=5)
class_type_var = tk.IntVar()
class_type_var.set(0)  
online_radio = ttk.Radiobutton(data_frame, text="Online", variable=class_type_var, value=1)
online_radio.grid(row=3, column=1, padx=5, pady=5)
in_person_radio = ttk.Radiobutton(data_frame, text="In-Person", variable=class_type_var, value=0)
in_person_radio.grid(row=3, column=2, padx=5, pady=5)

# Create a button to add data and update the graph
add_button = ttk.Button(data_frame, text="Add Data", command=update_graph)
add_button.grid(row=4, columnspan=2, padx=5, pady=10)

# Create a frame for displaying the graph
graph_frame = ttk.Frame(root)
graph_frame.pack(padx=20, pady=20)

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
