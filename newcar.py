# This Code is Heavily Inspired By The YouTuber: Cheesy AI
# Code Changed, Optimized And Commented By: NeuralNine (Florian Dedov)
# This code has again been hoisted by the CGS Digital Innovation Department
# giving credit to the above authors for the benfit of our education in ML

import math
import random
import sys
import os

import neat
import pygame

# Constants
# WIDTH = 1600
# HEIGHT = 880

WIDTH = 1920
HEIGHT = 1080

CAR_SIZE_X = 95
CAR_SIZE_Y = 95

BORDER_COLOR = (255, 255, 255, 255)  # Color To Crash on Hit

current_generation = 0  # Generation counter
"""
The Car Class 

Throughout this section, you will need to explore each function
and provide extenive comments in the spaces denoted by the 
triple quotes(block quotes) """ """.
Your comments should describe each function and what it is doing, 
why it is necessary and where it is being used in the rest of the program.

"""


class Car:
    """1. This Function:
    This function is the 'Class Constructor'. This is a special type of function in a class that is immediately called when
    a new version of a class is created. Inside of a Class Constructor, any code can be run, however, the code should mainly
    have the objective of initializing the new classes properties/attributes.

    In this constructor, the car sprite is loaded into memory (a storage space where a computer can access information a lot
    quicker). The scale of the sprite is then calculated based on 2 defined values, 'CAR_SIZE_X' and 'CAR_SIZE_Y' (both being the value 50). The sprite
    is then copied into another variable called 'rotated_sprite'.

    The sprites starting position is then set to an array with the values: 830 (x) and 920 (y) and it's angle and speed are also initialised (both to 0).
    Another value called 'speed_set' is also initialised to False, this value will later be used to set the car's speed to a value greater than 0 (effectively
    starting the car).

    'self.center' is initialised to an array that will calculate the center point of the car. Both 'self.radars' and 'self.drawing_radars' are both initialised
    to empty arrays. 'self.alive' is a value used to check whether the car has crashed or not, and is initialised to True (alive). 'self.distance' and 'self.time'
    are both initialised to 0, both of these variables being a measure for how well this Car has performed.
    """

    def __init__(self):
        # Load Car Sprite and Rotate
        self.sprite = pygame.image.load(
            "car-green.png"
        ).convert()  # Convert Speeds Up A Lot
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite

        # self.position = [690, 740] # Starting Position
        self.position = [830, 920]  # Starting Position
        self.angle = 0
        self.speed = 0

        self.speed_set = False  # Flag For Default Speed Later on

        self.center = [
            self.position[0] + CAR_SIZE_X / 2,
            self.position[1] + CAR_SIZE_Y / 2,
        ]  # Calculate Center

        self.radars = []  # List For Sensors / Radars
        self.drawing_radars = []  # Radars To Be Drawn

        self.alive = True  # Boolean To Check If Car is Crashed

        self.distance = 0  # Distance Driven
        self.time = 0  # Time Passed

    """ 2. This Function:
    'draw()' is a custom function that aims to take the value of the Car in memory and draw it on the screen. This is done through 'screen.blit()' where 'blit'
    stands for 'Block Image Transfer'. It is used to draw a loaded object (object/image in memory) onto the screen. The 'screen' is the surface for where the
    image will be drawn. 'blit()' takes 2 compulsory parameters: 'source' and 'dest'. 'source' is the image you want to load onto the surface, and 'dest' is a
    tuple (array) of where on the screen you want the image to be drawn. 'draw_radar()' is the next function and is optional
    """

    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position)  # Draw Sprite
        self.draw_radar(screen)  # OPTIONAL FOR SENSORS

    """ 3. This Function:
    'draw_radar()' is an optional function that gives a visual representation of the cars sensors and radar. The function takes 2 parameters, 'self' (used to
    access it's own classes properties/attributes) and 'screen' (the screen of the computer). It starts by looping through all the radars in 'radars' and then
    creates a variable called 'position' that takes the current loop cycle's radar's position. The function then uses pygame's 'draw.line()' and 'draw.circle()'
    to draw them onto the screen. They both take 4 compulsory parameters with 2 of them being shared between both: 'surface' and 'colour'. 'surface', as discussed
    previously, is the canvas that you are drawing this object on, such as the screen. 'colour' takes a tuple (array) as it's value in the form of 3 elements, each
    corresponding to an RGB (Red, Green, Blue) value for 0 to 255. 'draw.line()' has 2 other compulsory arguments: 'start_pos' and 'end_pos', both taking a tuple
    in the form of a coordinate, for which a line will be drawn by pygame between the two. 'draw.circle' also has another 2 arguments: 'center' and 'radius'.
    'center' is a tuple that corresponds to the coordinate of where the circle will be drawn and 'radius' needs a value that corresponds with the amount of pxiels
    that the radius of the circle will be.
    """

    def draw_radar(self, screen):
        # Optionally Draw All Sensors / Radars
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    """ 4. This Function:
    'check_collision()' is a custom function that checks whether or not the corners of the car have had a collision with the racetrack borders. The function
    achieves this by using the 'get_at' method in the pygame library to obtain the pixel value at a specific coordinate on a surface, which in this context
    is the 'game_map' a.k.a the png file that represents the racetrack for the cars. The function checks each corner of the car using 'self.corners' and
    represents them as a variable called 'point'. 'point's 'x' and 'y' coordinate are used as parameters for 'get_at' and typecast to integers before being
    compared to 'BORDER_COLOR's value. If it is true that one of the points RGB value is the same as BORDER_COLOR's, then the 'self.alive' variable's value
    changed to false and the for loop breaks (it stops looping).
    """

    def check_collision(self, game_map):
        self.alive = True
        for point in self.corners:
            # If Any Corner Touches Border Color -> Crash
            # Assumes Rectangle
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break

    """ 5. This Function:
    'check_radar()' is a custom function that checks whether a radar-like system around the car collides with the racetrack border. This function has 4 main
    variables that are important: 
        - 'length'
        - 'x'
        - 'y'
        - 'BORDER_COLOR'
    'length' acts as the radius for the radar. While the function runs, it slowly increments by 1 to extend the radar. 'x' and 'y' are the point along the
    line of the radar that is being checked for a collision. 'BORDER_COLOR' is the RGB value that is compared to the RGB value of the point on the line, if
    RGB values match then there is a collison. This function initiates by calculating the starting x and y coordinates based on the input angle (adjusted 
    by the object's current angle) and trigonometric functions. It then enters a while loop that persists until the radar either collides with a border, 
    discerned by a matching color code, or reaches a maximum distance of 300 units. Within each loop iteration, it incrementally extends the radar's length 
    by one unit, thereby updating the x and y coordinates to examine a further point along the radar line. Upon exiting the loop, the function computes the
    distance between the center and the detected point using the Pythagorean theorem,which is then appended to the self.radars list along with the coordinates 
    of the detected point.
    """

    def check_radar(self, degree, game_map):
        length = 0
        x = int(
            self.center[0]
            + math.cos(math.radians(360 - (self.angle + degree))) * length
        )
        y = int(
            self.center[1]
            + math.sin(math.radians(360 - (self.angle + degree))) * length
        )

        # While We Don't Hit BORDER_COLOR AND length < 300 (just a max) -> go further and further
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length = length + 1
            x = int(
                self.center[0]
                + math.cos(math.radians(360 - (self.angle + degree))) * length
            )
            y = int(
                self.center[1]
                + math.sin(math.radians(360 - (self.angle + degree))) * length
            )

        # Calculate Distance To Border And Append To Radars List
        dist = int(
            math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2))
        )
        self.radars.append([(x, y), dist])

    """ 6. This Function:
    The 'update()' function is a custom function that aims to update the car's state every frame/iteration of the game loop. The beginning of this function makes
    sure that the car is moving first by checking whether 'speed_set' is True. If it isn't, then it is set to True and the 'speed' variable is then set to 20.
    The function then makes sure that the car is rotated in the right direction. It uses the 'rotate_center' angle, which in summary for when this function is
    actually discussed, basically returns a rotated version of the sprite based on the angle parameter it is given. The position of the car is then updated based
    on which angle the car is rotated on multiplied by the cars speed. The function then restricts the cars position on the x-coordinate to be within a certain
    range (that being 20px to the left edge and 120px to the right edge of the surface/screen). The function then increases the 'distance' variable by the 'speed'
    variable and the 'time' variable by 1. The function does what it did to the x-coordinate of the cars position to the y-coordinate. The function then sets the
    center of the car again based on the changes made to the values previously. Next, the function sets the values of the corners of the car and assigns them to
    the 'corners' variable. After updating all the values, the function then calls the 'check_collision()' function, using it's updated values as the parameters.
    It then clears the 'radar' list's elements. The function then sets up a for loop where 'd' will start at -90 degrees and increment by 45 degrees until it
    reaches 120 degrees. In each iteration of the loop, it plugs that value as the degree parameter for the 'check_radar()' function.
    """

    def update(self, game_map):
        # Set The Speed To 20 For The First Time
        # Only When Having 4 Output Nodes With Speed Up and Down
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True

        # Get Rotated Sprite And Move Into The Right X-Direction
        # Don't Let The Car Go Closer Than 20px To The Edge
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

        # Increase Distance and Time
        self.distance += self.speed
        self.time += 1

        # Same For Y-Position
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)

        # Calculate New Center
        self.center = [
            int(self.position[0]) + CAR_SIZE_X / 2,
            int(self.position[1]) + CAR_SIZE_Y / 2,
        ]

        # Calculate Four Corners
        # Length Is Half The Side
        length = 0.5 * CAR_SIZE_X
        left_top = [
            self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length,
            self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length,
        ]
        right_top = [
            self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length,
            self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length,
        ]
        left_bottom = [
            self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length,
            self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length,
        ]
        right_bottom = [
            self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length,
            self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length,
        ]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Check Collisions And Clear Radars
        self.check_collision(game_map)
        self.radars.clear()

        # From -90 To 120 With Step-Size 45 Check Radar
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    """ 7. This Function:
    'get_data()' is a custom function that aims to retreive data from 'radars' and scale it down. The function first assigns the radar values to 'radars' and
    then creates an array with 5 values all equalling 0 inside. It then iterates over each value in 'radars', assigning the radar distance divided by 30 as a
    typecast integer into 'return_values' current index determined by 'i'. The function then returns 'return_values'
    """

    def get_data(self):
        # Get Distances To Border
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    """ 8. This Function:
    'is_alive' is a custom function that will send a True boolean value if the 'alive' variable is True and vice versa if it is False.
    """

    def is_alive(self):
        # Basic Alive Function
        return self.alive

    """ 9. This Function:
    'get_reward()' is a custom function that returns a value based on how far the car has driven divided by half of it's size
    """

    def get_reward(self):
        # Calculate Reward (Maybe Change?)
        # return self.distance / 50.0
        return self.distance / (CAR_SIZE_X / 2)

    """ 10. This Function:
    'rotate_center()' is a custom function that rotates a sprite around it's center based on a specific degree given. The function first obtains the rectangle
    that surrounds the sprite and assigns it to the 'rectangle' variable. The function then rotates the sprite using the image parameter (the sprite) and
    rotates it by the given 'angle' parameter. A new variable is then created called 'rotated_rectangle' and it has all the properties of the 'rectangle'
    variable. 'rotated_rectangle' is then assigned a center based on the 'rotated_image's center. The 'rotated_image' variable is then assigned to itself but the
    subsurface method is appended create a new image object using the area defined by rotated_rectangle. This is done to cut off any extra space and to keep the 
    image dimensions consistent with the original. 'rotated_image' is then returned.
    """

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image


