import numpy as np
import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('punkt')

resumeDataSet = pd.read_csv(r'C:\Users\annad\OneDrive\Documents\Programmes\Resume Parser\resume_dataset.csv', encoding='utf-8')

def cleanResume(resumeText):
    resumeText = re.sub('https+s*', ' ', resumeText)
    resumeText = re.sub('RT|cc', ' ', resumeText)
    resumeText = re.sub('#s+', '', resumeText)
    resumeText = re.sub('@s+', '  ', resumeText)
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)
    return resumeText

resumeDataSet['cleaned_resume'] = resumeDataSet['Resume'].apply(lambda x: cleanResume(x))

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    return text

def tokenize_and_remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

def extract_skills(resume_text):
    cleaned_resume = preprocess_text(resume_text)
    tokens = tokenize_and_remove_stopwords(cleaned_resume)
    nouns = [word for (word, pos) in nltk.pos_tag(tokens) if pos.startswith('NN')]
    return nouns

resume_vectorizer = TfidfVectorizer(sublinear_tf=True, stop_words='english', max_features=1500)
resume_features = resume_vectorizer.fit_transform(resumeDataSet['cleaned_resume'])

le_category = LabelEncoder()
encoded_categories = le_category.fit_transform(resumeDataSet['Category'])

knn_classifier = KNeighborsClassifier()
knn_classifier.fit(resume_features, encoded_categories)

def predict_category(job_title):
    return job_title

def relevant_skills_for_category(job_title):
    relevant_skills = []
    predicted_category = predict_category(job_title)
    relevant_resumes = resumeDataSet[resumeDataSet['Category'] == predicted_category]
    if not relevant_resumes.empty:
        resume_text = relevant_resumes['cleaned_resume'].iloc[0]
        extracted_skills = extract_skills(resume_text)
        relevant_skills.extend(extracted_skills)
    return relevant_skills

def get_relevant_skills_for_job_title(job_title):
    relevant_skills = relevant_skills_for_category(job_title)
    return relevant_skills

import pandas as pd
from difflib import get_close_matches

def extract_closest_skills(job_title):
    resume_dataset = pd.read_csv(r'C:\Users\annad\OneDrive\Documents\Programmes\Resume Parser\resume_dataset.csv')
    unique_job_titles = resume_dataset['Category'].unique()
    print("Job title is ", job_title)
    print("Unique ones are ",  unique_job_titles)
    def find_closest_job_title(input_title, job_titles):
        closest_match = get_close_matches(input_title, job_titles, n=1, cutoff=0.5)
        if closest_match:
            return closest_match[0]
        else:
            return job_titles[0]

    closest_job_title = find_closest_job_title(job_title, unique_job_titles)
    output_list = get_relevant_skills_for_job_title(closest_job_title)
    out_str = ""
    for elem in output_list:
        out_str += (elem + " ")
    return out_str

# print(extract_closest_skills("Scientist"))
