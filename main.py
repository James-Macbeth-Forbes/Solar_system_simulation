import pygame
import math
from datetime import datetime, timedelta

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulator")

# Astronomical unit scaling
AU = 100
MIN_AU = 10
MAX_AU = 200

# Set up planet data
planet_data = [
    {"name": "Mercury", "T": 87.97, "e": 0.2056, "a": 0.39, "color": "gray", "theta0_deg": 69.2},
    {"name": "Venus", "T": 225.0, "e": 0.0068, "a": 0.72, "color": "yellow", "theta0_deg": 45.3},
    {"name": "Earth", "T": 365.256, "e": 0.0167, "a": 1.0, "color": "green", "theta0_deg": 97.5},
    {"name": "Mars", "T": 687.0, "e": 0.0934, "a": 1.52, "color": "red", "theta0_deg": 15.8},
    {"name": "Jupiter", "T": 4333.0, "e": 0.0489, "a": 5.2, "color": "orange", "theta0_deg": 124.3},
    {"name": "Saturn", "T": 10759.0, "e": 0.0565, "a": 9.58, "color": "gold", "theta0_deg": 53.6},
    {"name": "Uranus", "T": 30687.0, "e": 0.0461, "a": 19.22, "color": "lightblue", "theta0_deg": 137.5},
    {"name": "Neptune", "T": 60190.0, "e": 0.0086, "a": 30.05, "color": "blue", "theta0_deg": 302.1}
]

# Convert ephemeris angles to radians and update initial mean anomaly
for planet in planet_data:
    e = planet["e"]
    T = planet["T"]
    theta0 = math.radians(planet["theta0_deg"])

    E0 = 2 * math.atan(math.sqrt((1 - e) / (1 + e)) * math.tan(theta0 / 2))
    M0 = E0 - e * math.sin(E0)
    planet["M0"] = M0

# Function to draw planets
font = pygame.font.Font(None, 18)


def draw_planet(day, planet, AU):
    T, e, a = planet["T"], planet["e"], planet["a"] * AU
    M0 = planet["M0"]

    # Mean anomaly (M)
    M = (2 * math.pi / T) * day + M0

    # Solve Kepler’s equation using Newton-Raphson method
    E = M
    for _ in range(10):  # Iteration limit
        E_new = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        if abs(E_new - E) < 1e-6:
            break
        E = E_new

    # True anomaly (theta)
    theta = 2 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2), math.sqrt(1 - e) * math.cos(E / 2))

    # Radial distance r
    r = a * (1 - e ** 2) / (1 + e * math.cos(theta))

    # Convert to screen coordinates (adjusting for elliptical orbits)
    x = WIDTH // 2 + r * math.cos(theta)
    y = HEIGHT // 2 + r * math.sin(theta) * (1 - e)

    # Draw planet
    pygame.draw.circle(screen, planet["color"], (int(x), int(y)), 6)

    # Draw planet name
    text_surface = font.render(planet["name"], True, "white")
    screen.blit(text_surface, (x - 10, y + 10))


# Initialize date
start_date = datetime(2025, 3, 6)
day = 0
paused = False
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    screen.fill("black")
    pygame.draw.circle(screen, "yellow", (WIDTH // 2, HEIGHT // 2), 15)  # Sun

    for planet in planet_data:
        draw_planet(day, planet, AU)

    # Display date
    current_date = start_date + timedelta(days=day)
    date_str = current_date.strftime("%B %d, %Y")
    text_surface = pygame.font.Font(None, 36).render(date_str, True, "white")
    screen.blit(text_surface, (10, 10))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                AU = min(AU + 10, MAX_AU)
            if event.key == pygame.K_MINUS:
                AU = max(AU - 10, MIN_AU)

    if not paused:
        day += 1

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
