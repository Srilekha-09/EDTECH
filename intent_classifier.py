import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random
import time

from twilio.rest import Client

from universalScraper import scrape_text
from pdfScraper import pdf_search
from videoScraper import scrape_video
from db import userauth, check, update
from career_prediction_final import growthRate
from job_scrape import job_seek


stop_words = stopwords.words('english')

def clean_corpus(corpus):
  corpus = [ doc.lower() for doc in corpus]
  cleaned_corpus = []
  
  stop_words = stopwords.words('english')
  wordnet_lemmatizer = WordNetLemmatizer()

  for doc in corpus:
    tokens = word_tokenize(doc)
    cleaned_sentence = [] 
    for token in tokens: 
      if token not in stop_words and token.isalpha(): 
        cleaned_sentence.append(wordnet_lemmatizer.lemmatize(token)) 
    cleaned_corpus.append(' '.join(cleaned_sentence))
  return cleaned_corpus

with open('intents.json', 'r',encoding='utf-8') as file:
  intents = json.load(file)

corpus = []
tags = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        corpus.append(pattern)
        tags.append(intent['tag'])

cleaned_corpus = clean_corpus(corpus)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(cleaned_corpus)
encoder = OneHotEncoder()
y = encoder.fit_transform(np.array(tags).reshape(-1,1))

model = Sequential([
                    Dense(150, input_shape=(X.shape[1],), activation='relu'),
                    Dropout(0.2),
                    Dense(75, activation='relu'),
                    Dropout(0.2),
                    Dense(y.shape[1], activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

history = model.fit(X.toarray(), y.toarray(), epochs=22, batch_size=1)

INTENT_NOT_FOUND_THRESHOLD = 0.90

def predict_intent_tag(message):
  message = clean_corpus([message])
  X_test = vectorizer.transform(message)
  
  y = model.predict(X_test.toarray()) 

  if y.max() < INTENT_NOT_FOUND_THRESHOLD:
    return 'noanswer'
  
  prediction = np.zeros_like(y[0])
  prediction[y.argmax()] = 1
  tag = encoder.inverse_transform([prediction])[0][0]
  return tag

def get_intent(tag):
  
  for intent in intents['intents']:
    if intent['tag'] == tag:
      return intent

job_lst = []
def search(query):

  tag = predict_intent_tag(query)
  intent = get_intent(tag)

  if intent != None and intent['tag'] == 'greeting' and check('flow') == 'EMPTY':
    db_check = userauth('919538533738')
    if db_check == 'new User':
      return 'We are all set👍'
    else:
      response = random.choice(intent['responses'])
      return response

  elif check('flow') == 'career' or (intent != None and intent['tag'] == 'career'):
    if(check('num') == -1):
        # update from EMPTY to career in db
        update('flow', 'EMPTY', 'career')
        update('num', -1, 1)
        # send list
        lst = ['career', 'Please refer the below website to get an insight of all the skills👇', 'https://marcresi.github.io/CareerList/', 'Enter you skills:']
        return lst
    else:
        career_lst = growthRate(query)
        # update in db
        update('flow', 'career', 'EMPTY')
        update('num', 1, -1)
        return career_lst
    

  elif check('flow') == 'job' or (intent != None and intent['tag'] == 'job'):

    if(check('num') == -1):
        # update from EMPTY to job in db
        update('flow', 'EMPTY', 'job')
        update('num', -1, 1)
        return "Enter job:"

    elif (check('num') == 1):
        job_lst.append(query)
        update('num', 1, 2)
        return "Enter location:"

    elif (check('num') == 2):
        job_lst.append(query)
        update('num', 2, 3)
        return "Enter job type:"

    elif (check('num') == 3):
        job_lst.append(query)
        job_res = job_seek(job_lst)
        job_lst.clear()
        # update in db
        update('flow', 'job', 'EMPTY')
        update('num', 3, -1)
        return job_res

  elif intent != None and intent['tag'] != 'document' and intent['tag'] != 'video':
    response = random.choice(intent['responses'])
    return response

  account_sid = 'AC483282f4bea90c5993e20076bf7f6e55'
  auth_token = '64513d72f378add3b78a408a1124572d'
  client = Client(account_sid, auth_token)

  message = client.messages \
      .create(
           from_='whatsapp:+14155238886',
           body='🤖Bot is thinking...',
           to='whatsapp:+916361276796'
       )

  print(message.sid)

  if intent != None and intent['tag'] == 'document':
    pdf_res = pdf_search(query)
    return pdf_res
  elif intent != None and intent['tag'] == 'video':
    vid_res = scrape_video(query)
    return vid_res

  text_res = scrape_text(query)
  return text_res
