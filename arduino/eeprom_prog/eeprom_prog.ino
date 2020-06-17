#include <EEPROM.h>
#include <Ethernet.h>

#define ERASE_FIRST 0

const byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
const char serial[] = "abcd1234";

struct netConfig {
  IPAddress address;
  unsigned int port;
};

netConfig config = {
  {192, 168, 10, 123},
  8000
};

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
