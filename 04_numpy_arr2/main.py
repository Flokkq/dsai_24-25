import numpy as np

np.random.seed(0)

array_int = np.random.randint(1, 101, 100)
print("Integer Array:\n", array_int)

array_float = np.random.rand(100)
print("\nFloat Array:\n", array_float)

array_int_mod = np.where(array_int < 50, 50, array_int)
print("\nModified Integer Array (values < 50 set to 50):\n", array_int_mod)

array_float_mod = np.where(array_float < 0.5, 0.5, array_float)
print("\nModified Float Array (values < 0.5 set to 0.5):\n", array_float_mod)

array3 = np.where(array_float_mod > 0.7, array_int_mod, -1)
print("\nThird Array based on condition:\n", array3)

positive_values_count = np.sum(array3 > 0)
print("\nNumber of values > 0 in the third array:", positive_values_count)

division_result = np.divide(
    array_int_mod,
    array_float_mod,
    out=np.zeros_like(array_int_mod, dtype=float),
    where=array_float_mod != 0
)
print("\nResult of element-wise division:\n", division_result)
