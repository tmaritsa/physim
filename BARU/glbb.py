import pygame
import pymunk

class GLBBSimulation:
    def __init__(self, width=800, height=400):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.font = pygame.font.SysFont("Arial", 20)

        self.floor_y = self.height - 60
        self.initial_pos = (self.width // 4, self.floor_y - (40 / 2) - 5)

        self.BG_COLOR = (255, 255, 255)
        self.BOX_COLOR = (55, 65, 81)
        self.FLOOR_COLOR = (209, 213, 219)
        self.ARROW_COLOR = (220, 38, 38)

        self.space = pymunk.Space()
        self.space.gravity = (0, 0)

        self.floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.floor_shape = pymunk.Segment(self.floor_body, (0, self.floor_y), (self.width, self.floor_y), 5)
        self.floor_shape.friction = 1.0
        self.space.add(self.floor_body, self.floor_shape)

        self.box_width, self.box_height = 60, 40
        self.mass = 2
        self.moment = pymunk.moment_for_box(self.mass, (self.box_width, self.box_height))
        self.box_body = pymunk.Body(self.mass, self.moment)
        self.box_shape = pymunk.Poly.create_box(self.box_body, (self.box_width, self.box_height))
        self.box_shape.friction = 0.9
        self.space.add(self.box_body, self.box_shape)

        self.acceleration = 0.0
        
        self.reset()

    def set_acceleration(self, acc):
        self.acceleration = acc

    def step(self, dt=1/60.0):
        force_x = self.mass * self.acceleration
        self.box_body.force = (force_x, 0)
        self.space.step(dt)

        pos_x = self.box_body.position.x
        half_width = self.box_width / 2

        if pos_x - half_width < 0:
            self.box_body.position = (half_width, self.box_body.position.y)
            self.box_body.velocity = (0, self.box_body.velocity.y)
        
        if pos_x + half_width > self.width:
            self.box_body.position = (self.width - half_width, self.box_body.position.y)
            self.box_body.velocity = (0, self.box_body.velocity.y)

    def draw(self):
        self.surface.fill(self.BG_COLOR)
        pygame.draw.line(self.surface, self.FLOOR_COLOR, (0, self.floor_y), (self.width, self.floor_y), 6)
        
        points = [self.box_body.position + p.rotated(self.box_body.angle) for p in self.box_shape.get_vertices()]
        points_tuple = [(int(p.x), int(p.y)) for p in points]
        pygame.draw.polygon(self.surface, self.BOX_COLOR, points_tuple)

        if self.acceleration != 0:
            start_pos = self.box_body.position
            arrow_length = self.acceleration * 3 
            end_pos = start_pos + (arrow_length, 0)
            
            pygame.draw.line(self.surface, self.ARROW_COLOR, start_pos, end_pos, 3)
            
            arrow_head_length = 8
            if arrow_length > 0:
                p1 = (end_pos.x - arrow_head_length, end_pos.y - arrow_head_length)
                p2 = (end_pos.x - arrow_head_length, end_pos.y + arrow_head_length)
            else:
                p1 = (end_pos.x + arrow_head_length, end_pos.y - arrow_head_length)
                p2 = (end_pos.x + arrow_head_length, end_pos.y + arrow_head_length)

            pygame.draw.line(self.surface, self.ARROW_COLOR, end_pos, p1, 3)
            pygame.draw.line(self.surface, self.ARROW_COLOR, end_pos, p2, 3)

        vel_x = self.box_body.velocity.x
        accel_text = f"Acceleration (m/s²): {self.acceleration:.2f}"
        vel_text = f"Velocity (m/s): {vel_x:.2f}"
        pos_text = f"Position (m): {self.box_body.position.x:.2f}"
        self.surface.blit(self.font.render(accel_text, True, (0, 0, 0)), (10, 10))
        self.surface.blit(self.font.render(vel_text, True, (0, 0, 0)), (10, 35))
        self.surface.blit(self.font.render(pos_text, True, (0, 0, 0)), (10, 60))

    def reset(self):
        self.acceleration = 0.0
        self.box_body.position = self.initial_pos
        self.box_body.velocity = (0, 0)
        self.box_body.angle = 0
        self.box_body.angular_velocity = 0
        self.box_body.force = (0, 0)

    def resize(self, new_width, new_height):
        self.width = new_width
        self.height = new_height
        self.surface = pygame.Surface((new_width, new_height))

        self.floor_y = self.height - 60
        
        self.space.remove(self.floor_shape)

        self.floor_shape = pymunk.Segment(self.floor_body, (0, self.floor_y), (self.width, self.floor_y), 5)
        self.floor_shape.friction = 1.0
        
        self.space.add(self.floor_shape)

        self.initial_pos = (self.width // 4, self.floor_y - (self.box_height / 2) - 5)
        
        current_pos_x = self.box_body.position.x
        
        new_box_x = max(self.box_width / 2, min(current_pos_x, self.width - self.box_width / 2))
        new_box_y = self.floor_y - (self.box_height / 2) - 5
        
        self.box_body.position = (new_box_x, new_box_y)