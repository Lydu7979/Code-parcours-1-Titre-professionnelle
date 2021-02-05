from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Dict, Optional
import joblib
import uvicorn
import logging
import pickle
import numpy as np 
from pydantic import BaseModel



app = FastAPI()
logging.basicConfig(filename='applilog.log', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')

class Entre(BaseModel):
    
    text : str



@app.get("/Bienvenue")
async def get():
    logging.info('good connection')
    result = {"Message": "Bonjour, ceci est la beta d'un algorithm d'analyse de sentiment", "Status Code": 200}
    return result

# Page sentiment
@app.post("/sentiment",response_model=Entre)
async def sentiment(item: Entre, token: str = Header(...)):
    
    texte = item.text
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

if __name__ == '__main__':
    uvicorn.run('fastapi1:app', host='0.0.0.0', port = 8000)
