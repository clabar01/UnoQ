import time

from arduino.app_utils import App

      - TCS34725: read red, green, blue channels from the library.
      - LEGO NXT color sensor: read I2C color/RGB values.
      - LEGO SPIKE/Powered Up sensor: usually easier through a LEGO hub,
        then send color data to the Uno only if needed.
  */
  Rgb rgb = {255, 0, 0};
  return rgb;
}

Hsv rgbToHsv(Rgb rgb) {
  if (RGB_FULL_SCALE <= 0) {
    Hsv dark = {0, 0, 0};
    return dark;
  }

  float r = constrain(rgb.r / RGB_FULL_SCALE, 0.0, 1.0);
  float g = constrain(rgb.g / RGB_FULL_SCALE, 0.0, 1.0);
  float b = constrain(rgb.b / RGB_FULL_SCALE, 0.0, 1.0);

  float cMax = max(r, max(g, b));
  float cMin = min(r, min(g, b));
  float delta = cMax - cMin;

  Hsv hsv;
  hsv.v = cMax;
  hsv.s = (cMax == 0) ? 0 : delta / cMax;

  if (delta == 0) {
    hsv.h = 0;
  } else if (cMax == r) {
    hsv.h = 60.0 * fmod(((g - b) / delta), 6.0);
  } else if (cMax == g) {
    hsv.h = 60.0 * (((b - r) / delta) + 2.0);
  } else {
    hsv.h = 60.0 * (((r - g) / delta) + 4.0);
  }

  if (hsv.h < 0) {
    hsv.h += 360.0;
  }

  return hsv;
}

BrickColor classifyColor(Hsv hsv) {
  if (hsv.v < 0.18) {
    return COLOR_BLACK;
  }

  if (hsv.s < 0.20 && hsv.v > 0.65) {
    return COLOR_WHITE;
  }

  if ((hsv.h >= 345 || hsv.h <= 18) && hsv.s > 0.35 && hsv.v > 0.20) {
    return COLOR_RED;
  }

  if (hsv.h >= 35 && hsv.h <= 70 && hsv.s > 0.35 && hsv.v > 0.35) {
    return COLOR_YELLOW;
  }

  if (hsv.h >= 85 && hsv.h <= 155 && hsv.s > 0.30 && hsv.v > 0.20) {
    return COLOR_GREEN;
  }

  if (hsv.h >= 190 && hsv.h <= 250 && hsv.s > 0.30 && hsv.v > 0.20) {
    return COLOR_BLUE;
  }

  return COLOR_UNKNOWN;
}

void feedBrickToSensor() {
  runFeedMotor(150);
  delay(700);
  stopFeedMotor();
}

void feedBrickIntoBin() {
  runFeedMotor(170);
  delay(900);
  stopFeedMotor();
}

void moveGateToColor(BrickColor color) {
  switch (color) {
    case COLOR_RED:
      turnGateLeft(250);
      break;
    case COLOR_YELLOW:
      resetGate();
      break;
    case COLOR_BLUE:
      turnGateRight(250);
      break;
    case COLOR_GREEN:
      turnGateLeft(500);
      break;
    case COLOR_WHITE:
      turnGateRight(500);
      break;
    case COLOR_BLACK:
      turnGateRight(750);
      break;
    default:
      resetGate();
      break;
  }
}

void resetGate() {
  stopGateMotor();
  delay(100);
}

void runFeedMotor(int speed) {
  digitalWrite(FEED_MOTOR_DIR, HIGH);
  analogWrite(FEED_MOTOR_PWM, constrain(speed, 0, 255));
}

void stopFeedMotor() {
  analogWrite(FEED_MOTOR_PWM, 0);
}

void turnGateLeft(int durationMs) {
  digitalWrite(GATE_MOTOR_DIR, LOW);
  analogWrite(GATE_MOTOR_PWM, 120);
  delay(durationMs);
  stopGateMotor();
}

void turnGateRight(int durationMs) {
  digitalWrite(GATE_MOTOR_DIR, HIGH);
  analogWrite(GATE_MOTOR_PWM, 120);
  delay(durationMs);
  stopGateMotor();
}

void stopGateMotor() {
  analogWrite(GATE_MOTOR_PWM, 0);
}

void printReading(Rgb rgb, Hsv hsv, BrickColor color) {
  Serial.print("RGB ");
  Serial.print(rgb.r);
  Serial.print(", ");
  Serial.print(rgb.g);
  Serial.print(", ");
  Serial.print(rgb.b);
  Serial.print(" | HSV ");
  Serial.print(hsv.h);
  Serial.print(", ");
  Serial.print(hsv.s);
  Serial.print(", ");
  Serial.print(hsv.v);
  Serial.print(" | Color ");
  Serial.println(colorName(color));
}

const char* colorName(BrickColor color) {
  switch (color) {
    case COLOR_RED: return "red";
    case COLOR_YELLOW: return "yellow";
    case COLOR_GREEN: return "green";
    case COLOR_BLUE: return "blue";
    case COLOR_WHITE: return "white";
    case COLOR_BLACK: return "black";
    default: return "unknown";
  }
}

