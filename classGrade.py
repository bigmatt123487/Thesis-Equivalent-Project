import tkinter as tk
from tkinter import ttk
from tkinter import filedialog  
import warnings
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd  
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error



warnings.filterwarnings("ignore", message="X does not have valid feature names")
years = []
grades = []
descriptions = []
modality = []  
classtype = []
imported = False

OnlineClassFil = True 
InPersonClassFil = True 
appFil = True
theoryFil = True
linearReg = False
nameToggle = True
randomForestToggle =  False
multiRegress = False

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

def toggle_regress():
    global linearReg
    linearReg = not linearReg
    plot_graph()

def toggle_name():
    global nameToggle
    nameToggle = not nameToggle
    plot_graph()

def toggle_randomForest():
    global randomForestToggle
    randomForestToggle = not randomForestToggle
    plot_graph()
    
def toggle_multiRegress():
    global multiRegress
    multiRegress = not multiRegress
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
            chart.clear()
            plot_graph()
    else:
        plot_graph()

def plot_graph():
        # Separate data points into online and in-person classes
        yearsTemp = years.copy()
        gradesTemp = grades.copy()
        descriptionsTemp = descriptions.copy()
        descriptionsGradeTemp = grades.copy()
        modalityTemp = modality.copy()
        classtypeTemp = classtype.copy()
        
        # sort data based on year asc
        tuple = list(zip(yearsTemp, gradesTemp, descriptionsTemp, descriptionsGradeTemp, modalityTemp, classtypeTemp))
        sort = sorted(tuple, key=lambda x: x[0])
        yearsTemp = [pair[0] for pair in sort]
        gradesTemp = [pair[1] for pair in sort]
        descriptionsTemp = [pair[2] for pair in sort]
        descriptionsGradeTemp = [pair[3] for pair in sort]
        modalityTemp = [pair[4] for pair in sort]
        classtypeTemp = [pair[5] for pair in sort]
        
        # remove online classes
        if not OnlineClassFil:
            for i in range(len(modalityTemp) - 1, -1, -1):
                if modalityTemp[i] == 1:
                    del yearsTemp[i]
                    del gradesTemp[i]
                    del descriptionsTemp[i]
                    del descriptionsGradeTemp[i]
                    del modalityTemp[i]
                    del classtypeTemp[i]
        # remove inperson classes
        if not InPersonClassFil:
            for i in range(len(modalityTemp) - 1, -1, -1):
                if modalityTemp[i] == 0:
                    del yearsTemp[i]
                    del gradesTemp[i]
                    del descriptionsTemp[i]
                    del descriptionsGradeTemp[i]
                    del modalityTemp[i]
                    del classtypeTemp[i]
        # remove application type
        if not appFil:
            for i in range(len(classtypeTemp) - 1, -1, -1):
                if classtypeTemp[i] == 1:
                    del yearsTemp[i]
                    del gradesTemp[i]
                    del descriptionsTemp[i]
                    del descriptionsGradeTemp[i]
                    del modalityTemp[i]
                    del classtypeTemp[i]
         # remove theory type
        if not theoryFil:
            for i in range(len(classtypeTemp) - 1, -1, -1):
                if classtypeTemp[i] == 0:
                    del yearsTemp[i]
                    del gradesTemp[i]
                    del descriptionsTemp[i]
                    del descriptionsGradeTemp[i]
                    del modalityTemp[i]
                    del classtypeTemp[i]
        
        
        chart.clear()
        # performs linear regressor
        if linearReg and len(gradesTemp) > 0:
            
            dates = np.array(yearsTemp)
            grade = np.array(gradesTemp)

            X = dates.reshape(-1, 1)
            model = LinearRegression()
            model.fit(X, grade)
            predicted_grade = model.predict(X)

            # Calculate RMSE
            rmse = round(np.sqrt(mean_squared_error(grade, predicted_grade)), 3)
            # Predict grades for the next 5 years
            greatDate = dates[len(dates) - 1]
            next_years = np.array([greatDate  + 1, greatDate  + 2 , greatDate  + 3, greatDate+ 4, greatDate + 5]).reshape(-1, 1)
            predicted_grades = model.predict(next_years)
            textValue = "Best-Fit : RMSE = "+str(rmse)
            
            for i in range(len(predicted_grades)):
                if predicted_grades[i] > 100:
                    predicted_grades[i] = 100
            chart.scatter(next_years, predicted_grades, marker='o', s=100, label=textValue, color='red')
            chart.scatter(yearsTemp, gradesTemp, marker='o', s=100, color='blue')
            for x, y, predicted_grades in zip(next_years, predicted_grades, predicted_grades):
                chart.annotate(str(round(predicted_grades, 1)), (x, y), fontsize=10, ha='center', va='bottom')
            if len(yearsTemp) > 1:
                classesBestFit = np.polyfit(yearsTemp, gradesTemp, 1)
                bestFitLine = np.poly1d(classesBestFit)
                chart.plot(yearsTemp, bestFitLine(yearsTemp), color='red', linestyle='--')
                

        # performs random forest regressor   
        if randomForestToggle:
            if OnlineClassFil and InPersonClassFil or appFil and theoryFil:
                chart.scatter([], [], marker='o', s=100, label="Random Forest: Select only 1 modality and type field", color='orange')
                
            elif (OnlineClassFil or InPersonClassFil) and (appFil or theoryFil):      
                X = list(zip(years, modality, classtype))
                y = grades

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # Train the model
                randomFRegressor = RandomForestRegressor(n_estimators=50, random_state=1)
                randomFRegressor.fit(X_train, y_train)

                # Make predictions on the test set
                predicted_grades = randomFRegressor.predict(X_test)
                
                rmse = round(np.sqrt(mean_squared_error(y_test, predicted_grades)), 3)

                future_years = np.array([max(years)+1])  
                
                
                mode = 0
                type = 0
                if appFil:
                    type = 1
                if OnlineClassFil:
                    mode = 1
                predicted_grades = randomFRegressor.predict([[max(grades)+1, mode, type]])


                for i in range(len(predicted_grades)):
                    if predicted_grades[i] > 100:
                        predicted_grades[i] = 100
                textValue = "Random Forest: MAE ="+str(round(rmse,2))        
                chart.scatter(future_years, predicted_grades, marker='o', s=100, label=textValue, color='orange')
                for x, y, predicted_grades in zip(future_years, predicted_grades, predicted_grades):
                    chart.annotate(str(round(predicted_grades,1)), (x, y), fontsize=10, ha='center', va='bottom')
                    
        # performs linear regression with features[]
        if multiRegress:
            if OnlineClassFil and InPersonClassFil or appFil and theoryFil:
                chart.scatter([], [], marker='o', s=100, label="Multi-Regression: Select only 1 modality and type field", color='green')
                
            elif (OnlineClassFil or InPersonClassFil) and (appFil or theoryFil):
                data = pd.DataFrame({'grades': grades, 'year': years, 'modality': modality, 'classtype': classtype})
                X = data[['year', 'modality', 'classtype']]  
                y = data['grades']  
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
                model = LinearRegression()
                model.fit(X_train, y_train)

                mode = 0
                type = 0
                if appFil:
                    type = 1
                if OnlineClassFil:
                    mode = 1
                next_years = np.array([[max(years) + 1, mode, type], [max(years) + 2, mode, type], [max(years) + 3, mode, type], [max(years) + 4, mode, type], [max(years) + 5, mode, type]])
                predictions = model.predict(next_years)
                ypredicted = model.predict(X_test)
                rmse = np.sqrt(mean_squared_error(y_test, ypredicted))
                textValue = "Multi-Regression: RMSE = "+str(round(rmse,2))
                next_years1 = [max(years) + 1, max(years) + 2,max(years) + 3,max(years) + 4,max(years) + 5]
                for i in range(len(predictions)):
                    if predictions[i] > 100:
                        predictions[i] = 100
                chart.scatter(next_years1, predictions, marker='o', s=100, label=textValue, color='green')
                for x, y, prediction in zip(next_years1, predictions, predictions):
                    chart.annotate(str(round(prediction,1)), (x, y), fontsize=10, ha='center', va='bottom')
                            
    # Redraw the gradeGraph  
        chart.scatter(yearsTemp, gradesTemp, marker='o', s=100, label='Class Grade', color='blue')

        if nameToggle:
            for x, y, desc in zip(yearsTemp, gradesTemp, descriptionsTemp):
                chart.annotate(desc, (x, y), fontsize=10, ha='center', va='bottom')
        else: 
            for x, y, desc in zip(yearsTemp, gradesTemp,[]):
                chart.annotate(desc, (x, y), fontsize=10, ha='center', va='bottom')   

        chart.set_title("Class Percentage Grades Over the Years")
        chart.set_xlabel("Year")
        chart.set_ylabel("Percentage Grade")
        chart.grid(True)
        chart.legend()

        chart.set_xlim(min(years)-2, max(years)+7)
        chart.set_ylim(50, 105)
        chart.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        gradeGraph.draw()
 
