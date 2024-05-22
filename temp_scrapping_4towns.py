import requests
import csv
from bs4 import BeautifulSoup

# URL of the page containing the town names
url = "https://meteo.go.ke/forecast/todays-weather/"

# Function to fetch the webpage content
def fetch_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to extract minimum and maximum temperatures from the HTML content
def extract_temperatures(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    min_temperatures = []
    max_temperatures = []

    for temp_detail in soup.find_all('div', class_='temp-detail'):
        min_temp_tag = temp_detail.find('span', string='Min: ')
        max_temp_tag = temp_detail.find('span', string='Max: ')

        if min_temp_tag:
            min_temp = min_temp_tag.find_next_sibling(string=True).strip()
            min_temperatures.append(min_temp)

        if max_temp_tag:
            max_temp = max_temp_tag.find_next_sibling(string=True).strip()
            max_temperatures.append(max_temp)

    return min_temperatures, max_temperatures
def extract_town_names(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    town_names = []
    for town_div in soup.find_all('div', class_='views-field views-field-field-town'):
        town_name = town_div.find('div', class_='field-content').get_text().strip()
        town_names.append(town_name)  # Append each town name to the list
    return town_names
# Fetch the content of the webpage
html_content = fetch_page_content(url)

if html_content:
    # Extract the minimum and maximum temperatures
    min_temperatures, max_temperatures = extract_temperatures(html_content)
    town = extract_town_names(html_content)

    weather_data = zip(town, min_temperatures, max_temperatures)
    weather_data = list(weather_data)
    print(weather_data)
    # Write the data into a CSV file
    with open('test_weather_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Town', 'Min', 'Max']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for town, min_temperatures, max_temperatures in weather_data:
            writer.writerow({'Town': town, 'Min':min_temperatures, 'Max':max_temperatures })
            
    print("SUCCESSS")
else:
    print("Failed to fetch the webpage content.")