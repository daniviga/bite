/***
    eeprom_get example.

    This shows how to use the EEPROM.get() method.

    To pre-set the EEPROM data, run the example sketch eeprom_put.
    This sketch will run without it, however, the values shown
    will be shown from what ever is already on the EEPROM.

    This may cause the serial object to print out a large string
    of garbage if there is no null character inside one of the strings
    loaded.

    Written by Christopher Andrews 2015
    Released under MIT licence.
***/

#include <EEPROM.h>

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  readConfig(); //Run the next test.
}

struct config {
  byte mac[6];
  byte remoteAddr[4];
  char serial[4];
  int remotePort;
  char name[128];
};

void printAddr(byte addr[], int size, Stream *stream) {
  for (int thisByte = 0; thisByte < size; thisByte++) {
    // print the value of each byte of the IP address:
    stream->print(addr[thisByte], HEX);
    if (thisByte < size - 1) {
      stream->print(".");
    }
  }
}

void readConfig() {
  int eeAddress = 0; //Move address to the next byte after float 'f'.

  config customVar; //Variable to store custom object read from EEPROM.
  EEPROM.get(eeAddress, customVar);

  Serial.println("Read custom object from EEPROM: ");
  printAddr(customVar.mac, sizeof(customVar.mac), &Serial);
  Serial.println();
  printAddr(customVar.remoteAddr, sizeof(customVar.remoteAddr), &Serial);
  Serial.println();
  Serial.println(customVar.remotePort);
  Serial.println(customVar.serial);
  Serial.println(customVar.name);
}

void loop() {
  /* Empty loop */
}
