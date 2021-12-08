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
#include <Ethernet.h>
#include "settings.h"

#define ERASE_FIRST 0

const byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
const char serial[] = SERIAL;

struct netConfig {
  IPAddress iot_address = IOT_IP;
  unsigned int iot_port = IOT_PORT;
  IPAddress ntp_address = NTP_IP;
  unsigned int ntp_port = NTP_PORT;
} config;

void setup() {

  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

#if ERASE_FIRST
  // initialize the LED pin as an output.
  pinMode(13, OUTPUT);
  // turn the LED on while erasing
  digitalWrite(13, HIGH);
  for (int i = 0 ; i < EEPROM.length() ; i++) {
    EEPROM.write(i, 0);
  }
  // turn the LED on when we're done
  digitalWrite(13, LOW);
#endif

  int eeAddress = 0;   //Location we want the data to be put.

  EEPROM.put(eeAddress, mac);
  eeAddress += sizeof(mac);
  EEPROM.put(eeAddress, serial);
  eeAddress += sizeof(serial);

  EEPROM.put(eeAddress, config);
  Serial.println("Data written!");
}

void loop() {
  /* Empty loop */
}
