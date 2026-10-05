# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

import time

from arduino.app_utils import App
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.weather_forecast import WeatherForecast

# Medford, MA, USA
LATITUDE = "42.4184"
LONGITUDE = "-71.1061"
REFRESH_SECONDS = 600  # 10 minutes

CATEGORY_ICONS = {
    "sunny": "☀️",
    "cloudy": "☁️",
    "rainy": "🌧️",
    "snowy": "❄️",
    "foggy": "🌫️",
}

ui = WebUI()
forecaster = WeatherForecast()

last_payload = None


def build_payload():
    forecast = forecaster.get_forecast_by_coords(latitude=LATITUDE, longitude=LONGITUDE)
    temperature = getattr(forecast, "temperature", None)
    return {
        "category": forecast.category,
        "description": forecast.description,
        "icon": CATEGORY_ICONS.get(forecast.category, "🌡️"),
        "temperature": temperature,
    }


def on_get_weather():
    global last_payload
    try:
        last_payload = build_payload()
    except Exception as e:
        print(f"Weather fetch error: {e}")
    return last_payload or {}


ui.expose_api("GET", "/weather", on_get_weather)


def loop():
    global last_payload
    try:
        payload = build_payload()
        if payload != last_payload:
            last_payload = payload
            ui.send_message("weather_update", payload)
    except Exception as e:
        print(f"Weather fetch error: {e}")
    time.sleep(REFRESH_SECONDS)


App.run(user_loop=loop)
