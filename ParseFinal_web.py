from transformers import pipeline
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import preprocess_string
from sklearn.metrics.pairwise import cosine_similarity
import os
import pdfminer
import docx2txt
import PyPDF2
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import OutAI
import ExtractSkills

resume_path = None
resumes_folder = None
smart_mode = None
multi_resume_mode = None
job_title = None
ideal_job_description = None
text_output = ""
suggestions_text = ""

def web_app_start(smode, mmode, fpath, fopath, jtitle, jdesc):
    resume_path = fpath
    resumes_folder = fopath
    smart_mode = smode
    multi_resume_mode = mmode
    job_title = jtitle
    print("Title is ", job_title)
    ideal_job_description = jdesc

    def preprocess_text(text):
        return preprocess_string(text)

    def train_doc2vec_model(documents):
        tagged_documents = [TaggedDocument(preprocess_text(doc), [i]) for i, doc in enumerate(documents)]
        model = Doc2Vec(tagged_documents, vector_size=100, window=5, min_count=1, epochs=20)
        return model

    def calculate_similarity(candidate_text, ideal_job_description, model):
        candidate_vector = model.infer_vector(preprocess_text(candidate_text))
        ideal_job_vector = model.infer_vector(preprocess_text(ideal_job_description))
        similarity_score = cosine_similarity([candidate_vector], [ideal_job_vector])[0][0]
        return similarity_score

    def generate_job_description(job_title):
        # return OutAI.get_completion(f"The skills and experiences sought in a candidate applying for the role of a {job_title} are ")
        return ExtractSkills.extract_closest_skills(job_title)

    def suggest_improvements(in_job_title):
        return OutAI.get_completion(f"The suggested skills for the role of a {in_job_title} are:")

    def extract_text_from_pdf(file_path):
        text = ""
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""

    def extract_skills_experience_from_resume(resume_path):
        if resume_path.endswith(".pdf"):
            return extract_text_from_pdf(resume_path)
        elif resume_path.endswith(".docx"):
            try:
                resume_text = docx2txt.process(resume_path)
                return resume_text
            except Exception as e:
                print(f"Error reading DOCX: {e}")
                return ""
        else:
            print("Unsupported file format. Please provide a PDF or DOCX file.")
            return ""

    def process_single_resume(ideal_job_description, smart_mode):
        # resume_path = input("Enter the path to your resume (PDF or DOCX): ")
        candidate_text = extract_skills_experience_from_resume(resume_path)
        return candidate_text, ideal_job_description

    def process_multiple_resumes(ideal_job_description, smart_mode):
        # resumes_folder = input("Enter the path to the folder containing multiple resumes (PDF or DOCX): ")
        candidate_texts = []
        for filename in os.listdir(resumes_folder):
            if filename.endswith(".pdf") or filename.endswith(".docx"):
                resume_path = os.path.join(resumes_folder, filename)
                candidate_text = extract_skills_experience_from_resume(resume_path)
                candidate_texts.append((candidate_text, filename))
        return candidate_texts, ideal_job_description

    def make_output(input_string):
        words = input_string.split()
        new_string = ""
        for i, word in enumerate(words, 1):
            new_string += word + " "
            if i % 10 == 0:
                new_string += "<br>"
        return new_string

    def start_function():
        global text_output
        global suggestions_text
        # smart_mode = input("Do you want smart help? (yes/no): ").lower()
        # multi_resume_mode = input("Do you want to process multiple resumes? (yes/no): ").lower()

        if smart_mode == "yes":
            # job_title = input("Enter the job title: ")
            print(job_title)
            ideal_job_description = generate_job_description(job_title)
            print(f"\nGenerated ideal job description:\n{ideal_job_description}\n")
        else:
            # ideal_job_description = input("Enter the ideal job description: ")
            pass

        if multi_resume_mode == "yes":
            candidate_texts, _ = process_multiple_resumes(ideal_job_description, smart_mode)
            similarity_scores = []
            for candidate_text, filename in candidate_texts:
                model = train_doc2vec_model([candidate_text, ideal_job_description])
                similarity_score = calculate_similarity(candidate_text, ideal_job_description, model)
                similarity_scores.append((filename, similarity_score))

            sorted_resumes = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            text_output = "\nRanked resumes based on relevancy percentage:<br>"
            for i, (filename, score) in enumerate(sorted_resumes, start=1):
                text_output += f"\n<h5>{i}. {filename}</h5>: {(score-0.11) * 100}%<br>"
        else:
            candidate_text, _ = process_single_resume(ideal_job_description, smart_mode)
            model = train_doc2vec_model([candidate_text, ideal_job_description])
            similarity_score = calculate_similarity(candidate_text, ideal_job_description, model)
            text_output = f"\nRelevancy percentage for the provided resume: <h5> {(similarity_score-0.11) * 100}% </h5> <br>"
            suggestions_text = "<div></div>"
            improvements = suggest_improvements(job_title)
            if smart_mode == "yes":
                suggestions_text = f"<div><p style=\"font-size: 18px; color: #333; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);\">{improvements}</p></div>"

    # final_list = ParseGUIFinal.app_start()

    # #  final_list = [self.smart_mode, self.multi_mode, self.file_path, self.folder_path, self.job_title, self.ideal_job_description]
    # smart_mode = final_list[0]
    # multi_resume_mode = final_list[1]
    # resume_path = final_list[2]
    # resumes_folder = final_list[3]
    # if resume_path != None:
    #     resume_path = final_list[2][0]
    #     resumes_folder = None
    # if resumes_folder != None:
    #     resumes_folder = final_list[3]
    #     resume_path = None
    # job_title = final_list[4]
    # ideal_job_description = final_list[5]

    start_function()
    # text_output = make_output(text_output)
    final_output = f'''<!DOCTYPE html><html><head><title>"Dheeraj Anna's Portfolio"</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Crimson+Text&family=Nunito:ital,wght@1,300&display=swap" rel="stylesheet"><link rel="stylesheet" href="./style.css"></head><body><section id="title"><div class="container px-4 py-5 mb-5 text-center title-hero"><img class="d-block mx-auto mb-4" src="./assets/coffee-cup.png" alt="" width="120" height="120"><h1 class="display-5 fw-bold text-body-emphasis" id="name-heading" style=" margin-top: 40px; margin-bottom: 40px;">Here are the results!</h1><div class="col-lg-6 mx-auto"><p class="lead mb-4">{text_output}</p></div>{suggestions_text}<div class="flex-container all-beans"><img class="coffee-beans" id = "beans-1" src="./assets/coffee-beans.png" width="65" height="57"><img class="coffee-beans" id = "beans-2" src="./assets/coffee-beans.png" width="65" height="57"><img class="coffee-beans" id = "beans-3" src="./assets/coffee-beans.png" width="65" height="57"></div></div></section></body></html>'''
    with open(r"C:\Users\annad\OneDrive\Documents\Programmes\Resume Parser\index_web.html", "w") as file:
        file.write(final_output)
        file.close()

# OutputGUI.display_string(text_output)

#The text output consisting of generated suggestions needs work
#Open AI API key: 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