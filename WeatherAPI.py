import os
from tkinter import *
from tkinter import messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

API_KEY = "326c24b8408af829e184489c6692a359"

root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

def get_weather():
    city = textfield.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return
    try:
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)
        if not location:
            messagebox.showerror("Error", "City not found!")
            return

        obj = TimezoneFinder()
        timezone = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        if not timezone:
            messagebox.showerror("Error", "Could not determine the timezone!")
            return

        home = pytz.timezone(timezone)
        local_time = datetime.now(home).strftime("%I:%M %p")
        clock.config(text=local_time)
        name.config(text="CURRENT WEATHER")

        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(api_url)
        response.raise_for_status()
        json_data = response.json()
        if json_data["cod"] != 200:
            messagebox.showerror("Error", json_data.get("message", "Unknown error").capitalize())
            return

        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        t.config(text=f"{temp}°C")
        c.config(text=f"{condition} | FEELS LIKE {temp}°C")
        w.config(text=f"{wind} km/h")
        h.config(text=f"{humidity}%")
        d.config(text=description.capitalize())
        p.config(text=f"{pressure} hPa")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"API request failed: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

search_image_path = r"C:\Users\abdel\OneDrive\Desktop\Réalisation Informatique\Programmation\search.png"
search_icon_path = r"C:\Users\abdel\OneDrive\Desktop\Réalisation Informatique\Programmation\search_icon.png"
logo_image_path = r"C:\Users\abdel\OneDrive\Desktop\Réalisation Informatique\Programmation\logo.png"
frame_image_path = r"C:\Users\abdel\OneDrive\Desktop\Réalisation Informatique\Programmation\box.png"

search_image = PhotoImage(file=search_image_path)
search_icon = PhotoImage(file=search_icon_path)
Logo_image = PhotoImage(file=logo_image_path)
Frame_image = PhotoImage(file=frame_image_path)

Label(image=search_image).place(x=20, y=20)
textfield = Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=100, y=35)
textfield.focus()

Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=get_weather).place(x=400, y=34)

Label(image=Logo_image).place(x=150, y=100)
Label(image=Frame_image).pack(padx=5, pady=5, side=BOTTOM)

name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)

Label(root, text="WIND", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef").place(x=120, y=400)
Label(root, text="HUMIDITY", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef").place(x=250, y=400)
Label(root, text="DESCRIPTION", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef").place(x=430, y=400)
Label(root, text="PRESSURE", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef").place(x=650, y=400)

w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)
h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)
d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=430, y=430)
p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

root.mainloop()
