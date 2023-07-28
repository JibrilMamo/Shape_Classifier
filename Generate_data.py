import pygame
import math
import os
import random as r
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 64
screen_height = 64



# Colors (RGB format)
white = (255, 255, 255)
Black = (0, 0, 0)

# Set up the Pygame window
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(white)
pygame.display.set_caption("Make Shapes")


def circle():
    # Calculate the position of the circle's center to keep it within the canvas
    x = r.randint(5, screen_width - 5)
    y = r.randint(5, screen_height - 5)

    # Calculate the radius of the circle, limiting it to a maximum of 50 pixels
    radius = r.randint(5, min(min(screen_width - x,x), min(screen_height - y,y), screen_height // 2 -10))

    # Calculate varying width and height radii for the circle
    width_radius = r.randint(5, radius)
    height_radius = r.randint(5, radius)

    pygame.draw.ellipse(screen, (0, 0, 0), (x - width_radius, y - height_radius, width_radius * 2, height_radius * 2), 2)

def draw_polygon(screen, points):
    pygame.draw.polygon(screen, (0,0,0), points, 1)
    pygame.display.flip()

def draw_random_polygon(screen, num_points):
    while True:
        points = []
        min_distance = 8
        while len(points) < num_points:
            x = r.randint(5, screen_width - 5)
            y = r.randint(5, screen_height - 5)
            valid_point = True
            for point in points:
                x_diff = abs(point[0] - x)
                y_diff = abs(point[1] - y)
                if x_diff < min_distance or y_diff < min_distance:
                    valid_point = False
                    break
            if valid_point:
                points.append((x, y))

        if num_points == 3:
            break  # No need to check for convexity, a triangle is always convex

        if is_convex(points) and abs(points[0][0]-points[0][1]) >= 5:
            break

    screen.fill((255,255,255))  # Fill the screen with black
    draw_polygon(screen, points)

def is_convex(points):
    def dot_product(p1, p2):
        # Calculate the dot product of vectors p1 and p2
        return p1[0] * p2[0] + p1[1] * p2[1]

    # Check if the polygon formed by the points is convex
    if len(points) != 4:
        return False

    def cross_product(p1, p2, p3):
        # Calculate the cross product of vectors (p2 - p1) and (p3 - p2)
        return (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])

    prev_cross = cross_product(points[-2], points[-1], points[0])
    for i in range(len(points) - 1):
        curr_cross = cross_product(points[i - 1], points[i], points[i + 1])
        if curr_cross * prev_cross < 0:
            return False
        prev_cross = curr_cross

    return True




# Main game loop
count = 0
while count <= 150:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Create a folder for shapes if it doesn't exist
    if not os.path.exists("shapes"):
        os.mkdir("shapes")

    # Draw and save the square
    screen.fill(white)
    draw_random_polygon(screen,4)
    pygame.display.flip()
    pygame.image.save(screen, f"shapes/square/square_{count}.png")
    # Draw and save the circle
    screen.fill(white)
    circle()
    pygame.display.flip()
    pygame.image.save(screen, f"shapes/circle/circle_{count}.png")
    # Draw and save the triangle
    screen.fill(white)
    draw_random_polygon(screen,3)
    pygame.display.flip()
    pygame.image.save(screen, f"shapes/triangle/triangle_{count}.png")
    count += 1

pygame.quit()
quit()



