import pandas as pd
import numpy as np
import streamlit as st
import string
import nltk
nltk.download('punkt')
import spacy
import pickle as p
import requests   # Importing requests to extract content from a url
from bs4 import BeautifulSoup as bs # Beautifulsoup is for web scrapping...used to scrap specific content 
import requests
import sys
import contractions
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser # Creating the parser
from sumy.summarizers.kl import KLSummarizer
from nltk.stem import WordNetLemmatizer
import re
from textblob import TextBlob    


def getTextFromURL(url):
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text


#Cleansing the text
def cleaned_text(column):
    texts = []
    for row in column:
        eBook = re.sub("[^A-Za-z" "]+"," ", str(row)).lower()
        eBook = re.sub("[0-9" "]+"," ", str(row)).lower()
        eBook = re.sub(r'[^\w]', ' ', str(row)).lower()
        eBook = re.sub(r'[^\S]', ' ', str(row)).lower()
        eBook = re.sub(r'\[.+\]', ' ', str(row)).lower()
        eBook = re.sub(r'[_—]', ' ', str(row)).lower()
        eBook = re.sub(r'[‘’“”]', '', str(row)).lower()
        eBook = eBook.split()
        eBook = ' '.join(eBook)
        texts.append(eBook)
    while("" in texts) :
        texts.remove("")    
    return texts

# Creating the summarizer
def kl_summarizer(column):
    parser=PlaintextParser.from_string(column,Tokenizer('english'))
    kl_summarizer=KLSummarizer()
    kl_summary=kl_summarizer(parser.document,sentences_count=3)
    summary_list = [str(sentence) for sentence in kl_summary]
    result = ' '.join(summary_list)

    return result
    

def expanded_text(text):
    expanded_words = []
    for word in text.split():
        expanded_words.append(contractions.fix(word)) #using contractions.fix to expand the shotened words
    expanded_text = ' '.join(expanded_words)
    return expanded_text

def user_input_info():
    raw_url = st.text_input("Enter URL", "https://www.gutenberg.org/cache/epub/46/pg46-images.html")
    return raw_url

def main():
    st.title("**Team-6**")
    st.title("Summary Generator")
    st.write("**This app generate summary and its sentiment**")
    
    html_temp = """
    <div style="background-color:#20B2AA;padding:10px">
    <h2 style="color:white;text-align:center">E-BOOK SUMMARY </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    
    Url = user_input_info()
    r = requests.get(Url)
    soup = bs(r.text, "html.parser")
    Title = soup.title
    Title = Title.get_text()
    st.write('Book Title:-', Title)

    chapter_name = st.selectbox("Select Chapter", ["Chapter-1","Chapter-2","Chapter-3","Chapter-4","Chapter-5"])

    text = getTextFromURL(Url)
    chapter1 = expanded_text(text)[515:36432]
    chapter2 = expanded_text(text)[36433:70202]
    chapter3 = expanded_text(text)[70204:116232]
    chapter4 = expanded_text(text)[116233:145137]
    chapter5 = expanded_text(text)[145138:157592]
        
    en = spacy.load('en_core_web_sm')
    df = pd.DataFrame({"ChapterName":[1,2,3,4,5],
           "story":[en(chapter1), en(chapter2), en(chapter3), en(chapter4), en(chapter5)]})

    df['story'] = cleaned_text(df['story'])
    summary_result = ""
    sentiment = ""
    if st.button("Summarize"):
        if chapter_name == 'Chapter-1':
            summary_result = kl_summarizer(df['story'][0])
        elif chapter_name == 'Chapter-2':
            summary_result = kl_summarizer(df['story'][1])            
        elif chapter_name == 'Chapter-3':
            summary_result = kl_summarizer(df['story'][2])
        elif chapter_name == 'Chapter-4':
            summary_result = kl_summarizer(df['story'][3])
        elif chapter_name == 'Chapter-5':
            summary_result = kl_summarizer(df['story'][4])

        st.success('Summary:- {}'.format(summary_result))
        
        Analysis = TextBlob(summary_result)
        sentiment = f' {"Positive" if Analysis.polarity > 0 else "negative" if Analysis.polarity < 0 else "neutral"}'
        
        st.success('Sentiment:- {}'.format(sentiment)) 
  

    st.subheader("CREATED BY:-")
    st.write("***SAYED***",",","***NAYEEM***")
    st.write("***SAGAR***",",","***ANIL***")


if __name__=='__main__':
    main()
