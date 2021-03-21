/* -*- coding: utf-8 -*-
* vim: tabstop=2 shiftwidth=2 softtabstop=2
*
* BITE - A Basic/IoT/Example
* Copyright (C) 2020-2021 Daniele Viganò <daniele@vigano.me>
*
* BITE is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* BITE is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.
*
* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <EEPROM.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <PubSubClient.h>
#include <NTPClient.h>
#include <ArduinoJson.h>

#define DEBUG_TO_SERIAL   1   // debug on serial port
#define USE_MQTT          1   // use mqtt protocol instead of http post
#define USE_INTERNAL_NTP  1   // use default ntp server or the internal one
#define TELEMETRY_DELAY  10   // second between telemetry samples

// const String serverName = "sensor.server.domain";
const size_t capacity = 2 * JSON_OBJECT_SIZE(3) + JSON_OBJECT_SIZE(2) + 20;

DynamicJsonDocument telemetry(capacity);
JsonObject payload = telemetry.createNestedObject("payload");

unsigned int counter = 0;

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);
bool NTPValid = false;

WiFiClient ethClient;
PubSubClient clientMQTT(ethClient);

const char* ssid = "";
const char* password = "";
const char* serial = "esp32_1";

struct netConfig {
  IPAddress address;
  unsigned int port;
};

netConfig config = {
  {192, 168, 10, 123},
  80
};

const String apiURL = "/api/device/subscribe/";
const String telemetryURL = "/telemetry/";

void setup(void) {
  Serial.begin(115200);

  StaticJsonDocument<64> api;

  /*
  int eeAddress = 0;

  EEPROM.get(eeAddress, serial);
  eeAddress += sizeof(serial);
  EEPROM.get(eeAddress, config);
  */

  Serial.println("Starting connecting WiFi.");
  delay(10);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  Serial.print("IoT #");
  Serial.print(serial);
  Serial.print(" at address: ");
  Serial.println(WiFi.localIP());
  Serial.println();
  Serial.print("Connecting to: ");
  Serial.print(config.address);
  Serial.print(":");
  Serial.print(config.port);
  Serial.print(" every ");
  Serial.print(TELEMETRY_DELAY);
  Serial.println("s");

#if USE_INTERNAL_NTP
  timeClient.setPoolServerIP(config.address);
#endif
  timeClient.begin();
  if (timeClient.update()) {
    NTPValid = true;
  }

#if DEBUG_TO_SERIAL
  Serial.println("DEBUG: clock updated via NTP.");
#endif

  api["serial"] = serial;
  postData(config, apiURL, api);

  telemetry["device"] = serial;
  // payload["id"] = serverName;

#if USE_MQTT
  clientMQTT.setServer(config.address, 1883);
#endif
}

void loop(void) {
  const int postDelay = TELEMETRY_DELAY * 1000;

  if (NTPValid) {
    telemetry["clock"] = timeClient.getEpochTime();
  } else {
    telemetry["clock"] = NULL; // converted into 0
  }

  payload["hall"] = hallRead();
  payload["wifi-rssi"] = WiFi.RSSI();

#if USE_MQTT
  publishData(config, telemetry);
#else
  postData(config, telemetryURL, telemetry);
#endif

  if (counter == 6 * 120) { // Update clock every 6 times * 10 sec * 120 minutes = 2 hrs
    timeClient.update();
    counter = 0;
#if DEBUG_TO_SERIAL
    Serial.println("DEBUG: clock updated via NTP.");
#endif
  } else {
    counter++;
  }

  delay(postDelay);
}

#if USE_MQTT
void publishData(const netConfig &mqtt, const DynamicJsonDocument &json) {
  if (clientMQTT.connect(serial)) {
    char buffer[256];
    serializeJson(json, buffer);
    clientMQTT.publish(serial, buffer);

#if DEBUG_TO_SERIAL
    Serial.println("DEBUG: MQTT PUBLISH>>>");
    serializeJsonPretty(json, Serial);
    Serial.println("\n<<<");
#endif
  }
}
#endif

void postData(const netConfig &postAPI, const String &URL, const DynamicJsonDocument &json) {
  if (ethClient.connect(postAPI.address, postAPI.port)) {
    ethClient.print("POST ");
    ethClient.print(URL);
    ethClient.println(" HTTP/1.1");
    ethClient.print("Host: ");
    ethClient.print(postAPI.address);
    ethClient.print(":");
    ethClient.println(postAPI.port);
    ethClient.println("Content-Type: application/json");
    ethClient.print("Content-Length: ");
    ethClient.println(measureJson(json));
    ethClient.println("Connection: close");
    ethClient.println();
    serializeJson(json, ethClient);
    ethClient.stop();

#if DEBUG_TO_SERIAL
    Serial.println("DEBUG: HTTP POST>>>");
    serializeJsonPretty(json, Serial);
    Serial.println("\n<<<");
#endif
  }
}
