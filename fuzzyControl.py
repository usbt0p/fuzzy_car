import numpy as np
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import networkx as nx
import random

# define our universes
road_width = np.arange(0, 11, 1)
road_length = np.arange(0, 26, 1)

# Antecedent/Consequent objects hold universe variables and membership functions
# TODO no hay variables de velocidad: incorporar a futuro
distance_right = ctrl.Antecedent(road_width, 'distance_right')
distance_left = ctrl.Antecedent(road_width, 'distance_left')
distance_front = ctrl.Antecedent(road_length, 'distance_front')

steering = ctrl.Consequent(np.arange(-25, 26, 1),
                           'steering', defuzzify_method='mom')

print(steering.defuzzify_method)  # método por defecto de defuzz
# https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.defuzzify.html#defuzz
'''Controls which defuzzification method will be used. 
* 'centroid': Centroid of area 
* 'bisector': bisector of area 
* 'mom' : mean of maximum 
* 'som' : min of maximum 
* 'lom' : max of maximum'''

# Auto-membership function population is possible with .automf(3, 5, or 7)
# we can pass our own names to the functions

steer = ['left++',
         'left+',
         'left',
         'center',
         'right',
         'right+',
         'right++']

dist = ['low', 'medium', 'high']

distance_front.automf(3, names=dist)
distance_left.automf(3, names=dist)
distance_right.automf(3, names=dist)
steering.automf(7, names=steer)#, invert=True)

# TODO definir mejor la granularidad de los conjuntos
'''distance_right['low'] = fuzz.trimf(distance_right.universe, [0, 0, 5])
distance_right['medium'] = fuzz.trimf(distance_right.universe, [0, 5, 10])
distance_right['high'] = fuzz.trimf(distance_right.universe, [5, 10, 10])

distance_left['low'] = fuzz.trimf(distance_left.universe, [0, 0, 5])
distance_left['medium'] = fuzz.trimf(distance_left.universe, [0, 5, 10])
distance_left['high'] = fuzz.trimf(distance_left.universe, [5, 10, 10])

distance_front['low'] = fuzz.trimf(distance_front.universe, [0, 0, 13])
distance_front['medium'] = fuzz.trimf(distance_front.universe, [0, 13, 25])
distance_front['high'] = fuzz.trimf(distance_front.universe, [13, 25, 25])'''

# TODO decidir bien el output de esta variable, cambiar nombres
# plantearse si las funciones no deberían ser distintas en el sentido de;
# quiero que el coche se mueva poco a poco al principio o que lo haga de una ya??
'''steering['low'] = fuzz.trimf(steering.universe, [-10, -10, 0])
steering['medium'] = fuzz.trimf(steering.universe, [-10, 0, 10])
steering['high'] = fuzz.trimf(steering.universe, [0, 10, 10])'''

# You can see how these look with .view()
'''distance_right['medium'].view()
distance_left.view()
distance_front.view()
steering.view()
plt.show()'''

# TODO esto es lo que habrá que pensar mejor

rules = []

for i, d_sides in enumerate(dist):  # crea las combinaciones de reglas
    for j, d_front in enumerate(dist):
        
        turn = steer[j+i]

        if j == len(dist)-1 and i == len(dist)-1:
            # para los 2 ultimos casos se queda en el medio
            turn = steer[(len(steer)//2)]
        # print(d_sides, d_front, turn)
        rules.append(
            ctrl.Rule(distance_right[d_sides] &
                      distance_front[d_front], steering[turn])
        )

# una disyunción de conjunciones
# TODO habrá que usar regals OR, NOT y AND??
# TODO SIMPLIFICAR?? :
'''
R(a) & F(a) -> 1
R(a) & F(b) -> 2
R(a) & F(c) -> 3
R(b) & F(a) -> 2
R(b) & F(b) -> 3
R(b) & F(c) -> 4
...
Es equivalente a...

R(a) & F(a) -> 1
R(a) & F(b) | R(b) & F(a) -> 2
R(a) & F(c) | R(b) & F(b)-> 3
R(b) & F(c) -> 4
...

'''
'''
right1 = ctrl.Rule(distance_right['low'] & distance_front['low'], steering['left++'])
right2 = ctrl.Rule(distance_right['low'] & distance_front['medium'], steering['left+'])
right3 = ctrl.Rule(distance_right['low'] & distance_front['high'], steering['left'])

right1 = ctrl.Rule(distance_right['medium'] & distance_front['low'], steering['left+'])
right2 = ctrl.Rule(distance_right['medium'] & distance_front['medium'], steering['left'])
right3 = ctrl.Rule(distance_right['medium'] & distance_front['high'], steering['center']) # TODO esta puede estar mal?

right1 = ctrl.Rule(distance_right['high'] & distance_front['low'], steering['left'])
right2 = ctrl.Rule(distance_right['high'] & distance_front['medium'], steering['center'])
right3 = ctrl.Rule(distance_right['high'] & distance_front['high'], steering['center'])
'''


for i, d_sides in enumerate(dist):
    for j, d_front in enumerate(dist):

        turn = steer[-((i+j)+1)]  # reverse list indexing, start at the last one

        if j == len(dist)-1 and i == len(dist)-1:
            turn = steer[(len(steer)//2)]
        #print(d_sides, d_front, turn)
        rules.append(
            ctrl.Rule(distance_left[d_sides] &
                      distance_front[d_front], steering[turn])
        )

#nx.draw(rules[0].graph)  # FIXME hacer que se plotee solo y bien
# https://networkx.org/documentation/stable/reference/drawing.html

print(len(rules), rules)
steering_ctrl = ctrl.ControlSystem(rules)
steering_ctrl_simul = ctrl.ControlSystemSimulation(steering_ctrl)

# Pass inputs to the ControlSystem using Antecedent labels
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
steering_ctrl_simul.input['distance_left'] = 7
steering_ctrl_simul.input['distance_right'] = 6
steering_ctrl_simul.input['distance_front'] = 12

# Crunch the numbers
steering_ctrl_simul.compute()

# steering_ctrl_simul.print_state()

output = steering_ctrl_simul.output['steering']
print(output)
print()
#steering.view(sim=steering_ctrl_simul)


#plt.show()


if __name__ == '__main__':
   numreps = 5

   for _ in range(numreps):
      x = bool(random.getrandbits(1))
      if x:
         L = random.randint(0,10)
         R = 0
      else:
         R = random.randint(0,10)
         L = 0
      F = random.randint(0,25)

      steering_ctrl_simul.input['distance_left'] = L
      steering_ctrl_simul.input['distance_right'] = R
      steering_ctrl_simul.input['distance_front'] = F

      steering_ctrl_simul.compute()

      output = steering_ctrl_simul.output['steering']
      print(output)
      print()
      steering.view(sim=steering_ctrl_simul)

      plt.title(f'(L: {L}, R: {R}, F: {F}) -> Out: {output}')
      plt.show()