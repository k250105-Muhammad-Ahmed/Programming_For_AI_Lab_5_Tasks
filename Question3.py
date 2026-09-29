import json
import os

FILE_NAME="Question3.json"

def addData():
    model_name=input("Enter model name:").strip()
    accuracy=input("Enter the accuracy:").strip()
    precision=input("Enter the precision:").strip()
    recall=input("Enter the recall:").strip()
    f1_score=input("Enter F1-score:").strip()

    data={'model_name':model_name,'accuracy':accuracy,'precision':precision,'recall':recall,'f1_score':f1_score}

    if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
        with open(FILE_NAME,mode='r') as f:
            existing_data=json.load(f)
    else:
        existing_data=[]

    existing_data.append(data)

    with open(FILE_NAME,mode='w',newline='\n') as f:
        json.dump(existing_data,f,indent=4)

def readData():
    if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
        with open(FILE_NAME,mode='r') as f:
            mydata=json.load(f)

        highest_accuracy=0
        highest_F1_score=0
        model_highest_accuracy=None
        model_highest_f1_score=None

        for data in mydata:
            if float(data['accuracy'])>highest_accuracy:
                highest_accuracy=float(data['accuracy'])
                model_highest_accuracy=data

            if float(data['f1_score'])>highest_F1_score:
                highest_F1_score=float(data['f1_score'])
                model_highest_f1_score=data

        print(f"Model with highest accuracy:{model_highest_accuracy}")
        print(f"Model with highest f1 score:{model_highest_f1_score}")        

def editData():
    if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
        target=input("Enter the model name:").strip()

        with open(FILE_NAME,mode='r') as f:
            existing_data=json.load(f)
        found=False

        for data in existing_data:
            if (data['model_name']).lower()==target.lower():
                data['accuracy']=input("Enter accuracy and blank for existing one:").strip() or data['accuracy']
                data['precision']=input("Enter precision and blank for existing one:").strip() or data['precision']
                data['recall']=input("Enter recall and blank for existing one:").strip() or data['recall']                    
                data['f1_score']=input("Enter f1 score and blank for existing one:").strip() or data['f1_score']
                with open(FILE_NAME,mode='w',newline='\n') as f:
                    json.dump(existing_data,f,indent=4)
                found=True
                break

        if not found:
            print(f"No model {target} was in data")

def removeData():
    if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
        target=input("Enter the model name:").strip()
        
        with open(FILE_NAME,mode='r') as f:
            existing_data=json.load(f)
    
        new_data=[]

        for data in existing_data:
            if (data['model_name']).lower()==target.lower():
                continue
            else:
                new_data.append(data)

        with open(FILE_NAME,mode='w',newline='\n') as f:
            json.dump(new_data,f,indent=4)
        


if __name__=="__main__":
   while True:
        print("\n===== DATA MANAGEMENT MENU =====")
        print("1. Add Data")
        print("2. Read Data")
        print("3. Edit Data")
        print("4. Remove Data")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            addData()
        elif choice == '2':
            readData()
        elif choice == '3':
            editData()
        elif choice == '4':
            removeData()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 5.")