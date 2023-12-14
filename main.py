import pandas as pd
import os
from datetime import datetime
from tabulate import tabulate as tb
import pyfiglet
import requests
from dotenv import load

load()
api_token = os.getenv("MOVIE_API_TOKEN")

if not api_token:
    raise ValueError("API token not found. Please check your .env file.")

print(pyfiglet.figlet_format("Selamat Datang !",width=300))

url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_token}"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    apijson = response.json()
    movies = [
        {
            "Judul Film yang akan tayang": movie["title"],
            "Batas Umur": "Dewasa" if movie["adult"] else "Anak anak",
            "Tanggal Tayang": datetime.fromisoformat(movie["release_date"]).strftime("%d %b %Y")
        }
        for movie in apijson["results"][0:8]
        if datetime.fromisoformat(movie["release_date"]).year >= 2023
    ]

    df = pd.DataFrame(movies)
    df.index+=1

    def make_table_movies(movies):
        table = tb(movies,headers="keys",tablefmt="fancy_grid",numalign="center",stralign="center")
        return table
    print(make_table_movies(df))
    while True:
        user_input_film = int(input("Pilih Nomor Film : "))
        user_input_watchin = str(input("Apakah anda ingin menontonnya di IMAX? (y/n) (default=no) : "))
        if(user_input_film >= 0 and user_input_film <= len(movies)):
            print(df.loc[user_input_film]["Judul Film yang akan tayang"])
            continue
        else:
            print("Nomor yang kamu pilih tidak ada!")
        break
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
