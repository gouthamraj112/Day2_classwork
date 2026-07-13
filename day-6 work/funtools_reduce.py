from functools import reduce
numbers = [1, 2, 3, 4]
result = reduce(lambda x, y: x * y, numbers)
print("Product of all numbers:", result)

'''
multiply = lambda x, y: x * y
print(multiply(5, 3))
'''