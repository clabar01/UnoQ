// SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
//
// SPDX-License-Identifier: MPL-2.0

const socket = io(`http://${window.location.host}`);

const ipEl = document.getElementById("ip");
const dotEl = document.getElementById("dot");

function setIp(ip) {
  const ok = !!ip && ip !== "unavailable";
  ipEl.textContent = ok ? ip : "no network";
  dotEl.classList.toggle("offline", !ok);
}

fetch(`http://${window.location.host}/ip`, { cache: "no-store" })
  .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
  .then((data) => setIp(data?.ip))
  .catch(() => setIp(null));

socket.on("ip_update", (msg) => setIp(msg?.ip));
