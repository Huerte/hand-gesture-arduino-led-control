const int LED_PIN[5] = {8, 9, 10, 11, 12};

void setup() {

  Serial.begin(9600);

  for (const int PIN: LED_PIN) {
    pinMode(PIN, OUTPUT);
  }

}

void loop() {

  if (Serial.available() > 0){

    char msg = Serial.read();

    for (const int PIN: LED_PIN) {
      digitalWrite(PIN, (msg == '1')? HIGH: LOW);
    }

  }

}