#clears current data 
def import_data():
    global years 
    global grades 
    global descriptions 
    global modality   
    global classtype   
    years = []
    grades = []
    descriptions = []
    modality = []
    classtype = []
    import_data1()

# import the data    
def import_data1():
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
root.title("Class Grade Visualization Tool")
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
ttk.Label(data_frame, text="Class Type:").grid(row=4, column=0, padx=5, pady=5)
class_type_var1 = tk.IntVar()
class_type_var1.set(0)  
online_radio = ttk.Radiobutton(data_frame, text="Application", variable=class_type_var1, value=1)
online_radio.grid(row=4, column=1, padx=5, pady=5)
in_person_radio = ttk.Radiobutton(data_frame, text="Theory", variable=class_type_var1, value=0)
in_person_radio.grid(row=4, column=2, padx=5, pady=5)

# Create a button to add data and import data
add_button = ttk.Button(data_frame, text="Add Data", command=update_graph)
add_button.grid(row=5, columnspan=2, padx=5, pady=10)

import_button = ttk.Button(data_frame, text="Import Data", command=import_data)
import_button.grid(row=7, columnspan=2, padx=5, pady=10)


# GUI
graph_frame = ttk.Frame(root)
graph_frame.pack(padx=20, pady=20)

# feature fiilters
online_checkbox_var = tk.BooleanVar(value=OnlineClassFil)
online_checkbox = ttk.Checkbutton(data_frame, text="Online", variable=online_checkbox_var, command=toggle_online_class)
online_checkbox.grid(row=8, column=1, padx=5, pady=10)

