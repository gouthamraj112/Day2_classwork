def add(a, b):
    return a + b

def subtract(a, b):
    return a - b                

def multiply(a, b): 
    return a * b        

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def main():
    print("Select a function to perform: add, subtract, multiply, divide")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))

    if choice == '1':
        result = add(num1, num2)
        print(f"The result of addition is: {result}")   

    elif choice == '2':
        result = subtract(num1, num2)
        print(f"The result of subtraction is: {result}")        

    elif choice == '3':
        result = multiply(num1, num2)
        print(f"The result of multiplication is: {result}") 

    elif choice == '4':
        try:
            result = divide(num1, num2)
            print(f"The result of division is: {result}") 
        except ValueError as e:
            print(e)

    elif choice == '5':
        print("Exiting the calculator. Goodbye!")
        return      
    
if __name__ == "__main__":
    main()  

    
