
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ******  (2.1)  ******************************************************************

def integrate_riemann(f):
    dy = 20.0 / (len(f) - 1)
    return np.sum(f) * dy

# ******  (2.2)  ******************************************************************

h_bar = 1.054571817e-34

def phi_0(p):
    N = 1 
    L = 1.0 # [cm]
   
    p0 = h_bar / L
    delta = h_bar / L
    x0 = -5 * L
    
    gaussian = np.exp(-((p - p0) ** 2) / (2 * (delta ** 2)))
    
    phase = np.exp(-1j * p * x0 / h_bar)
    
    return N * gaussian * phase

def phi(x, t):
    L = 1.0 # [cm]
    p0 = h_bar / L
    m = h_bar / L
    
    y = np.linspace(-10, 10, 2000)
    
    p = y * p0
    
    free = (p ** 2) / (2 * m)
    exponent = (1j / h_bar) * (p * x - free * t)
    
    integrand = phi_0(p) * np.exp(exponent)
    
    integral_y = integrate_riemann(integrand)
    
    integral_p = integral_y * p0
    
    normalization_factor = 1 / np.sqrt(2 * np.pi * h_bar)
    
    return normalization_factor * integral_p

print(f"ψ(0, 0) = {phi(0, 0)}")

# ******  (2.3)  ******************************************************************

x = np.arange(-10, 10.1, 0.1)

psi_unnormalized = np.array([phi(x, 0) for x in x])

# ******  (2.4)  ******************************************************************

probability_density = np.abs(psi_unnormalized) ** 2

integral_x = integrate_riemann(probability_density)

N = 1 / np.sqrt(integral_x)

print(f"N = {N}")

# ******  (2.5)  ******************************************************************

x_vec = np.arange(-10, 10.1, 0.1)
t_vec = np.arange(0, 10.1, 0.1)

# empty matrix, rows will represent time steps, columns will represent spatial points.
psi_xt = np.zeros((len(t_vec), len(x_vec)), dtype=complex)

for i, t in enumerate(t_vec):
    for j, x in enumerate(x_vec):
        psi_xt[i, j] = N * phi(x, t)

# ******  (2.6)  *********************************************************************

prob_density = np.abs(psi_xt)**2

fig, ax = plt.subplots(figsize=(8, 5))

ax.set_xlim(-10, 10)
ax.set_ylim(0, np.max(prob_density) * 1.1) 

ax.set_title('Time Evolution of Probability Density $|\psi(x,t)|^2$')
ax.set_xlabel('Position (x)')
ax.set_ylabel('Probability Density')
ax.grid(True)

line, = ax.plot([], [], lw=2, color='blue')

# required for this graphic librery
def init():
    line.set_data([], [])
    return line,

# required for this graphic librery
def animate(i):
    line.set_data(x_vec, prob_density[i, :])
    ax.set_title(f'Time Evolution ($t = {t_vec[i]:.1f}$)')
    return line,

# main animation engine
anim = FuncAnimation(fig, animate, init_func=init,
                     frames=len(t_vec), interval=100, blit=True)

# generate the animation
plt.show()

# ******  (2.7)  *********************************************************************

