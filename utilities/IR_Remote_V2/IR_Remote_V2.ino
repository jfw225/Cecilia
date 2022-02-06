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
  // put your main code here, to run repeatedly:
  while (Serial.available()) {
    data = Serial.readString();

  }

  String code= "";
  for (int i = 0; i < data.length(); i++) {

    if (data.charAt(i) == ',') {

      if (contains(code, "stop")) { // Stops a signal from being sent.
        return;        
      } else if (contains(code, "r1")) { // Turns relay 1 on.
        digitalWrite(relay1, HIGH);
        digitalWrite(relay2, LOW);
      } else if (contains(code, "r2")) { // Turns relay 2 on.
        digitalWrite(relay1, LOW);
        digitalWrite(relay2, HIGH);
      } else if (contains(code, "r3")) { // Turns both relays on.
        digitalWrite(relay1, HIGH);
        digitalWrite(relay2, HIGH);
      }
      Serial.print(code);
      delay(1000);
      
      myHex= hexCodes[code.substring(3).toInt()];

      int i= 29;
      if (myHex == 0xFF3AC5 || myHex == 0xFFBA45) {
        i= 0;
      }
      while (i < 30) {
        irsend.sendNEC(myHex, 32);
        delay(50);
        i++;
      }

      code= "";
    } else {
      code+= data.charAt(i);
    }
  }
  

}


// Returns true is str1 contains str2, false if otherwise.
boolean contains(String str1, String str2) {
  if (str1.indexOf(str2) != -1) {
    return true;
  }
  return false;
}