inperson_checkbox_var = tk.BooleanVar(value=InPersonClassFil)
inperson_checkbox = ttk.Checkbutton(data_frame, text="In-Person", variable=inperson_checkbox_var, command=toggle_inperson_class)
inperson_checkbox.grid(row=8, column=2, padx=5, pady=10)

application_checkbox_var = tk.BooleanVar(value=appFil)
application_checkbox = ttk.Checkbutton(data_frame, text="Application", variable=application_checkbox_var, command=toggle_app)
application_checkbox.grid(row=8, column=3, padx=5, pady=10)

theory_checkbox_var = tk.BooleanVar(value=theoryFil)
theory_checkbox = ttk.Checkbutton(data_frame, text="Theory", variable=theory_checkbox_var, command=toggle_theory)
theory_checkbox.grid(row=8, column=5, padx=5, pady=10)


name_checkbox_var = tk.BooleanVar(value=nameToggle)
name_checkbox = ttk.Checkbutton(data_frame, text="Name / Grade", variable=name_checkbox_var, command=toggle_name)
name_checkbox.grid(row=8, column=7, padx=5, pady=10)

# predicitive models checkboxes 
linearReg_var = tk.BooleanVar(value=linearReg)
linearReg_checkbox = ttk.Checkbutton(data_frame, text="Best-Fit", variable=linearReg_var, command=toggle_regress)
linearReg_checkbox.grid(row=9, column=1, padx=5, pady=10)


randomForest_checkbox_var = tk.BooleanVar(value=randomForestToggle)
randomForest_checkbox = ttk.Checkbutton(data_frame, text="Random Forest", variable=randomForest_checkbox_var, command=toggle_randomForest)
randomForest_checkbox.grid(row=9, column=3, padx=5, pady=10)

multiReg_var = tk.BooleanVar(value=multiRegress)
multiReg_checkbox = ttk.Checkbutton(data_frame, text="Multi-Regression", variable=multiReg_var, command=toggle_multiRegress)
multiReg_checkbox.grid(row=9, column=2, padx=5, pady=10)

# Create a new 2D scatter plot
fig, chart = plt.subplots(figsize=(8, 6))
chart.set_title("Class Percentage Grades Over the Years")
chart.set_xlabel("Year")
chart.set_ylabel("Percentage Grade")
chart.grid(True)
chart.set_xlim(2002, 2028)
chart.set_ylim(50, 105)
chart.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

gradeGraph = FigureCanvasTkAgg(fig, master=graph_frame)
gradeGraph.get_tk_widget().pack()
gradeGraph.draw()
root.mainloop()