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
        norm = 6 # BUG por que al bajarlo a 5 se hace la funcion rara?
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
            distance_side.universe, [divs_r, divs_r*2, divs_r*3]) #FIXME
        
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

        side4 = ctrl.Rule(distance_side['medium'] & distance_front['low'], steering['some'])
        side5 = ctrl.Rule(distance_side['medium'] & distance_front['medium'], steering['no'])
        side6 = ctrl.Rule(distance_side['medium'] & distance_front['high'], steering['no']) # TODO esta puede estar mal?

        side7 = ctrl.Rule(distance_side['high'], steering['no'])
        
        '''Usamos 2 controladores ya que no se puede usar uno y no mandar input a uno de 
        los antecedentes.
        Si se mandan datos de las 2 variables, las reglas se ven "contaminadas" porque 
        dependen del orden de declaración.'''
        
        rules_side = [side1, side2, side3, side4, side5, side6, side7]#, side8, side9]
        # setup and begin simulation for the right controller
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
    # 400//50 = 8, 400//8 = 5
    # const.ROAD_WIDTH = 400

    #1 #  : primero hay que incorporar la distancia en y: cambiar con mayor o menor grado??
    
    #2 # : después de conseguir eso, commitear los cambios. Nueva rama o actual¿

    #3 # : ahora toca crear la funcion que manda solo el sensor del lado adecuado
    # Ya que las 2 hacen lo mismo, puede tener solo una, y mandar el que corresponda
    
    #4 # : luego, toca probar los resultados en el coche

    #5 # TODO : finalmente, ajustar y mergear. Los ajustes pueden ser de reglas, defuzz, de MF's, etc
    # ajuste 1: distintas MF's dan distintos resultados
    # vamos a probar a cambiar la mf de la distancia frontal:
    # esta debe ser 0 en distancias lejanas para que el coche no se mueva si esta lejos
    # no hay workarounds en otras funciones, porque se deben mandar todos los antececentes
    


    methods = ['centroid', 'bisector', 'mom', 'som', 'lom']
    # https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.defuzzify.html#defuzz
    '''Controls which defuzzification method will be used. 
    * 'centroid': Centroid of area 
    * 'bisector': bisector of area 
    * 'mom' : mean of maximum 
    * 'som' : min of maximum 
    * 'lom' : max of maximum'''

    control = FuzzyControl(methods[0])

    tests = range(0, const.ROAD_WIDTH+1, 100)
    fronts = range(0, const.SCREEN_HEIGHT+1, 150)

    for front in fronts:
        r = control.side_controller(250, front, debug=True)
        print(r)

    '''tests = range(0, 400+1, 100)
    fronts = range(0, const.SCREEN_HEIGHT+1, 150)

    for distance in tests:
        for front in fronts:
            r = control.side_controller(distance, front, debug=True)
            print(r)'''

    # TODO what to do with this: useful?
    '''rules = []

    for i, d_sides in enumerate(dist):  # crea las combinaciones de reglas
        for j, d_front in enumerate(dist):
            
            turn = steer[j+i]

            if j == len(dist)-1 and i == len(dist)-1:
                # para los 2 ultimos casos se queda en el medio
                turn = steer[(len(steer)//2)]
            print(d_sides, d_front, turn)
            rules.append(
                ctrl.Rule(distance_right[d_sides] &
                        distance_front[d_front], steering[turn])
            )'''
