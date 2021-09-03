import pytest

def test_sentiment():
  assert sentiment(item: "Le temps est magnifique, aujourd'hui.", token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")['text'] != ''
