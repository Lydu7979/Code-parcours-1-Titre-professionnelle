from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Dict, Optional
import joblib
import uvicorn
import logging
import pickle
import numpy as np 
from pydantic import BaseModel
import pytest
from unidecode import unidecode
import re
import nltk
import stop_words
from nltk.corpus import stopwords
from stop_words import get_stop_words
s_w=list(set(stopwords.words('french')+stop_words.get_stop_words('fr')))+['plus']



app = FastAPI()
logging.basicConfig(filename='applilog.log', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')

class Entre(BaseModel):
    
    text : str



@app.get("/Bienvenue")
async def get():
    logging.info('good connection')
    result = {"Message": "Bonjour, ceci est la beta d'un algorithm d'analyse de sentiment", "Status Code": 200}
    return result

#Nettoyage
def nettoyage(texte):
    tex=[]
    s_w=list(set(stopwords.words('french')+stop_words.get_stop_words('fr')))+['plus']
    s_w=[unidecode(elem.lower()) for elem in s_w]
    # mettre en minuscule
    texte=texte.lower()
    # enlever les accents
    texte=unidecode(texte).replace("'"," ")
    
    # Lematize/Stem
    
    
    # enlever les chiffres et caracteres spéciaux
    pattern="([a-z]+)"
    
    for elem in re.findall(pattern,texte):
        # enlever les stop words
        if elem in s_w:
            continue
        else:
            tex.append(elem)
    return ' '.join(tex)

# Page sentiment
@app.post("/sentiment",response_model=Entre)
async def sentiment(item: Entre, token: str = Header(...)):
    
    texte = item.text
    texte = nettoyage(texte)
    #checking if all fields are present
    #set1 = {token, texte}
    #res = set([token, texte])
    #if set1 != res:
        # missing_fields = ', '.join(set1.difference(res))
        # res2 = {"Message": f"{missing_fields} missing", "Status Code": 400}
        # logging.warning('all fields are present!')
        # return res2
    
    

    # checking if token is the good one
    if token != "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9":
        result1 = {"Message": "Token Invalide", "Status Code": 401}
        logging.warning('token is the bad one!')
        return result1
    if texte == "":
        logging.warning('token is the good one!')
        return {"Message": "Texte empty", "Status Code": 200}
    
    
    
    #
    clf_pipe = joblib.load('sentiment_pipe(1).joblib')
    prediction = clf_pipe.predict([texte])[0]
   
    prediction = "Positif" if prediction == 1 else "Négatif"   
    response = {"text": texte, "prediction": prediction}
    # manageprediction_output = ["Positif", "Négatif"]
    # if prediction not in manageprediction_output:
    #     raise HTTPException(status_code=400, detail=f"prediction not in {manageprediction_output}")
    logging.basicConfig(filename='applilog.log', encoding='utf-8', level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    logging.info('Prediction OK')
    return response

def test_sentiment():
  assert sentiment(item: "Le temps est magnifique, aujourd'hui.", token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")['text'] != ''



if __name__ == '__main__':
    uvicorn.run('fastapi1:app', host='0.0.0.0', port = 8000)
