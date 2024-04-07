from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def page1():
    return render_template('page1.html')

@app.route('/page2', methods=['POST'])
def page2():
    smart_mode = request.form.get('smart_mode')
    return render_template('page2.html', smart_mode=smart_mode)

@app.route('/page3', methods=['POST'])
def page3():
    multi_mode = request.form.get('multi_mode')
    return render_template('page3.html', multi_mode=multi_mode)

@app.route('/submit', methods=['POST'])
def submit():
    smart_mode = request.form.get('smart_mode')
    multi_mode = request.form.get('multi_mode')
    job_title = request.form.get('job_title')
    job_description = request.form.get('job_description')
    
    if multi_mode == 'yes':
        folder_path = request.form.get('folderInput')
        file_path = None
    else:
        file_path = request.form.get('fileInput')
        folder_path = None
    
    # Process the form data here
    print("Smart Mode:", smart_mode)
    print("Multi Mode:", multi_mode)
    print("Job Title:", job_title)
    print("Job Description:", job_description)
    print("File Path:", file_path)
    print("Folder Path:", folder_path)
    
    return 'Form submitted successfully!'


if __name__ == '__main__':
    app.run(debug=True)
