import pandas as pd
import os
from datetime import datetime
from tabulate import tabulate as tb
import pyfiglet
import requests
from dotenv import load
import time
import random
from babel.numbers import format_currency, format_number
from babel import Locale


load()
api_token = os.getenv("MOVIE_API_TOKEN")
os.system("clear||cls")

if not api_token:
    raise ValueError("API Tidak ditemukan. Please cek .env anda.")

print(pyfiglet.figlet_format("Welcome !",font="larry3d", width=300))
# print(pyfiglet.figlet_format("Kelompok 4",font="larry3d", width=300))
indonesian_locale = Locale('id', 'ID')

url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_token}"
}

response = requests.get(url, headers=headers)

# Simulate loading animation
print("Fetching Data Film ", end="")
for i in range(10):
    time.sleep(0.1)  # Sleep for 0.1 seconds
    if(i % 2 == 0):
        print("⏳", end="", flush=True)
    else:
        print("⌛️", end="", flush=True)


print("\n")  # Move to the next line after the loading animation

if response.status_code == 200:
    apijson = response.json()

    if not apijson["results"]:
        print("Film yang akan tayang kosong 😢")
    else:
        def generate_duration():
            # Menghasilkan durasi acak antara 1 jam 45 menit (105 menit) dan 2 jam (120 menit)
            duration_minutes = random.randint(105, 120)
            
            # Memastikan durasi adalah kelipatan 5
            duration_minutes = (duration_minutes // 5) * 5
            
            # Konversi durasi menjadi jam dan menit
            hours = duration_minutes // 60
            minutes = duration_minutes % 60
            if minutes == 0:
                formatted_duration = f"{hours} Jam"
            else:
                formatted_duration = f"{hours} Jam {minutes} Menit"
            return formatted_duration           

        movies = [
            {
                "Judul Film yang akan tayang 🎥": movie["title"],
                "Minimal Umur 👨‍👩‍👧‍👦": "18-25" if movie["adult"] else "6-18",
                "Tanggal Tayang 📆": datetime.fromisoformat(movie["release_date"]).strftime("%d %b %Y"),
                "Durasi ⏱":generate_duration()
            }
            for movie in apijson["results"][0:8]
            if datetime.fromisoformat(movie["release_date"]).year >= 2023
        ]

        def generate_watch_time():
            open_mall = 10
            arr_of_time = []

            for index, movie in enumerate(movies):
                duration_parts = movie["Durasi ⏱"].split()
                hours = int(duration_parts[0]) if "Jam" in duration_parts else 0
                minutes = int(duration_parts[-2]) if "Menit" in duration_parts else 0
                minute = minutes + 3

                if len(arr_of_time) > 0:
                    start_time = arr_of_time[index-1].split('-')[1].strip()
                else:
                    start_time = f"{open_mall:02d}:00"

                end_time = pd.to_datetime(start_time, format="%H:%M") + pd.to_timedelta(f"{hours} hours {minute} minutes")
                end_time_str = end_time.strftime("%H:%M")

                arr_of_time.append(f"{start_time} - {end_time_str}")

                open_mall = int(end_time_str.split(":")[0])
            
            return arr_of_time

        df = pd.DataFrame(movies)
        df.index.name = "No"
        df.index += 1
        df["Pukul 🕘"] = generate_watch_time()

        def make_table_movies(movies):
            table = tb(movies, headers="keys", tablefmt="fancy_grid", numalign="center", stralign="center")
            return table

        print(make_table_movies(df))

        days = ("senin","selasa","rabu","kamis","jumat","sabtu","minggu")
        special_days = ("sabtu","minggu")
        user_tickets = []
        options = ["y", "yes", "ya","iya","yea"]
        price = 0
        total_price_with_tax = 0
        tax = 0.073
        while True:
            userinput_ticket_film = int(input("Pilih Nomor Film : "))
            if(not(1 <= userinput_ticket_film <= len(movies))):
                print("Input nomor film anda tidak ada!")
                continue
            userinput_ticket_quantity = int(input("Jumlah Tiket : "))
            if(userinput_ticket_quantity <= 0):
                print("Jumlah tiket anda kosong")
                continue
            if(userinput_ticket_quantity > 10):
                print("Jumlah tiket lebih dari batas maksimal (10)!")
                continue
            userinput_ticket_day = str(input("Masukkan hari untuk menonton : ")).casefold()
            if(userinput_ticket_day not in days):
                print("Input hari anda salah!")
                continue
            user_input_watch_in = str(input("Apakah anda ingin menontonnya di IMAX? (y/n) (default=no) : ")).casefold()
            if user_input_watch_in in options and userinput_ticket_day in special_days:
                price =  70000 * userinput_ticket_quantity
            elif user_input_watch_in in options:
                price =  65000 * userinput_ticket_quantity
            else:
                price = 50000 * userinput_ticket_quantity
            formatted_price = format_currency(price, 'IDR', locale='id_ID')
            tax_amount = price*tax
            total_price_with_tax += tax_amount + price
            user_movie_option = {
                "Tiket Film yang dipesan 🍿": df.loc[userinput_ticket_film]["Judul Film yang akan tayang 🎥"]+f" ({str(userinput_ticket_quantity)})",
                "Menonton di IMAX 🎥": "✅" if user_input_watch_in in options else "❌",
                "Hari 📆":userinput_ticket_day.capitalize(),
                "Pukul 🕘":df.loc[userinput_ticket_film]["Pukul 🕘"],
                "Harga 💲":formatted_price
            }
            user_tickets.append(user_movie_option)
            user_continue = str(input("Apakah anda ingin membeli tiket yang lain? (y/n) (default=no) : ")).lower()
            if user_continue.casefold() in options:
                continue
            last_row_total = {
                "Tiket Film yang dipesan 🍿": "",
                "Menonton di IMAX 🎥": "",
                "Hari 📆":"",
                "Pukul 🕘":"Total Harga Tiket w/ pajak :",
                "Harga 💲":format_currency(total_price_with_tax,"IDR",locale="id_ID")
            }
            user_tickets.append(last_row_total)
            user_ticket_table = tb(user_tickets, headers="keys", tablefmt="fancy_grid", numalign="center", stralign="center")
            print(user_ticket_table)
            print("✨ Terimakasih telah menggunakan program kami ✨")
            break
else:
    print(f"Fetch Api Gagal!. Status code: {response.status_code}")
