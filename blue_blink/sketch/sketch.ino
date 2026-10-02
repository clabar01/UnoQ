// SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
//
// SPDX-License-Identifier: MPL-2.0

#include "Arduino_RouterBridge.h"

void setup() {
    // RGB LED 3 is MCU-controlled; drive only its blue channel
    pinMode(LED3_R, OUTPUT);
    pinMode(LED3_G, OUTPUT);
    pinMode(LED3_B, OUTPUT);
    digitalWrite(LED3_R, HIGH);
    digitalWrite(LED3_G, HIGH);
    digitalWrite(LED3_B, HIGH);

    Bridge.begin();
    Bridge.provide("set_led_state", set_led_state);
}

void loop() {
}

void set_led_state(bool state) {
    // LOW state means LED is ON
    digitalWrite(LED3_B, state ? LOW : HIGH);
}
