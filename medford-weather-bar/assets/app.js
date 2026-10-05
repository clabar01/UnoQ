// SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
//
// SPDX-License-Identifier: MPL-2.0

const socket = io(`http://${window.location.host}`);

const iconEl = document.getElementById("icon");
const descEl = document.getElementById("desc");
const tempEl = document.getElementById("temp");

function setWeather(data) {
  if (!data || !data.description) {
    iconEl.textContent = "⚠️";
    descEl.textContent = "unavailable";
    tempEl.textContent = "";
    return;
  }
  iconEl.textContent = data.icon || "🌡️";
  descEl.textContent = data.description;
  tempEl.textContent =
    data.temperature !== null && data.temperature !== undefined
      ? `${Math.round(data.temperature)}°C`
      : "";
}

fetch(`http://${window.location.host}/weather`, { cache: "no-store" })
  .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
  .then(setWeather)
  .catch(() => setWeather(null));

socket.on("weather_update", setWeather);
