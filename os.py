# -*- coding: utf-8 -*-


import pandas as pd
import streamlit as st
import numpy as np
import docx2txt,textract
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from wordcloud import WordCloud,ImageColorGenerator
import plotly.express as px
import matplotlib.pyplot  as plt

from pickle import load
import pickle
model=load(open(r"C:\Users\Naimish\Desktop\Resume\RandomForestClassifier.pkl",'rb'))
vectors = pickle.load(open(r"C:\Users\Naimish\Desktop\Resume\vector.pkl",'rb'))



resume = []

def display(doc_file):
    if doc_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume.append(docx2txt.process(doc_file))
    else :
        with pdfplumber.open(doc_file) as pdf:
            pages=pdf.pages[0]
            resume.append(pages.extract_text())
            
    return resume
    
def mostcommon_words(cleaned,i):
    tokenizer = RegexpTokenizer(r'\w+')
    words=tokenizer.tokenize(cleaned)
    mostcommon=FreqDist(cleaned.split()).most_common(i)
    return mostcommon


def display_wordcloud(mostcommon):
    wordcloud=WordCloud(width=1000, height=600, background_color='black').generate(str(mostcommon))
    a=px.imshow(wordcloud)
    st.plotly_chart(a)
    
def display_words(mostcommon_small):
    x,y=zip(*mostcommon_small)
    chart=pd.DataFrame({'keys': x,'values': y})
    fig=px.bar(chart,x=chart['keys'],y=chart['values'],height=700,width=700)
    st.plotly_chart(fig)    

def preprocess(sentence):
    sentence=str(sentence)
    sentence = sentence.lower()
    sentence=sentence.replace('{html}',"") 
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', sentence)
    rem_url=re.sub(r'http\S+', '',cleantext)
    rem_num = re.sub('[0-9]+', '', rem_url)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(rem_num)  
    filtered_words = [w for w in tokens if len(w) > 2 if not w in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    lemma_words=[lemmatizer.lemmatize(w) for w in filtered_words]
    return " ".join(lemma_words)  




def main():
    menu = ["Prediction page","About"]
    choice = st.sidebar.selectbox("Menu",menu)
    html_temp = """
    <div style ="background-color:black;padding:13px">
    <h1 style ="color:white;text-align:center;"> RESUME CLASSIFICATION </h1>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    
    
    if choice == "Prediction page":
        st.subheader("Prediction Application")
    upload_file = st.file_uploader('Please Upload a Resume you want to predict for ',
                                type= ['docx','pdf'],accept_multiple_files=True)
        
    if st.button("Predict"):
        for doc_file in upload_file:
            if doc_file is not None:
               
                file_details = {'filename':[doc_file.name],
                               'filetype':doc_file.type.split('.')[-1].upper(),
                               'filesize':str(doc_file.size)+' KB'}
                file_type=pd.DataFrame(file_details)
                st.write(file_type.set_index('filename'))
                displayed=display(doc_file)
                cleaned=preprocess(display(doc_file))
                predicted= model.predict(vectors.transform([cleaned]))

                if int(predicted) == 0:
                    st.header("The Resume Is From Peoplesoft Resumes")
                elif int(predicted) == 1:
                    st.header("The Resume Is From ReactJs Developer ")
                elif int(predicted) == 2:
                    st.header("The Resume Is From  SQL Developer Lightning insight")
                else:
                    st.header("The Resume Is From  Workday Resumes ")

               
                
                cleaned=preprocess(display(doc_file))
                predicted= model.predict(vectors.transform([cleaned]))
                
                string='The Uploaded Resume is belongs to '
                st.header(string)
                
                st.subheader('WORDCLOUD')
                display_wordcloud(mostcommon_words(cleaned,100))
                
                st.header('Frequency of 20 Most Common Words')
                display_words(mostcommon_words(cleaned,20))
                target = {0:'Peoplesoft',1:'SQL Developer',2:'React JS Developer',3:'Workday'}

    elif choice == "About":
        st.header("About") 
        st.subheader("This is a Resume Classification by Group 2")
        st.info("Naimish Wankhade")
        st.info("Akhand Chitransh")
        st.info("Rushikesh Nere")
        st.info("Divyanshu Sharma")
        st.info("Pooja Patil")
        st.info("Susmita Ajagekar")
        st.info("Dashrath Khatri")
        

                
    
if __name__ == '__main__':
     main()