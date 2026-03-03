import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io
import gecoder
API_KEY = "b843dfdfd46cb7cb118581d9af2473ad"

KENYAN_CITIES = [
    "Nairobi", "Mombasa", "Kisumu",
    "Nakuru", "Eldoret", "Thika",
    "Malindi", "Kitale",
     "Homa Bay", "Nyeri", "Muranga",
    "Nakuru", "Eldoret", "Tharakanithi",
    "kericho", "Kirinyaga"
]


# -------- Weather Logic --------
def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def fetch_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_weather():
    city = city_combo.get()

    if not city:
        messagebox.showwarning("Input Error", "Please select a city")
        return

    data = fetch_weather(f"{city},KE")

    if int(data["cod"]) != 200:
        result_label.config(text="City not found ❌", fg="red")
        return

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    desc = data["weather"][0]["description"]
    icon_code = data["weather"][0]["icon"]

    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    icon_data = requests.get(icon_url).content
    image = Image.open(io.BytesIO(icon_data))
    photo = ImageTk.PhotoImage(image)

    icon_label.config(image=photo)
    icon_label.image = photo

    result_label.config(
        text=(
            f"{city}, Kenya 🇰🇪\n"
            f"🌡 Temp: {temp}°C\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬 Wind: {wind} m/s\n"
            f"☁ Condition: {desc.title()}"
        ),
        fg="#09ff00"
    )

    show_forecast(city)

def show_forecast(city):
    forecast = fetch_forecast(f"{city},KE")
    text = "\n📅 5-Day Forecast\n"

    for i in range(0, 40, 8):
        day = forecast["list"][i]
        text += f"{day['dt_txt'][:10]} : {day['main']['temp']}°C\n"

    forecast_label.config(text=text)

def detect_location():
    g = geocoder.ip('me')
    if g.city:
        city_combo.set(g.city)

# -------- GUI --------
window = tk.Tk()
window.title("Ultimate Weather App")
window.geometry("420x600")
window.configure(bg="#1e1e1e")
window.resizable(False, False)

style = ttk.Style()
style.theme_use("default")
style.configure("TCombobox", fieldbackground="#2e2e2e", background="#2e2e2e")

tk.Label(
    window, text="🌦 Weather App",
    font=("Arial", 18, "bold"),
    bg="#1e1e1e", fg="#00ffcc"
).pack(pady=10)

tk.Label(
    window, text="Select City (Kenya)",
    font=("Arial", 12),
    bg="#1e1e1e", fg="white"
).pack(pady=5)

city_combo = ttk.Combobox(
    window,
    values=KENYAN_CITIES,
    font=("Arial", 12),
    state="readonly"
)
city_combo.pack(pady=5)

tk.Button(
    window, text="🌍 Auto Detect Location",
    command=detect_location
).pack(pady=5)

tk.Button(
    window, text="Get Weather",
    font=("Arial", 12),
    command=get_weather
).pack(pady=10)

icon_label = tk.Label(window, bg="#1e1e1e")
icon_label.pack()

result_label = tk.Label(
    window, font=("Arial", 12),
    bg="#1e1e1e", fg="white", justify="center"
)
result_label.pack(pady=10)

forecast_label = tk.Label(
    window, font=("Arial", 11),
    bg="#1e1e1e", fg="#cccccc", justify="center"
)
forecast_label.pack(pady=10)

window.mainloop()