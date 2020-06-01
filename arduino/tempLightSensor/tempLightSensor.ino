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
int tempReading;
int photocellPin = A1;
int photocellReading;

const byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
const byte remoteAddr[] = {
  192, 168, 10, 123 };
const int remotePort = 8000;
const int postDelay = 10*1000;

const String serialNum = "abcde12345";
const String URL = "/telemetry/";

void printAddr(byte addr[], Stream *stream) {
  for (byte thisByte = 0; thisByte < 4; thisByte++) {
    // print the value of each byte of the IP address:
    stream->print(addr[thisByte], DEC);
    if (thisByte < 3) {
      stream->print(".");
    }
  }
}

void setup(void) {
  Serial.begin(9600);
  
  analogReference(EXTERNAL);
  
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // no point in carrying on, so do nothing forevermore:
    for(;;)
      ;
  } 
  
  Serial.print("IoT started at address: ");
  printAddr(Ethernet.localIP(), &Serial);
  Serial.println();

  doc["device"] = 1;  // FIXME
  payload["id"] = serverName;
}

void loop(void) {
  photocellReading = analogRead(photocellPin);
  tempReading = analogRead(tempPin);

  float tempVoltage = tempReading * AREF_VOLTAGE / 1024.0;
  float tempC = (tempVoltage - 0.5) * 100 ;

  payload["light"] = photocellReading;

  temp["celsius"] = tempC;
  temp["raw"] = tempReading;
  temp["volts"] = tempVoltage;
  
  if (EthernetClient client = client.connect(remoteAddr, remotePort)) {
    client.print("POST ");
    client.print(URL);
    client.println(" HTTP/1.1");
    client.print("Host: ");
    printAddr(remoteAddr, &client);
    client.print(":");
    client.println(remotePort);
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
