import pandas as pd
import random

# List of classes
classes = [
    {"name": "CIST 1400", "description": "INTRODUCTION TO COMPUTER SCIENCE I", "application": "application"},
    {"name": "CSCI 1620", "description": "INTRODUCTION TO COMPUTER SCIENCE II", "application": "application"},
    {"name": "CSCI 2240", "description": "INTRODUCTION TO C PROGRAMMING", "application": "application"},
    {"name": "CIST 2100", "description": "ORGANIZATIONS, APPLICATIONS AND TECHNOLOGY", "application": "THEORY"},
    {"name": "CIST 3110", "description": "INFORMATION TECHNOLOGY ETHICS", "application": "THEORY"},
    {"name": "MATH 1950", "description": "CALCULUS", "application": "THEORY"},
    {"name": "CSCI 2030", "description": "MATHEMATICAL FOUNDATIONS OF COMPUTER SCIENCE", "application": "THEORY"},
    {"name": "CSCI 2040", "description": "INTRODUCTION TO MATHEMATICAL PROOFS", "application": "THEORY"},
    {"name": "MATH 2050", "description": "APPLIED LINEAR ALGEBRA", "application": "THEORY"},
    {"name": "CIST 2500", "description": "INTRODUCTION TO APPLIED STATISTICS FOR IS&T", "application": "THEORY"},
    {"name": "CSCI 3320", "description": "DATA STRUCTURES", "application": "application"},
    {"name": "CSCI 3550", "description": "COMMUNICATION NETWORKS", "application": "application"},
    {"name": "CSCI 3660", "description": "THEORY OF COMPUTATION", "application": "THEORY"},
    {"name": "CSCI 3710", "description": "INTRODUCTION TO DIGITAL DESIGN AND COMPUTER ORGANIZATION", "application": "THEORY"},
    {"name": "CSCI 4100", "description": "INTRODUCTION TO ALGORITHMS", "application": "THEORY"},
    {"name": "CSCI 4220", "description": "PRINCIPLES OF PROGRAMMING LANGUAGES", "application": "THEORY"},
    {"name": "CSCI 4350", "description": "COMPUTER ARCHITECTURE", "application": "application"},
    {"name": "CSCI 4500", "description": "OPERATING SYSTEMS", "application": ""},
    {"name": "CSCI 4830", "description": "INTRODUCTION SOFTWARE ENGINEERING", "application": "application"},
    {"name": "CSCI 4970", "description": "CAPSTONE PROJECT", "application": "application"},
    {"name": "CSCI 4000", "description": "ASSESSMENT", "application": "application"}
]

# data columns
df = pd.DataFrame(columns=["year", "name", "description", "application", "modality", "grade"])

# dictionary to keep track of scheduled classes for each year
scheduled_classes = {year: set() for year in range(2005, 2020)}

# Generate the class schedule a range of years
for year in range(2005, 2020):
    year_data = []
    for _ in range(5):
        # choose a class that is not repeated 
        available_classes = [c for c in classes if c["name"] not in scheduled_classes[year]]
        if not available_classes:
            break  
        class_data = random.choice(available_classes)
        year_class = {
            "year": year,
            "name": class_data["name"],
            "description": class_data["description"],
            "application": class_data["application"],
            "modality": random.choice(["online", "in person"]),
            "grade": random.randint(50, 100)
        }
        year_data.append(year_class)
        # Update the set of scheduled classes for this year
        scheduled_classes[year].add(class_data["name"])
    df = pd.concat([df, pd.DataFrame(year_data)], ignore_index=True)
    # df = pd.concat([df, pd.DataFrame({col: [''] for col in df.columns})], ignore_index=True)

# Save the excel
df.to_excel("class_schedule2.xlsx", index=False, sheet_name="testData")
