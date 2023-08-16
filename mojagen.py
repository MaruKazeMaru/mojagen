#!/usr/bin/python3

import numpy as np
from numpy import ndarray
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class moja_gen2:
    def generate(self, freq):
        t = np.linspace(0.0, 2.0 * np.pi, 100)
        x = np.sin(freq * (np.random.rand() + 1.0) * t) + np.cos(freq * (np.random.rand() + 1.0) * t)
        y = np.sin(freq * (np.random.rand() + 1.0) * t) + np.cos(freq * (np.random.rand() + 1.0) * t)
        z = np.sin(freq * (np.random.rand() + 1.0) * t) + np.cos(freq * (np.random.rand() + 1.0) * t)
        return (x, y, z)


class moja_gen:
    def __init__(self, tor_0=1.0, tor_coef=1.0):
        self.length = 25.0
        self.point_num = 100
        self.tau_0 = tor_0
        self.tau_c = tor_coef
        self.switch_time = 0.0
        self.tau = 0.0
        self.mode = "l"
        self.switch_mode()


    def switch_mode(self):
        self.switch_time += np.random.rand() * self.length / 2.5
        if self.mode == "l":
            self.mode = "r"
            self.tau = self.tau_c * (np.random.randn() + 2.0)
        elif self.mode == "r":
            self.mode = "l"
            self.tau = self.tau_c * (np.random.randn() - 2.0)
        """
        print("switch mode")
        print("mode = %s" % self.mode)
        print("next switch time = %f" % self.switch_time)
        print("dtau = %f" % self.tau)
        """


    def f(self, s:float, X:tuple) -> ndarray:
        i = np.array(X[0:3]).T
        c = np.array(X[3:6]).T
        t = np.array(X[6:9]).T
        n = np.array(X[9:12]).T
        b = np.array(X[12:15]).T
        kappa = 1.0
        if s > self.switch_time:
            self.switch_mode()
        tau = self.tau
        """
        if s == 0.0:
            o = np.zeros((3,))
        else:
            o = i / s - c
        l = np.dot(o, o)
        """
        ret = np.concatenate([c, t, kappa * n, -kappa * t + tau * b, -tau * n]).reshape([15])
        #ret = np.append(ret, self.tau)
        #ret = np.append(ret, self.tau_c * np.dot(o, b))
        #ret = np.append(ret, -np.dot(o, n))
        #ret = np.append(ret, 0)
        return ret


    def generate(self) -> ndarray:
        s_start = 0.0
        s_end = self.length
        s_span = [s_start, s_end]
        iv = [
            0.0, 0.0, 0.0,
            0.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0#,
            #self.tau_0
        ]
        s_eval = np.linspace(s_start, s_end, self.point_num)
        sol = solve_ivp(self.f, s_span, iv, t_eval=s_eval)
        return sol.y


class curve_generator:
    def __init__(self):
        self.length = 25.0
        self.point_num = 100
    def curvurture(self, s:float, i:ndarray, c:ndarray, t:ndarray, n:ndarray, b:ndarray) -> float:
        return 0.0
    def torsion(self, s:float, i:ndarray, c:ndarray, t:ndarray, n:ndarray, b:ndarray) -> float:
        return 0.0


    def f(self, s:float, X:tuple) -> ndarray:
        i = np.array(X[0:3]).T
        c = np.array(X[3:6]).T
        t = np.array(X[6:9]).T
        n = np.array(X[9:12]).T
        b = np.array(X[12:15]).T
        kappa = self.curvurture(s, i, c, t, n, b)
        tau = self.torsion(s, i, c, t, n, b)
        return np.concatenate([c, t, kappa * n, -kappa * t + tau * b, -tau * n]).reshape([15])


    def generate(self) -> ndarray:
        s_start = 0.0
        s_end = self.length
        s_span = [s_start, s_end]
        iv = [
            0.0, 0.0, 0.0,
            0.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0
        ]
        S_eval = np.linspace(s_start, s_end, self.point_num)
        sol = solve_ivp(self.f, s_span, iv, t_eval=S_eval)
        return sol.y


class helicoid_generator(curve_generator):
    def __init__(self, curvurture=0.0, torsion=0.0):
        super().__init__()
        self.kappa = curvurture
        self.tau = torsion
    def curvurture(self, s: float, i: ndarray, c: ndarray, t: ndarray, n: ndarray, b: ndarray) -> float:
        return self.kappa
    def torsion(self, s: float, i: ndarray, c: ndarray, t: ndarray, n: ndarray, b: ndarray) -> float:
        return self.tau


