import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import scipy.integrate as sci
xs = np.arange(12) + 7
ys = np.array([304.08994, 229.13878, 173.71886, 135.75499,
               111.096794, 94.25109, 81.55578, 71.30187,
               62.146603, 54.212032, 49.20715, 46.765743])
ys_flip = np.array([46, 173, 235, 257,
                    265, 274, 277, 278,
                    278.7, 279.3, 279.5, 279.6])

plt.plot(xs, ys, '.')
plt.title("Original Data")


def monoExp(x, m, t, b):
    return m * np.exp(-t * x) + b

def uncharging(x, m, t, c, b):
	return m*(np.exp(-(x-c)*t)) + b

def charging(x, a, b, c, d):
	return a*(1-np.exp(-b*(x-c))) + d

# define the true objective function
def objective(x, a, b, c):
	return a * x + b * x**2 + c

# perform the fit
p0 = (500, .1, 10, 50) # start with values near those we expect
params, cv = scipy.optimize.curve_fit(uncharging, xs, ys, p0)
m, t, c, b = params
sampleRate = 20_000 # Hz
tauSec = (1 / t) / sampleRate

# determine quality of the fit
squaredDiffs = np.square(ys - uncharging(xs, m, t, c, b))
squaredDiffsFromMean = np.square(ys - np.mean(ys))
rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
print(f"R² = {rSquared}")

# plot the results
plt.subplot(1,4,1)
plt.plot(xs, ys, '.', label="data")
plt.plot(xs, uncharging(xs, m, t, c, b), '--', label="uncharging", color="blue")

# 색칠하기 #######################
# 정해진 범위 [-1, 1]에 파란색 점선으로 수직선 표시
plt.axvline(-1, linestyle='--', color='blue', alpha=.7)
plt.axvline(1, linestyle='--', color='blue', alpha=.7)

# 정해진 범위 [-1, 1] 내에 하늘색으로 면적 칠하기
plt.fill_between(xs, 0, uncharging(xs, m, t, c, b), where=(xs >= min(xs)) & (xs <= max(xs)), facecolor='skyblue', alpha=.8,)
# 색칠하기 - E #####################################
plt.plot(xs, ys_flip, '.', label="data2",color="black")
p1 = (500, .1, 10, 50) # start with values near those we expect
params_c, cv_c = scipy.optimize.curve_fit(charging, xs, ys_flip, p1)
a, b, c, d = params_c
plt.plot(xs, charging(xs, a, b, c, d), '--', label="charging", color="red")
plt.title("Uncharging")



# inspect the parameters
print(f"Y = {m} * e^(-{t} * (x - c)) + {b}")
print(f"Tau = {tauSec * 1e6} µs")



# perform the fit
p0 = (2000, .1, 50) # start with values near those we expect
params, cv = scipy.optimize.curve_fit(monoExp, xs, ys, p0)
m, t, b = params
sampleRate = 20_000 # Hz
tauSec = (1 / t) / sampleRate

# determine quality of the fit
squaredDiffs = np.square(ys - monoExp(xs, m, t, b))
squaredDiffsFromMean = np.square(ys - np.mean(ys))
rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
print(f"R² = {rSquared}")

# plot the results
plt.subplot(1,4,2)
plt.plot(xs, ys, '.', label="data")
plt.plot(xs, monoExp(xs, m, t, b), '--', label="fitted")
plt.title("Fitted Exponential Curve")

# inspect the parameters
print(f"Y = {m} * e^(-{t} * x) + {b}")
print(f"Tau = {tauSec * 1e6} µs")


xs2 = np.arange(25)
ys2 = monoExp(xs2, m, t, b)

plt.subplot(1,4,3)

plt.plot(xs, ys, '.', label="data")
plt.plot(xs2, ys2, '--', label="fitted")
plt.title("Extrapolated Exponential Curve")


def monoExpZeroB(x, m, t):
    return m * np.exp(-t * x)

# perform the fit using the function where B is 0
p0 = (2000, .1) # start with values near those we expect
paramsB, cv = scipy.optimize.curve_fit(monoExpZeroB, xs, ys, p0)
mB, tB = paramsB
sampleRate = 20_000 # Hz
tauSec = (1 / tB) / sampleRate

# inspect the results
print(f"Y = {mB} * e^(-{tB} * x)")
print(f"Tau = {tauSec * 1e6} µs")

# compare this curve to the original
ys2B = monoExpZeroB(xs2, mB, tB)
plt.subplot(1,4,4)
plt.plot(xs, ys, '.', label="data")
plt.plot(xs2, ys2, '--', label="fitted")
plt.plot(xs2, ys2B, '--', label="zero B")



########################
# Integral
#####################
import sympy as sy
a, b, c, d = sy.symbols('a b c d')
m, t = sy.symbols('m t')

x = sy.symbols('x')
y = sy.symbols('y')


def charging_for_sym():
    return a * (1 - sy.exp(-b * (x - c))) + d

def charging_for_sym2(a,b,c,d):
    return a * (1 - sy.exp(-b * (x - c))) + d

I = sy.Integral(charging_for_sym(),(x,a,b))
print(sy.pretty(I))
a, b, c, d = params_c
int_func = sy.integrate(charging_for_sym2(a,b,c,d),x)
Fb = int_func.subs(x,17).evalf()
Fa = int_func.subs(x,8).evalf()

print(Fb-Fa)


plt.show()

