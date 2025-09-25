import pygame
import time
import os
import array
import math

def create_sine_wave_sound(frequency, duration_ms, volume=0.5, sample_rate=44100):
    """
    Generates a stereo sine wave sound.
    frequency: frequency in Hz
    duration_ms: duration in milliseconds
    volume: amplitude (0.0 to 1.0)
    sample_rate: samples per second
    """
    num_samples = int(sample_rate * (duration_ms / 1000.0))
    # Pygame's default for Sound is 16-bit signed, so values from -32768 to 32767
    max_amplitude = 32767 * volume

    samples = array.array('h') # 'h' for signed short (2 bytes)

    for i in range(num_samples):
        # Calculate sine wave value
        value = max_amplitude * math.sin(2 * math.pi * frequency * (i / sample_rate))
        samples.append(int(value))
        samples.append(int(value)) # For stereo, append twice

    return pygame.mixer.Sound(samples)

print("--- Pygame Extended Sound Test ---")

# Try setting the audio driver (common for Linux are 'pulse' or 'alsa')
# You can uncomment and test these one by one if the default doesn't work.
# os.environ['SDL_AUDIODRIVER'] = 'pulse'
# os.environ['SDL_AUDIODRIVER'] = 'alsa'

try:
    # Initialize Pygame mixer with specific parameters for clarity
    # (Optional: you can remove arguments to use defaults, but specifying can help)
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
    print(f"Pygame mixer initialized. Driver: {pygame.mixer.get_init()}")

    # Create longer, more distinct sounds
    high_pitch_sound = create_sine_wave_sound(1200, 3000, volume=0.6) # 1200 Hz for 3 seconds
    medium_pitch_sound = create_sine_wave_sound(600, 3000, volume=0.6) # 600 Hz for 3 seconds
    low_pitch_sound = create_sine_wave_sound(200, 3000, volume=0.6)  # 200 Hz for 3 seconds

    print("\nPlaying HIGH pitch sound (1200 Hz for 3 seconds)...")
    high_pitch_sound.play()
    time.sleep(3.5) # Wait a bit longer than sound duration

    print("\nPlaying MEDIUM pitch sound (600 Hz for 3 seconds)...")
    medium_pitch_sound.play()
    time.sleep(3.5)

    print("\nPlaying LOW pitch sound (200 Hz for 3 seconds)...")
    low_pitch_sound.play()
    time.sleep(3.5)

    print("\nAll sounds played. Quitting mixer.")
    pygame.mixer.quit()

except Exception as e:
    print(f"\nAn error occurred: {e}")
    # If the mixer failed to initialize, get_init() might return None or raise an error
    try:
        if not pygame.mixer.get_init():
            print("Pygame mixer failed to initialize. Check audio drivers and system setup.")
    except Exception:
        pass # Ignore if get_init() itself fails
    print("Please ensure your audio devices are working and 'pygame' is correctly installed and configured.")

print("\n--- Test finished ---")
