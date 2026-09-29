import csv
import os

FILE_NAME="Data_Patients.csv"
HEADER=["ID","Age","BMI","Blood Pressure","Glucose level","Diabetes Prediction Level"]

def addRecord():
    ID=input("Enter the ID:").strip()
    age=input("Enter age: ").strip()
    BMI=input("Enter BMI:").strip()
    blood_pressure=input("Enter blood pressure:").strip()
    glucose_level=input("Enter glucose level:").strip()
    diabetes_prediction_label=input("Enter diabetes prediction label(1 or 0):").strip()

    file_exist=os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME)>0

    row_data = {
        "ID": ID,
        "Age": age,
        "BMI": BMI,
        "Blood Pressure": blood_pressure,
        "Glucose level": glucose_level,
        "Diabetes Prediction Level": diabetes_prediction_label
    }

    with open(FILE_NAME,'a',newline='') as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        if not file_exist:
            writer.writeheader()

        writer.writerow(row_data)

def readRecords():
    file_exist=os.path.exists(FILE_NAME)
    data_list=[]
    if file_exist:
        with open(FILE_NAME, mode='r',newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data_list.append(row)
    
    positive=0
    negative=0
    count=0
    sum_BMI=0
    sum_glucose=0
    threshold=float(input("Enter threshold of glucose:"))
    for data in data_list:
        count+=1
        if int(data['Diabetes Prediction Level'])==1:
            positive+=1
        else:
            negative+=1

        if float(data["Glucose level"])>threshold:
            print(f"The patient above {threshold}:{data}")

        sum_glucose+=float(data["Glucose level"])
        sum_BMI+=float(data["BMI"])

    print(f"Total patients:{count}")
    print(f"Total positive patient:{positive}")
    print(f"Total negative patient:{negative}")
    print(f"Average glucose:{sum_glucose/count}")
    print(f"Average BMI:{sum_BMI/count}")

def editRecord():
    target = input("Enter ID to edit: ").strip()
    if not os.path.exists(FILE_NAME):
        print("No records file found.")
        return

    rows = []
    updated = False
    with open(FILE_NAME, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == target:
                print(f"Current data: {row}")
                print("Enter new values (leave blank to keep current):")
                
                age = input(f"Enter age [{row['Age']}]: ").strip() or row['Age']
                BMI = input(f"Enter BMI [{row['BMI']}]: ").strip() or row['BMI']
                bp = input(f"Enter blood pressure [{row['Blood Pressure']}]: ").strip() or row['Blood Pressure']
                glucose = input(f"Enter glucose level [{row['Glucose level']}]: ").strip() or row['Glucose level']
                label = input(f"Enter diabetes prediction label (1 or 0) [{row['Diabetes Prediction Level']}]: ").strip() or row['Diabetes Prediction Level']
                
                row["Age"] = age
                row["BMI"] = BMI
                row["Blood Pressure"] = bp
                row["Glucose level"] = glucose
                row["Diabetes Prediction Level"] = label
                updated = True
            rows.append(row)
            
    if updated:
        with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADER)
            writer.writeheader()
            writer.writerows(rows)
    else:
        print("ID not found.")



if __name__=="__main__":
    while True:
        print("\n==============================")
        print("  PATIENT DATABASE SYSTEM   ")
        print("==============================")
        print("1. Add New Record")
        print("2. Read and Analyze Records")
        print("3. Edit Existing Record")
        print("4. Exit System")
        print("==============================")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            addRecord()
        elif choice == '2':
            readRecords()
        elif choice == '3':
            editRecord()
        elif choice == '4':
            print("\nExiting program. Goodbye!")
            break
        else:
            print("Invalid input! Please choose a number between 1 and 4.")