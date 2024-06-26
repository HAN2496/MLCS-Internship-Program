import numpy as np
import matplotlib.pyplot as plt
from qpsolvers import solve_qp



# QP: minimize x.T P x + q.T x  s.t.  Gx <= h
P = np.array(
    [
        [1.0, 0.4],
        [0.4, 2.0]
    ]
)
q = np.array([0.6, 1.2])

G = np.array(
    [
        [-1.0, -2.0],
        [-2.0, -1.0],
        [-1.0, 2.0],
        [1.0, 1.0],
        [2.0, -1.0]
    ]
)
h = np.array([1.0, 2.0, 6.0, 3.0, 3.0])


# Solve QP
invP = np.linalg.inv(P)
x_unc = -invP @ q  # solution for unconstrained problem
active = G @ x_unc > h  # check active inequality constraints
u_opt = -np.linalg.solve(G[active] @ invP @ G[active].T, G[active] @ invP @ q + h[active])  # solve argmin_x x.T P x + q.T x  s.t.  G_active x = h_active
x_opt = -invP @ (G[active].T @ u_opt + q)


# Plot result
cost = []
x_grid = np.array(np.meshgrid(np.linspace(-3, 3, 101), np.linspace(-3, 3, 101)))
for x in x_grid.reshape((2, -1)).T:
    cost.append(0.5 * x.T @ P @ x + q @ x)
plt.contourf(*x_grid, np.reshape(cost, (101, 101)), levels=16)  # plot cost function
plt.plot([1.0, -1.0, -2.0, 0.0, 2.0, 1.0], [-1.0, 0.0, 2.0, 3.0, 1.0, -1.0], "k", alpha=0.5)  # plot inequality constraints
plt.scatter(*x_opt, c="r")  # plot optimal solution
plt.show()
