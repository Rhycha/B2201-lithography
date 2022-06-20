import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import scipy.integrate as sci
import sympy as sy
import numpy.polynomial.polynomial as polynomial


############
# x values, y values
#########
xs2 = np.arange(12) + 19
xs = np.arange(12) + 7
# ys = np.array([275.08994, 219.13878, 173.71886, 135.75499,
#                111.096794, 94.25109, 81.55578, 71.30187,
#                62.146603, 54.212032, 49.20715, 46.765743])
ys = np.array([304.08994, 229.13878, 173.71886, 135.75499,
               111.096794, 94.25109, 81.55578, 71.30187,
               62.146603, 54.212032, 49.20715, 46.765743])
ys2 = np.array([46, 173, 235, 257,
                    265, 274, 277, 278,
                    278.7, 279.3, 279.5, 279.6])


def uncharging(x, A, t, c, b):
	return A*(np.exp(-(x-c)*t)) + b

def charging(x, A, t, c, b):
	return A*(1-np.exp(-t*(x-c))) + b

# define the true objective function
def objective(x, a, b, c):
	return a * x + b * x**2 + c


##########
## integral variable & function
#########
A, t, c, b = sy.symbols('A t c b')

x = sy.symbols('x')
y = sy.symbols('y')

def uncharging_for_sym():
    return A * (1 - sy.exp(-t * (x - c))) + b

def uncharging_for_sym2(A, t, c, b):
    return A * (1 - sy.exp(-t * (x - c))) + b

def charging_for_sym():
    return A * (1 - sy.exp(-t * (x - c))) + b

def charging_for_sym2(A,t,c,b):
    return A * (1 - sy.exp(-t * (x - c))) + b



###########
### Uncharging ploting
##########
# perform the fit
p0 = (500, .1, 10, 50) # start with values near those we expect

params, cv = scipy.optimize.curve_fit(uncharging, xs, ys, p0)
A, t, c, b = params
# determine quality of the fit
squaredDiffs = np.square(ys - uncharging(xs, A, t, c, b))
squaredDiffsFromMean = np.square(ys - np.mean(ys))
rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
print(f"R² = {rSquared}")

# plot the results
plt.subplot(1,1,1)
plt.plot(xs, ys, '.', label="data", color='black', alpha=0.5)
plt.plot(xs, uncharging(xs, A, t, c, b), '--', label="uncharging", color="black")

# 색칠하기 #######################
# 정해진 범위 내에 하늘색으로 면적 칠하기
plt.fill_between(xs, 0, uncharging(xs, A, t, c, b), where=(xs >= min(xs)) & (xs <= max(xs)), facecolor='red', alpha=.8,)



########################
# Integral
#####################

int_func = sy.integrate(charging_for_sym2(A,t,c,b),x)
Fb = int_func.subs(x,17).evalf()
Fa = int_func.subs(x,8).evalf()

print(Fb-Fa)



#############
### Plot Charging
############
p1 = (500, .1, 10, 50) # start with values near those we expect
params_c, cv_c = scipy.optimize.curve_fit(charging, xs2, ys2, p1)
A, t, c, b = params_c
plt.plot(xs2, ys2, '.', label="data", color='black', alpha=0.5)
plt.plot(xs2, charging(xs2, A, t, c, b), '--', label="charging", color="black")

# 색칠하기 #######################
# 정해진 범위 내에 하늘색으로 면적 칠하기
plt.fill_between(xs2, 0, charging(xs2, A, t, c, b), where=(xs2 >= min(xs2)) & (xs2 <= max(xs2)), facecolor='skyblue', alpha=.7,)



plt.title("Uncharging & charging")

int_func = sy.integrate(charging_for_sym2(A,t,c,b),x)
Fb = int_func.subs(x,39).evalf()
Fa = int_func.subs(x,20).evalf()

print(Fb-Fa)

# plt.xticks(range(1, 30))
plt.xlim(0, 30)


# def transientArea(xs, ys, xs2, ys2):
#     (x1, y1) =xs[-1], ys[-1]
#     x2, y2 = xs2[0], ys2[0]
#     dx = x2-x1
#     dy = y2-y1
#     meany = (y2+y1)/2
#     area = meany*dx
#
#     # plt.plot((1, 30), (30, 600), '--', label="transient", color="green")
#     plt.plot(x, ((dy/dx)*(x-x1)+y1), '--', label="transient", color="green")
#     # plt.fill_between(x, 0, ((dy/dx)*(x-x1)+y1), where=(x >= x1) & (x <= x2), facecolor='green', alpha=.7, )
#
#     return area


def transientArea(xs, ys, xs2, ys2):

    (x1, x2) =xs[-1], xs2[0]
    (y1, y2) = ys[-1], ys2[0]
    dx = x2-x1
    meany = (y2+y1)/2
    area = meany*dx

    plt.plot((x1, x2),(y1, y2) , '--', label="charging", color="green")
    plt.fill_between((x1, x2),(y1, y2), facecolor='green', alpha=.7, )

    # p_fitted = polynomial.Polynomial.fit((x1, x2),(y1, y2), 1)
    # polyfunc = polynomial.Polynomial(p_fitted)
    # print(polyfunc)

    return area

print(transientArea(xs, ys, xs2, ys2))
print(1)

# plt.plot([1, 30], [30, 600], label="transient", color="green")
# plt.plot(x,firstOrderEq(a,b), '--', label="transient", color="green")
# plt.fill_between(x, 0, ((dy/dx)*(x-x1)+y1), where=(x >= x1) & (x <= x2), facecolor='green', alpha=.7, )


# transientArea(xs,ys,xs2,ys2)




if __name__=='__main__':
    plt.show()
