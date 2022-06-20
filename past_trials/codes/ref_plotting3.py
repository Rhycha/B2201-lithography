# fit a line to the economic data
import numpy as np
from numpy import sin
from numpy import sqrt
from numpy import arange
from pandas import read_csv
from scipy.optimize import curve_fit
from matplotlib import pyplot
# define the true objective function
def objective(x, a, b, c, d):
	return a * sin(b - x) + c * x**2 + d

def uncharging(x, a, c, d):
	return a*(np.exp(-(x-c))) + d

def charging(x, a, c, d):
	return a*(1-np.exp(-(x-c))) + d

# load the dataset
url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
dataframe = read_csv(url, header=None)
data = dataframe.values
# print(data)
# choose the input and output variables
x, y = data[:, 4], data[:, -1]

# curve fit
p0 = (100, 1, 1, -70) # start with values near those we expect
popt, _ = curve_fit(objective, x, y, p0)
# summarize the parameter values
a, b, c, d = popt
print(popt)
# plot input vs output
pyplot.scatter(x, y)
# define a sequence of inputs between the smallest and largest known inputs
x_line = arange(min(x), max(x), 1)
# calculate the output for the range
y_line = objective(x_line, a, b, c, d)
# create a line plot for the mapping function
pyplot.plot(x_line, y_line, '--', color='red')

p0 = (0.1, 100, 60) # start with values near those we expect
popt, _ = curve_fit(charging, x, y, p0)
# summarize the parameter values
a, c, d = popt
print(popt)
# plot input vs output
pyplot.scatter(x, y)
# define a sequence of inputs between the smallest and largest known inputs
x_line = arange(min(x), max(x), 1)
# calculate the output for the range
y_line = charging(x_line, a, c, d)
# create a line plot for the mapping function
pyplot.plot(x_line, y_line, '--', color='green')

#
# p0 = (100, 1, -70) # start with values near those we expect
# popt, _ = curve_fit(uncharging, x, y, p0)
# # summarize the parameter values
# a, c, d = popt
# print(popt)
# # plot input vs output
# pyplot.scatter(x, y)
# # define a sequence of inputs between the smallest and largest known inputs
# x_line = arange(min(x), max(x), 1)
# # calculate the output for the range
# y_line = uncharging(x_line, a, c, d)
# # create a line plot for the mapping function
# pyplot.plot(x_line, y_line, '--', color='blue')
# xs2 = np.arange(200)
# ys2 = uncharging(xs2, a, c, d)
# pyplot.plot(xs2, ys2, '--', color='blue')

xs3 = np.arange(100,200)
ys3 = charging(xs3, a, c, d)
pyplot.plot(xs3, ys3, '--', color='blue')


pyplot.show()


