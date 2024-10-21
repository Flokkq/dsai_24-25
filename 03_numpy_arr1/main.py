import numpy as np

np.random.seed(0)

array1 = np.random.randint(1, 101, 50)
print("Array 1:\n", array1)

array2 = np.random.randint(1, 101, 50)
print("\nArray 2:\n", array2)

sum_arrays = array1 + array2
print("\nSum of arrays:\n", sum_arrays)

difference_arrays = array1 - array2
print("\nDifference of arrays:\n", difference_arrays)

product_arrays = array1 * array2
print("\nProduct of arrays:\n", product_arrays)

array3 = array1[array1 > 50]
print("\nElements from Array 1 greater than 50:\n", array3)

sum_array1 = np.sum(array1)
print("\nSum of all elements in Array 1:", sum_array1)

product_array1 = np.prod(array1)
print("Product of all elements in Array 1:", product_array1)

equal_elements_count = np.sum(array1 == array2)
print("\nNumber of equal elements at the same position:", equal_elements_count)
