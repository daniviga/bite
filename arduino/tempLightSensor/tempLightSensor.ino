#include <EEPROM.h>
#include <Ethernet.h>
#include <ArduinoJson.h>

#define DEBUG_TO_SERIAL 1
#define AREF_VOLTAGE 3.3

const String serverName = "sensor.server.domain";

const size_t capacity = JSON_OBJECT_SIZE(1) + 2*JSON_OBJECT_SIZE(6);
DynamicJsonDocument doc(capacity);
JsonObject payload = doc.createNestedObject("payload");
JsonObject temp = payload.createNestedObject("temperature");

int tempPin = A0;
int photocellPin = A1;

struct netConfig {
  IPAddress address;
  int port;
};
netConfig config;

const String URL = "/telemetry/";
const int postDelay = 10 * 1000;

void setup(void) {
  Serial.begin(9600);
  
  analogReference(EXTERNAL);

  byte mac[6];
  char serial[9];
  
  int eeAddress = 0;

  EEPROM.get(eeAddress, mac);
  eeAddress += sizeof(mac);
  EEPROM.get(eeAddress, serial);
  eeAddress += sizeof(serial);
  
  Serial.println("Initialize Ethernet with DHCP:");
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    if (Ethernet.hardwareStatus() == EthernetNoHardware) {
      Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
    } else if (Ethernet.linkStatus() == LinkOFF) {
      Serial.println("Ethernet cable is not connected.");
    }
    // no point in carrying on, so do nothing forevermore:
    while (true) {
      delay(1);
    }
  }
  EEPROM.get(eeAddress, config);
  
  Serial.print("IoT #");
  Serial.print(serial);
  Serial.println(" started at address:");
  Serial.println(Ethernet.localIP());
  Serial.println();
  Serial.println("Connecting to:");
  Serial.print(config.address);
  Serial.print(":");
  Serial.println(config.port);

  doc["device"] = serial;  // FIXME
  payload["id"] = serverName;
}

void loop(void) {
  
  int photocellReading = analogRead(photocellPin);
  int tempReading = analogRead(tempPin);

  float tempVoltage = tempReading * AREF_VOLTAGE / 1024.0;
  float tempC = (tempVoltage - 0.5) * 100 ;

  payload["light"] = photocellReading;

  temp["celsius"] = tempC;
  temp["raw"] = tempReading;
  temp["volts"] = tempVoltage;
  
  if (EthernetClient client = client.connect(config.address, config.port)) {
    client.print("POST ");
    client.print(URL);
    client.println(" HTTP/1.1");
    client.print("Host: ");
    printAddr(config.address, &client);
    client.print(":");
    client.println(config.port);
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(measureJsonPretty(doc));
    client.println("Connection: close");
    client.println();
    serializeJson(doc, client);
    client.stop();
    
    #if DEBUG_TO_SERIAL
    serializeJsonPretty(doc, Serial);
    #endif
  }

  delay(postDelay);
}
