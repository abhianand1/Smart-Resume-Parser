import streamlit as st
import os
import ParseFinal_web

final_list = []

# Customizing Streamlit theme colors
st.markdown(
    """
    <style>
    body {
        background-color: #f0f5f5; /* Set the background color of the body */
    }
    .sidebar .sidebar-content {
        background-color: #2b6d73; /* Set the background color of the sidebar */
        color: white; /* Set the text color in the sidebar */
    }
    </style>
    """,
    unsafe_allow_html=True
)

class InterfaceApp:
    def __init__(self):
        self.file_or_folder = None
        self.smart_mode = None
        self.multi_mode = None
        self.ideal_job_title = None
        self.ideal_job_description = None
        self.file_path = None
        self.folder_path = None

    def run(self):
        self.ask_options()

    def ask_options(self):
        st.title("Job Description Analyzer")

        # Select File or Folder
        st.header("Select File or Folder")
        self.file_or_folder = st.radio("Select Mode:", ("File", "Folder"), key="file_or_folder")
        if self.file_or_folder == "File" or self.file_or_folder == "Folder":
            self.ask_file()

        # Smart Mode
        st.header("Smart Mode")
        self.smart_mode = st.checkbox("Enable Smart Mode", key="smart_mode")
        if self.smart_mode:
            self.smart_mode = "yes"
        else:
            self.smart_mode = "no"

        # Multi Mode
        st.header("Multi Mode")
        self.multi_mode = st.checkbox("Enable Multi Mode", key="multi_mode")
        if self.multi_mode:
            self.multi_mode = "yes"
        else:
            self.multi_mode = "no"

        # Ideal Job Description
        st.header("Ideal Job Details")
        input_details = st.text_input("Enter Ideal Job Title/Description", key="input_details")
        if self.smart_mode:
            self.ideal_job_title = input_details
        else:
            self.ideal_job_description = input_details

        if st.button("Submit"):
            st.success("Data saved successfully!")
            ParseFinal_web.web_app_start(self.smart_mode, self.multi_mode, self.file_path, self.folder_path, self.ideal_job_title, self.ideal_job_description)

    def ask_file(self):
        st.subheader("File Selection" if self.file_or_folder == "File" else "Folder Selection")
        filenames = os.listdir(r"C:\Users\annad\OneDrive\Documents\Programmes\Resume Parser")
        selected_filename = st.selectbox('Select a file', filenames, key="selected_filename")
        if self.file_or_folder == "File":
            self.file_path = ('C:\\Users\\annad\\OneDrive\\Documents\\Programmes\\Resume Parser\\' + selected_filename)
        else:
            self.folder_path = ('C:\\Users\\annad\\OneDrive\\Documents\\Programmes\\Resume Parser\\' + selected_filename)

    def get_values(self):
        if self.smart_mode:
            self.smart_mode = "yes"
        else:
            self.smart_mode = "no"

        if self.multi_mode:
            self.multi_mode = "yes"
        else:
            self.multi_mode = "no"
        final_list.append(self.smart_mode)
        final_list.append(self.multi_mode)
        final_list.append(self.file_path)
        final_list.append(self.folder_path)
        final_list.append(self.ideal_job_title)
        final_list.append(self.ideal_job_description)

def app_start():
    interface_app = InterfaceApp()
    interface_app.run()
    return final_list

app_start()
