# -*- coding: utf-8 -*-
"""
Similation an acute respiratory syndrome outbreak

"""

import numpy as np
import matplotlib.pyplot as plt

"""
ToDO
 
(important)

- data class
    -contruct dataframe during simulation
    - methods to analyze data

-Vizualise class
    -methods to plott analyzed data 
    
    - animate movment, and state
    
- unbound move 

- test complete code

less important

- tests, checks 

- more elegant code, use some advanced concepts when reasonable

- change/ improve simulation class 

- try more but smaller movment steps per day -> more contacts

- improve comments

optional

- performance improvment (seems slow)
    
- different viruses

- different movement and space  
    2d lattice, check only neighbours for infection -> faster
    blocks of groups
    
    no position only network (nodes, contacts)

"""

class Human:
    def __init__(self, number, position2d, size_space, age):
        """Impelements Person with attributes relevant to dicease dynamics"""
        
        """ 
            Input:
                number      - identifier, unique for every person
                position2d  - position in 2d space (at start of simulation)
                size_space  - size of the NxN grid, human exists on
                age         - age of human, effect on movement infection_rate, death_rate
                (age not yet implementet)
        """
        
        """Test if input has correct format, type"""
        #(not complete)
        if(not isinstance(number, int)):
            raise TypeError("number must be int")
        if(not isinstance(position2d, (list, tuple, np.ndarray, np.generic))):
            raise TypeError("position must be list or tuple")
        if(len(position2d) !=2):
            raise TypeError("Coordinates have wrong dimension")
        if(not 0<age<150):
            raise TypeError("Person too old, not existing")
              
        self.number = number            # name, identifier of person
        self.age = age                  # 
        self.xy = position2d
        self.start_position =position2d # used for bound movement around minimum(position at start of simulation)            
        self.size_space = size_space

        self.infected = "False" 
        self.alive = "True"
        self.imune = "False"
        self.velocity = 1.5               # personal speed of movment in simulation, todo age dependent, random 
        self.recovery_rate = 0.5        # chance of recovery on any given day after the duration of illnes (14days)
        
        # Should this be in a virus class ?
        self.infectivity = 0.5         # how likely is it to infect others, chance for single contact
        self.infection_date = -1 
        self.safe_dist = 1.0             # for smaller distances than safe_dist between two humans transmission possible 
        self.death_prob = 0.001        # chance to die on a given day, over time of illness should lead to 4%-0.1% death rate 
        
    """ possible get-, set-methods for attributes, not neccersary, variables not private"""
    
    def get_pos(self):
        return self.xy
    
    def set_pos(self, new_pos):             # (setter, property function)
        self. xy = new_pos
    
    """ Class methods concerning movement in 2d space"""
    
    def move(self):
        """unbound random movement with differrent velocitys"""
        self.xy += np.random.uniform(-1,1,size=len(self.xy))* self.velocity
        
        # limit of space
        # torrus, no borders
        if self.xy[0] < 0: self.xy[0] += self.size_space
        if self.xy[1] < 0: self.xy[1] += self.size_space
        
        if self.xy[0] > self.size_space: self.xy[0] -= self.size_space
        if self.xy[1] > self.size_space: self.xy[1] -= self.size_space
    
    def bound_move(self, position_minimum):
        """ bound random movement around a minimum"""
        # still under construction, not coorect
        movment_radius =self.velocity * 2
        
        if (np.linalg.norm(self.xy -position_minimum)>movment_radius):   # not right 
            self.xy -= (position_minimum -self.xy)* np.randon.nrand()
        else:
            self.xy += np.random.uniform(-1,1,size=len(self.xy))* self.velocity*0.5
    
    """Class methods, spread and effects of virus"""
    def virus_transmission(self, other, date):
        """ Transmision of virus to other human"""
        # maybe list of all other humans of input ?
        if self.infected=="True":
            if other.imune =="False" and other.infected=="False":
                if(np.linalg.norm(self.xy - other.xy) < self.safe_dist and self.number != other.number):
                    if (np.random.rand()<self.infectivity):
                            other.infected = "True"
                            other.infection_date = date
    
    def recovery(self, date, duration_illness):
        """Simulates if infected recovers"""
        if self.infected=="True":
           # print(date,"  ", self.infection_date, " ", duration_illness)
            if (date - self.infection_date > duration_illness):
                if (np.random.rand() < self.recovery_rate):
                    self.infected = "False"
                    self.imune    = "True"     # 100% immunity after illness, maybe make it variable
            
    def death(self):
        """Simulates if infected dies"""
        if self.infected=="True":
            if (np.random.rand()< self.death_prob):
                self.alive = "False"
                self.infected = "False"
                self.imune = "True"
                self.velocity = 0         # dead humans dont move
                
