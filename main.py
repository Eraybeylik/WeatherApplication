import tkinter as tk
from tkinter import messagebox
import requests
from tkinter import font, PhotoImage
from PIL import Image, ImageTk

OPENCAGE_API_KEY = 'APİ KEY GİRİNİZ'

# Open Meteo API'si için temel URL
OPEN_METEO_URL = 'https://api.open-meteo.com/v1/forecast'
OPENCAGE_URL = 'https://api.opencagedata.com/geocode/v1/json'

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning('Uyarı', 'Şehir adını girin!')
        return

    geocode_url = f'{OPENCAGE_URL}?q={city}&key={OPENCAGE_API_KEY}'

    try:
        response = requests.get(geocode_url)
        data = response.json()

        if data['results']:
            latitude = data['results'][0]['geometry']['lat']
            longitude = data['results'][0]['geometry']['lng']

            weather_url = f'{OPEN_METEO_URL}?latitude={latitude}&longitude={longitude}&current_weather=true'
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            if 'current_weather' in weather_data:
                temperature = weather_data['current_weather']['temperature']
                weather_description_code = weather_data['current_weather']['weathercode']
                weather_description = {
                    0: 'Açık hava',
                    1: 'Genellikle açık',
                    2: 'Parçalı bulutlu',
                    3: 'Kapalı',
                    45: 'Sis',
                    48: 'Buzlu sis',
                    51: 'Hafif çiseleme',
                    53: 'Orta çiseleme',
                    55: 'Yoğun çiseleme',
                    56: 'Hafif donma çiseleme',
                    57: 'Yoğun donma çiseleme',
                    61: 'Hafif yağmur',
                    63: 'Orta yağmur',
                    65: 'Yoğun yağmur',
                    66: 'Hafif donma yağı',
                    67: 'Yoğun donma yağı',
                    71: 'Hafif kar',
                    73: 'Orta kar',
                    75: 'Yoğun kar',
                    77: 'Kar taneleri',
                    80: 'Hafif yağmur sağanakları',
                    81: 'Orta yağmur sağanakları',
                    82: 'Yoğun yağmur sağanakları',
                    85: 'Hafif kar sağanakları',
                    86: 'Yoğun kar sağanakları',
                    95: 'Gök gürültülü fırtına',
                    96: 'Gök gürültülü fırtına ve dolu',
                    99: 'Gök gürültülü fırtına ve dolu'
                }.get(weather_description_code, 'Bilinmiyor')

                weather_info.set(f'Sıcaklık: {temperature}°C\nDurum: {weather_description}')
            else:
                weather_info.set('Hava durumu bilgisi burada görünecek.')
                messagebox.showerror('Hata', 'Hava durumu verisi alınamadı!')
        else:
            weather_info.set('Hava durumu bilgisi burada görünecek.')
            messagebox.showerror('Hata', 'Şehir adı bulunamadı!')
    except requests.RequestException as e:
        weather_info.set('Hava durumu bilgisi burada görünecek.')
        messagebox.showerror('Hata', f'Bir hata oluştu: {e}')

# Arayüz kısımı
window = tk.Tk()
window.title('Hava Durumu Uygulaması')

# Pencere boyutları
window.geometry('500x400')
window.configure(bg='#FFFFFF')  # Arka plan beyaz yapıldı

# Arka Plan
bg_image = Image.open('arkaplan.png')
bg_image = bg_image.resize((500, 400), Image.LANCZOS)  # Pencere boyutlarına göre yeniden boyutlandırma
bg_image = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(window, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Başlık
title_font = font.Font(family='Helvetica', size=22, weight='bold')
tk.Label(window, text='Hava Durumu Uygulaması', font=title_font, bg='#FFFFFF', fg='#000000').pack(pady=15)

# Şehir girişi
entry_font = font.Font(family='Helvetica', size=14)
city_frame = tk.Frame(window, bg='#FFFFFF')
city_frame.pack(pady=10)

tk.Label(city_frame, text='Şehir Adı:', bg='#FFFFFF', fg='#000000').pack(side=tk.LEFT, padx=5)
city_entry = tk.Entry(city_frame, font=entry_font, width=20)
city_entry.pack(side=tk.LEFT, padx=5)

# Hava durumu bilgisi
weather_info = tk.StringVar()
weather_info.set('Hava durumu bilgisi burada görünecek.')

info_label = tk.Label(window, textvariable=weather_info, font=('Helvetica', 14), bg='#FFFFFF', fg='#000000')
info_label.pack(pady=20)

# Hava durumu butonu
button_font = font.Font(family='Helvetica', size=12, weight='bold')
get_weather_button = tk.Button(window, text='Hava Durumunu Getir', font=button_font, command=get_weather, bg='#000000',
                               fg='#FFFFFF', relief='raised')
get_weather_button.pack(pady=10)


window.mainloop()
