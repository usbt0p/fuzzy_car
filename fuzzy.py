import numpy as np
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from elements.environment import Constants as const
import skfuzzy as fuzz


class FuzzyControl:

    def __init__(self, defuzz_method):
        # Declare al future attributes for reference
        self.steering = None
        self.ctrl_simul_right = None
        self.ctrl_simul_right = None
        self.defuzz_method = defuzz_method

        # define our universes
        road_width = np.arange(0, (const.ROAD_WIDTH+1)//2) # FIXME averiguar como afecta esta normalizacióna al movimiento!!
        road_length = np.arange(0, (const.SCREEN_HEIGHT+1)//2)
        norm = 4 # BUG por que al bajarlo a 5 se hace la funcion rara?
        steering_universe = np.arange(0, norm+1) # TODO normalizar en funcion de lo mucho que se mueva, y de la velocidad!!!

        # Antecedent/Consequent objects hold universe variables and membership functions
        distance_side = ctrl.Antecedent(road_width, 'distance_right')
        distance_front = ctrl.Antecedent(road_length, 'distance_front')
        steering = ctrl.Consequent(steering_universe,
                                'steering', defuzzify_method=defuzz_method)
        self.steering = steering # para plottear en el debug

        # membership for right distance
        r_sets = 2
        divs_r = const.ROAD_WIDTH/r_sets
        distance_side['low'] = fuzz.trimf(distance_side.universe, [0, 0, divs_r])
        distance_side['medium'] = fuzz.trimf(
            distance_side.universe, [0, divs_r, divs_r*2])
        distance_side['high'] = fuzz.trimf(
            distance_side.universe, [divs_r, divs_r*2, divs_r*3])
        
        # membership for front distance
        f_sets = 2
        divs_f = const.SCREEN_HEIGHT/f_sets
        distance_front['low'] = fuzz.trimf(distance_front.universe, [0, 0, divs_f])
        distance_front['medium'] = fuzz.trimf(
            distance_front.universe, [0, divs_f, divs_f*2])
        distance_front['high'] = fuzz.trimf(
            distance_front.universe, [divs_f, divs_f*2, divs_f*3])

        # membership for steering output
        s_sets = 2
        divs_s = norm/s_sets
        steering['no'] = fuzz.trimf(steering.universe, [0, 0, divs_s])
        steering['some'] = fuzz.trimf(steering.universe, [0, divs_s, divs_s*2])
        steering['a_lot'] = fuzz.trimf(steering.universe, [divs_s, divs_s*2, divs_s*3])

        # side + front rules
        side1 = ctrl.Rule(distance_side['low'] & distance_front['low'], steering['a_lot'])
        side2 = ctrl.Rule(distance_side['low'] & distance_front['medium'], steering['some'])
        side3 = ctrl.Rule(distance_side['low'] & distance_front['high'], steering['some'])

        side4 = ctrl.Rule(distance_side['medium'] & distance_front['low'], steering['no'])
        side5 = ctrl.Rule(distance_side['medium'] & distance_front['medium'], steering['no'])
        side6 = ctrl.Rule(distance_side['medium'] & distance_front['high'], steering['no'])

        # FIXME poner o no en funcion de la performance 
        # mezclando con otro controlador de cercania podria funcionar
        '''side7 = ctrl.Rule(distance_side['high'] & distance_front['low'], steering['no'])
        side8 = ctrl.Rule(distance_side['high'] & distance_front['medium'], steering['no'])
        side9 = ctrl.Rule(distance_side['high'] & distance_front['high'], steering['no'])'''

        
        # setup and begin simulation for the side controller
        rules_side = [side1, side2, side3, side4, side5, side6]#, side7, side8, side9]
        steering_ctrl_right = ctrl.ControlSystem(rules_side)
        self.ctrl_simul_right = ctrl.ControlSystemSimulation(steering_ctrl_right)


    def side_controller(self, x_sensor, y_sensor, debug=False):

        self.ctrl_simul_right.input['distance_right'] = x_sensor
        self.ctrl_simul_right.input['distance_front'] = y_sensor
        self.ctrl_simul_right.compute()    # Crunch the numbers
        output = self.ctrl_simul_right.output['steering']

        if debug:
            print("\n ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ NEW DEBUG ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n")
            self.ctrl_simul_right.print_state()
            self.steering.view(sim=self.ctrl_simul_right)
            print(self.ctrl_simul_right._get_inputs())
            print(self.ctrl_simul_right.output)
            plt.title(f'In: (R: {x_sensor}, F: {y_sensor}) -> Out: ({output})')
            plt.show()

        return output


if __name__ == '__main__':
    methods = ['centroid', 'bisector', 'mom', 'som', 'lom']
    # https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.defuzzify.html#defuzz

    control = FuzzyControl(methods[0])

    tests = range(0, const.ROAD_WIDTH+1, 100)
    fronts = range(0, const.SCREEN_HEIGHT+1, 150)

    for front in fronts:
        r = control.side_controller(250, front, debug=True)
        print(r)
