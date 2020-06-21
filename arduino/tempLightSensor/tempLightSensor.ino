#include <EEPROM.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <PubSubClient.h>
#include <NTPClient.h>
#include <ArduinoJson.h>

#define DEBUG_TO_SERIAL   0   // debug on serial port
#define USE_MQTT          1   // use mqtt protocol instead of http post
#define USE_INTERNAL_NTP  1   // use default ntp server or the internal one
#define TELEMETRY_DELAY  10   // second between telemetry samples
#define AREF_VOLTAGE      3.3 // set aref voltage to 3.3v instead of default 5v

char serial[9];

// const String serverName = "sensor.server.domain";
const size_t capacity = 2 * JSON_OBJECT_SIZE(3) + JSON_OBJECT_SIZE(2) + 20;

DynamicJsonDocument telemetry(capacity);
JsonObject payload = telemetry.createNestedObject("payload");
JsonObject temp = payload.createNestedObject("temperature");

unsigned int counter = 0;

EthernetUDP ntpUDP;
NTPClient timeClient(ntpUDP);
bool NTPValid = false;

EthernetClient ethClient;
PubSubClient clientMQTT(ethClient);

struct netConfig {
  IPAddress address;
  unsigned int port;
};
netConfig config;

const String apiURL = "/api/device/subscribe/";
const String telemetryURL = "/telemetry/";

void setup(void) {
  Serial.begin(9600);

  analogReference(EXTERNAL);

  StaticJsonDocument<20> api;

  byte mac[6];
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
  Serial.print(" at address: ");
  Serial.println(Ethernet.localIP());
  Serial.println();
  Serial.print("Connecting to: ");
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

#if USE_MQTT
  clientMQTT.setServer(config.address, 1883);
#endif
}

void loop(void) {
  const int postDelay = TELEMETRY_DELAY * 1000;

  unsigned int tempReading = analogRead(A0);
  unsigned int photocellReading = analogRead(A1);

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
