import pygame
import math
import os
from flask import Flask, render_template
import threading

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Exoplanet Orbiting Star")

app = Flask(__name__)

def load_image(file_name, size=None):
    """ Load an image from file with optional scaling. """
    if os.path.exists(file_name):
        image = pygame.image.load(file_name).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    else:
        raise FileNotFoundError(f"Could not find the file {file_name}")

def draw_orbit(x, y, radius):
    """ Draw a circular orbit with reduced opacity. """
    color = (200, 200, 200)  # Reduced opacity for the orbit line
    pygame.draw.circle(screen, color, (x, y), radius, 1)

def setup_images():
    """ Load and return all necessary images. """
    try:
        background_image = load_image('sp.jpg', (screen_width, screen_height))
    except FileNotFoundError:
        background_image = pygame.Surface((screen_width, screen_height))
        background_image.fill((0, 0, 0))
    
    try:
        star_image = load_image('Proxima Centauri b/Proxima Centauri.png', (100, 100))
    except FileNotFoundError:
        star_image = pygame.Surface((100, 100))
        star_image.fill((255, 255, 0))
    
    try:
        planet_image = load_image('Proxima Centauri b/Proxima Centauri b.png', (50, 50))
    except FileNotFoundError:
        planet_image = pygame.Surface((50, 50))
        planet_image.fill((0, 0, 255))
    
    return background_image, star_image, planet_image

class Exoplanet:
    """ Class to represent an orbiting exoplanet. """
    def __init__(self, image, radius, orbit_speed):
        self.image = image
        self.radius = radius
        self.angle = 0
        self.orbit_speed = orbit_speed

    def update(self):
        self.angle += self.orbit_speed

    def draw(self, screen, center_x, center_y):
        exoplanet_x = center_x + self.radius * math.cos(self.angle)
        exoplanet_y = center_y + self.radius * math.sin(self.angle)
        screen.blit(self.image, (exoplanet_x - self.image.get_width() // 2, exoplanet_y - self.image.get_height() // 2))
        return exoplanet_x, exoplanet_y

def run_pygame():
    """ Main Pygame loop to run in a separate thread. """
    background_image, star_image, planet_image = setup_images()
    planet = Exoplanet(planet_image, 250, 0.005)
    star_x = screen_width // 2
    star_y = screen_height // 2
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background_image, (0, 0))
        screen.blit(star_image, (star_x - star_image.get_width() // 2, star_y - star_image.get_height() // 2))
        planet_x, planet_y = planet.draw(screen, star_x, star_y)
        planet.update()
        
        planet_name_surface = pygame.font.SysFont('Arial', 24).render('Proxima Centauri b', True, (255, 255, 255))
        screen.blit(planet_name_surface, (planet_x - planet_name_surface.get_width() // 2, planet_y - 60))

        info_text = [
            "Planet Name: Proxima Centauri b",
            "Type: Super Earth",
            "Mass: 1.07 Earths",
            "Orbital Radius: 0.04856 AU",
            "Orbital Period: 11.2 days",
            "Eccentricity: 0.02",
            "Discovery Date: 2016"
        ]
        for i, line in enumerate(info_text):
            info_surface = pygame.font.SysFont('Arial', 20).render(line, True, (255, 255, 255))
            screen.blit(info_surface, (10, 10 + i * 30))

        draw_orbit(star_x, star_y, planet.radius)
        pygame.display.flip()

    pygame.quit()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    threading.Thread(target=run_pygame).start()
    app.run(debug=True)