""" This Function:

1.  Empty Collections Initialization:
    nets: A list to hold neural networks corresponding to each genome.
    cars: A list to hold instances of the Car class that the neural networks control.
    
2.  Initializing PyGame and Display:
    The Pygame library is initialized, and a display window is created with the specified dimensions.

3.  Creating Neural Networks and Cars:
    For each genome passed into the run_simulation function:
    A neural network is created using the neat.nn.FeedForwardNetwork.create(g, config) method. The genome g and configuration config are used to create the network.
    The neural network is added to the nets list, and the genome's fitness is set to 0.
    A new instance of the Car class is created and added to the cars list.

4.  Clock and Font Settings:
    A PyGame clock is created to control the frame rate of the simulation.
    Different fonts are loaded for displaying information on the screen.

Updating the Generation Counter:

The current_generation global variable is incremented, indicating the current generation being simulated.
Main Simulation Loop:

The loop runs indefinitely, simulating the behavior of each car and updating the neural networks based on their actions.
Event Handling:

PyGame events are processed within the loop.
If the user closes the window or presses the escape key, the program exits.
Car Actions and Neural Network Activation:

For each car, the neural network is activated with the car's sensor data using nets[i].activate(car.get_data()).
The highest value in the output of the neural network determines the car's action: left, right, slow down, or speed up.
Updating Fitness and Car Movement:

For each alive car, the car's fitness is increased, and its position and movement are updated based on its action.
Checking Car Survival:

The number of cars that are still alive is counted.
If no cars are alive, the simulation loop is terminated.
Time Limit for Simulation:

A simple counter is used to roughly limit the duration of the simulation.
Drawing the Game Environment:

The game map is drawn on the screen.
For each alive car, its image is drawn on the screen.
Displaying Information:

Text information about the current generation, number of cars alive, and mean fitness is displayed on the screen.
Updating Display and Frame Rate:

The display is updated with the drawn elements.
The frame rate is controlled using the clock, ensuring a maximum of 60 frames per second.


"""


