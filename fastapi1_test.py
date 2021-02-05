from fastapi.testclient import TestClient

from fastapi1 import app

client = TestClient(app)


def test_read_main():
    response = client.get("/Bienvenue")
    assert response.status_code == 200
    assert response.json() == {"Message": "Bonjour, ceci est la beta d'un algorithm d'analyse de sentiment", "Status Code": 200}


    

def test_output_sentiment():
    reponse = client.post("/sentiment", headers = {​​​​​​​​"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"}​​​​​​​​,
    json = {​​​​​​​​"text": "super"}​​​​​​​​) 
    #assert 0==1, reponse.json()
    prediction = reponse.json()["prediction"]
    #assert prediction in ['Positif', 'Négatif']
    assert reponse.status_code ==200,reponse.json()
    assert reponse.json() =={​​​​​​​​ "text": "super", "prediction": prediction}​​​​​​​​

 

