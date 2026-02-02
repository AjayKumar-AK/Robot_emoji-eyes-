import pygame
import pygame.gfxdraw
import random
import time
from enum import IntEnum

class Mood(IntEnum):
    DEFAULT = 0
    TIRED = 1
    ANGRY = 2
    HAPPY = 3

class Position(IntEnum):
    N = 1   # north, top center
    NE = 2  # north-east, top right
    E = 3   # east, middle right
    SE = 4  # south-east, bottom right
    S = 5   # south, bottom center
    SW = 6  # south-west, bottom left
    W = 7   # west, middle left
    NW = 8  # north-west, top left

class RoboEyes:
    def __init__(self, width=1024, height=512):
        """
        Initialize RoboEyes with native resolution rendering (no scaling).
        Default is 1024x512 for smooth, high-quality display.
        """
        pygame.init()
        self.screen_width = width
        self.screen_height = height
        # Render directly at native resolution - NO SCALING
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("RoboEyes - Press ESC to exit")
        
        self.BG_COLOR = (0, 0, 0)
        self.MAIN_COLOR = (0, 200, 255)
        
        self.clock = pygame.time.Clock()
        self.fps = 50
        
        self.tired = False
        self.angry = False
        self.happy = False
        self.curious = False
        self.cyclops = False
        self.eye_l_open = False
        self.eye_r_open = False
        
        # Scale everything proportionally to the screen size
        self.eye_l_width_default = 288
        self.eye_l_height_default = 288
        self.eye_l_width_current = self.eye_l_width_default
        self.eye_l_height_current = 1
        self.eye_l_width_next = self.eye_l_width_default
        self.eye_l_height_next = self.eye_l_height_default
        self.eye_l_height_offset = 0
        self.eye_l_border_radius = 40
        self.eye_l_border_radius_current = 40
        self.eye_l_border_radius_next = 40
        
        self.eye_r_width_default = 288
        self.eye_r_height_default = 288
        self.eye_r_width_current = self.eye_r_width_default
        self.eye_r_height_current = 1
        self.eye_r_width_next = self.eye_r_width_default
        self.eye_r_height_next = self.eye_r_height_default
        self.eye_r_height_offset = 0
        self.eye_r_border_radius = 40
        self.eye_r_border_radius_current = 40
        self.eye_r_border_radius_next = 40
        
        self.space_between_default = 80
        self.space_between_current = self.space_between_default
        self.space_between_next = 80
        
        self.eye_l_x_default = ((self.screen_width) - (self.eye_l_width_default + self.space_between_default + self.eye_r_width_default)) // 2
        self.eye_l_y_default = (self.screen_height - self.eye_l_height_default) // 2
        self.eye_l_x = self.eye_l_x_default
        self.eye_l_y = self.eye_l_y_default
        self.eye_l_x_next = self.eye_l_x
        self.eye_l_y_next = self.eye_l_y
        
        self.eye_r_x_default = self.eye_l_x + self.eye_l_width_current + self.space_between_default
        self.eye_r_y_default = self.eye_l_y
        self.eye_r_x = self.eye_r_x_default
        self.eye_r_y = self.eye_r_y_default
        self.eye_r_x_next = self.eye_r_x
        self.eye_r_y_next = self.eye_r_y
        
        self.eyelids_tired_height = 0
        self.eyelids_tired_height_next = 0
        self.eyelids_angry_height = 0
        self.eyelids_angry_height_next = 0
        self.eyelids_happy_bottom_offset = 0
        self.eyelids_happy_bottom_offset_next = 0
        
        self.h_flicker = False
        self.h_flicker_alternate = False
        self.h_flicker_amplitude = 16
        
        self.v_flicker = False
        self.v_flicker_alternate = False
        self.v_flicker_amplitude = 80
        
        self.autoblinker = False
        self.blink_interval = 1
        self.blink_interval_variation = 4
        self.blink_timer = 0
        
        self.idle = False
        self.idle_interval = 1
        self.idle_interval_variation = 3
        self.idle_timer = 0
        
        self.confused = False
        self.confused_timer = 0
        self.confused_duration = 500
        self.confused_toggle = True
        
        self.laugh = False
        self.laugh_timer = 0
        self.laugh_duration = 500
        self.laugh_toggle = True
        
        self.sweat = False
        self.sweat_border_radius = 16
        self.sweat1_x_initial = 16
        self.sweat1_x = self.sweat1_x_initial
        self.sweat1_y = 16.0
        self.sweat1_y_max = 160
        self.sweat1_height = 16.0
        self.sweat1_width = 8.0
        
        self.sweat2_x_initial = 16
        self.sweat2_x = self.sweat2_x_initial
        self.sweat2_y = 16.0
        self.sweat2_y_max = 160
        self.sweat2_height = 16.0
        self.sweat2_width = 8.0
        
        self.sweat3_x_initial = 16
        self.sweat3_x = self.sweat3_x_initial
        self.sweat3_y = 16.0
        self.sweat3_y_max = 160
        self.sweat3_height = 16.0
        self.sweat3_width = 8.0
    
    def get_screen_constraint_x(self):
        return self.screen_width - self.eye_l_width_current - self.space_between_current - self.eye_r_width_current
    
    def get_screen_constraint_y(self):
        return self.screen_height - self.eye_l_height_default
    
    def set_mood(self, mood):
        if mood == Mood.TIRED:
            self.tired, self.angry, self.happy = True, False, False
        elif mood == Mood.ANGRY:
            self.tired, self.angry, self.happy = False, True, False
        elif mood == Mood.HAPPY:
            self.tired, self.angry, self.happy = False, False, True
        else:
            self.tired, self.angry, self.happy = False, False, False
    
    def set_position(self, position):
        if position == Position.N:
            self.eye_l_x_next = self.get_screen_constraint_x() // 2
            self.eye_l_y_next = 0
        elif position == Position.NE:
            self.eye_l_x_next = self.get_screen_constraint_x()
            self.eye_l_y_next = 0
        elif position == Position.E:
            self.eye_l_x_next = self.get_screen_constraint_x()
            self.eye_l_y_next = self.get_screen_constraint_y() // 2
        elif position == Position.SE:
            self.eye_l_x_next = self.get_screen_constraint_x()
            self.eye_l_y_next = self.get_screen_constraint_y()
        elif position == Position.S:
            self.eye_l_x_next = self.get_screen_constraint_x() // 2
            self.eye_l_y_next = self.get_screen_constraint_y()
        elif position == Position.SW:
            self.eye_l_x_next = 0
            self.eye_l_y_next = self.get_screen_constraint_y()
        elif position == Position.W:
            self.eye_l_x_next = 0
            self.eye_l_y_next = self.get_screen_constraint_y() // 2
        elif position == Position.NW:
            self.eye_l_x_next = 0
            self.eye_l_y_next = 0
        else:
            self.eye_l_x_next = self.get_screen_constraint_x() // 2
            self.eye_l_y_next = self.get_screen_constraint_y() // 2
    
    def set_autoblinker(self, active, interval=1, variation=4):
        self.autoblinker = active
        self.blink_interval = interval
        self.blink_interval_variation = variation
    
    def set_idle_mode(self, active, interval=1, variation=3):
        self.idle = active
        self.idle_interval = interval
        self.idle_interval_variation = variation
    
    def set_curiosity(self, curious):
        self.curious = curious
    
    def set_cyclops(self, cyclops):
        self.cyclops = cyclops
    
    def set_h_flicker(self, flicker, amplitude=16):
        self.h_flicker = flicker
        self.h_flicker_amplitude = amplitude
    
    def set_v_flicker(self, flicker, amplitude=80):
        self.v_flicker = flicker
        self.v_flicker_amplitude = amplitude
    
    def set_sweat(self, sweat):
        self.sweat = sweat
    
    def close(self, left=True, right=True):
        if left:
            self.eye_l_height_next = 1
            self.eye_l_open = False
        if right:
            self.eye_r_height_next = 1
            self.eye_r_open = False
    
    def open(self, left=True, right=True):
        if left:
            self.eye_l_open = True
        if right:
            self.eye_r_open = True
    
    def blink(self, left=True, right=True):
        self.close(left, right)
        self.open(left, right)
    
    def anim_confused(self):
        self.confused = True
    
    def anim_laugh(self):
        self.laugh = True
    
    def draw_smooth_rounded_rect(self, surface, color, rect, radius):
        """Smooth rounded rectangle using pygame's built-in anti-aliasing"""
        x, y, w, h = rect
        if w <= 0 or h <= 0:
            return
        
        # Clamp radius to valid range
        radius = max(0, min(radius, w // 2, h // 2))
        
        # Use pygame's built-in rounded rectangle (has built-in anti-aliasing)
        pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    def draw_eyes(self):
        current_time = pygame.time.get_ticks()
        
        if self.curious:
            if self.eye_l_x_next <= 80:
                self.eye_l_height_offset = 64
            elif self.eye_l_x_next >= (self.get_screen_constraint_x() - 80) and self.cyclops:
                self.eye_l_height_offset = 64
            else:
                self.eye_l_height_offset = 0
            
            if self.eye_r_x_next >= self.screen_width - self.eye_r_width_current - 80:
                self.eye_r_height_offset = 64
            else:
                self.eye_r_height_offset = 0
        else:
            self.eye_l_height_offset = 0
            self.eye_r_height_offset = 0
        
        self.eye_l_height_current = (self.eye_l_height_current + self.eye_l_height_next + self.eye_l_height_offset) // 2
        self.eye_l_y += (self.eye_l_height_default - self.eye_l_height_current) // 2
        self.eye_l_y -= self.eye_l_height_offset // 2
        
        self.eye_r_height_current = (self.eye_r_height_current + self.eye_r_height_next + self.eye_r_height_offset) // 2
        self.eye_r_y += (self.eye_r_height_default - self.eye_r_height_current) // 2
        self.eye_r_y -= self.eye_r_height_offset // 2
        
        if self.eye_l_open and self.eye_l_height_current <= 1 + self.eye_l_height_offset:
            self.eye_l_height_next = self.eye_l_height_default
        if self.eye_r_open and self.eye_r_height_current <= 1 + self.eye_r_height_offset:
            self.eye_r_height_next = self.eye_r_height_default
        
        self.eye_l_width_current = (self.eye_l_width_current + self.eye_l_width_next) // 2
        self.eye_r_width_current = (self.eye_r_width_current + self.eye_r_width_next) // 2
        self.space_between_current = (self.space_between_current + self.space_between_next) // 2
        
        self.eye_l_x = (self.eye_l_x + self.eye_l_x_next) // 2
        self.eye_l_y = (self.eye_l_y + self.eye_l_y_next) // 2
        
        self.eye_r_x_next = self.eye_l_x_next + self.eye_l_width_current + self.space_between_current
        self.eye_r_y_next = self.eye_l_y_next
        self.eye_r_x = (self.eye_r_x + self.eye_r_x_next) // 2
        self.eye_r_y = (self.eye_r_y + self.eye_r_y_next) // 2
        
        if self.autoblinker and current_time >= self.blink_timer:
            self.blink()
            self.blink_timer = current_time + (self.blink_interval * 1000) + (random.randint(0, self.blink_interval_variation) * 1000)
        
        if self.laugh:
            if self.laugh_toggle:
                self.set_v_flicker(True, 40)
                self.laugh_timer = current_time
                self.laugh_toggle = False
            elif current_time >= self.laugh_timer + self.laugh_duration:
                self.set_v_flicker(False, 0)
                self.laugh_toggle = True
                self.laugh = False
        
        if self.confused:
            if self.confused_toggle:
                self.set_h_flicker(True, 160)
                self.confused_timer = current_time
                self.confused_toggle = False
            elif current_time >= self.confused_timer + self.confused_duration:
                self.set_h_flicker(False, 0)
                self.confused_toggle = True
                self.confused = False
        
        if self.idle and current_time >= self.idle_timer:
            self.eye_l_x_next = random.randint(0, self.get_screen_constraint_x())
            self.eye_l_y_next = random.randint(0, self.get_screen_constraint_y())
            self.idle_timer = current_time + (self.idle_interval * 1000) + (random.randint(0, self.idle_interval_variation) * 1000)
        
        eye_l_x_draw = self.eye_l_x
        eye_r_x_draw = self.eye_r_x
        eye_l_y_draw = self.eye_l_y
        eye_r_y_draw = self.eye_r_y
        
        if self.h_flicker:
            offset = self.h_flicker_amplitude if self.h_flicker_alternate else -self.h_flicker_amplitude
            eye_l_x_draw += offset
            eye_r_x_draw += offset
            self.h_flicker_alternate = not self.h_flicker_alternate
        
        if self.v_flicker:
            offset = self.v_flicker_amplitude if self.v_flicker_alternate else -self.v_flicker_amplitude
            eye_l_y_draw += offset
            eye_r_y_draw += offset
            self.v_flicker_alternate = not self.v_flicker_alternate
        
        eye_r_width_draw = 0 if self.cyclops else self.eye_r_width_current
        eye_r_height_draw = 0 if self.cyclops else self.eye_r_height_current
        
        # Draw directly to screen - NO SCALING
        self.screen.fill(self.BG_COLOR)
        
        # Use smooth rounded rectangles
        self.draw_smooth_rounded_rect(self.screen, self.MAIN_COLOR, 
                                     (eye_l_x_draw, eye_l_y_draw, self.eye_l_width_current, self.eye_l_height_current),
                                     self.eye_l_border_radius_current)
        
        if not self.cyclops:
            self.draw_smooth_rounded_rect(self.screen, self.MAIN_COLOR,
                                         (eye_r_x_draw, eye_r_y_draw, eye_r_width_draw, eye_r_height_draw),
                                         self.eye_r_border_radius_current)
        
        if self.tired:
            self.eyelids_tired_height_next = self.eye_l_height_current // 2
            self.eyelids_angry_height_next = 0
        else:
            self.eyelids_tired_height_next = 0
        
        if self.angry:
            self.eyelids_angry_height_next = self.eye_l_height_current // 2
            self.eyelids_tired_height_next = 0
        else:
            self.eyelids_angry_height_next = 0
        
        if self.happy:
            self.eyelids_happy_bottom_offset_next = self.eye_l_height_current // 2
        else:
            self.eyelids_happy_bottom_offset_next = 0
        
        self.eyelids_tired_height = (self.eyelids_tired_height + self.eyelids_tired_height_next) // 2
        self.eyelids_angry_height = (self.eyelids_angry_height + self.eyelids_angry_height_next) // 2
        self.eyelids_happy_bottom_offset = (self.eyelids_happy_bottom_offset + self.eyelids_happy_bottom_offset_next) // 2
        
        if self.eyelids_tired_height > 0:
            if not self.cyclops:
                pygame.draw.polygon(self.screen, self.BG_COLOR, [
                    (eye_l_x_draw, eye_l_y_draw - 1),
                    (eye_l_x_draw + self.eye_l_width_current, eye_l_y_draw - 1),
                    (eye_l_x_draw, eye_l_y_draw + self.eyelids_tired_height - 1)
                ])
                pygame.draw.polygon(self.screen, self.BG_COLOR, [
                    (eye_r_x_draw, eye_r_y_draw - 1),
                    (eye_r_x_draw + eye_r_width_draw, eye_r_y_draw - 1),
                    (eye_r_x_draw + eye_r_width_draw, eye_r_y_draw + self.eyelids_tired_height - 1)
                ])
            else:
                pygame.draw.polygon(self.screen, self.BG_COLOR, [
                    (eye_l_x_draw, eye_l_y_draw - 1),
                    (eye_l_x_draw + self.eye_l_width_current // 2, eye_l_y_draw - 1),
                    (eye_l_x_draw, eye_l_y_draw + self.eyelids_tired_height - 1)
                ])
                pygame.draw.polygon(self.screen, self.BG_COLOR, [
                    (eye_l_x_draw + self.eye_l_width_current // 2, eye_l_y_draw - 1),
                    (eye_l_x_draw + self.eye_l_width_current, eye_l_y_draw - 1),
                    (eye_l_x_draw + self.eye_l_width_current, eye_l_y_draw + self.eyelids_tired_height - 1)
                ])
        
        if self.eyelids_angry_height > 0:
            if not self.cyclops:
                pygame.draw.polygon(self.screen, self.BG_COLOR, [
                    (eye_l_x_draw, eye_l_y_draw - 1),
                    (eye_l_x_draw + self.eye_l_width_current, eye_l_y_draw - 1),
                    (eye_l_x_draw + self.eye_l_width_current, eye_l_y_draw + self.eyelids_angry_height - 1)
                ])
                pygame.draw.polygon(self.screen, self.BG_COLOR, [
                    (eye_r_x_draw, eye_r_y_draw - 1),
                    (eye_r_x_draw + eye_r_width_draw, eye_r_y_draw - 1),
                    (eye_r_x_draw, eye_r_y_draw + self.eyelids_angry_height - 1)
                ])
            else:
                pygame.draw.polygon(self.screen, self.BG_COLOR, [
                    (eye_l_x_draw, eye_l_y_draw - 1),
                    (eye_l_x_draw + self.eye_l_width_current // 2, eye_l_y_draw - 1),
                    (eye_l_x_draw + self.eye_l_width_current // 2, eye_l_y_draw + self.eyelids_angry_height - 1)
                ])
                pygame.draw.polygon(self.screen, self.BG_COLOR, [
                    (eye_l_x_draw + self.eye_l_width_current // 2, eye_l_y_draw - 1),
                    (eye_l_x_draw + self.eye_l_width_current, eye_l_y_draw - 1),
                    (eye_l_x_draw + self.eye_l_width_current // 2, eye_l_y_draw + self.eyelids_angry_height - 1)
                ])
        
        if self.eyelids_happy_bottom_offset > 0:
            self.draw_smooth_rounded_rect(self.screen, self.BG_COLOR,
                                         (eye_l_x_draw - 1, 
                                          (eye_l_y_draw + self.eye_l_height_current) - self.eyelids_happy_bottom_offset + 1,
                                          self.eye_l_width_current + 2, self.eye_l_height_default),
                                         self.eye_l_border_radius_current)
            if not self.cyclops:
                self.draw_smooth_rounded_rect(self.screen, self.BG_COLOR,
                                             (eye_r_x_draw - 1,
                                              (eye_r_y_draw + eye_r_height_draw) - self.eyelids_happy_bottom_offset + 1,
                                              eye_r_width_draw + 2, self.eye_r_height_default),
                                             self.eye_r_border_radius_current)
        
        if self.sweat:
            if self.sweat1_y <= self.sweat1_y_max:
                self.sweat1_y += 0.5
            else:
                self.sweat1_x_initial = random.randint(0, 240)
                self.sweat1_y = 16.0
                self.sweat1_y_max = random.randint(80, 160)
                self.sweat1_width = 8.0
                self.sweat1_height = 16.0
            
            if self.sweat1_y <= self.sweat1_y_max / 2:
                self.sweat1_width += 0.5
                self.sweat1_height += 0.5
            else:
                self.sweat1_width = max(0.8, self.sweat1_width - 0.1)
                self.sweat1_height = max(0.8, self.sweat1_height - 0.5)
            
            self.sweat1_x = self.sweat1_x_initial - self.sweat1_width / 2
            if self.sweat1_width > 0 and self.sweat1_height > 0:
                self.draw_smooth_rounded_rect(self.screen, self.MAIN_COLOR,
                                             (int(self.sweat1_x), int(self.sweat1_y), 
                                              max(1, int(self.sweat1_width)), max(1, int(self.sweat1_height))),
                                             self.sweat_border_radius)
            
            if self.sweat2_y <= self.sweat2_y_max:
                self.sweat2_y += 0.5
            else:
                self.sweat2_x_initial = random.randint(240, self.screen_width - 240)
                self.sweat2_y = 16.0
                self.sweat2_y_max = random.randint(80, 160)
                self.sweat2_width = 8.0
                self.sweat2_height = 16.0
            
            if self.sweat2_y <= self.sweat2_y_max / 2:
                self.sweat2_width += 0.5
                self.sweat2_height += 0.5
            else:
                self.sweat2_width = max(0.8, self.sweat2_width - 0.1)
                self.sweat2_height = max(0.8, self.sweat2_height - 0.5)
            
            self.sweat2_x = self.sweat2_x_initial - self.sweat2_width / 2
            if self.sweat2_width > 0 and self.sweat2_height > 0:
                self.draw_smooth_rounded_rect(self.screen, self.MAIN_COLOR,
                                             (int(self.sweat2_x), int(self.sweat2_y),
                                              max(1, int(self.sweat2_width)), max(1, int(self.sweat2_height))),
                                             self.sweat_border_radius)
            
            if self.sweat3_y <= self.sweat3_y_max:
                self.sweat3_y += 0.5
            else:
                self.sweat3_x_initial = self.screen_width - 240 + random.randint(0, 240)
                self.sweat3_y = 16.0
                self.sweat3_y_max = random.randint(80, 160)
                self.sweat3_width = 8.0
                self.sweat3_height = 16.0
            
            if self.sweat3_y <= self.sweat3_y_max / 2:
                self.sweat3_width += 0.5
                self.sweat3_height += 0.5
            else:
                self.sweat3_width = max(0.8, self.sweat3_width - 0.1)
                self.sweat3_height = max(0.8, self.sweat3_height - 0.5)
            
            self.sweat3_x = self.sweat3_x_initial - self.sweat3_width / 2
            if self.sweat3_width > 0 and self.sweat3_height > 0:
                self.draw_smooth_rounded_rect(self.screen, self.MAIN_COLOR,
                                             (int(self.sweat3_x), int(self.sweat3_y),
                                              max(1, int(self.sweat3_width)), max(1, int(self.sweat3_height))),
                                             self.sweat_border_radius)
        
        # NO SCALING - direct display update
        pygame.display.flip()
        self.clock.tick(self.fps)


def main():
    # Create at native 1024x512 resolution - perfectly smooth, no pixelation!
    eyes = RoboEyes(1024, 512)
    eyes.open()
    eyes.set_autoblinker(True, 2, 3)
    
    running = True
    demo_state = 0
    state_timer = pygame.time.get_ticks()
    state_duration = 3000
    
    print("RoboEyes Demo Started! (Native Resolution - No Scaling)")
    print("Press ESC to exit")
    print("\nControls:")
    print("1 - Normal mood")
    print("2 - Happy mood")
    print("3 - Tired mood")
    print("4 - Angry mood")
    print("5 - Toggle Idle mode")
    print("6 - Laugh animation")
    print("7 - Confused animation")
    print("8 - Toggle Sweat")
    print("9 - Toggle Cyclops")
    print("C - Toggle Curiosity")
    print("Arrow keys - Move eyes")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:
                    eyes.set_mood(Mood.DEFAULT)
                elif event.key == pygame.K_2:
                    eyes.set_mood(Mood.HAPPY)
                elif event.key == pygame.K_3:
                    eyes.set_mood(Mood.TIRED)
                elif event.key == pygame.K_4:
                    eyes.set_mood(Mood.ANGRY)
                elif event.key == pygame.K_5:
                    eyes.set_idle_mode(not eyes.idle)
                elif event.key == pygame.K_6:
                    eyes.anim_laugh()
                elif event.key == pygame.K_7:
                    eyes.anim_confused()
                elif event.key == pygame.K_8:
                    eyes.set_sweat(not eyes.sweat)
                elif event.key == pygame.K_9:
                    eyes.set_cyclops(not eyes.cyclops)
                elif event.key == pygame.K_c:
                    eyes.set_curiosity(not eyes.curious)
                elif event.key == pygame.K_UP:
                    eyes.set_position(Position.N)
                elif event.key == pygame.K_DOWN:
                    eyes.set_position(Position.S)
                elif event.key == pygame.K_LEFT:
                    eyes.set_position(Position.W)
                elif event.key == pygame.K_RIGHT:
                    eyes.set_position(Position.E)
                elif event.key == pygame.K_SPACE:
                    eyes.blink()
        
        current_time = pygame.time.get_ticks()
        if current_time - state_timer > state_duration:
            demo_state = (demo_state + 1) % 8
            state_timer = current_time
            
            if demo_state == 0:
                eyes.set_mood(Mood.DEFAULT)
                eyes.set_position(Mood.DEFAULT)
                print("Demo: Normal blinking")
            elif demo_state == 1:
                eyes.set_mood(Mood.HAPPY)
                print("Demo: Happy mood")
            elif demo_state == 2:
                eyes.set_mood(Mood.TIRED)
                print("Demo: Tired mood")
            elif demo_state == 3:
                eyes.set_mood(Mood.ANGRY)
                print("Demo: Angry mood")
            elif demo_state == 4:
                eyes.set_mood(Mood.DEFAULT)
                eyes.set_curiosity(True)
                eyes.set_idle_mode(True, 1, 2)
                print("Demo: Curious + Idle mode")
            elif demo_state == 5:
                eyes.set_curiosity(False)
                eyes.set_idle_mode(False)
                eyes.anim_laugh()
                print("Demo: Laugh animation")
            elif demo_state == 6:
                eyes.anim_confused()
                print("Demo: Confused animation")
            elif demo_state == 7:
                eyes.set_sweat(True)
                print("Demo: Sweat effect")
        
        eyes.draw_eyes()
    
    pygame.quit()

if __name__ == "__main__":
    print("This is a library try adding 'main()' or try 'testing.py'")
