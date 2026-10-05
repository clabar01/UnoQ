# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

import socket
import time

from arduino.app_utils import App
from arduino.app_bricks.web_ui import WebUI

ui = WebUI()

REFRESH_SECONDS = 10


def get_ip_address() -> str:
    """Best-effort discovery of the board's primary IPv4 address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return "unavailable"
    finally:
        s.close()


def on_get_ip():
    return {"ip": get_ip_address()}


ui.expose_api("GET", "/ip", on_get_ip)

last_ip = None


def loop():
    global last_ip
    ip = get_ip_address()
    if ip != last_ip:
        last_ip = ip
        ui.send_message("ip_update", {"ip": ip})
    time.sleep(REFRESH_SECONDS)


App.run(user_loop=loop)
