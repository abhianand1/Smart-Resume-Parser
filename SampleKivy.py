from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MyApp(App):
    def build(self):
        # Create a vertical box layout
        layout = BoxLayout(orientation='vertical')

        # Add a label widget
        label = Label(text='Hello, Kivy!')
        layout.add_widget(label)

        # Add a button widget
        button = Button(text='Click Me!')
        button.bind(on_press=self.on_button_click)
        layout.add_widget(button)

        return layout

    def on_button_click(self, instance):
        print('Button clicked!')

if __name__ == '__main__':
    MyApp().run()
