import requests
from bs4 import BeautifulSoup

response = requests.get("https://meteo.go.ke/forecast/todays-weather/")
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    weather_data = []

    for town_name in ["Lodwar", "Makindu"]:
        town_weather_block = soup.find('div', class_='field-content', string=town_name)

        if town_weather_block:
            weather_desc_element = town_weather_block.find_next_sibling('div', class_='weather-desc')
            if weather_desc_element:
                weather_desc = weather_desc_element.text.strip()
            else:
                weather_desc = "Weather description not found"

            temp_element = town_weather_block.find_next_sibling('div', class_='temp')
            if temp_element:
                temp_details = temp_element.find_all('div', class_='temp-detail')
                min_temp = temp_details[0].get_text(strip=True)
                max_temp = temp_details[1].get_text(strip=True)
            else:
                min_temp = "N/A"
                max_temp = "N/A"

            weather_data.append({
                'Town': town_name,
                'Weather': weather_desc,
                'Min Temperature': min_temp,
                'Max Temperature': max_temp
            })
        else:
            print(f"Town '{town_name}' not found on the webpage")

    for data in weather_data:
        print(f"Town: {data['Town']}")
        print(f"Weather: {data['Weather']}")
        print(f"Min Temperature: {data['Min Temperature']}")
        print(f"Max Temperature: {data['Max Temperature']}")
        print("-" * 20)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
