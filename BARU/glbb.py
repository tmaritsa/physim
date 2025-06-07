import pygame
import pymunk
import math

# Initialize Pygame and Pymunk
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GLBB Simulation: Moving Box with Acceleration Control")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)  # Use a default font

# Colors
BG_COLOR = (255, 255, 255)
BOX_COLOR = (55, 65, 81)
FLOOR_COLOR = (209, 213, 219)
ARROW_COLOR = (59, 130, 246)
TEXT_COLOR = (107, 114, 128)

# Pymunk setup
space = pymunk.Space()
space.gravity = (0, 0)

# Floor as static segment
floor_y = HEIGHT - 60
floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
floor_shape = pymunk.Segment(floor_body, (0, floor_y), (WIDTH, floor_y), 5)
floor_shape.friction = 1.0
space.add(floor_body, floor_shape)

# Box dynamic body and shape
box_width, box_height = 60, 40
mass = 2
moment = pymunk.moment_for_box(mass, (box_width, box_height))
box_body = pymunk.Body(mass, moment)
box_body.position = WIDTH // 4, floor_y - box_height / 2 - 5
box_shape = pymunk.Poly.create_box(box_body, (box_width, box_height))
box_shape.friction = 0.9
space.add(box_body, box_shape)

# Simulation parameters
acceleration = 0.0
accel_step = 200.0
accel_max = 400.0
accel_min = -400.0

def draw_box(surface, body, shape):
    points = shape.get_vertices()
    points = [body.position + p.rotated(body.angle) for p in points]
    points = [(int(p.x), int(p.y)) for p in points]
    pygame.draw.polygon(surface, BOX_COLOR, points)  # Removed border_radius

def draw_floor(surface):
    pygame.draw.line(surface, FLOOR_COLOR, (0, floor_y), (WIDTH, floor_y), 6)

def draw_acceleration_arrow(surface, body, acceleration_value):
    base_x, base_y = int(body.position.x), int(body.position.y - box_height/2 - 60)
    max_arrow_length = 150
    length = (acceleration_value / accel_max) * max_arrow_length
    length = max(-max_arrow_length, min(length, max_arrow_length))

    if abs(length) < 5:
        return

    end_x = base_x + length
    end_y = base_y

    pygame.draw.line(surface, ARROW_COLOR, (base_x, base_y), (end_x, end_y), 6)

    arrow_size = 12
    direction = 1 if length > 0 else -1
    point1 = (end_x, end_y)
    point2 = (end_x - direction * arrow_size, end_y - arrow_size // 2)
    point3 = (end_x - direction * arrow_size, end_y + arrow_size // 2)
    pygame.draw.polygon(surface, ARROW_COLOR, [point1, point2, point3])

def draw_stats(surface, velocity_val, acceleration_val):
    vel_text = font.render(f"Velocity: {velocity_val:.2f} px/s", True, TEXT_COLOR)
    acc_text = font.render(f"Acceleration: {acceleration_val:.2f} px/s²", True, TEXT_COLOR)

    surface.blit(vel_text, (20, 20))
    surface.blit(acc_text, (20, 50))

def main():
    global acceleration

    running = True
    dt = 1/60
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            acceleration += accel_step * dt
        if keys[pygame.K_a]:
            acceleration -= accel_step * dt

        acceleration = max(accel_min, min(acceleration, accel_max))

        force_x = mass * acceleration
        box_body.force = (force_x, 0)

        space.step(dt)

        screen.fill(BG_COLOR)

        draw_floor(screen)
        draw_box(screen, box_body, box_shape)
        draw_acceleration_arrow(screen, box_body, acceleration)

        velocity_x = box_body.velocity.x
        draw_stats(screen, velocity_x, acceleration)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
