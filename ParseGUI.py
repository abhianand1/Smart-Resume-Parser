from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView

class InterfaceApp(App):
    def build(self):
        self.smart_mode = None
        self.multi_mode = None

        layout = BoxLayout(orientation='vertical')

        # Smart Mode Toggle
        smart_mode_label = Label(text="Smart Mode:")
        self.smart_mode_toggle = ToggleButton(text="On", group="smart_mode")
        layout.add_widget(smart_mode_label)
        layout.add_widget(self.smart_mode_toggle)

        # Multi Mode Toggle
        multi_mode_label = Label(text="Multi Mode:")
        self.multi_mode_toggle = ToggleButton(text="On", group="multi_mode")
        layout.add_widget(multi_mode_label)
        layout.add_widget(self.multi_mode_toggle)

        # Submit Button
        submit_button = Button(text="Submit", on_press=self.submit_response)
        layout.add_widget(submit_button)

        return layout

    def submit_response(self, instance):
        if self.smart_mode_toggle.state == 'down':
            self.smart_mode = 'yes'
        else:
            self.smart_mode = 'no'

        if self.multi_mode_toggle.state == 'down':
            self.multi_mode = 'yes'
        else:
            self.multi_mode = 'no'

        if self.smart_mode == 'yes':
            self.ask_job_title()
        else:
            self.ask_ideal_job_description()

    def ask_job_title(self):
        layout = self.root
        layout.clear_widgets()

        job_title_label = Label(text="Enter Job Title:")
        job_title_input = TextInput()
        submit_button = Button(text="Submit", on_press=lambda x: self.set_job_title(job_title_input.text))

        layout.add_widget(job_title_label)
        layout.add_widget(job_title_input)
        layout.add_widget(submit_button)

    def set_job_title(self, job_title):
        self.job_title = job_title
        self.ask_multi_mode()

    def ask_ideal_job_description(self):
        layout = self.root
        layout.clear_widgets()

        job_description_label = Label(text="Enter Ideal Job Description:")
        job_description_input = TextInput()
        submit_button = Button(text="Submit", on_press=lambda x: self.set_ideal_job_description(job_description_input.text))

        layout.add_widget(job_description_label)
        layout.add_widget(job_description_input)
        layout.add_widget(submit_button)

    def set_ideal_job_description(self, ideal_job_description):
        self.ideal_job_description = ideal_job_description
        self.ask_multi_mode()

    def ask_multi_mode(self):
        layout = self.root
        layout.clear_widgets()

        if self.multi_mode == 'yes':
            folder_chooser = FileChooserListView(path='.')
            layout.add_widget(folder_chooser)
            submit_button = Button(text="Submit", on_press=lambda x: self.process_folder(folder_chooser.path))
        else:
            file_chooser = FileChooserListView(path='.')
            layout.add_widget(file_chooser)
            submit_button = Button(text="Submit", on_press=lambda x: self.process_file(file_chooser.selection))

        layout.add_widget(submit_button)

    def process_folder(self, folder_path):
        print(f"Folder path selected: {folder_path}")
        # Here you can perform further actions with the selected folder

    def process_file(self, file_path):
        print(f"File path selected: {file_path}")
        # Here you can perform further actions with the selected file

if __name__ == "__main__":
    InterfaceApp().run()
