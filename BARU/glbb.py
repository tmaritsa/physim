# glbb_revised_v3.py

import pygame
import pymunk

class GLBBSimulation:
    def __init__(self, width=800, height=400):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.font = pygame.font.SysFont("Arial", 20)

        # Simpan posisi awal untuk keperluan reset
        self.floor_y = self.height - 60
        self.initial_pos = (self.width // 4, self.floor_y - (40 / 2) - 5)

        # Warna
        self.BG_COLOR = (255, 255, 255)
        self.BOX_COLOR = (55, 65, 81)
        self.FLOOR_COLOR = (209, 213, 219)
        # Warna baru untuk panah vektor
        self.ARROW_COLOR = (220, 38, 38) # Merah

        # Pengaturan Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)

        # Lantai statis
        self.floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        # Recreate floor shape when resizing to match new width
        self.floor_shape = pymunk.Segment(self.floor_body, (0, self.floor_y), (self.width, self.floor_y), 5)
        self.floor_shape.friction = 1.0
        self.space.add(self.floor_body, self.floor_shape) # floor_body and floor_shape are added initially

        # Objek kotak
        self.box_width, self.box_height = 60, 40
        self.mass = 2
        self.moment = pymunk.moment_for_box(self.mass, (self.box_width, self.box_height))
        self.box_body = pymunk.Body(self.mass, self.moment)
        self.box_shape = pymunk.Poly.create_box(self.box_body, (self.box_width, self.box_height))
        self.box_shape.friction = 0.9
        self.space.add(self.box_body, self.box_shape)

        # Kontrol akselerasi
        self.acceleration = 0.0
        
        # Panggil reset untuk mengatur kondisi awal
        self.reset()

    def set_acceleration(self, acc):
        """Sets the acceleration for the box."""
        self.acceleration = acc

    def step(self, dt=1/60.0):
        """Advances the simulation by a given time step."""
        force_x = self.mass * self.acceleration
        self.box_body.force = (force_x, 0)
        self.space.step(dt)

        # --- PENAMBAHAN 1: BATASAN GERAK KOTAK ---
        pos_x = self.box_body.position.x
        half_width = self.box_width / 2

        # Cek batas kiri
        if pos_x - half_width < 0:
            self.box_body.position = (half_width, self.box_body.position.y)
            self.box_body.velocity = (0, self.box_body.velocity.y)
        
        # Cek batas kanan
        if pos_x + half_width > self.width:
            self.box_body.position = (self.width - half_width, self.box_body.position.y)
            self.box_body.velocity = (0, self.box_body.velocity.y)

    def draw(self):
        """Draws the current state of the simulation onto the surface."""
        self.surface.fill(self.BG_COLOR)
        # Draw floor based on current width
        pygame.draw.line(self.surface, self.FLOOR_COLOR, (0, self.floor_y), (self.width, self.floor_y), 6)
        
        # Gambar kotak
        points = [self.box_body.position + p.rotated(self.box_body.angle) for p in self.box_shape.get_vertices()]
        points_tuple = [(int(p.x), int(p.y)) for p in points]
        pygame.draw.polygon(self.surface, self.BOX_COLOR, points_tuple)

        # --- PENAMBAHAN 2: MENGGAMBAR VEKTOR PERCEPATAN ---
        if self.acceleration != 0:
            # Tentukan titik awal, panjang, dan titik akhir panah
            start_pos = self.box_body.position
            # Skalakan panjang panah agar terlihat bagus (panjang = percepatan * 3)
            arrow_length = self.acceleration * 3 
            end_pos = start_pos + (arrow_length, 0)
            
            # Gambar garis utama panah
            pygame.draw.line(self.surface, self.ARROW_COLOR, start_pos, end_pos, 3)
            
            # Gambar mata panah
            arrow_head_length = 8
            if arrow_length > 0: # Panah ke kanan
                p1 = (end_pos.x - arrow_head_length, end_pos.y - arrow_head_length)
                p2 = (end_pos.x - arrow_head_length, end_pos.y + arrow_head_length)
            else: # Panah ke kiri
                p1 = (end_pos.x + arrow_head_length, end_pos.y - arrow_head_length)
                p2 = (end_pos.x + arrow_head_length, end_pos.y + arrow_head_length)

            pygame.draw.line(self.surface, self.ARROW_COLOR, end_pos, p1, 3)
            pygame.draw.line(self.surface, self.ARROW_COLOR, end_pos, p2, 3)

        # Gambar teks info (tidak berubah)
        vel_x = self.box_body.velocity.x
        accel_text = f"Acceleration (m/s²): {self.acceleration:.2f}"
        vel_text = f"Velocity (m/s): {vel_x:.2f}"
        pos_text = f"Position (m): {self.box_body.position.x:.2f}"
        self.surface.blit(self.font.render(accel_text, True, (0, 0, 0)), (10, 10))
        self.surface.blit(self.font.render(vel_text, True, (0, 0, 0)), (10, 35))
        self.surface.blit(self.font.render(pos_text, True, (0, 0, 0)), (10, 60))

    def reset(self):
        """Resets the simulation to its initial state."""
        self.acceleration = 0.0
        self.box_body.position = self.initial_pos
        self.box_body.velocity = (0, 0)
        self.box_body.angle = 0
        self.box_body.angular_velocity = 0
        self.box_body.force = (0, 0)

    def resize(self, new_width, new_height):
        """
        Resizes the Pygame surface and adjusts simulation elements
        to fit the new dimensions.
        """
        self.width = new_width
        self.height = new_height
        self.surface = pygame.Surface((new_width, new_height)) # Recreate the surface with new dimensions

        # Update floor position based on new height
        self.floor_y = self.height - 60
        
        # Remove old floor shape from space before adding new one
        self.space.remove(self.floor_shape)

        # Create new floor shape with updated dimensions and attach to the existing floor_body
        self.floor_shape = pymunk.Segment(self.floor_body, (0, self.floor_y), (self.width, self.floor_y), 5)
        self.floor_shape.friction = 1.0
        
        # Add only the new floor shape to the space (floor_body is already added)
        self.space.add(self.floor_shape)

        # Adjust initial position of the box based on new dimensions for reset
        self.initial_pos = (self.width // 4, self.floor_y - (self.box_height / 2) - 5)
        
        # Reset the box position relative to the new floor if it's currently on screen
        current_pos_x = self.box_body.position.x
        
        # Keep box roughly in the same relative horizontal position, within new bounds
        new_box_x = max(self.box_width / 2, min(current_pos_x, self.width - self.box_width / 2))
        new_box_y = self.floor_y - (self.box_height / 2) - 5 # Always on top of the floor
        
        self.box_body.position = (new_box_x, new_box_y)
        # No need to reset velocity unless explicitly desired on resize
