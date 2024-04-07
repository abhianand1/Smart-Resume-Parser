from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView

final_list = []

class InterfaceApp(App):
    def build(self):
        self.smart_mode = None
        self.multi_mode = None
        self.file_path = None
        self.folder_path = None
        self.job_title = None
        self.ideal_job_description = None

        layout = BoxLayout(orientation='vertical')

        smart_mode_label = Label(text="Smart Mode:")
        self.smart_mode_toggle = ToggleButton(text="Click to toggle Smart Mode", group="smart_mode")
        layout.add_widget(smart_mode_label)
        layout.add_widget(self.smart_mode_toggle)

        multi_mode_label = Label(text="Multi Mode:")
        self.multi_mode_toggle = ToggleButton(text="Click to toggle Multi Mode", group="multi_mode")
        layout.add_widget(multi_mode_label)
        layout.add_widget(self.multi_mode_toggle)

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
        self.folder_path = folder_path
        print(f"Folder path selected: {self.folder_path}")
        self.get_values()

    def process_file(self, file_path):
        self.file_path = file_path
        print(f"File path selected: {self.file_path}")
        self.get_values()

    def get_values(self):
        global final_list
        final_list = [self.smart_mode, self.multi_mode, self.file_path, self.folder_path, self.job_title, self.ideal_job_description]


def app_start():
    global final_list
    interface_app = InterfaceApp()
    interface_app.run()
    return final_list

def app_stop():
    interface_app.stop()