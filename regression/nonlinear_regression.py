import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.optimize import least_squares


def illustrate():
    rcParams['figure.figsize'] = (10, 6)
    rcParams['legend.fontsize'] = 16
    rcParams['axes.labelsize'] = 16

    r = np.linspace(0, 5, 100)
    linear = r ** 2
    huber = r ** 2
    huber[huber > 1] = 2 * r[huber > 1] - 1
    soft_l1 = 2 * (np.sqrt(1 + r ** 2) - 1)
    cauchy = np.log1p(r ** 2)
    arctan = np.arctan(r ** 2)

    plt.plot(r, linear, label='linear')
    plt.plot(r, huber, label='huber')
    plt.plot(r, soft_l1, label='soft_l1')
    plt.plot(r, cauchy, label='cauchy')
    plt.plot(r, arctan, label='arctan')
    plt.xlabel("$r$")
    plt.ylabel(r"$\rho(r^2)$")
    plt.legend(loc='upper left')
    plt.show()


def generate_data(t, A, sigma, omega, noise=0, n_outliers=0, random_state=0):
    y = A * np.exp(-sigma * t) * np.sin(omega * t)
    rnd = np.random.RandomState(random_state)
    error = noise * rnd.randn(t.size)
    outliers = rnd.randint(0, t.size, n_outliers)
    error[outliers] *= 35
    return y + error


def cal_residuals_least_squares_minimization(x, t, y):
    return x[0] * np.exp(-x[1] * t) * np.sin(x[2] * t) - y


def main():
    # illustrate()
    A = 2
    sigma = 0.1
    omega = 0.1 * 2 * np.pi
    x_true = np.array([A, sigma, omega])

    noise = 0.1

    t_min = 0
    t_max = 300

    t_train = np.linspace(t_min, t_max, 300)
    y_train = generate_data(t_train, A, sigma, omega, noise=noise, n_outliers=4)
    x0 = np.ones(3)

    res_lsq = least_squares(cal_residuals_least_squares_minimization, x0, args=(t_train, y_train))
    res_robust = least_squares(cal_residuals_least_squares_minimization, x0, loss='soft_l1', f_scale=1,
                               args=(t_train, y_train))

    t_test = np.linspace(t_min, t_max, 300)
    y_test = generate_data(t_test, A, sigma, omega)

    y_lsq = generate_data(t_test, *res_lsq.x)
    y_robust = generate_data(t_test, *res_robust.x)

    plt.plot(t_train, y_train, 'o', label='data')
    plt.plot(t_test, y_test, label='true')
    plt.plot(t_test, y_lsq, label='lsq')
    plt.plot(t_test, y_robust, label='robust lsq')
    plt.xlabel('$t$')
    plt.ylabel('$y$')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
