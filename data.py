import os
import json
from dotenv import load
import requests


load()
api_token = os.getenv("MOVIE_API_TOKEN")
os.system("clear||cls")

url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_token}"
}

response = requests.get(url, headers=headers)
formatjson = json.dumps(response.json()["results"],indent=4)

print(formatjson)
