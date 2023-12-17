import os
from flask import Flask, flash, redirect, render_template, request, session
import os
import requests
import urllib.parse

# from helping import location, climate

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/", methods = ["GET", "POST"])
def aaaa():
    # se for post
    if request.method == "POST":
        # primeiro o cara pede api key por meio da location api
        city = request.form.get("city")
        tiempo = tiempo_data(city)
        # dpoi so imprimir no html #PST #TMJ
        return render_template("aaaa.html", tiempo = tiempo)
    else:
        return render_template("aaaa.html")

# onde vai ter as funçoes pre definidas
api_key = os.environ.get("API_KEY")
params = {
    "apikey": "1eVY8dj92ca9b3uL8BLLvfmRxOtxhoQq",
    "details": "true"
}

k = 0
c = 1
f = 2

# climate == corrent conditions
def tiempo_data(city):
    try:
        # Get location key for the city
        location_key = location(city)
        if not location_key:
            return None

        # Get current conditions for the location
        current_conditions = climate(location_key)
        if not current_conditions:
            return None

        return {
            "temperature": current_conditions.get("Temperature", {}).get("Metric", {}).get("Value"),
            "weather_text": current_conditions.get("WeatherText"),
            "is_daytime": current_conditions.get("IsDayTime"),
            "weather_icon": current_conditions.get("WeatherIcon")
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def location(city):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/autocomplete"
    paramis = {"apikey": api_key, "q": city}
    response = requests.get(url, params=paramis)
    response.raise_for_status()
    dalin = response.json()
    #     return {
    #         "key": dalin["Key"]
    #     }
    if dalin:
        return dalin[0].get("Key")
    return None

def climate(location):

    # url = f"http://dataservice.accuweather.com/currentconditions/v1/{id}?apikey=%20{api_key}"
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location}"
    response = requests.get(url, params=params)
    response.raise_for_status()
    dalin = response.json()
    # return {
    #     "temperature": clima["Temperature.Metric.Value"]
        # }
    if dalin and isinstance(dalin, list):
        return dalin[0]
    return None

if __name__ == "__main__":
    app.run(debug=True)

    # AUGN0SpcXakXe1BAPRNgh7LFEgd4NV2C
    # 1eVY8dj92ca9b3uL8BLLvfmRxOtxhoQq