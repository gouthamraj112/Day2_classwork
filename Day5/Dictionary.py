employees = {
    101: {"name": "Ravi", "dept": "IT", "salary": 50000},
    102: {"name": "Anu", "dept": "HR", "salary": 45000},
    103: {"name": "John", "dept": "Finance", "salary": 55000}
}

#Add new employee
employees[104] = {"name": "Meena", "dept": "Marketing", "salary": 48000}    

#update employee salary
employees[102]["salary"] = 47000

#Removing employees
employees.pop(103)

#Get All Employee IDs (keys())
print(employees.keys())

#Get All Employee Details (values())
print(employees.values())

#Retrieve Key-Value Pairs (items())
print(employees.items())

#Check Employee Existence
if 101 in employees:
    print("Employee 101 exists")
else:
    print("Employee 101 does not exist")

#Copy Employee Records (copy())
backup = employees.copy()

#Clear Employee Records (clear())
employees.clear()
