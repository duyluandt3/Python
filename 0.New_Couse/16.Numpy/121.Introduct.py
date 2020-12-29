import numpy

n = numpy.arange(27)
print(n)
print(type(n))

# Tao ra mang 2 chieu, 3 hang va 9 cot, tu 0 den 27
m = n.reshape(3,9)
print(m)

k = n.reshape(3, 3, 3)
print(k)