import os
import json
import requests
import configparser

def readConfig():
    global config
    config = configparser.ConfigParser()
    config.read("./config.ini")

def entryToCityName(entryText):
    l = entryText.split()
    return " ".join(l)

def getWeatherObject(data):
    class WeatherObject():
        def __init__(self, data):
            self.data = data
            self.name = data["name"]
            self.icon = data["weather"][0]["icon"].lower()
            self.country = data["sys"]["country"].lower()
            self.description = data["weather"][0]["description"].capitalize()
            self.temp = round(data["main"]["temp"])
            self.pressure = round(data["main"]["pressure"])
            self.humidity = round(data["main"]["humidity"])
            self.wind_speed = data["wind"]["speed"]
            self.wind_deg = data["wind"]["deg"]

        def getIcon(self):
            iconPath = f"./pictures/weather/{self.icon}.png"

            if os.path.isfile(iconPath):
                return iconPath

            return f"./pictures/weather/warning.png"

        def getCountryFlag(self):
            flagPath = f"./pictures/flags/{self.country}.png"

            if os.path.isfile(flagPath):
                return flagPath

        def getExtraInfo(self):
            return f"Description : {self.description}\n\nHumidity : {self.humidity}%\n\nPressure : {self.pressure} hPa\n\nWind speed : {self.wind_speed} m/s\n\nWind direction : {self.wind_deg}°"

    return WeatherObject(data)

def getWeatherJson(cityName: str):
    weather_section = config["weather_api"]
    url = weather_section["url"].format(cityName, weather_section["key"])
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Something went wrong trying to get json.\nStatus Code : `{response.status_code}`\nContact the developer.")

if __name__ != "__main__":
    readConfig()