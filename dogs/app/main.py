import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
from fastapi import FastAPI


app = FastAPI()
cats_url = os.environ.get("CATS_URL")


def response_model(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


@app.get("/")
def read_root():
    return {"message": "Welcome to this fantastic doggg app!"}


@app.get("/dogs/cats")
async def get_all_cats():
    """Send request to cat service to retrieve cat data"""
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    response = session.get(cats_url + '/cats')
    print(response.json())
    cats = dict(response.json())['data']

    if cats:
        return response_model(cats, "Cats data from dog app retrieved successfully")
    return response_model(cats, "Empty list returned")
