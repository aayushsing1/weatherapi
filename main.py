from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        location = request.form.get("location")
        weather_data = get_weather_data(location)
        return render_template("index.html", weather_data=weather_data)
    return render_template("index.html", weather_data=None)



def get_weather_data(location):
    url = "https://tomorrow-io1.p.rapidapi.com/v4/weather/forecast"
    querystring = {"location": location, "timesteps": "1h", "units": "metric"}
    headers = {
        "X-RapidAPI-Key": "26cf59768bmsh6cb0cdb7d6e45b5p1d4f61jsna529a5b00b79",
        "X-RapidAPI-Host": "tomorrow-io1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        weather_data = response.json()
        
        # Get the current hour from the system time
        current_hour = datetime.now().hour
        
        # Find the data for the current hour in the hourly timeline
        current_hour_data = None
        for hour_data in weather_data.get("timelines", {}).get("hourly", []):
            hour = int(hour_data["time"].split("T")[1].split(":")[0])
            if hour == current_hour:
                current_hour_data = hour_data
                break
        
        print(current_hour_data)
        return current_hour_data
    else:
        return None



if __name__ == "__main__":
    app.run(debug=True)
