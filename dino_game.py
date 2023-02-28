#!/usr/bin/env python3
import pygame
import sys
import numpy as np

# This is my first attempt writing a python version of the chrome dino game
pygame.init()
# create the neural network
input_layer_size = 2
hidden_layer_size = 3
output_layer_size = 1

# randomly initialize the weights and biases for the input and hidden layers
weights_input_hidden = np.random.rand(input_layer_size, hidden_layer_size)
bias_hidden = np.random.rand(1, hidden_layer_size)
weights_hidden_output = np.random.rand(hidden_layer_size, output_layer_size)
bias_output = np.random.rand(1, output_layer_size)
print("Initial weights_input_hidden:\n", weights_input_hidden)
print("Initial bias_hidden:\n", bias_hidden)
print("Initial weights_hidden_output:\n", weights_hidden_output)
print("Initial bias_output:\n", bias_output)

# define the sigmoid activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# define the feedforward function to make predictions
def feedforward(inputs):
    # calculate the values for the hidden layer
    hidden_layer = sigmoid(np.dot(inputs, weights_input_hidden) + bias_hidden)

    # calculate the value for the output layer
    output_layer = sigmoid(np.dot(hidden_layer, weights_hidden_output) + bias_output)

    # return the output layer value as the prediction
    return output_layer

# set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
count_level = 0
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chrome Dino Game")

# create a font object
font = pygame.font.Font(None, 40)
##########################
# create a cactus and a dinosaur rectangle
##########################
cactus_rect = pygame.Rect(500, 300, 20, 50)
dino_rect = pygame.Rect(20, 300, 50, 50)
is_jumping = False
gravity  = 0.1
velocity = 0
should_jump = 0

# start the game loop
while True:
    # check for user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
# if want to maually control the game uncomment this section & comment the NN section
#        if event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_SPACE and not is_jumping:
#                is_jumping = True
#                velocity = -5  # set the initial velocity of the jump

# the NN sets the should_jump variable to 1 if it thinks the dinosaur should jump
    if should_jump==1:
        if not is_jumping:
            is_jumping = True
            velocity = -5  # set the initial velocity of the jump

    # update the game state
    cactus_rect.x -= 3+(0.2*count_level)  # move the cactus towards the dinosaur

    # update the game state
    if is_jumping:
       # calculate the new vertical position of the dinosaur
       dino_rect.y += velocity
       velocity += gravity
       # check if the dinosaur has landed
       if dino_rect.y > 300:
           dino_rect.y = 300
           is_jumping = False
           velocity = 0

    # keep the dinosaur within the screen boundaries
    if dino_rect.y > WINDOW_HEIGHT - dino_rect.height:
        print("boundaries error", dino_rect.y )
        pygame.quit()
        sys.exit()

    # check if the cactus goes off-screen
    if cactus_rect.x < 0:
        # reset the cactus position
        cactus_rect.x = WINDOW_WIDTH
        cactus_rect.y = 300
        count_level += 1
    # check for collision between the cactus and the dinosaur
    if cactus_rect.colliderect(dino_rect):
        print("Game over")

    # draw the game screen
    game_window.fill((255, 255, 255))  # fill the screen with white
    pygame.draw.rect(game_window, (0, 255, 0), dino_rect)  # draw the dinosaur rectangle on the game window
    pygame.draw.rect(game_window, (255, 0, 0), cactus_rect)  # draw the cactus rectangle on the game window


    # render the score text
    score_text = font.render(f"Score: {count_level}", True, (0, 0, 0))
    # draw the score text on the game window
    game_window.blit(score_text, (10, 10))
    
    pygame.display.update()


    # get the game current state so i can feed it to the neural network
    distance = cactus_rect.x - dino_rect.x
    speed_of_cactus =  count_level
    # call the neural network to get the next move
    # make a prediction using the neural network
    inputs = np.array([distance, speed_of_cactus]).reshape(1, -1)
    should_jump = feedforward(inputs) > 0.8

    # set the frame rate
    pygame.time.delay(7)