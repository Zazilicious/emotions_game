import pygame
import os
import random
import sys

# setup
pygame.init()
WIDTH, HEIGHT = 1280, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess the Emotion")
font = pygame.font.SysFont("arial", 32)
small_font = pygame.font.SysFont("arial", 24)
clock = pygame.time.Clock()

# load pics
import re

def load_images(folder):
    images = []
    for file in os.listdir(folder):
        if file.endswith(".jpg") or file.endswith(".png"):
            emotion_match = re.match(r"([a-zA-Z]+)", file)
            if emotion_match:
                emotion = emotion_match.group(1).lower()
                img = pygame.image.load(os.path.join(folder, file))
                img = pygame.transform.scale(img, (400, 400))
                images.append((img, emotion))
    return images

images = load_images("emotions")
random.shuffle(images)

# variables
input_text = ""
score = 0
index = 0
feedback = ""
running = True

def draw(image, input_text, score, feedback):
    win.fill((255, 255, 255))
    win.blit(image, (200, 50))

    input_surface = font.render(f"Your Guess: {input_text}", True, (0, 0, 0))
    win.blit(input_surface, (50, 480))

    score_surface = small_font.render(f"Score: {score}", True, (0, 128, 0))
    win.blit(score_surface, (10, 10))

    feedback_surface = small_font.render(feedback, True, (255, 0, 0) if "Wrong" in feedback else (0, 0, 255))
    win.blit(feedback_surface, (50, 520))

    pygame.display.flip()

while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                correct_emotion = images[index][1]
                if input_text.lower().strip() == correct_emotion:
                    score += 1
                    feedback = "Correct!"
                else:
                    feedback = f"Wrong! It was '{correct_emotion}'."
                input_text = ""
                index += 1
                if index >= len(images):
                    running = False
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    if index < len(images):
        draw(images[index][0], input_text, score, feedback)

pygame.quit()
print(f"Final Score: {score} / {len(images)}")
sys.exit()
