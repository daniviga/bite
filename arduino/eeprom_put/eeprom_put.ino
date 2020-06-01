/***
    eeprom_put example.

    This shows how to use the EEPROM.put() method.
    Also, this sketch will pre-set the EEPROM data for the
    example sketch eeprom_get.

    Note, unlike the single byte version EEPROM.write(),
    the put method will use update semantics. As in a byte
    will only be written to the EEPROM if the data is actually
    different.

    Written by Christopher Andrews 2015
    Released under MIT licence.
***/

#include <EEPROM.h>

struct config {
  byte mac[6];
  byte remoteAddr[4];
  char serial[4];
  int remotePort;
  char name[128];
};

void setup() {

  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  int eeAddress = 0;   //Location we want the data to be put.

  /** Put is designed for use with custom structures also. **/

  //Data to store.
  config customVar = {
    { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED },
    { 192, 168, 10, 123 },
    "abcd",
    80,
    "sensor.server.domain"
  };

  EEPROM.put(eeAddress, customVar);
  Serial.print("Written custom data type! \n\nView the example sketch eeprom_get to see how you can retrieve the values!");
}

void loop() {
  /* Empty loop */
}
