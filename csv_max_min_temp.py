import requests
from bs4 import BeautifulSoup
import csv
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
        min_temp_tag = temp_detail.find('span', text='Min: ')
        max_temp_tag = temp_detail.find('span', text='Max: ')
        if min_temp_tag:
            min_temp = min_temp_tag.find_next_sibling(text=True).strip()
            min_temperatures.append(min_temp)
        if max_temp_tag:
            max_temp = max_temp_tag.find_next_sibling(text=True).strip()
            max_temperatures.append(max_temp)
    return min_temperatures, max_temperatures

# Fetch the content of the webpage
html_content = fetch_page_content(url)
if html_content:
    # Extract the minimum and maximum temperatures
    min_temperatures, max_temperatures = extract_temperatures(html_content)
    # Print the list of minimum temperatures
    print("List of Minimum Temperatures:")
    print(min_temperatures)
    print("\nList of Maximum Temperatures:")
    print(max_temperatures)
    weather_data = zip(min_temperatures, max_temperatures)
    
    with open('TEMP DATA_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Min ', 'Max']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for min_temp, max_temp in weather_data:
            writer.writerow({'Min ':min_temp, 'Max':max_temp})
    print("TEMP CSV CREATED")

else:
    print("Failed to fetch the webpage content.")
