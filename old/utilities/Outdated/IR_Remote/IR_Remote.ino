// Include IR Remote Library by Ken Shirriff
// If on MEGA, make sure to use pin 9
#include <IRremote.h>

// Create IR Send Object
IRsend irsend;

// Define pins
const int relay1= 7;
const int relay2= 8;

// Define the interpreted String
String data;

// Define an array of hex codes where each index corresponds to a device number in the excel spreadsheet.
long hexCodes[] = {0, 0xFF3AC5, 0xFFBA45, 0xFF827D, 0xFF02FD, 0xFF1AE5, 0xFF9A65, 0xFFA25D, 0xFF22DD, 0xFF2AD5, 0xFFAA55, 0xFF926D, 0xFF12ED, 0xFF0AF5, 0xFF8A75, 0xFFB24D, 0xFF32CD, 0xFF38C7, 0xFFB847, 0xFF7887, 0xFFF807, 0xFF18E7, 0xFF9867, 0xFF58A7, 0xFFD827, 0xFF28D7, 0xFFA857, 0xFF6897, 0xFFE817, 0xFF08F7, 0xFF8877, 0xFF48B7, 0xFFC837, 0xFF30CF, 0xFFB04F, 0xFF708F, 0xFFF00F, 0xFF10EF, 0xFF906F, 0xFF50AF, 0xFFD02F};

// Define the variable that determines the color
long myHex;

void setup() {
  // put your setup code here, to run once:
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  Serial.begin(9600);

}

void loop() {
  while (Serial.available()) {
    data= Serial.readString();
  }

   if (contains(data, "stop")) { // Stops a signal from being sent.
    delay(1000);
    return;
   } else if (contains(data, "r1")) { // Turns relay 2 off.
    digitalWrite(relay2, LOW);
    digitalWrite(relay1, HIGH);
    delay(1000);   
  } else if (contains(data, "r2")) { // Turns relay 1 off.
    digitalWrite(relay1, LOW);
    digitalWrite(relay2, HIGH);
    delay(1000);
  } else if (contains(data, "r3")) { // Turns both relays on.
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, HIGH);
    delay(1000);
  }
  
  myHex= hexCodes[data.substring(3).toInt()];
  irsend.sendNEC(myHex, 32);
  delay(1000);
  //irsend.sendNEC(0xFFA25D, 32); // Blue

}

// Returns true is str1 contains str2, false if otherwise.
boolean contains(String str1, String str2) {
  if (str1.indexOf(str2) != -1) {
    return true;
  }
  return false;
}
