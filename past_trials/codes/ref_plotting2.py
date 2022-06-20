import scipy.stats as stats

# 통계함수를 이용한 표준정규분포 [-1, 1]의 면적 계산
areaWithStats = stats.norm(0, 1).cdf(1) - stats.norm(0, 1).cdf(-1)
print('with stats:', areaWithStats)

from sympy import Symbol, exp, sqrt, pi, Integral

# 적분함수를 이용한 표준정규분포 [-1, 1]의 면적 계산
x = Symbol('x')
f = exp(-x ** 2 / 2) / sqrt(2 * pi)
area = Integral(f, (x, -1, 1)).doit().evalf()
print('with integral:', area)

import numpy as np
import matplotlib.pyplot as plt

# plot 작성
x = np.linspace(-4, 4, 101)          # x 정의
y = stats.norm(0, 1).pdf(x)

plt.figure(figsize=(10, 6))          # 플롯 사이즈 지정
plt.plot(x, y, color="blue")         # 선을 파랑색으로 지정하여 plot 작성

plt.axhline(0, color='black')        # x축을 수평선으로 표시

# 정해진 범위 [-1, 1]에 파란색 점선으로 수직선 표시
plt.axvline(-1, linestyle='--', color='blue', alpha=.7)
plt.axvline(1, linestyle='--', color='blue', alpha=.7)

# 정해진 범위 [-1, 1] 내에 하늘색으로 면적 칠하기
plt.fill_between(x, 0, y, where=(x >= -1) & (x <= 1), facecolor='skyblue', alpha=.8,)

# 표준편차를 그리스 문자로 표시
for i in range(7):
    j = i - 3
    plt.text(j, -.03, '0' if (j == 0) else str(j) + r'$\sigma$',
             fontsize=12, horizontalalignment='center', color='blue')

# 면적을 텍스트로 표시
plt.text(0, .2, 'area=' + str(round(area, 4)), fontsize=14, horizontalalignment='center')
plt.text(0, .2, 'area=' + str(round(area, 4)), fontsize=8, horizontalalignment='center')
plt.text(0, .2, 'area=' + str(round(area, 4)), fontsize=20, horizontalalignment='center')

plt.xlabel("x")                      # x축 레이블 지정
plt.ylabel("y")                      # y축 레이블 지정
plt.ylim(-.05, )
plt.grid()                           # 플롯에 격자 보이기
plt.title("Standard Normal Distribution [-1, 1]")     # 타이틀 표시
plt.legend(["N(0, 1)"])              # 범례 표시
plt.show()                           # 플롯 보이기
