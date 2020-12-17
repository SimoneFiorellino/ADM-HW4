import numpy as np
#import cupy as np

class HyperLogLog:
    
    def __init__(self, bit_num, size=139000000):
        self.bit_num = bit_num
        self.m = 2 ** self.bit_num   #num of buckets
        self.cost = 0.7213/(1+ 1.079/self.m)
        #self.two_pow = [ 2 ** i for i in range(0, self.bit_num) ]
        self.size = size
        self.p_num = 286687811
        #self.coefficent = [47, 180, 3, 278, 36, 9, 235, 62] #previously selected coefficients
        self.coefficent = [47, 181, 3, 281, 37, 13, 239, 67]

# hash functions
    def hash8(self, string):
        #splits string in 8 chucks and conversion in integer
        splits = np.array([int(string[start:start+4], 16) for start in range(0,32,4)], dtype=int)
        y = sum(splits*self.coefficent)  # dot product of vector of chucks with vector of random coefficents.
        return (y%self.p_num) #compute y modN

# number of bucket j
    def buck_num(self, n):
        # the binary address determined by the first num_bits bits of n. 
        # n.b. we are considering num_bits + 1 to avoid the i range [15,31]
        n = n >> (int(np.log2(n)+1) - (self.bit_num + 1))
        n = n & 31
        return n

# number of consecutive zeros
# ******10101010  left to right
    def zeros_count(self, n):
        len_n = int(np.log2(n)+1) - (self.bit_num + 1)
        y = n & ((2 ** len_n) - 1)
        if y == 0:
            return len_n
        len_y = int(np.log2(y)+1)
        return (len_n - len_y + 1)

# my cardinalities
    def my_armonic_mean(self, my_Rj):
        sum = 0
        for i in my_Rj:
            sum += 1 / (2 ** (i))
        return (1/sum) * self.m

    def my_average(self, my_Rj):
        return (1/self.m)*(np.sum(my_Rj))

    def my_max(self, my_Rj):
        return max(my_Rj)

# main function to fill the buckets
    def fill_the_buckets(self):
        #values
        my_buckets = [ 0 for i in range(self.m) ] #set the array with m zeros

        #open the file
        fh = open('hash.txt')
        count = 1
        #read every line
        for line in fh:
            try:
                my_num = self.hash8(line.strip())
                num_bucket = self.buck_num(my_num)
                num_zeros = self.zeros_count(my_num)
                if my_buckets[num_bucket] < num_zeros:
                    my_buckets[num_bucket]=num_zeros
            except:
                print(line.strip())
                continue
         
            if count == self.size:
                break
            count+=1
        fh.close()
        return my_buckets

    def fill_the_buckets_(self):
        #values
        my_buckets = [ 0 for i in range(self.m) ] #set the array with m zeros

        #open the file
        fh = open('hash.txt')
        #read every line
        for line in fh:
            try:
                my_num = self.hash8(line.strip())
                num_bucket = self.buck_num(my_num)
                num_zeros = self.zeros_count(my_num)
                if my_buckets[num_bucket] < num_zeros:
                    my_buckets[num_bucket]=num_zeros
            except:
                print(line.strip())
                continue

        fh.close()
        return my_buckets

    def HLL(self, buckets):
        return int(self.cost * self.m * self.my_armonic_mean(buckets))

    def LL(self, buckets):
        return int(self.cost * self.m * (2 ** self.my_average(buckets)))

    #2.8
    # def error_ll(self, my_ll):
    #     e = self.size / 100 * 2.8
    #     my_range = [int(my_ll-e), int(my_ll+e)]
    #     return my_range

    # def error_hll(self, my_hll):
    #     #sigma = 1.04 / np.sqrt(self.m)
    #     e = self.size / 100 * 18.4
    #     print(e)
    #     my_range = [int(my_hll-e), int(my_hll+e)]
    #     return my_range
    
    def find_no_zero(self, my_bucks):
        summation = 0
        for i in my_bucks:
            if i == 0:
                summation += 0
        return summation

    def get_cardinality_correction(self, my_hll, my_buckets):
        if my_hll <= (self.bit_num / 2) * self.m:
            V = self.find_no_zero(my_buckets)
            if V != 0:
                my_new_hll = self.m * np.log(self.m / V)
            else:
                my_new_hll = my_hll
        elif my_hll <= (1 / 30) * (2 ** self.m):
            my_new_hll = my_hll
        else:
            my_new_hll = -(2 ** self.m) *  np.log(1 - (my_hll / (2 ** self.m)))
        
        return my_new_hll


    def get_cardinality(self):
        buckets = self.fill_the_buckets()
        ll = self.LL(buckets)
        hll = self.HLL(buckets)
        hll = self.get_cardinality_correction(hll, buckets)
        return f'll: {ll}\nhll: {hll}'