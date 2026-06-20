
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ******  (2.1)  ******************************************************************

def integrate_riemann(f):
    dy = 20.0 / (len(f) - 1)
    return np.sum(f) * dy

# ******  (2.2)  ******************************************************************

print("\nThe first steps of the exercise")
print("***************************************************************************")

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

# save to GIF
anim.save('part2_6.gif', writer='pillow', fps=10)

# generate the animation
plt.show()

# ******  (2.7)  *********************************************************************

print("\npart 2.7:")
print("***************************************************************************")

h_bar = 1.054571817e-34

# The Fourier transform of the given function which I assume should be: ψ(x, 0)
def phi_0_zayin(p):
    N = 1 
    L = 1.0
    
    p0 = h_bar / L
    delta = L
    x0 = -5.0 * L 
    
    lorentz = np.exp(- (np.abs(p - p0) * delta) / h_bar)
    
    phase = np.exp(-1j * p * x0 / h_bar)
    
    return N * lorentz * phase

# The rest of the code is the same as the previous parts of the question...

def phi(x, t):
    L = 1.0 # [cm]
    p0 = h_bar / L
    m = h_bar / L
    
    y = np.linspace(-10, 10, 2000)
    
    p = y * p0
    
    free = (p ** 2) / (2 * m)
    exponent = (1j / h_bar) * (p * x - free * t)
    
    integrand = phi_0_zayin(p) * np.exp(exponent)
    
    integral_y = integrate_riemann(integrand)
    
    integral_p = integral_y * p0
    
    normalization_factor = 1 / np.sqrt(2 * np.pi * h_bar)
    
    return normalization_factor * integral_p

print(f"ψ(0, 0) = {phi(0, 0)}")

x = np.arange(-10, 10.1, 0.1)

psi_unnormalized = np.array([phi(x, 0) for x in x])

probability_density = np.abs(psi_unnormalized) ** 2

integral_x = integrate_riemann(probability_density)

N = 1 / np.sqrt(integral_x)

print(f"N = {N}")

x_vec = np.arange(-10, 10.1, 0.1)
t_vec = np.arange(0, 10.1, 0.1)

# empty matrix, rows will represent time steps, columns will represent spatial points.
psi_xt = np.zeros((len(t_vec), len(x_vec)), dtype=complex)

for i, t in enumerate(t_vec):
    for j, x in enumerate(x_vec):
        psi_xt[i, j] = N * phi(x, t)

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

# save to GIF
anim.save('part2_7.gif', writer='pillow', fps=10)

# generate the animation
plt.show()

# ******  part 3  *********************************************************************

print("\npart 3:")
print("***************************************************************************")

h_bar = 1.0
m = 1.0
V0 = 5.0
x0 = -15.0 
Delta_q = 0.5

# (E = V0)
q_critical = np.sqrt(2 * m * V0)

# Here you decide which section to run!
# ==========================================
# א) (E < V0): q0 = 2.0
# ב) (E > V0): q0 = 4.0 
# ג) (E ~ V0): q0 = q_critical 
# ==========================================

part_number = 1
parts = [2.0, 4.0, q_critical]

for part in parts:
    q0 = part

    def phi_step(x, t):
        q_values = np.linspace(q0 - 6*Delta_q, q0 + 6*Delta_q, 1000)
        dq = q_values[1] - q_values[0]

        phi_0_q = np.exp(-((q_values - q0)**2) / (2 * Delta_q**2)) * np.exp(-1j * q_values * x0 / h_bar)

        E_q = (q_values**2) / (2 * m)

        time_phase = np.exp(-1j * E_q * t / h_bar)

        integral_sum = 0

        for i, q in enumerate(q_values):
            k_prime = np.sqrt(q**2 - 2 * m * V0 + 0j)

            R = (q - k_prime) / (q + k_prime)
            T = 2 * q / (q + k_prime)

            if x < 0:
                psi_xq = np.exp(1j * q * x / h_bar) + R * np.exp(-1j * q * x / h_bar)
            else:
                psi_xq = T * np.exp(1j * k_prime * x / h_bar)

            integral_sum += phi_0_q[i] * psi_xq * time_phase[i] * dq

        return integral_sum

    # From here it's similar to the previous code... just creating the animation

    print(f"Critical Momentum for E=V0 is: {q_critical:.2f}")
    print("Calculating space-time grid. This will take a moment...")

    x_values = np.arange(-30, 20, 0.2)
    t_values = np.arange(0, 15, 0.1)

    psi_xt = np.zeros((len(t_values), len(x_values)), dtype=complex)

    for i, t in enumerate(t_values):
        for j, x in enumerate(x_values):
            psi_xt[i, j] = phi_step(x, t)

    prob_density = np.abs(psi_xt)**2
    prob_density = prob_density / np.max(prob_density)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(-30, 20)
    ax.set_ylim(0, 1.1)

    # We will see the potential step as a red line
    ax.plot([0, 0], [0, 1.1], color='red', linestyle='--', alpha=0.5, label='Potential Step (x=0)')
    ax.fill_between([0, 20], 0, 1.1, color='red', alpha=0.05)

    line, = ax.plot([], [], lw=2, color='blue', label='$|\psi(x,t)|^2$')
    ax.legend(loc='upper right')
    ax.set_xlabel('Position (x)')
    ax.set_ylabel('Normalized Probability')

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        line.set_data(x_values, prob_density[i, :])
        ax.set_title(f'Wavepacket Scattering ($E_0$ proxy $q_0={q0}$) | Time: {t_values[i]:.1f}')
        return line,

    anim = FuncAnimation(fig, animate, init_func=init,
                         frames=len(t_values), interval=100, blit=True)

    # save to GIF
    anim.save(f'part3_{part_number}.gif', writer='pillow', fps=10)
    part_number += 1

    plt.show()