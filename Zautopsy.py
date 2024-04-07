import streamlit as st

def main():
    st.title("File Selection Example")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        file_path = uploaded_file.name
        st.write("File Path:", file_path)

if __name__ == "__main__":
    main()
