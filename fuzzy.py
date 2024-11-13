import numpy as np
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from elements.environment import Constants as const

class FuzzyControl:

    def __init__(self, defuzz_method):
        # Declare al future attributes for reference
        self.steering = None
        self.ctrl_simulator = None
        self.defuzz_method = defuzz_method
        self.memberships = []

        road_width = np.arange(0, ((const.ROAD_WIDTH+1)-const.CAR_WIDTH)//2)
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
        steering_ctrl_right = ctrl.ControlSystem(rules)
        self.ctrl_simulator = ctrl.ControlSystemSimulation(steering_ctrl_right)


    def side_controller(self, x_sensor, y_sensor, debug=False):

        self.ctrl_simulator.input['distance_right'] = x_sensor
        self.ctrl_simulator.input['distance_front'] = y_sensor
        self.ctrl_simulator.compute()    # Crunch the numbers
        output = self.ctrl_simulator.output['steering']

        if debug:
            print("\n ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ NEW DEBUG ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n")
            self.ctrl_simulator.print_state()
            self.steering.view(sim=self.ctrl_simulator)
            print(self.ctrl_simulator._get_inputs())
            print(self.ctrl_simulator.output)
            plt.title(f'In: (R: {x_sensor}, F: {y_sensor}) -> Out: ({output})')
            plt.show()

        return output


if __name__ == '__main__':
    methods = ['centroid', 'bisector', 'mom', 'som', 'lom']
    # https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.defuzzify.html#defuzz

    control = FuzzyControl(methods[0])
    for mem in control.memberships:
        mem.view()
    plt.show()

    '''
    tests = range(0, const.ROAD_WIDTH+1, 100)
    fronts = range(0, const.SCREEN_HEIGHT+1, 150)

    for front in fronts:
        r = control.side_controller(250, front, debug=True)
        print(r)'''
