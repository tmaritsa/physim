# harmonic_simulation.py

import pygame
import pymunk
import math # Import math for sine/cosine functions

class SHMSimulation:
    """
    Simulation for Simple Harmonic Motion (SHM) of a mass on a spring.
    """
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.font = pygame.font.SysFont("Arial", 20)

        # Colors
        self.BG_COLOR = (255, 255, 255)
        self.MASS_COLOR = (55, 65, 81) # Dark grey for the mass
        self.SPRING_COLOR = (150, 75, 0) # Brown for the spring
        self.CEILING_COLOR = (209, 213, 219) # Light grey for the ceiling

        # Pymunk space
        self.space = pymunk.Space()
        self.space.gravity = (0, 0) # SHM is typically modeled without gravity in vertical direction or with it balanced

        # Ceiling (static body)
        self.ceiling_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.ceiling_body.position = (self.width // 2, 50)
        self.ceiling_shape = pymunk.Segment(self.ceiling_body, (-self.width/2, 0), (self.width/2, 0), 5)
        self.space.add(self.ceiling_body, self.ceiling_shape)

        # Mass body
        self.mass_radius = 25
        self.mass_val = 1 # kg
        self.mass_moment = pymunk.moment_for_circle(self.mass_val, 0, self.mass_radius)
        self.mass_body = pymunk.Body(self.mass_val, self.mass_moment)
        self.mass_body.position = (self.width // 2, self.height // 2) # Initial position
        self.mass_shape = pymunk.Circle(self.mass_body, self.mass_radius)
        self.mass_shape.friction = 0.5
        self.space.add(self.mass_body, self.mass_shape)

        # Spring
        self.rest_length = 150 # pixels (equilibrium position)
        self.stiffness = 50 # N/m (spring constant)
        self.damping = 1.0 # Damping coefficient

        self.spring_joint = pymunk.DampedSpring(
            self.ceiling_body, self.mass_body,
            (0, 0), (0, 0), # Anchors on bodies (relative to body center)
            self.rest_length, self.stiffness, self.damping
        )
        self.space.add(self.spring_joint)

        # Initial displacement
        self.initial_displacement = 100 # pixels
        self.mass_body.position = (self.width // 2, self.height // 2 + self.initial_displacement)
        self.mass_body.velocity = (0, 0)

        self.time = 0.0 # To track time for analytical solution/damping effects

        # Control parameters for UI
        self.amplitude = 100 # Initial amplitude for display/reset
        self.k_constant = self.stiffness # Spring constant for UI control
        self.m_mass = self.mass_val # Mass for UI control

        self.reset()

    def set_amplitude(self, amp):
        """Sets the initial displacement (amplitude) for reset."""
        self.amplitude = amp
        self.reset() # Reset to apply new amplitude

    def set_k_constant(self, k):
        """Sets the spring constant (stiffness)."""
        self.k_constant = k
        self.spring_joint.stiffness = k
        self.reset() # Reset to see immediate effect on oscillation frequency

    def set_mass(self, m):
        """Sets the mass of the oscillating body."""
        # Pymunk bodies are immutable for mass/moment, so recreate
        self.m_mass = m
        old_body = self.mass_body
        old_shape = self.mass_shape
        old_spring = self.spring_joint
        
        self.space.remove(old_body, old_shape, old_spring) # Remove old components

        self.mass_moment = pymunk.moment_for_circle(self.m_mass, 0, self.mass_radius)
        self.mass_body = pymunk.Body(self.m_mass, self.mass_moment)
        self.mass_body.position = old_body.position # Keep current position
        self.mass_body.velocity = old_body.velocity # Keep current velocity
        self.mass_shape = pymunk.Circle(self.mass_body, self.mass_radius)
        self.mass_shape.friction = 0.5
        self.space.add(self.mass_body, self.mass_shape)

        self.spring_joint = pymunk.DampedSpring(
            self.ceiling_body, self.mass_body,
            (0, 0), (0, 0),
            self.rest_length, self.stiffness, self.damping
        )
        self.space.add(self.spring_joint)
        self.reset() # Reset to apply new mass and re-initialize spring

    def step(self, dt=1/60.0):
        """Advances the simulation by a given time step."""
        self.space.step(dt)
        self.time += dt # Increment time

    def draw(self):
        """Draws the current state of the SHM simulation."""
        self.surface.fill(self.BG_COLOR)

        # Draw ceiling
        pygame.draw.line(self.surface, self.CEILING_COLOR, 
                         (0, self.ceiling_body.position.y), 
                         (self.width, self.ceiling_body.position.y), 5)

        # Draw spring
        spring_start_pos = pymunk.Vec2d(self.ceiling_body.position.x, self.ceiling_body.position.y)
        spring_end_pos = self.mass_body.position

        # Draw spring as a zig-zag line (simple representation)
        num_coils = 10
        coil_width = 15 # Width of the zig-zag
        
        # Calculate vector from start to end of spring
        dx = spring_end_pos.x - spring_start_pos.x
        dy = spring_end_pos.y - spring_start_pos.y
        
        # Normalize direction
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            nx = dx / length
            ny = dy / length
        else:
            nx, ny = 0, 1 # Default to vertical if no length

        # Perpendicular vector for zig-zag offset
        px = -ny
        py = nx

        points = [spring_start_pos]
        for i in range(num_coils):
            t = (i + 0.5) / num_coils # Position along the spring
            point_on_axis = spring_start_pos + pymunk.Vec2d(dx * t, dy * t)
            offset = coil_width * ((-1)**i)
            points.append(point_on_axis + pymunk.Vec2d(px * offset, py * offset))
        points.append(spring_end_pos)

        # Draw lines between points
        for i in range(len(points) - 1):
            pygame.draw.line(self.surface, self.SPRING_COLOR, points[i], points[i+1], 3)

        # Draw mass
        p = self.mass_body.position
        pygame.draw.circle(self.surface, self.MASS_COLOR, (int(p.x), int(p.y)), int(self.mass_radius))
        pygame.draw.circle(self.surface, (0,0,0), (int(p.x), int(p.y)), int(self.mass_radius), 2) # Outline

        # Display info
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
        """Resets the SHM simulation to initial displacement."""
        self.mass_body.position = (self.width // 2, self.ceiling_body.position.y + self.rest_length + self.amplitude)
        self.mass_body.velocity = (0, 0) # Start from rest
        self.time = 0.0 # Reset time

    def resize(self, new_width, new_height):
        """
        Resizes the Pygame surface and adjusts simulation elements
        to fit the new dimensions.
        """
        self.width = new_width
        self.height = new_height
        self.surface = pygame.Surface((new_width, new_height)) # Recreate the surface

        # Update ceiling position relative to new width
        self.ceiling_body.position = (new_width // 2, 50)
        
        # Remove old ceiling shape and add new one
        if self.ceiling_shape in self.space.shapes:
             self.space.remove(self.ceiling_shape)
        # Recreate ceiling shape with updated dimensions and attach to the existing ceiling_body
        self.ceiling_shape = pymunk.Segment(self.ceiling_body, (-new_width/2, 0), (new_width/2, 0), 5)
        self.space.add(self.ceiling_shape)

        # Adjust mass initial position relative to new ceiling and height
        equilibrium_y = self.ceiling_body.position.y + self.rest_length
        
        new_mass_x = new_width // 2
        new_mass_y = equilibrium_y + self.amplitude 
        
        self.mass_body.position = (new_mass_x, new_mass_y)
        self.mass_body.velocity = (0, 0) # Reset velocity on resize to prevent strange behavior
        self.time = 0.0 # Reset time on resize
