#include <EEPROM.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <NTPClient.h>
#include <ArduinoJson.h>

#define DEBUG_TO_SERIAL 1
#define USE_INTERNAL_NTP 0 // use default ntp server or the internal one
#define AREF_VOLTAGE 3.3

// const String serverName = "sensor.server.domain";
const size_t capacity = 2 * JSON_OBJECT_SIZE(3) + JSON_OBJECT_SIZE(2) + 20;

DynamicJsonDocument telemetry(capacity);
JsonObject payload = telemetry.createNestedObject("payload");
JsonObject temp = payload.createNestedObject("temperature");

unsigned int counter = 0;
int tempPin = A0;
int photocellPin = A1;

EthernetUDP ntpUDP;
NTPClient timeClient(ntpUDP);
bool NTPValid = false;

struct netConfig {
  IPAddress address;
  unsigned int port;
};
netConfig config;

const String apiURL = "/api/subscribe/";
const String telemetryURL = "/telemetry/";
const int postDelay = 10 * 1000;

void setup(void) {
  Serial.begin(9600);

  analogReference(EXTERNAL);

  StaticJsonDocument<20> api;

  byte mac[6];
  char serial[9];

  int eeAddress = 0;

  EEPROM.get(eeAddress, mac);
  eeAddress += sizeof(mac);
  EEPROM.get(eeAddress, serial);
  eeAddress += sizeof(serial);

  if (Ethernet.begin(mac) == 0) {
    if (Ethernet.hardwareStatus() == EthernetNoHardware) {
      Serial.println("ERROR: ethernet shield was not found.");
    }
    while (true) {
      delay(1);
    }
  }
  EEPROM.get(eeAddress, config);

  Serial.print("IoT #");
  Serial.print(serial);
  Serial.println(" at address:");
  Serial.println(Ethernet.localIP());
  Serial.println();
  Serial.println("Connecting to:");
  Serial.print(config.address);
  Serial.print(":");
  Serial.println(config.port);

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
}

void loop(void) {

  unsigned int photocellReading = analogRead(photocellPin);
  unsigned int tempReading = analogRead(tempPin);

  float tempVoltage = tempReading * AREF_VOLTAGE / 1024.0;
  float tempC = (tempVoltage - 0.5) * 100 ;

  if (NTPValid) {
    telemetry["clock"] = timeClient.getEpochTime();
  } else {
    telemetry["clock"] = NULL; // converted into 0
  }
  payload["light"] = photocellReading;

  temp["celsius"] = tempC;
  temp["raw"] = tempReading;
  temp["volts"] = tempVoltage;

  postData(config, telemetryURL, telemetry);

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

void postData(const netConfig &postAPI, const String &URL, const DynamicJsonDocument &json) {
  if (EthernetClient client = client.connect(postAPI.address, postAPI.port)) {
    client.print("POST ");
    client.print(URL);
    client.println(" HTTP/1.1");
    client.print("Host: ");
    client.print(postAPI.address);
    client.print(":");
    client.println(postAPI.port);
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(measureJsonPretty(json));
    client.println("Connection: close");
    client.println();
    serializeJson(json, client);
    client.stop();

#if DEBUG_TO_SERIAL
    Serial.println("DEBUG: >>>");
    serializeJsonPretty(json, Serial);
    Serial.println("\n<<<");
#endif
  }
}
