
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
import json

class MainMenu(Screen):
    pass

class GameScreen(Screen):
    pass

class GameWidget(Widget):
    player_x = NumericProperty(0)
    player_y = NumericProperty(0)
    player_velocity = ListProperty([0, 0])
    gravity = NumericProperty(-1.2)  # Adjusted gravity for more realistic feel
    move_speed = NumericProperty(5)
    touch_threshold = NumericProperty(20)  # Threshold for touch sensitivity
    jump_sound = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.background_music = SoundLoader.load('background_music.mp3')
        self.jump_sound = SoundLoader.load('jump_sound.wav')  # Load jump sound effect
        if self.background_music:
            self.background_music.loop = True
            self.background_music.play()

    def on_touch_move(self, touch):
        # Implement left/right movement with touch sensitivity threshold
        if abs(touch.x - self.player_x) > self.touch_threshold:
            if touch.x < self.player_x:
                self.player_velocity[0] = -self.move_speed
            elif touch.x > self.player_x:
                self.player_velocity[0] = self.move_speed

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.jump()

    def jump(self):
        if self.player_y == 0:  # Check if player is on the ground
            self.player_velocity[1] = 20  # Adjusted for jump height
            if self.jump_sound:
                self.jump_sound.play()  # Play jump sound effect

    def update(self, dt):
        self.player_x += self.player_velocity[0] * dt
        self.player_y += self.player_velocity[1] * dt

        # Apply gravity
        if self.player_y > 0:
            self.player_velocity[1] += self.gravity
        else:
            self.player_y = 0
            self.player_velocity[1] = 0
            self.player_velocity[0] = 0  # Stop horizontal movement when landing

        # Future implementation: Sophisticated collision detection with obstacles and enemies

class MysticMinerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    MysticMinerApp().run()