class Superspreader(Human):
    """ Special Human more Contacts, Different Infectionmechanism, Speed, ..."""
    """ maybe part of more future simulations """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Virus:
    def __init__(self, name, transmission_radius, death_prob, duration_illness, typical_recovery):
        self.name = name
        self.safe_distance = transmission_radius
        self.death_prob = death_prob               
        # probability not rate, death_rate (Sterblichkeit) = 1 - (1-death_prob)^(duration_illnes+1)
        # The +1 is exact wenn recovery_rate = 0.5  
        self.duration_illness = duration_illness
        self.recovery_rate = typical_recovery   # also not a rate, naming sheme not exakt
        
    def setting_properties_in_population(self,population):
        """ Changes attributes of member of given population to values that fit to given virus"""
        
        
        #better Tests nessecary if population has the right attributes"""
        for member in population:
            if(isinstance(member,Human)):
                #print(member.number)
                member.safe_dist = self.safe_distance
                member.recovery_rate = self.recovery_rate
                member.death_prob = self.death_prob
                
class data:
    def __init__(self, population, *args, **kwarg):
        
        if(not isinstance(population, (list, tuple))):
            raise TypeError("population must be list or tuple")
        self.pop = population
        
        
    def get_number_population(self):
        return len(self.pop)
    
    def get_number_infected(self):
        n_infected = 0
        for elem in self.pop:
            if(elem.infected=="True"):
                n_infected +=1
        return n_infected
    
    def get_number_dead(self):
        n_dead = 0
        for elem in self.pop:
            if(elem.alive=="False"):
                n_dead +=1
        return n_dead    
    
    def get_number_recovered(self):
        n_recovered = 0
        for elem in self.pop:
            if(elem.alive=="True" and elem.imune=="True"):
                n_recovered +=1
        return n_recovered       


class Visualize:
    def __init__(self, dataframe):
        self.data = dataframe

    def animate2d():
        pass
    
    def plot():
        pass


class Dynamics_Simulator:
    def __init__(self, Animation_on= "False"):
        self.animation_flag = Animation_on   
        
    
    def virus_simulation(self, virus, N, infected_at_start, grid_size, time_simulated):
            
        #initialize population of humans with n infected 
        
        duration = 14    # minimal duration of illness
        result = []      # contains data resulting from simulation 
        pop =[]
        
        day = 0
        
        for n in range(N):
            start_pos = np.random.rand(2)*grid_size

            pop.append(Human(n,start_pos,grid_size,age = 20))
            if (n<infected_at_start):
                pop[n].infected = "True"
                pop[n].infection_date = day
                
        virus.setting_properties_in_population(pop)
        
        for day in range(time_simulated):
            
            for elem in pop:
                elem.move()
                elem.recovery(day,duration)
                elem.death()
                #print("elem:", elem.number)
                for i in range(len(pop)):
                    elem.virus_transmission(pop[i], date = day)
                    
            if (day%10 ==0):
                result = data(pop)
                print("Tag: ",day)
                print("Infected: ", result.get_number_infected())
                print("Dead: ",result.get_number_dead())
                print("Recovered: ",result.get_number_recovered())
        return result





def main():
    
    covid = Virus("covid-19", 0.6, 0.001, 16, 0.5)
    sim1 = Dynamics_Simulator()
    res1 = sim1.virus_simulation(covid, 400, 5, 40, 120)
    print("Simulation ended succesfully:",res1.get_number_recovered())
    
if __name__== "__main__":
    main()