class moja_generator(curve_generator):
    def __init__(self, tor_0=1.0, tor_coef=1.0):
        super().__init__()
        self.tau = tor_0
        self.tau_c = tor_coef


    def curvurture(self, s: float, i: ndarray, c: ndarray, t: ndarray, n: ndarray, b: ndarray) -> float:
        return 1.0


    def torsion(self, s: float, i: ndarray, c: ndarray, t: ndarray, n: ndarray, b: ndarray) -> float:
        if s == 0.0:
            o = np.zeros((3,))
        else:
            o = i / s - c
        l = np.dot(o, o)
        self.tau += self.tau_c * np.dot(o, b) * self.length / self.point_num
        return self.tau


class rand_moja_generator(curve_generator):
    def __init__(self, tor_0=1.0, tor_coef=1.0):
        super().__init__()
        self.tau = tor_0
        self.tau_c = tor_coef


    def curvurture(self, s: float, i: ndarray, c: ndarray, t: ndarray, n: ndarray, b: ndarray) -> float:
        """
        self.kappa += self.kappa_c * np.random.randn(1)[0] / self.point_num
        return self.kappa
        """
        return 1.0


    def torsion(self, s: float, i: ndarray, c: ndarray, t: ndarray, n: ndarray, b: ndarray) -> float:
        return self.tau_c * np.random.randn()
        #return self.tau
    

class sin_tor_generator(curve_generator):
    def __init__(self, freq_cur=0.0, freq_tor=1.0, tor_coef=1.0):
        super().__init__()
        self.freq_c = freq_cur
        self.freq_t = freq_tor
        self.tor_c = tor_coef


    def curvurture(self, s: float, i: ndarray, c: ndarray, t: ndarray, n: ndarray, b: ndarray) -> float:
        return 1.0


    def torsion(self, s: float, i: ndarray, c: ndarray, t: ndarray, n: ndarray, b: ndarray) -> float:
        return self.tor_c * np.sin(self.freq_t * s)


if __name__ == "__main__":
    import sys
    #moja = sin_tor_generator(freq_tor=1.5, tor_coef=0.1).generate()
    #moja = rand_moja_generator(tor_0=0.0, tor_coef=10.0).generate()
    #moja = moja_generator(tor_0=1.202, tor_coef=0.1).generate()
    #tau_0 = 1.0 + np.random.randn()
    #print(tau_0)
    moja = moja_gen(tor_0=float(sys.argv[1]), tor_coef=float(sys.argv[2])).generate()
    #print(type(moja))
    #print(moja.shape)
    #print(moja)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    x = moja[3, :]
    y = moja[4, :]
    z = moja[5, :]
    max_x = max(x)
    min_x = min(x)
    max_y = max(y)
    min_y = min(y)
    max_z = max(z)
    min_z = min(z)
    cen_x = (max_x + min_x) / 2.0
    cen_y = (max_y + min_y) / 2.0
    cen_z = (max_z + min_z) / 2.0
    ax_scale = max(max_x - min_x, max_y - min_y, max_z - min_z) / 2.0
    ax.set_xlim(cen_x - ax_scale, cen_x + ax_scale)
    ax.set_ylim(cen_y - ax_scale, cen_y + ax_scale)
    ax.set_zlim(cen_z - ax_scale, cen_z + ax_scale)
    ax.plot(x, y, z)
    plt.show()
    #moja = moja_gen2().generate(float(sys.argv[1]))
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    x = moja[0]
    y = moja[1]
    z = moja[2]
    max_x = max(x)
    min_x = min(x)
    max_y = max(y)
    min_y = min(y)
    max_z = max(z)
    min_z = min(z)
    cen_x = (max_x + min_x) / 2.0
    cen_y = (max_y + min_y) / 2.0
    cen_z = (max_z + min_z) / 2.0
    ax_scale = max(max_x - min_x, max_y - min_y, max_z - min_z) / 2.0
    ax.set_xlim(cen_x - ax_scale, cen_x + ax_scale)
    ax.set_ylim(cen_y - ax_scale, cen_y + ax_scale)
    ax.set_zlim(cen_z - ax_scale, cen_z + ax_scale)
    ax.plot(x, y, z)
    plt.show()
    """
