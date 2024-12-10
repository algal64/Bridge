# -*- coding: cp1251 -*-

import math
import numpy as np
import matplotlib.pyplot as plt


Tmax = 100  
# время расчета, пока в сек

n = 10000 # количество отсчетов по времени
h = Tmax/n # шаг по времени

# начальные условия
X0 = 0
Y0 = 0

# параметры системы как они даны в статье
f = 1.63 # Гц
ksi = 0.028
gamma = 0.014
Pi = 3.141592

# параметры системы в каноническом виде

omega = 2*Pi/f      # частота
beta =  omega*ksi    # вязкое трение
alfa = 0.05            # сухое трение 

# параметры внешнего воздействия
# полагаем возбуждение тремя прямоугольными импльсами амплитудой А1,A2,A3, 
# длительностью Т1, Т2, Т3 в моменты времени tt1, tt2, tt3   
A1 = 2
A2 = 2
A3 = 2

T1 = 1
T2 = 1
T3 = 1

tt1 = 2
tt2 = 5
tt3 = 8


# нагрузка 
def Qext(t):
    if  tt1 <= t <= (tt1+T1): 
        return A1
    elif tt2 <= t <= (tt2+T2):
        return A2
    elif tt3 <= t <= (tt3+T3):  
        return A3
    else: 
        return 0
   


# Определяем систему дифференциальных уравнений:
def V(y):
        return y

def U(t, x, y, q):
        if y < 0:
            sgn = -1
        else:
            sgn = 1

        return q - 2*beta* y - alfa * sgn - omega**2 *x

# Графический модуль
def plott_my(str_x, str_y, str_label, xx_array, yy_array):
        plt.figure(figsize=(8,5))
        strq = 'alfa =' + str(round(alfa,2)) + '   beta = ' + str(round(beta,2)) + '   omega = ' + str(round(omega,2))
        plt.title(strq)
        plt.xlabel(str_x)
        plt.ylabel(str_y)
        plt.grid()
        plt.plot(yy_array, xx_array, label=str_label)
        plt.legend()
        plt.show()




# расчет следующего шага
def next(t,x,y,q):
        q0 = U(t, x, y,q)
        k0 = V(y)
        q1 = U(t + h/2, x + h/2*k0, y + h/2*q0,q)
        k1 = V(y + h/2*q0)
        q2 = U(t + h/2, x + h/2*k1, y + h/2*q1,q)
        k2 = V(y + h/2*q1)
        q3 = U(t, x + h*k2, y + h*q2,q)
        k3 = V(y + h*q2)
        k_n = h/6*(k0 + 2*k1 + 2*k2 + k3)
        q_n = h/6*(q0 + 2*q1 + 2*q2 + q3)
        xn = x + k_n
        yn = y + q_n

        return xn,yn

def Kutt ():
        # задаем начальные значения 
        tt, qq = 0, Qext(0)
        xx, yy = X0, Y0
        # заполняем массивы нулями ? 
        X_array, Y_array = np.zeros(n+1), np.zeros(n+1)
        Q_array, t_array = np.zeros(n+1), np.zeros(n+1)

        for i in range(0, n+1):
            # кладем в массив значения функций
            X_array[i] = xx
            Y_array[i] = yy
            t_array[i] = tt
            Q_array[i] = qq

            # считаем значения функций на следующем шаге
            xx, yy = next(tt, xx, yy, qq)
            tt += h
            qq = Qext(tt)
            
     
        return X_array, Y_array, Q_array, t_array


X_array, Y_array, Q_array, t_array = Kutt()

str_x = 'X'
str_y = 'Y'
str_label = 'фазовая диаграмма'
plott_my(str_x, str_y, str_label, X_array, Y_array)
        
    

str_x = 't'
str_y = 'X'
str_label = 'Временная реализация'
plott_my(str_x, str_y, str_label, X_array, t_array)
       

str_x = 't'
str_y = 'Q'
str_label = 'Нагрузка'
plott_my(str_x, str_y, str_label, Q_array, t_array)
     







#plt.figure(figsize=(8,5))
#plt.title(f'Load')
#plt.xlabel('x')
#plt.ylabel('q')
#plt.grid()
#plt.plot(np.linspace(a,b,int(n/2)), [q(i) for i in np.linspace(a,b,int(n/2))], label='load')
#plt.legend()
#plt.savefig(f'/content/load.png', bbox_inches='tight')



#plt.figure(figsize=(8,5))
#plt.title(f'load')
#plt.xlabel('x')
#plt.ylabel('q')
#plt.grid()
#plt.plot(np.linspace(a,b/6,int(n/2)), [q(i) for i in np.linspace(a,b/6,int(n/2))], label='load')
#plt.legend()
#plt.savefig(f'/content/load1.png', bbox_inches='tight')

   
        #plt.savefig(f'/content/fig x--x_h alpfa = {round(alpfa_f,3)}, vitta = {round(vitta_f,3)}, omego = {round(omego_f,3)}.png', bbox_inches='tight')
        #plt.show()
        #plt.close()
