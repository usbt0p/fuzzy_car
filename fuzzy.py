import numpy as np
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from elements.environment import Constants as const

class FuzzyControl:

    def __init__(self, defuzz_method):
        # Declare al future attributes for reference
        self.ctrl_steering = None
        self.ctrl_move_to_center = None

        self.defuzz_method = defuzz_method
        self.memberships = []

        self.steering = None # Variables for use in debug 
        self.steer_center = None

        # minus the car's width since it can't get out of road boundaries
        available_road_space = ((const.ROAD_WIDTH+1)-const.CAR_WIDTH)//2

        road_width = np.arange(0, available_road_space)
        road_length = np.arange(0, (const.SCREEN_HEIGHT+1))
        norm = 6 # this parameter changes the max value of the outputed steering. 
        # it roughly maps to the 'acceleration' the car will have when turning
        steering_universe = np.arange(0, norm+1)

        # Antecedent/Consequent objects hold universe variables and membership functions
        distance_side = ctrl.Antecedent(road_width, 'distance_right')
        distance_front = ctrl.Antecedent(road_length, 'distance_front')
        steering = ctrl.Consequent(steering_universe,
                                'steering', defuzzify_method=defuzz_method)
        self.steering = steering # para plottear en el debug

        # membership for right distance
        distance_side.automf(5, variable_type='quant')
        self.memberships.append(distance_side)
        
        # membership for front distance
        distance_front.automf(5, variable_type='quant')
        self.memberships.append(distance_front)

        # membership for steering output
        steering.automf(5, variable_type='quant')
        self.memberships.append(steering)

        # side + front rules, automf values: 'lower'; 'low'; 'average'; 'high', or 'higher'
        # we have combinations of two 5-valued variables, so: 
        # 5*5 = 25 combinations without accounting consequents, but some rules are ignored

        # reaction to close obstacles. the first rule being the one with the highest priority
        # makes the car overpower the steering when there are other non-close obstacles activating the other rules
        rules = [ctrl.Rule(distance_side['lower'] & distance_front['lower'], steering['higher'])]
        rules.append(ctrl.Rule(distance_side['lower'] & distance_front['low'], steering['average']))
        rules.append(ctrl.Rule(distance_side['lower'] & distance_front['average'], steering['low']))
        # rules for supressing influence from far away obstacles
        rules.append(ctrl.Rule(distance_side['lower'] & distance_front['high'], steering['lower']))
        rules.append(ctrl.Rule(distance_side['lower'] & distance_front['higher'], steering['lower']))
        
        # rules for for medium-low side reaction 
        # TODO temporarily removed: these seem be almost a better turned off, + better performance 
        '''rules.append(ctrl.Rule(distance_side['low'] & distance_front['lower'], steering['average']))
        rules.append(ctrl.Rule(distance_side['low'] & distance_front['low'], steering['low']))
        rules.append(ctrl.Rule(distance_side['low'] & distance_front['average'], steering['lower']))'''
        # rules for supressing influence from far away obstacles
        rules.append(ctrl.Rule(distance_side['low'] & distance_front['high'], steering['lower']))
        rules.append(ctrl.Rule(distance_side['low'] & distance_front['higher'], steering['lower']))
        
        # supress influence from obstacles that are close to the front but far away from the side
        rules.append(ctrl.Rule(distance_side['higher'] |  distance_side['high'] | distance_side['average'] 
                               & distance_front['lower'], steering['lower']))
        rules.append(ctrl.Rule(distance_side['higher'] |  distance_side['high'] | distance_side['average'] 
                               & distance_front['low'], steering['lower']))

        # setup and begin simulation for the side controller
        steering_ctrl = ctrl.ControlSystem(rules)
        self.ctrl_steering = ctrl.ControlSystemSimulation(steering_ctrl)
        # end of first controller declarations




        # CENTER CONTROLLER
        center_distance = np.arange(0, available_road_space//2)

        distance_to_center = ctrl.Antecedent(center_distance, 'distance_to_center')
        steer_center = ctrl.Consequent(steering_universe, 'steer_center', defuzzify_method='bisector')
        self.steer_center = steer_center

        distance_to_center.automf(5, variable_type='quant') #variable_type='quant')
        self.memberships.append(distance_to_center)
        steer_center.automf(4, names=['lower', 'low', 'average', 'high'])
        self.memberships.append(steer_center)

        center_rules = [] #ctrl.Rule(distance_to_center['lower'], steer_center['lower'])
        center_rules.append(ctrl.Rule(distance_to_center['low'] | distance_to_center['lower'], steer_center['lower']))
        center_rules.append(ctrl.Rule(distance_to_center['average'], steer_center['low']))
        center_rules.append(ctrl.Rule(distance_to_center['high'], steer_center['average']))
        center_rules.append(ctrl.Rule(distance_to_center['higher'], steer_center['high']))

        # setup and begin simulation for the center movement controller
        move_to_center_ctrl = ctrl.ControlSystem(center_rules)
        self.ctrl_move_to_center = ctrl.ControlSystemSimulation(move_to_center_ctrl)

    def side_controller(self, x_sensor, y_sensor, debug=False):

        self.ctrl_steering.input['distance_right'] = x_sensor
        self.ctrl_steering.input['distance_front'] = y_sensor
        self.ctrl_steering.compute()    # Crunch the numbers
        output = self.ctrl_steering.output['steering']

        if debug:
            print("\n ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ NEW DEBUG ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n")
            self.ctrl_steering.print_state()
            self.steering.view(sim=self.ctrl_steering)
            print(self.ctrl_steering._get_inputs())
            print(self.ctrl_steering.output)
            plt.title(f'(side: {x_sensor}, front: {y_sensor}) -> steer: ({output})')
            plt.show()

        return output
    
    def center_controller(self, location_sensor, debug=False):
        self.ctrl_move_to_center.input['distance_to_center'] = location_sensor

        self.ctrl_move_to_center.compute()    # Crunch the numbers
        output = self.ctrl_move_to_center.output['steer_center']

        if debug:
            print("\n ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ NEW DEBUG ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n")
            self.ctrl_move_to_center.print_state()
            self.steer_center.view(sim=self.ctrl_move_to_center)
            print(self.ctrl_move_to_center._get_inputs())
            print(self.ctrl_move_to_center.output)
            plt.title(f'(distance_to_center: {location_sensor}) -> steer: ({output})')
            plt.show()

        return output



if __name__ == '__main__':
    methods = ['centroid', 'bisector', 'mom', 'som', 'lom']
    # https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.defuzzify.html#defuzz

    control = FuzzyControl(methods[2])
    '''for mem in control.memberships:
        mem.view()
    plt.show()
    '''
    # TODO pasos para añadir el control de retorno al centro:
    # 1- incorporar todos los elementos en modulo de logica difusa, que acepte input
    # 2- cambiar las llamadads a la función del controlador
    # 3- hacer que en el main se recogan las lecturas del sensor de centro en una variable
    # 4- pasarla al coche 
    # 5- ver que se rompe
    # 6- si no funciona separar en otro controlador que se active bajo ciertas condiciones

    '''dists_center = range(0, (
        ((const.ROAD_WIDTH+1)-const.CAR_WIDTH)//4
            ), 20
        )
    
    for center in dists_center:
        r = control.center_controller(center, debug=True)
        print(r)'''

    
    tests = range(0, const.ROAD_WIDTH+1, 100)
    fronts = range(0, const.SCREEN_HEIGHT+1, 150)

    for front in fronts:
        r = control.side_controller(50, front, debug=True)
        print(r)
