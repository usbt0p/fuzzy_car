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
        road_width = np.arange(0, const.ROAD_WIDTH+1)
        road_length = np.arange(0, const.SCREEN_HEIGHT+1)
        steering_universe = np.arange(0, 20+1)

        # Antecedent/Consequent objects hold universe variables and membership functions
        distance_right = ctrl.Antecedent(road_width, 'distance_right')
        distance_left = ctrl.Antecedent(road_width, 'distance_left')
        distance_front = ctrl.Antecedent(road_length, 'distance_front')
        steering = ctrl.Consequent(steering_universe,
                                'steering', defuzzify_method=defuzz_method)
        self.steering = steering # para plottear en el debug

        # membership for right distance
        r_sets = 2
        divs_r = const.ROAD_WIDTH/r_sets
        distance_right['low'] = fuzz.trimf(distance_right.universe, [0, 0, divs_r])
        distance_right['medium'] = fuzz.trimf(
            distance_right.universe, [0, divs_r, divs_r*2])
        distance_right['high'] = fuzz.trimf(
            distance_right.universe, [divs_r, divs_r*2, divs_r*3])
        
        # membership for left distance
        l_sets = 2
        divs_l = const.ROAD_WIDTH/l_sets
        distance_left['low'] = fuzz.trimf(distance_left.universe, [0, 0, divs_l])
        distance_left['medium'] = fuzz.trimf(
            distance_left.universe, [0, divs_l, divs_l*2])
        distance_left['high'] = fuzz.trimf(
            distance_left.universe, [divs_l, divs_l*2, divs_l*3])
        
        # membership for front distance
        f_sets = 2
        divs_f = const.ROAD_WIDTH/f_sets
        distance_front['low'] = fuzz.trimf(distance_front.universe, [0, 0, divs_f])
        distance_front['medium'] = fuzz.trimf(
            distance_front.universe, [0, divs_f, divs_f*2])
        distance_front['high'] = fuzz.trimf(
            distance_front.universe, [divs_f, divs_f*2, divs_f*3])

        # membership for steering output
        s_sets = 2
        divs_s = 20/s_sets
        steering['no'] = fuzz.trimf(steering.universe, [0, 0, divs_s])
        steering['some'] = fuzz.trimf(steering.universe, [0, divs_s, divs_s*2])
        steering['a_lot'] = fuzz.trimf(steering.universe, [divs_s, divs_s*2, divs_s*3])

        # right rules
        '''
        right1 = ctrl.Rule(distance_right['low'], steering['a_lot'])
        right2 = ctrl.Rule(distance_right['medium'], steering['some'])
        right3 = ctrl.Rule(distance_right['high'], steering['no'])
        '''
        right1 = ctrl.Rule(distance_right['low'] & distance_front['low'], steering['a_lot'])
        right2 = ctrl.Rule(distance_right['low'] & distance_front['medium'], steering['some'])
        right3 = ctrl.Rule(distance_right['low'] & distance_front['high'], steering['some'])

        right4 = ctrl.Rule(distance_right['medium'] & distance_front['low'], steering['some'])
        right5 = ctrl.Rule(distance_right['medium'] & distance_front['medium'], steering['some'])
        right6 = ctrl.Rule(distance_right['medium'] & distance_front['high'], steering['no']) # TODO esta puede estar mal?

        right7 = ctrl.Rule(distance_right['high'] & distance_front['low'], steering['no'])
        right8 = ctrl.Rule(distance_right['high'] & distance_front['medium'], steering['no'])
        right9 = ctrl.Rule(distance_right['high'] & distance_front['high'], steering['no'])

        # left rules
        left1 = ctrl.Rule(distance_left['low'], steering['a_lot'])
        left2 = ctrl.Rule(distance_left['medium'], steering['some'])
        left3 = ctrl.Rule(distance_left['high'], steering['no'])
        
        '''Usamos 2 controladores ya que no se puede usar uno y no mandar input a uno de 
        los antecedentes.
        Si se mandan datos de las 2 variables, las reglas se ven "contaminadas" porque 
        dependen del orden de declaración.'''
        
        rules_right = [right1, right2, right3, right4, right5, right6, right7, right8, right9]
        # setup and begin simulation for the right controller
        steering_ctrl_right = ctrl.ControlSystem(rules_right)
        self.ctrl_simul_right = ctrl.ControlSystemSimulation(steering_ctrl_right)

        rules_left = [left1, left2, left3]
        # setup and begin simulation for the left controller
        steering_ctrl_left = ctrl.ControlSystem(rules_left)
        self.ctrl_simul_left = ctrl.ControlSystemSimulation(steering_ctrl_left)


    def right_controller(self, sensor_right, sensor_front, debug=False):

        self.ctrl_simul_right.input['distance_right'] = sensor_right
        self.ctrl_simul_right.input['distance_front'] = sensor_front
        self.ctrl_simul_right.compute()    # Crunch the numbers
        output = self.ctrl_simul_right.output['steering']

        if debug:
            print("\n ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ NEW DEBUG ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n")
            self.ctrl_simul_right.print_state()
            self.steering.view(sim=self.ctrl_simul_right)
            plt.title(f'In: (R: {sensor_right}, F: {sensor_front}) -> Out: ({output})')
            plt.show()

        return output
    
    def left_controller(self, sensor_left, debug=False):

        self.ctrl_simul_left.input['distance_left'] = sensor_left
        self.ctrl_simul_left.compute()    # Crunch the numbers
        output = self.ctrl_simul_left.output['steering']

        if debug:
            print("\n ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ NEW DEBUG ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n")
            self.ctrl_simul_left.print_state()
            self.steering.view(sim=self.ctrl_simul_left)
            plt.title(f'In: (L: {sensor_left}) -> Out: ({output})')
            plt.show()

        return output


if __name__ == '__main__':
    # 400//50 = 8, 400//8 = 5
    # const.ROAD_WIDTH = 400

    #1 # TODO : primero hay que incorporar la distancia en y: cambiar con mayor o menor grado??
    
    #2 # TODO: después de conseguir eso, commitear los cambios. Nueva rama o actual¿

    #3 # TODO : ahora toca crear la funcion que manda solo el sensor del lado adecuado
    # Ya que las 2 hacen lo mismo, puede tener solo una, y mandar el que corresponda
    
    #4 # TODO : luego, toca probar los resultados en el coche

    #5 # TODO : finalmente, ajustar y mergear. Los ajustes pueden ser de reglas, defuzz, de MF's, etc
    


    methods = ['centroid', 'bisector', 'mom', 'som', 'lom']
    control = FuzzyControl(methods[0])
    tests = range(0, 400+1, 100)
    fronts = range(0, const.SCREEN_HEIGHT+1, 150)

    for distance in tests:
        for front in fronts:
            r = control.right_controller(distance, front, debug=True)
            print(r)

            l = control.left_controller(distance, debug=True)
            print(l)
