import tensorflow as tf
from keras.models import load_model
import numpy as np
from PIL import Image
import os
import pygame

def draw_text(window, text, position, color):
    font = pygame.font.SysFont(None, 30)
    text_surface = font.render(text, True, color)
    text_width = text_surface.get_width()
    window.blit(text_surface, (position[0] - text_width // 2, position[1]))

# Load the image classification model
model = load_model('my_image_classifier.keras')

def preprocess_image(img):
    img = img.convert("RGB")
    img = img.resize((64, 64))
    img_array = np.array(img)
    if img_array.shape[-1] == 4:
        img_array = img_array[:, :, :4]
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_image(img):
    img = img.resize((64, 64))
    img = preprocess_image(img)
    predictions = model.predict(img)
    class_index = np.argmax(predictions)
    probability = np.max(predictions)
    return class_index, probability

# Initialize Pygame
pygame.init()

# Window dimensions
width, height = 600, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the Pygame window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Drawing with Mouse")

# Variables to track drawing
drawing = False
last_pos = None

# Main game loop
running = True
window.fill(WHITE)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                drawing = True
                last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                drawing = False
                # Get the drawn image from the window and predict
                drawn_surface = pygame.surfarray.array3d(window)
                drawn_image = Image.fromarray(drawn_surface)
                predicted_class_index, prediction_probability = predict_image(drawn_image)

                class_labels = ['circle', 'square', 'triangle']
                predicted_class_label = class_labels[predicted_class_index]
                draw_text(window,f"{predicted_class_label}, {prediction_probability*100:.3f}%",(width//2,10),BLACK)

                #print(f"Predicted class: {predicted_class_label}, Certainty: {prediction_probability:.2f}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                window.fill(WHITE)

        if drawing:
            current_pos = event.pos
            pygame.draw.line(window, BLACK, last_pos, current_pos, 2)
            last_pos = current_pos

    pygame.display.flip()

# Quit Pygame
pygame.quit()