def run_simulation(genomes, config):
    # Empty Collections For Nets and Cars
    nets = []
    cars = []

    # Initialize PyGame And The Display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    # For All Genomes Passed Create A New Neural Network
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car())

    # Clock Settings
    # Font Settings & Loading Map
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    mean_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load("map.png").convert()  # Convert Speeds Up A Lot

    global current_generation
    current_generation += 1

    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while True:
        # Exit On Quit Event
        """
        Mod: added on keydown/esc to quit the game
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)

        # For Each Car Get The Acton It Takes
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10  # Left
            elif choice == 1:
                car.angle -= 10  # Right
            elif choice == 2:
                if car.speed - 2 >= 12:
                    car.speed -= 2  # Slow Down
            else:
                car.speed += 2  # Speed Up

        # Check If Car Is Still Alive
        # Increase Fitness If Yes And Break Loop If Not
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map)
                genomes[i][1].fitness += car.get_reward()

        if still_alive == 0:
            break

        counter += 1
        if counter == 30 * 40:  # Stop After About 20 Seconds
            break

        # Draw Map And All Cars That Are Alive
        screen.blit(game_map, (0, 0))
        for car in cars:
            if car.is_alive():
                car.draw(screen)

        # Display Info
        text = generation_font.render(
            "Generation: " + str(current_generation), True, (0, 0, 0)
        )
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)

        text = mean_font.render(
            "Mean Fitness: " + str(neat.StatisticsReporter().get_fitness_mean()),
            True,
            (0, 0, 0),
        )
        text_rect = text.get_rect()
        text_rect.center = (900, 530)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS


""" 1. This Section: The program main section
    The if __name__ == "__main__": block ensures that the code within it 
    only executes when the script is run directly (not when imported as a module).
    
    The config.txt file settings are loaded into the config variable using Config()
        neat.DefaultGenome
            Various options that control genome node activation, aggregation, bias, 
            compatibility, connection management, feed-forward architecture, response, 
            and weight settings.
            num_hidden, num_inputs, num_outputs: 
            Specifies the number of hidden, input, and output nodes, respectively.
            These parameters collectively define the structure and characteristics 
            of the neural networks represented by the genomes.
            
        neat.DefaultReproduction
            elitism: Specifies the number of elite genomes that are directly passed 
            to the next generation.
            survival_threshold: Sets the survival threshold, indicating the proportion 
            of genomes in each species that are considered for reproduction.
            
        neat.DefaultSpeciesSet
            compatibility_threshold: Specifies the compatibility threshold used for 
            determining species separation. Genomes with compatibility distance below 
            this threshold belong to the same species.
            
        neat.DefaultStagnation
            species_fitness_func: Defines the function to use when determining species 
            fitness. In this case, 'max' indicates that the maximum fitness of a 
            species is used.
            max_stagnation: Specifies the maximum number of generations a species 
            can remain stagnant before it's considered for stagnation and possible 
            extinction.
            species_elitism: Specifies the number of elite genomes from each species 
            that are preserved to the next generation.
            
        config_path
    
    
"""
if __name__ == "__main__":
    # Load Config
    config_path = "./config.txt"
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_simulation, 1000)
