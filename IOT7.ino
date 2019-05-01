#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// led related
#define LED 5
#define BUTTON 4
#define LEDRed 0

// light sensor
//#define Light_sensor
// wifi/MQTT parameters
//#define WLAN_SSID "dan"
//#define WLAN_PASS "supersecretpassword"
#define WLAN_SSID "ForTheHorde"
#define WLAN_PASS "panda1111"
#define BROKER_IP "192.168.86.39"

WiFiClient client;
PubSubClient mqttclient(client);

int b;
void callback (char* topic, byte* payload, unsigned int length) {
//  Serial.println(topic);
//  Serial.write(payload, length);
//  Serial.println(length);
    char payloadString[1];
    payloadString[0] = (char)payload[0];
    Serial.println(payloadString[0]);

    int b = payloadString[0] - '0';
      if( b == 1 )
      {
        digitalWrite(LED,HIGH);
      }
      else if ( b == 2)
      {
        digitalWrite(LED,LOW);
      }

      if( b == 3 )
      {
        digitalWrite(LEDRed,HIGH);
      }
      else if ( b == 4 )
      {
        digitalWrite(LEDRed,LOW);
      }
//      Serial.println( digitalRead(BUTTON));
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  // setup led
  pinMode(LED,OUTPUT);
  pinMode(LEDRed,OUTPUT);

  pinMode(BUTTON,INPUT);
  
  //connect to wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }

  Serial.println(F("WiFi connected"));
  Serial.println(F("IP address: "));
  Serial.println(WiFi.localIP());

  // connect to mqtt server
  mqttclient.setServer(BROKER_IP, 1883);
  mqttclient.setCallback(callback);
  connect();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (!mqttclient.connected()) {
    connect();
  }  

    delay(1000);
//    Serial.println(digitalRead(LEDRed));
//    digitalWrite(LEDRed,HIGH);
//    ### light sensor ###
//    int Light_sensor = analogRead(A0);
//    char sNum[4];
//    itoa(Light_sensor, sNum, 10);
//    
//    Serial.println(sNum);
//    mqttclient.publish("/sLight", sNum, false);

//    ### messaging ###    
//  if (digitalRead(BUTTON) == 1) {
//    digitalWrite(LED,HIGH);
//    mqttclient.publish("/test1", "button is pressed", true);
//  }
//  else{
//  }

//  ### Button ###
//  else if ( digitalRead(BUTTON) == 0)
//  {
//    delay(5000);
//    digitalWrite(LED,LOW);
//  }
  
  mqttclient.loop();
}

void connect() {
  while (WiFi.status() != WL_CONNECTED) {
      Serial.println(F("Wifi issue"));
      delay(3000);
  }
  Serial.print(F("Connecting to MQTT server..."));
  while(!mqttclient.connected()) {
    if(mqttclient.connect(WiFi.macAddress().c_str())) {
      Serial.println(F("MQTT server Connected!"));

      mqttclient.subscribe("/test3");
    }
    else
    {
      Serial.print(F("MQTT server connection failed re-"));
      Serial.print(mqttclient.state());
      Serial.println("try again in 10 second");

      delay(20000);
    }
  }
}
