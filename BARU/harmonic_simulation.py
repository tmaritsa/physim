import pygame
import pymunk
import math 

class SHMSimulation:

    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.font = pygame.font.SysFont("Arial", 20)

        self.BG_COLOR = (255, 255, 255)
        self.MASS_COLOR = (55, 65, 81) 
        self.SPRING_COLOR = (150, 75, 0)
        self.CEILING_COLOR = (209, 213, 219) 

        self.space = pymunk.Space()
        self.space.gravity = (0, 0) 

        self.ceiling_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.ceiling_body.position = (self.width // 2, 50)
        self.ceiling_shape = pymunk.Segment(self.ceiling_body, (-self.width/2, 0), (self.width/2, 0), 5)
        self.space.add(self.ceiling_body, self.ceiling_shape)

        self.mass_radius = 25
        self.mass_val = 1 
        self.mass_moment = pymunk.moment_for_circle(self.mass_val, 0, self.mass_radius)
        self.mass_body = pymunk.Body(self.mass_val, self.mass_moment)
        self.mass_body.position = (self.width // 2, self.height // 2) 
        self.mass_shape = pymunk.Circle(self.mass_body, self.mass_radius)
        self.mass_shape.friction = 0.5
        self.space.add(self.mass_body, self.mass_shape)

        self.rest_length = 150 
        self.stiffness = 50 
        self.damping = 1.0 

        self.spring_joint = pymunk.DampedSpring(
            self.ceiling_body, self.mass_body,
            (0, 0), (0, 0),
            self.rest_length, self.stiffness, self.damping
        )
        self.space.add(self.spring_joint)

        self.initial_displacement = 100
        self.mass_body.position = (self.width // 2, self.height // 2 + self.initial_displacement)
        self.mass_body.velocity = (0, 0)

        self.time = 0.0

        self.amplitude = 100
        self.k_constant = self.stiffness
        self.m_mass = self.mass_val

        self.reset()

    def set_amplitude(self, amp):
        self.amplitude = amp
        self.reset()

    def set_k_constant(self, k):
        self.k_constant = k
        self.spring_joint.stiffness = k
        self.reset()

    def set_mass(self, m):
        self.m_mass = m
        old_body = self.mass_body
        old_shape = self.mass_shape
        old_spring = self.spring_joint
        
        self.space.remove(old_body, old_shape, old_spring)

        self.mass_moment = pymunk.moment_for_circle(self.m_mass, 0, self.mass_radius)
        self.mass_body = pymunk.Body(self.m_mass, self.mass_moment)
        self.mass_body.position = old_body.position
        self.mass_body.velocity = old_body.velocity
        self.mass_shape = pymunk.Circle(self.mass_body, self.mass_radius)
        self.mass_shape.friction = 0.5
        self.space.add(self.mass_body, self.mass_shape)

        self.spring_joint = pymunk.DampedSpring(
            self.ceiling_body, self.mass_body,
            (0, 0), (0, 0),
            self.rest_length, self.stiffness, self.damping
        )
        self.space.add(self.spring_joint)
        self.reset()

    def step(self, dt=1/60.0):
        self.space.step(dt)
        self.time += dt

    def draw(self):
        self.surface.fill(self.BG_COLOR)

        pygame.draw.line(self.surface, self.CEILING_COLOR, 
                         (0, self.ceiling_body.position.y), 
                         (self.width, self.ceiling_body.position.y), 5)

        spring_start_pos = pymunk.Vec2d(self.ceiling_body.position.x, self.ceiling_body.position.y)
        spring_end_pos = self.mass_body.position

        num_coils = 10
        coil_width = 15
        
        dx = spring_end_pos.x - spring_start_pos.x
        dy = spring_end_pos.y - spring_start_pos.y
        
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            nx = dx / length
            ny = dy / length
        else:
            nx, ny = 0, 1

        px = -ny
        py = nx

        points = [spring_start_pos]
        for i in range(num_coils):
            t = (i + 0.5) / num_coils
            point_on_axis = spring_start_pos + pymunk.Vec2d(dx * t, dy * t)
            offset = coil_width * ((-1)**i)
            points.append(point_on_axis + pymunk.Vec2d(px * offset, py * offset))
        points.append(spring_end_pos)

        for i in range(len(points) - 1):
            pygame.draw.line(self.surface, self.SPRING_COLOR, points[i], points[i+1], 3)

        p = self.mass_body.position
        pygame.draw.circle(self.surface, self.MASS_COLOR, (int(p.x), int(p.y)), int(self.mass_radius))
        pygame.draw.circle(self.surface, (0,0,0), (int(p.x), int(p.y)), int(self.mass_radius), 2)

        freq = math.sqrt(self.k_constant / self.m_mass) / (2 * math.pi) if self.m_mass > 0 else 0
        period = 1 / freq if freq > 0 else float('inf')
        
        displacement_y = self.mass_body.position.y - (self.ceiling_body.position.y + self.rest_length)
        vel_y = self.mass_body.velocity.y

        freq_text = f"Frequency (Hz): {freq:.2f}"
        period_text = f"Period (s): {period:.2f}"
        disp_text = f"Displacement (m): {displacement_y:.2f}"
        vel_text = f"Velocity (m/s): {vel_y:.2f}"
        
        self.surface.blit(self.font.render(freq_text, True, (0, 0, 0)), (10, 10))
        self.surface.blit(self.font.render(period_text, True, (0, 0, 0)), (10, 35))
        self.surface.blit(self.font.render(disp_text, True, (0, 0, 0)), (10, 60))
        self.surface.blit(self.font.render(vel_text, True, (0, 0, 0)), (10, 85))
        
        k_text = f"Spring Const (N/m): {self.k_constant:.2f}"
        m_text = f"Mass (kg): {self.m_mass:.2f}"
        self.surface.blit(self.font.render(k_text, True, (0, 0, 0)), (self.width - 200, 10))
        self.surface.blit(self.font.render(m_text, True, (0, 0, 0)), (self.width - 200, 35))

    def reset(self):
        self.mass_body.position = (self.width // 2, self.ceiling_body.position.y + self.rest_length + self.amplitude)
        self.mass_body.velocity = (0, 0)
        self.time = 0.0

    def resize(self, new_width, new_height):
        self.width = new_width
        self.height = new_height
        self.surface = pygame.Surface((new_width, new_height))

        self.ceiling_body.position = (new_width // 2, 50)
        
        if self.ceiling_shape in self.space.shapes:
            self.space.remove(self.ceiling_shape)
        self.ceiling_shape = pymunk.Segment(self.ceiling_body, (-new_width/2, 0), (new_width/2, 0), 5)
        self.space.add(self.ceiling_shape)

        equilibrium_y = self.ceiling_body.position.y + self.rest_length
        
        new_mass_x = new_width // 2
        new_mass_y = equilibrium_y + self.amplitude 
        
        self.mass_body.position = (new_mass_x, new_mass_y)
        self.mass_body.velocity = (0, 0)
        self.time = 0.0