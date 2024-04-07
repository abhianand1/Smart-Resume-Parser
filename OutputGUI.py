from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class StringDisplayApp(App):
    def __init__(self, text_to_display="", **kwargs):
        super().__init__(**kwargs)
        self.text_to_display = text_to_display

    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        display_label = Label(text=self.text_to_display, font_size=18)
        layout.add_widget(display_label)

        return layout

def display_string(text_to_display):
    StringDisplayApp(text_to_display=text_to_display).run()

