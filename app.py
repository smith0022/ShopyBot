import pandas as pd
import numpy as np
import nltk
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from flask import Flask, request, jsonify
from flask.helpers import send_from_directory
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS,cross_origin
from engineio.async_drivers import eventlet
from flaskwebgui import FlaskUI
import re
nltk.download('punkt')
app = Flask(__name__,static_folder='front-end/build',static_url_path="")
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, async_mode='eventlet',cors_allowed_origins="*")
# Load the dataset
data = pd.read_csv('home_sdf_marketing_sample_for_amazon_in-ecommerce__20191001_20191031__30k_data - home_sdf_marketing_sa.csv')

@app.route('/')
@socketio.on("response")
def getcomport(comport):
    
    # Define tokenizer and stemmer
    stemmer = SnowballStemmer('english')
    def tokenize_and_stem(text):
        tokens = nltk.word_tokenize(text.lower())
        stems = [stemmer.stem(t) for t in tokens]
        return stems

    # Create stemmed tokens column

    # Define TF-IDF vectorizer and cosine similarity function
    tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize_and_stem)
    def cosine_sim(text1, text2):
        # tfidf_matrix = tfidf_vectorizer.fit_transform([text1, text2])
        text1_concatenated = ' '.join(text1)
        text2_concatenated = ' '.join(text2)
        tfidf_matrix = tfidf_vectorizer.fit_transform([text1_concatenated, text2_concatenated])
        return cosine_similarity(tfidf_matrix)[0][1]

    # Define search function
    def search_products(query):
        query_stemmed = tokenize_and_stem(query)
        data['similarity'] = data['stemmed_tokens'].apply(lambda x: cosine_sim(query_stemmed, x))
        results = data.sort_values(by=['similarity'], ascending=False).head(1)[['Product Title', 'Category','Image Urls']]
        return results
    genai.configure(api_key = 'AIzaSyD1a-t6qcECmlLup17EQS0tPPXprjONNo0')
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("'" + comport + "'  " + " token words from this statement and give the answer in 6 words separated by comas the first two word should be the product, next two words should be keywords for product title, next two words should be keywords for product description and all given keywords should be in single word and no quotes allowed and you have to mandatorily give 6 words")
    user_keywords = response.text.split(",")
    print(user_keywords)
    data = count_unique_keywords(user_keywords)
    print(data.size)
    try :

        data['stemmed_tokens'] = data.apply(lambda row: tokenize_and_stem(row['Product Title'] + ' ' + str(row['Product Description']) + " " + row['Category']), axis=1)
        res = search_products(response.text)
        print(str(res.iloc[0]['Product Title']))
        emit("response",[str(res.iloc[0]['Product Title']),res.iloc[0]['Image Urls'],comport])
    except:
        emit("response",["NO apt products for your request  !!!","",comport]) 
# Remove unnecessary columns
# data = data.drop('id', axis=1)

def count_unique_keywords(k1):
    # Read the CSV file into a DataFrame
    df = pd.read_csv('home_sdf_marketing_sample_for_amazon_in-ecommerce__20191001_20191031__30k_data - home_sdf_marketing_sa.csv')

    # Convert NaN (missing) values in 'Product Title' and 'Product Description' to empty strings
    df['Product Title'] = df['Product Title'].fillna('')
    df['Product Description'] = df['Product Description'].fillna('')
    df['Category'] = df['Category'].fillna('')
    df['Brand'] = df['Brand'].fillna('')

    # Convert keywords to lowercase for case-insensitive matching
    for i in range(len(k1)):
        k1[i] = k1[i].lower()

    # Generate regex pattern for whole word matching
    for i in  range(len(k1)):
        k1[i] = r'\b{}\b'.format(re.escape(k1[i]))

    # Function to count unique occurrences of keywords in a given text
    def count_unique_matches(text, pt):
        unique_matches = set(re.findall(pt, text.lower()))
        return len(unique_matches)

    # Create new column to store the count of unique keywords found in each row
    df['Unique Keyword Count'] = 0

    # Filter rows where keyword1 is found only in 'Product Title'
    keyword1_filtered_df = df[df['Product Title'].str.contains(k1[0], case=False)]
    semaphore = 0
    # Count unique keyword occurrences in 'Product Title' and update 'Unique Keyword Count' column
    for i in k1[1:] :
            if semaphore == 0:
                keyword1_filtered_df['Unique Keyword Count'] += 2 * keyword1_filtered_df['Product Title'].apply(count_unique_matches, pt=i)
                semaphore = 1
            else :
                keyword1_filtered_df['Unique Keyword Count'] += keyword1_filtered_df['Product Description'].apply(count_unique_matches, pt=i)
                semaphore = 0

    # Sort the DataFrame by 'Unique Keyword Count' in descending order
    sorted_df = keyword1_filtered_df.sort_values(by='Unique Keyword Count', ascending=False)
    sorted_df.drop('Unique Keyword Count', axis=1)
    return sorted_df

# web app
# img = Image.open('img.png')
# st.image(img,width=600)
# st.title("Search Engine and Product Recommendation System ON Am Data")
# query = st.text_input("Enter Product Name")
# sumbit = st.button('Search')
# if sumbit:

# def response():
#         genai.configure(api_key = 'AIzaSyD1a-t6qcECmlLup17EQS0tPPXprjONNo0')
#         model = genai.GenerativeModel('gemini-pro')
#         response = model.generate_content("'" + query + "'  " + " token words from this statement and give the answer in 5 words separated by comas")
#         print(response.text)
#         res = search_products(response.text)
#         return res
# res = response()
if __name__ == '__main__':
    socketio.run(app,port=5001)