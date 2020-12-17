#Libraries
import numpy as np
#import cupy as np
import q1_functions as q1 #here we are working with strings bin(line)[2:]
import q1_2_functions as q1_2 #here we are working with numbers
# cardinality = 139000000
# cardinality = 15290346 <-- HLL with q1_2_functions

# my_hll = q1.HyperLogLog(5, 10000)
# print(my_hll.get_cardinality())

my_hll = q1_2.HyperLogLog(5, 10000)
print(my_hll.get_cardinality())
#print(my_hll.error_hll(15290346))

# string = '9e0b082181c2324467cb3a7a28bdf416'
# n = my_hll.hash8(string)
# print(bin(n))
# print(my_hll.buck_num(n))
# print(my_hll.zeros_count(n))


# try:
#     num_bucket = my_hll.buck_num(n)
#     print(num_bucket)
# except:
#     pass


# try:
#     num_zeros = my_hll.zeros_count(n)
#     print(num_zeros)
# except:
#     pass