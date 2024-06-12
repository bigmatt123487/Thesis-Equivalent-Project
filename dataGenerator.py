import pandas as pd
import random



onlineDiff = False
onlineDelta = 6

inpersonDiff = True
inpersonDelta = 8

applicationDiff = False
applicationDelta = 5  #value between -10 and 8

theoryDiff = False
theoryDelta = -10

increasing = True
factor = -0.01 # use value between -0.1 and 0.15
factorshift = -0.03





# List of classes
classes = [
    {"name": "CIST 1400", "description": "INTRODUCTION TO COMPUTER SCIENCE I", "application": "application"},
    {"name": "CSCI 1620", "description": "INTRODUCTION TO COMPUTER SCIENCE II", "application": "application"},
    {"name": "CSCI 2240", "description": "INTRODUCTION TO C PROGRAMMING", "application": "application"},
    {"name": "CIST 2100", "description": "ORGANIZATIONS, APPLICATIONS AND TECHNOLOGY", "application": "theory"},
    {"name": "CIST 3110", "description": "INFORMATION TECHNOLOGY ETHICS", "application": "theory"},
    {"name": "MATH 1950", "description": "CALCULUS", "application": "theory"},
    {"name": "CSCI 2030", "description": "MATHEMATICAL FOUNDATIONS OF COMPUTER SCIENCE", "application": "theory"},
    {"name": "CSCI 2040", "description": "INTRODUCTION TO MATHEMATICAL PROOFS", "application": "theory"},
    {"name": "MATH 2050", "description": "APPLIED LINEAR ALGEBRA", "application": "theory"},
    {"name": "CIST 2500", "description": "INTRODUCTION TO APPLIED STATISTICS FOR IS&T", "application": "theory"},
    {"name": "CSCI 3320", "description": "DATA STRUCTURES", "application": "application"},
    {"name": "CSCI 3550", "description": "COMMUNICATION NETWORKS", "application": "application"},
    {"name": "CSCI 3660", "description": "THEORY OF COMPUTATION", "application": "theory"},
    {"name": "CSCI 3710", "description": "INTRODUCTION TO DIGITAL DESIGN AND COMPUTER ORGANIZATION", "application": "theory"},
    {"name": "CSCI 4100", "description": "INTRODUCTION TO ALGORITHMS", "application": "theory"},
    {"name": "CSCI 4220", "description": "PRINCIPLES OF PROGRAMMING LANGUAGES", "application": "theory"},
    {"name": "CSCI 4350", "description": "COMPUTER ARCHITECTURE", "application": "application"},
    {"name": "CSCI 4500", "description": "OPERATING SYSTEMS", "application": ""},
    {"name": "CSCI 4830", "description": "INTRODUCTION SOFTWARE ENGINEERING", "application": "application"},
    {"name": "CSCI 4970", "description": "CAPSTONE PROJECT", "application": "application"},
    {"name": "CSCI 4000", "description": "ASSESSMENT", "application": "application"},
    
    {"name": "CSCI 3000", "description": "elective", "application": "application"},
    {"name": "CSCI 3010", "description": "elective", "application": "theory"},
    {"name": "CSCI 3100", "description": "Ielective", "application": "theory"},
    {"name": "CSCI 3900", "description": "elective", "application": "theory"},
    {"name": "CSCI 3800", "description": "elective", "application": "theory"},
    {"name": "CSCI 3400", "description": "elective", "application": "application"},
    {"name": "CSCI 3610", "description": "elective", "application": "theory"},
    {"name": "CSCI 4050", "description": "elective", "application": "application"},
    {"name": "CSCI 4110", "description": "elective", "application": "application"},
    {"name": "CSCI 4660", "description": "elective", "application": "application"},
    
    {"name": "CSCI 2050", "description": "elective", "application": "application"},
    {"name": "CSCI 2090", "description": "elective", "application": "theory"},
    {"name": "CSCI 2110", "description": "Ielective", "application": "theory"},
    {"name": "CSCI 2550", "description": "elective", "application": "theory"},
    {"name": "CSCI 2600", "description": "elective", "application": "theory"},
    {"name": "CSCI 2900", "description": "elective", "application": "application"},
    {"name": "CSCI 2260", "description": "elective", "application": "theory"},
    {"name": "CSCI 4310", "description": "elective", "application": "application"},
    {"name": "CSCI 4390", "description": "elective", "application": "application"},
    {"name": "MATH 4660", "description": "elective", "application": "application"}
]

df = pd.DataFrame(columns=["year", "name", "description", "application", "modality", "grade"])

# dictionary to keep track of scheduled classes for each year
scheduled_classes = {year: set() for year in range(2005, 2020)}

# Generate the class schedule a range of years
for year in range(2006, 2019):
    year_data = []
    for _ in range(20):
        # choose a class
        available_classes = [c for c in classes if c["name"] not in scheduled_classes[year]]
        if not available_classes:
            break  
        class_data = random.choice(available_classes)
        modality = random.choice(["online", "in person"])
        application = class_data["application"]
        grade = 82 
        
        

        normalDis = random.normalvariate(0, 2)*4
        grade = grade + normalDis
        if onlineDiff and modality == "online":
           grade = grade + random.uniform(0.3, 1) * onlineDelta 
        elif inpersonDiff and modality == "in person":
            grade = grade + random.uniform(0.3, 1) * inpersonDelta
        if applicationDiff and application == 'application':
           grade = grade + random.uniform(0.3, 1)* onlineDelta
        elif theoryDiff and application == 'theory':
           grade = grade + random.uniform(0.3, 1) * theoryDelta  
        if increasing:
            grade = grade + random.random() * factor
            factor = factor + factorshift
        
            
        if grade > 100:
            grade = 100
        year_class = {
            "year": year,
            "name": class_data["name"],
            "description": class_data["description"],
            "application": class_data["application"],
            "modality": modality,
            "grade": grade
        }
        year_data.append(year_class)
        # Update the set of scheduled classes for this year
        scheduled_classes[year].add(class_data["name"])
    df = pd.concat([df, pd.DataFrame(year_data)], ignore_index=True)

# Save the excel
df.to_excel("onlineExample.xlsx", index=False, sheet_name="testData")
