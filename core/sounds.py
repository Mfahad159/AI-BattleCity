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

    def play_bg(self):
        if 'bg_music' in self.sounds:
            self.sounds['bg_music'].play(-1) # Loop forever

    def _generate_sounds(self):
        # Audible and clear sine-based sounds
        self.sounds['shoot'] = self._create_beep(660, 0.05, type='sine', vol=0.2)
        self.sounds['explosion'] = self._create_noise(0.2, vol=0.4)
        self.sounds['lose'] = self._create_beep(220, 1.0, type='sine', vol=0.5)
        self.sounds['level_start'] = self._create_beep(880, 0.2, type='sine', vol=0.4)
        self.sounds['bg_music'] = self._create_bg_loop()

    def _create_beep(self, freq, duration, type='sine', vol=0.5):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        
        if type == 'sine':
            samples = np.sin(2 * np.pi * freq * t)
        
        # Smooth fade out
        fade = np.linspace(1, 0, n_samples)**2
        samples = (samples * fade * 32767 * vol).astype(np.int16)
        
        # Make stereo
        stereo = np.zeros((n_samples, 2), dtype=np.int16)
        stereo[:, 0] = samples
        stereo[:, 1] = samples
        
        return pygame.sndarray.make_sound(stereo)

    def _create_noise(self, duration, vol=0.5):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        samples = np.random.uniform(-1, 1, n_samples)
        
        # Low pass filter for "thud" effect
        fade = np.linspace(1, 0, n_samples)**2
        samples = (samples * fade * 32767 * vol).astype(np.int16)
        
        stereo = np.zeros((n_samples, 2), dtype=np.int16)
        stereo[:, 0] = samples
        stereo[:, 1] = samples
        
        return pygame.sndarray.make_sound(stereo)

    def _create_bg_loop(self):
        # Techno-style background loop
        sample_rate = 22050
        duration = 1.0
        n_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        
        # 1. Bass Hum (Drone)
        drone = np.sin(2 * np.pi * 55 * t) * 0.3
        
        # 2. Rhythmic Kick (Four on the floor)
        kick = np.zeros(n_samples)
        for i in range(4):
            start = int(i * (n_samples // 4))
            k_t = np.linspace(0, 0.1, int(0.1 * sample_rate), False)
            k_wave = np.sin(2 * np.pi * (100 * np.exp(-30 * k_t)) * k_t) # Frequency sweep
            end = min(start + len(k_wave), n_samples)
            kick[start:end] = k_wave[:end-start]
            
        samples = (drone + kick * 0.4).astype(np.float32)
        samples = (samples * 0.15 * 32767).astype(np.int16) 
        
        stereo = np.zeros((n_samples, 2), dtype=np.int16)
        stereo[:, 0] = samples
        stereo[:, 1] = samples
        return pygame.sndarray.make_sound(stereo)

# Global instance
sounds = SoundManager()
