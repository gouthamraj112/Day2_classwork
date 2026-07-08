input="employees.txt"

output="payroll_report.txt"

echo "===============PAYROLL REPORT===============" > $output

printf "%-5s %-10s %-10s %-10s %-10s %-12s\n"\

        "ID" "Name" "Salary" "Tax" "Bonus" "NetSalary" >> $output

echo "--------------------------------------------" >> $output

while read id name salary

do

        if [[ $salary -le 30000 ]]
        then
                tax=$((salary * 5/100))
        elif [[ $salary -le 60000 ]]
        then
                tax=$((salary * 10/100))
        else
                tax=$((salary * 15/100))
        fi

        #Bonus calculation
        if [[ $salary -le 50000 ]]
        then
                bonus=2000
        else
                bonus=5000
        fi

        #NEt Salary
        net=$((salary + bonus - tax))
        printf "%-5s %-10s %-10s %-10s %-10s %-12s\n"\
                "$id" "$name" "$salary" "$tax" "$bonus" "$net" >> $output

done < $input
echo "Payroll report generated successfully."
 
