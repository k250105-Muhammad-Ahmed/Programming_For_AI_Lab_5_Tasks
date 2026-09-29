from pathlib import Path

def InputExperiments():
    ID=int(input("Enter expriment ID:"))
    model_name=input("Enter model name:")
    dataset_name=input("Enter data set name:")
    learning_rate=float(input("Enter learning rate:"))
    epochs=int(input("Enter number of epochs:"))

    with open("experiment.txt","a") as f:
        f.write(f"Experiment ID:{ID}| Model Name:{model_name}| Dataset name:{dataset_name}| Learning name:{learning_rate}| Epochs:{epochs}\n")
        f.close()

def readData(filepath):
    if filepath.exists():
        with open(filepath,"r") as f:
            data=f.read()
            f.close()

    print(data)

def DeleteExperiment(Filepath):
    if Filepath.exists():
        exp_ID=input("Enter id to remove:").strip()
        line_to_remove=f"Experiment ID:{exp_ID}"
        
        lines =Filepath.read_text().splitlines()
        found= any(line.startswith(line_to_remove) for line in lines)
        if not found: 
            print("\nNot found\n")
        else:
            print("\nFound\n")
            updated_lines = [line for line in lines if not line.startswith(line_to_remove)]
            Filepath.write_text("\n".join(updated_lines) + "\n")

def editExpriment(Filepath):
     if Filepath.exists():
        exp_ID=input("Enter id to edit:").strip()
        lines=Filepath.read_text().splitlines()
        line_to_edit=f"Experiment ID:{exp_ID}"
        updated_lines=[]

        for line in lines:
            if line.startswith(line_to_edit):
                ID=int(input("Enter expriment ID:"))
                model_name=input("Enter model name:")
                dataset_name=input("Enter data set name:")
                learning_rate=float(input("Enter learning rate:"))
                epochs=int(input("Enter number of epochs:"))

                Data=f"Experiment ID:{ID}| Model Name:{model_name}| Dataset name:{dataset_name}| Learning name:{learning_rate}| Epochs:{epochs}\n"
                updated_lines.append(Data)
            else:
                updated_lines.append(line)

        Filepath.write_text("\n".join(updated_lines) + "\n")


if __name__ == "__main__":
    path = Path("experiment.txt")
    
    while True:
        print("\n===== EXPERIMENT MANAGER =====")
        print("1. Add Experiment")
        print("2. View All Experiments")
        print("3. Edit Experiment")
        print("4. Delete Experiment")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            InputExperiments()
        elif choice == "2":
            readData(path)
        elif choice == "3":
            editExpriment(path)
            readData(path)  
        elif choice == "4":
            DeleteExperiment(path)
            readData(path)  
        elif choice == "5":
            print("\nExiting program. Goodbye!")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1 and 5.")