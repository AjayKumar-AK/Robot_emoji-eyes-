from emotions import RoboEyes, Mood, Position
import pygame

pygame.init()

eyes = RoboEyes(1024, 512)
eyes.open()
eyes.set_autoblinker(True, 2, 3)
    
running = True
demo_state = 0
state_timer = pygame.time.get_ticks()
state_duration = 3000
    
print("RoboEyes Demo Started!")
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
