import json
from app import app

def test_prediction():
    client = app.test_client()

    sample_input = {
        "Age": 30,
        "Gender": 1,
        "Speed_of_Impact": 50.0,
        "Helmet_Used": 1,
        "Seatbelt_Used": 1
    }

    response = client.post('/predict', data=json.dumps(sample_input), content_type='application/json')
    assert response.status_code == 200
    assert 'Survived' in response.json
