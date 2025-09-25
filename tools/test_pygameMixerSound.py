import pygame
import time

try:
    pygame.mixer.init()
    print("Pygame mixer initialized successfully.")
    # Create a simple sound
    beep_sound = pygame.mixer.Sound(b'\x00\xff\x00\xff' * 100)
    print("Playing beep sound...")
    beep_sound.play()
    time.sleep(1) # Keep script alive for sound to play
    print("Sound played. Quitting mixer.")
    pygame.mixer.quit()
except Exception as e:
    print(f"Error initializing or playing sound with Pygame: {e}")

