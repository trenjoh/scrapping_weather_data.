from bs4 import BeautifulSoup
import requests
import csv
response  = requests.get("https://meteo.go.ke/forecast/todays-weather/")
print(response.text)
# soup = BeautifulSoup(response.text, "html.parser")
# articles = soup.find("href")
# print(articles)
# for art in articles:
#     print(art.find("a").get_text)

