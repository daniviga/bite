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

#include <Preferences.h>
#include <Ethernet.h>
#include "settings.h"

#define ERASE_FIRST 1

Preferences preferences;
const char* serial = SERIAL;

const char* ssid = SECRET_SSID;
const char* password = SECRET_PASSWORD;

struct netConfig {
  IPAddress address = REMOTE_IP;
  unsigned int port = REMOTE_PORT;
} config;

void setup() {

  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  preferences.begin("iot", false);
#if ERASE_FIRST
  Serial.println("Erasing IoT data");
  preferences.clear();
#endif
  Serial.print("Writing IoT data");
  preferences.putString("serial", serial);
  Serial.print(".");
  Serial.println(".");

  preferences.putBytes("config", &config, sizeof(config));
  Serial.println("Committing...");
  preferences.end();
  Serial.println("IoT data written!");

  preferences.begin("wifi", false);
#if ERASE_FIRST
  Serial.println("Erasing WiFI data");
  preferences.clear();
#endif
  Serial.println("Writing WiFi data");
  preferences.putString("ssid", ssid);
  preferences.putString("password", password);
  Serial.println("Committing...");
  preferences.end();
  Serial.println("WiFi data written!");
}

void loop() {
  /* Empty loop */
}
