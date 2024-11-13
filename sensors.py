from elements.environment import Constants as const


class Sensors:
    # TODO test
    def obstacle_sensor_y_axis(self, obstacles):
        distances = []  # una lista ya que podría querer computarlo para mas de un obstáculo
        # TODO poner un if para casos en los que no haya obstaculo en frente
        for obstacle in obstacles:
            # el sensor no se para cuando el obstaculo esta detrás
                distance_y_axis = abs(
                    (obstacle.y + obstacle.height) - (self.y))
                distances.append(distance_y_axis)
        return distances
    
    # TODO test
    def obstacle_sensor_right(self, obstacles):
        distances = []

        for obstacle in obstacles:
            if self.front_x_coords >= obstacle.front_x_coords:
                distance_right = self.front_x_coords - obstacle.front_x_coords
                distances.append(distance_right)
            else:
                distances.append(None) 

        return distances
    # TODO test
    def obstacle_sensor_left(self, obstacles):
        distances = []

        for obstacle in obstacles:
            if self.front_x_coords <= obstacle.front_x_coords:
                distance_left = obstacle.front_x_coords - self.front_x_coords
                distances.append(distance_left)
            else:
                distances.append(None)

        return distances
    
    def relative_road_location(self):
        """Returns the distance from the center of the road to the car's front"""
        return abs(const.ROAD_WIDTH // 2 - self.front_x_coords)
    

if __name__ == '__main__':
    from elements.car import Car
    from elements.obstacle import Obstacle
    car = Car(None, (20, 50), (0, 0), 20, None)

    print('road width:', const.ROAD_WIDTH)
    print('half road width:', const.ROAD_WIDTH // 2)

    print('car x: ', car.x)
    dist_to_center = car.relative_road_location()
    print('car dist to center:', dist_to_center)


