import numpy as np

# Write a function that takes as input a list of numbers, and returns
# the list of values given by the softmax function.
def softmax(L):
    result = []
    divisor = sum(np.exp(L))
    for element in range(len(L)):
        result.append(np.exp(L[element-1])/divisor)
    return result


if __name__ == '__main__':
    test_list = [1,23,45,8]
    test_result = softmax(test_list)
