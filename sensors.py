from elements.environment import Constants as const


class Sensors:
    # TODO test
    def obstacle_sensor_y_axis(self, obstacles):
        distances = []  # una lista ya que podría querer computarlo para mas de un obstáculo
        # TODO poner un if para casos en los que no haya obstaculo en frente
        for obstacle in obstacles:
            if self.y > obstacle.y + obstacle.height:  # para sensor cuando esté detrás del coche
                distance_y_axis = abs(
                    (obstacle.y + obstacle.height) - (self.y))
                distances.append(distance_y_axis)
            else:
                # FIXME debe de haber una mejor solucion... 
                # hay que gestionar esto en otra funcion quizá
                distances.append(const.SCREEN_HEIGHT)

        return distances
    # TODO test
    def obstacle_sensor_right(self, obstacles):
        distances = []

        for obstacle in obstacles:
            # esto es el medio del coche
            if self.front_x_coords > obstacle.front_x_coords:
                distance_right = self.front_x_coords - obstacle.front_x_coords
                distances.append(distance_right)
            else:
                # FIXME debe de haber una mejor solucion...
                # hay que gestionar esto en otra funcion quizá
                distances.append(const.ROAD_WIDTH) 

        return distances
    # TODO test
    def obstacle_sensor_left(self, obstacles):
        distances = []

        for obstacle in obstacles:
            # esto es el medio del coche
            if self.front_x_coords < obstacle.front_x_coords:
                distance_left = obstacle.front_x_coords - self.front_x_coords
                distances.append(distance_left)
            else:
                # FIXME debe de haber una mejor solucion...
                # hay que gestionar esto en otra funcion quizá
                distances.append(const.ROAD_WIDTH)

        return distances
