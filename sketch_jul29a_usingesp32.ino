#include <ESP8266WiFi.h>// allows the esp to have functionalities like pinmode 
#include <WiFiClient.h> // allows us to browse
#include <ESP8266HTTPClient.h> // allows your esp to search for a particular hotspot and connect to it
#include <DHT.h>
String ipAddress = "192.168.1.232:8248";
String tempval = "30";
String humval = "90";

WiFiClient myHotspot;
#define DHTPIN D2
#define DHTTYPE DHT11
DHT dht(DHTPIN,DHTTYPE);

void setup() {
  // put your setup code here, to run once:
  WiFi.begin("STARLINK",""); //we set the wifi name and  pasword  for your hotspot(hotspotname,password)
  while (WiFi.status() != WL_CONNECTED){
    delay(500);// while waiting if the connection is successfull lets wait untill the connection is successfull
  }
  Serial.begin(9600);
  dht.begin();

}

void loop() {
  // put your main code here, to run repeatedly:
  delay(2000); 
  Serial.println("WE ARE IN....");
 
  float tempvalx = dht.readTemperature(); // Read temperature as Celsius
  float humvalx = dht.readHumidity();     // Read humidity
  if (isnan(tempvalx) || isnan(humvalx)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Print temperature and humidity to Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(tempvalx);
  Serial.print(" °C"); // Degree Celsius
  Serial.print("  Humidity: ");
  Serial.print(humvalx);
  Serial.println(" %"); // Percentage
  HTTPClient browser;
  String link ="http://" + ipAddress +"/saveData?"+"curr_temp="+ tempvalx+ "&&curr_hum="+ humvalx;
  Serial.println(link);
  browser.begin(myHotspot,link);
  if (browser.GET()>0) {
    Serial.println(browser.getString());
    delay(5000);
  }
  browser.end();

}

