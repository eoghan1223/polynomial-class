import numpy as np
import matplotlib.pyplot as plt
def simulate_sho(m, k, x0, v0,t_max, dt):
    '''Simulates the motion of a simple harmonic motion
    
    Parameters
    -------
        m: float
        The weight of the oscilator in kilograms
        k: float
        The spring constant in N/m
        x0:float
        The initial position at launch in metres
        v0:float
        The initial velocity in metres per second
        t_max:float
        The total simulation time in seconds
        dt:float
        The increment in the time in seconds

    Returns:
    --------
        times= An array containing all the simulation times
        position= An array specifying the x position at various times
        velocity= An array specifying the velocity at various times
        energy= An array specifying the total mechanical energy of the system at various times
    '''
    num_steps=int(t_max/dt) + 1
    times=np.linspace(0,t_max, num_steps)
    position = np.zeros(num_steps)
    velocity = np.zeros(num_steps)
    position[0]=x0
    velocity[0]=v0
    # Use the Euler-Cromer method to step through time
    for i in range (1,(num_steps)):
        # Calculates acceleration via Hook's Law
        acceleration= -(k/m)*position[i-1]
        velocity[i]=velocity[i-1] + acceleration*dt
        position[i]=position[i-1] + velocity[i]*dt
    energy= .5*k*(position)**2 + .5*m*(velocity)**2
    return(times,position,velocity, energy)
if __name__=="__main__":
    time_values,position_values,velocity_values,energy_values=simulate_sho(1,10,1,0,10,.01)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10), sharex=True)  
    fig.suptitle('Simple Harmonic Oscillator Simulation', fontsize=16)
    # Plot 1: Position vs. Time
    ax1.plot(time_values, position_values, label='Position')
    ax1.set_ylabel('Position (m)')
    ax1.grid(True)   
    # Plot 2: Velocity vs. Time
    ax2.plot(time_values, velocity_values, color='orange', label='Velocity')
    ax2.set_ylabel('Velocity (m/s)')
    ax2.grid(True)
    # Plot 3: Energy vs. Time
    ax3.plot(time_values, energy_values, color='green', label='Total Energy')
    ax3.set_ylabel('Energy (J)')
    ax3.set_xlabel('Time (s)')
    # Set y-axis limits to better see small fluctuations
    initial_energy = energy_values[0]
    ax3.grid(True)   
    plt.tight_layout(rect=[0, 0, 1, 0.96]) # Adjust layout to make room for suptitle
    plt.show()


    
