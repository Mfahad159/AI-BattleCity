import pygame
import numpy as np
import math

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2)
        self.sounds = {}
        self._generate_sounds()

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def _generate_sounds(self):
        # Generate simple retro sounds using numpy
        self.sounds['shoot'] = self._create_beep(440, 0.1, type='square')
        self.sounds['explosion'] = self._create_noise(0.3)
        self.sounds['move'] = self._create_beep(100, 0.05, type='sawtooth')

    def _create_beep(self, freq, duration, type='sine'):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        
        if type == 'sine':
            samples = np.sin(2 * np.pi * freq * t)
        elif type == 'square':
            samples = np.sign(np.sin(2 * np.pi * freq * t))
        elif type == 'sawtooth':
            samples = 2 * (t * freq - np.floor(0.5 + t * freq))
            
        # Fade out
        fade = np.linspace(1, 0, n_samples)
        samples = (samples * fade * 32767).astype(np.int16)
        
        # Make stereo
        stereo = np.zeros((n_samples, 2), dtype=np.int16)
        stereo[:, 0] = samples
        stereo[:, 1] = samples
        
        return pygame.sndarray.make_sound(stereo)

    def _create_noise(self, duration):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        samples = np.random.uniform(-1, 1, n_samples)
        
        # Low pass filter for "thud" effect
        fade = np.linspace(1, 0, n_samples)
        samples = (samples * fade * 32767).astype(np.int16)
        
        stereo = np.zeros((n_samples, 2), dtype=np.int16)
        stereo[:, 0] = samples
        stereo[:, 1] = samples
        
        return pygame.sndarray.make_sound(stereo)

# Global instance
sounds = SoundManager()
