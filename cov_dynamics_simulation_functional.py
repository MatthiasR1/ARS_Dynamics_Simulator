# -*- coding: utf-8 -*-
"""
Quick first try, not main project
Simulating disease dynamics 
"""


import numpy as np
from matplotlib import pyplot as plt

from celluloid import Camera
# Module for easy matplotlib animation
# from github: jwkvam/ celluloid

def initialize (population, size_of_world, number_infected):
    
    population[:,0:2] = np.random.rand(len(population),2)* size_of_world
    population[:,2] = 1          # vunerable
    population[:,3] = 0        # infected
    population[0:number_infected,3] = 1   # infected at start of simulation
    population[:,4] = 0         # date
    population[:,5] = 0         # death
    return population


def move(population,velocity, gridsize):
    """updates positions of population"""
    population[:,0:2] += np.random.uniform(-1,1,(len(population),2))* velocity
    
    #Randbedingungen Torrus
    population[np.where(population[:,0]<0), 0] += gridsize
    population[np.where(population[:,0]>gridsize), 0] -= gridsize
    
    population[np.where(population[:,1]<0), 1] += gridsize
    population[np.where(population[:,1]>gridsize), 1] -= gridsize
    return 0


def infection (population, infection_prob, death_prob, date):
    """spread of disease, resulting effects death, recovery """
    safe_dist = 1.15                    # parameter
    recovery_rate = 0.4   
    infections_per_day = 0
    # spread of decease

    for i in np.where(population[:,3]==1)[0]:
        #print(i)
        for j in range(len(population)):
            if (population[j,2] == 1):
                if (np.linalg.norm(population[i,0:2]-population[j,0:2]) < safe_dist and i!= j):
                    if (population[j,3] != 1):
                        if (np.random.rand()<infection_prob):
                            population[j,3] = 1 
                            population[j,4] = date
                            infections_per_day +=1
        # healing
        if (date- population[i,4] > 14):
            if(np.random.rand() < recovery_rate):
                population[i,3] = 0         # recovered
                population[i,2] = 0         # imune
        
        # death
        
        if (np.random.rand() < death_prob):
             population[i,5] = 1         # dead 
             population[i,3] = 0         # recovered/ not infectious
             population[i,2] = 0         # imune
    return infections_per_day


N = 1000
ninfected = int(N/100)
ngrid =  100

sim_time = 180
day = 0

labels = ["xpos", "ypos", "vunerable", "infected", "infection_date", "dead"]

population = np.zeros(shape = (N,len(labels))) 

population = initialize(population, ngrid, ninfected)

data_infections_per_day = []
#move(population,velocity=1)

fig = plt.figure()
camera = Camera(fig)

for day in range(1,sim_time):
    if(day%5==0): print("Day: ", day)
    plt.scatter(population[np.where(population[:,3]==0),0],population[np.where(population[:,3]==0),1],c = "green")
    plt.scatter(population[np.where(population[:,3]==1),0],population[np.where(population[:,3]==1),1],c = "red")
    plt.scatter(population[np.where(population[:,2]==0),0],population[np.where(population[:,2]==0),1],c = "blue")
    plt.scatter(population[np.where(population[:,5]==1),0],population[np.where(population[:,5]==1),1],c = "black")
    
    camera.snap()
    move(population,2, ngrid)
    
    data_infections_per_day.append(infection(population, 0.5, 0.001, day))

animation = camera.animate()    
animation.save("dynamics.mp4")  
plt.close(fig)


print("deaths:", sum(population[:,5]))                          # add all dead, 1 in column 5 
print("infected:", len(np.where(population[:,4]>0)[0])+ int(N/100))   # infection date > 0 + infected at start
print("recovered:", (N -sum(population[:,2])) -sum(population[:,5]))  # all - not imune  - imune, but dead

ninfections_over_time = []
for i in range(len(data_infections_per_day)):    
    ninfections_over_time.append(sum(data_infections_per_day[0:i]))

xaxis = np.arange(1,sim_time)
plt.plot(xaxis, data_infections_per_day)
plt.show()

plt.plot(xaxis, ninfections_over_time)
plt.show()  
# Error MovieWriter ffmpeg unavailable, solved    

    
    
