String data;

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  Serial.print("butt");
  // digitalWrite(13, HIGH);
  
}

void loop() {
  while (Serial.available()) {
    Serial.print("while");
    data= Serial.readString();
    Serial.print(data);
    if (data == "test\n") {
      Serial.print("hello");
    }
  }
  
  if (data == "116") {
    //digitalWrite(13, HIGH);
    Serial.print("hi");
  } else if (data == "off") {
    digitalWrite(13, LOW);
  } else if (data == "test") {
    Serial.print("test");
  }
  
}
