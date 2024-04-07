from transformers import pipeline
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import preprocess_string
from sklearn.metrics.pairwise import cosine_similarity
import os
import pdfminer
import docx2txt
import PyPDF2
import OutAI

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
    return OutAI.get_completion(f"For the Job Title: {job_title} the 15 core responsibilities, skills and experiences sought in an ideal candidate are")


def suggest_improvements(ideal_job_description, candidate_text):
    return OutAI.get_completion(f"For the ideal description: {ideal_job_description} and candidate description: {candidate_text}. Suggest some changes to make the candidate a better fit:")

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
    resume_path = input("Enter the path to your resume (PDF or DOCX): ")
    candidate_text = extract_skills_experience_from_resume(resume_path)
    return candidate_text, ideal_job_description

def process_multiple_resumes(ideal_job_description, smart_mode):
    resumes_folder = input("Enter the path to the folder containing multiple resumes (PDF or DOCX): ")
    candidate_texts = []
    for filename in os.listdir(resumes_folder):
        if filename.endswith(".pdf") or filename.endswith(".docx"):
            resume_path = os.path.join(resumes_folder, filename)
            candidate_text = extract_skills_experience_from_resume(resume_path)
            candidate_texts.append((candidate_text, filename))
    return candidate_texts, ideal_job_description

def start_function():
    smart_mode = input("Do you want smart help? (yes/no): ").lower()
    multi_resume_mode = input("Do you want to process multiple resumes? (yes/no): ").lower()

    if smart_mode == "yes":
        job_title = input("Enter the job title: ")
        ideal_job_description = generate_job_description(job_title)
        print(f"\nGenerated ideal job description:\n{ideal_job_description}\n")
    else:
        ideal_job_description = input("Enter the ideal job description: ")

    if multi_resume_mode == "yes":
        candidate_texts, _ = process_multiple_resumes(ideal_job_description, smart_mode)
        similarity_scores = []
        for candidate_text, filename in candidate_texts:
            model = train_doc2vec_model([candidate_text, ideal_job_description])
            similarity_score = calculate_similarity(candidate_text, ideal_job_description, model)
            similarity_scores.append((filename, similarity_score))

        sorted_resumes = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        print("\nRanked resumes based on similarity score:")
        for i, (filename, score) in enumerate(sorted_resumes, start=1):
            print(f"{i}. {filename}: {score:.2f}")
    else:
        candidate_text, _ = process_single_resume(ideal_job_description, smart_mode)
        model = train_doc2vec_model([candidate_text, ideal_job_description])
        similarity_score = calculate_similarity(candidate_text, ideal_job_description, model)
        print(f"\nSimilarity score for the provided resume: {similarity_score:.2f}")

start_function()
