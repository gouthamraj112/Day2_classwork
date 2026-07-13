from functools import cmp_to_key
def compare(x, y):
    print("x= ",x, "y= ",y,"b-a= ",y-x)
    return y - x    
nums=[3,1,4,2]
sprted_nums = sorted(nums, key=cmp_to_key(compare))
print("Sorted numbers in descending order:", sprted_nums)