#!/bin/bash

FILE="attendance.txt"

###########################################
# Display all employees
###########################################
display_records() {

    echo "=========== Employee Records ==========="

    cat "$FILE"

}

###########################################
# Search Employee
###########################################
search_employee() {

    echo "Enter Employee Name:"
    read name

    if grep -i "$name" "$FILE"
    then
        echo "Employee Found"
    else
        echo "Employee Not Found"
    fi

}

###########################################
# Count Absent Employees
###########################################
count_absent() {

    count=$(grep -c "Absent" "$FILE")

    echo "Absent Employees : $count"

}

###########################################
# Replace Absent with Present
###########################################
update_attendance() {

    echo "Enter Employee ID:"
    read id

    sed -i "/^$id,/ s/Absent/Present/" "$FILE"

    echo "Attendance Updated Successfully"

}

###########################################
# Total Salary of Present Employees
###########################################
calculate_salary() {

    total=$(awk -F',' '$4=="Present" {sum+=$5} END {print sum}' "$FILE")

    echo "Total Salary Paid : Rs.$total"

}

###########################################
# Display Department Employees
###########################################
department_records() {

    echo "Enter Department:"
    read dept

    awk -F',' -v dep="$dept" '

    BEGIN{
        print "Employees in Department:",dep
    }

    $3==dep{
        print $0
    }

    ' "$FILE"

}

###########################################
# Highest Salary Employee
###########################################
highest_salary() {

    awk -F',' '

    BEGIN{
        max=0
    }

    {
        if($5>max)
        {
            max=$5
            emp=$2
        }
    }

    END{
        print "Highest Salary Employee :",emp
        print "Salary :",max
    }

    ' "$FILE"

}

###########################################
# Menu
###########################################

while true
do

echo
echo "====================================="
echo " Employee Attendance Management"
echo "====================================="
echo "1.Display Records"
echo "2.Search Employee"
echo "3.Count Absent Employees"
echo "4.Update Attendance"
echo "5.Total Salary of Present Employees"
echo "6.Department Employees"
echo "7.Highest Salary"
echo "8.Exit"

echo "Enter Choice:"
read choice

case $choice in

1)
display_records
;;

2)
search_employee
;;

3)
count_absent
;;

4)
update_attendance
;;

5)
calculate_salary
;;

6)
department_records
;;

7)
highest_salary
;;

8)
echo "Thank You"
break
;;

*)
echo "Invalid Choice"

esac

done
